from cbuild.core import logger, paths, chroot
from cbuild.apk import sign as asign, util as autil, cli as acli

import shlex
import pathlib
import subprocess

_scripts = {
    ".pre-install": True,
    ".pre-upgrade": True,
    ".pre-deinstall": True,
    ".post-install": True,
    ".post-upgrade": True,
    ".post-deinstall": True,
    ".trigger": True,
}


def _get_old_deps(pkg, arch):
    if pkg.stage < 3:
        return None, None, None, None

    cpf = pkg.rparent.profile()

    if cpf.cross:
        sysp = paths.bldroot() / cpf.sysroot.relative_to("/")
    else:
        sysp = paths.bldroot()

    def _get_sum(allow_net):
        return (
            acli.call(
                "info",
                [
                    "--from=none",
                    "--depends",
                    "--provides",
                    "--install-if",
                    pkg.pkgname,
                ],
                pkg,
                root=sysp,
                capture_output=True,
                arch=arch,
                allow_untrusted=True,
                allow_network=allow_net,
            )
            .stdout.strip()
            .decode()
        )

    # first fetch from local repo, fall back to network
    # this is to prevent having to disambiguate between different
    # package providers and so on, always get only one...
    depsum = _get_sum(False)
    if len(depsum) == 0:
        depsum = _get_sum(True)

    depsum = depsum.splitlines()

    deps = []
    provides = []
    instif = []
    curpver = None

    parts = 0
    curcont = deps

    for ln in depsum:
        ln = ln.strip()
        # skip empty lines
        if ln == "":
            continue
        # extract info and determine lists
        if ln.endswith(":"):
            # only consider one package
            if parts == 3:
                break
            # use verbose mode, it sucks but no other way to get pkgver
            if ln.endswith(" depends on:"):
                curcont = deps
                ln = ln.removesuffix(" depends on:")
            elif ln.endswith(" provides:"):
                curcont = provides
                ln = ln.removesuffix(" provides:")
            elif ln.endswith(" has auto-install rule:"):
                curcont = instif
                ln = ln.removesuffix(" has auto-install rule:")
            parts += 1
            # extract pkgver
            if not curpver:
                pn, curpver = autil.get_namever(ln)
            continue
        # now add to current list
        curcont.append(ln)

    deps.sort()
    provides.sort()
    instif.sort()

    return curpver, deps, provides, instif


def _get_new_deps(pkg, origin):
    deps = []
    provides = []

    # bootstrap packages are not installable ootb
    if pkg.pkgname.endswith("-bootstrap") and pkg.build_style != "meta":
        deps += ["bootstrap:" + pkg.pkgname.removesuffix("-bootstrap")]

    # explicit package depends
    for c in pkg.depends:
        ploc = c.find("!")
        if ploc > 0:
            deps.append(c[0:ploc].removeprefix("virtual:"))
        else:
            deps.append(c.removeprefix("virtual:"))

    # shlib requires
    if hasattr(pkg, "so_requires"):
        deps += map(lambda v: f"so:{v}", sorted(pkg.so_requires))

    # .pc file requires
    if hasattr(pkg, "pc_requires"):
        deps += map(lambda v: f"pc:{v}", sorted(pkg.pc_requires))

    # alternatives provider
    if pkg.alternative:
        provides += [f"{origin}=0"]

    # explicit provides
    provides += pkg.provides

    # shlib provides
    if hasattr(pkg, "aso_provides"):
        provides += map(
            lambda x: f"so:{x[0]}={x[1]}",
            sorted(pkg.aso_provides, key=lambda x: x[0]),
        )

    # .pc file provides
    if hasattr(pkg, "pc_provides"):
        provides += map(lambda x: f"pc:{x}", sorted(pkg.pc_provides))

    # command provides
    if hasattr(pkg, "cmd_provides"):
        provides += map(lambda x: f"cmd:{x}", sorted(pkg.cmd_provides))

    deps.sort()
    provides.sort()

    # TODO: recommends (once implemented in apk)
    return deps, provides, sorted(pkg.replaces), sorted(pkg.install_if)


def _print_diff(head, pkg, over, oldl, newl):
    if oldl is None:
        return

    sold = set()
    snew = set()

    for v in oldl:
        sold.add(v.removesuffix(f"={over}"))
    for v in newl:
        snew.add(v.removesuffix(f"={pkg.pkgver}-r{pkg.pkgrel}"))

    log = pkg.rparent.logger

    ldiff = []

    for v in oldl:
        if v.removesuffix(f"={over}") not in snew:
            ldiff.append((v, False))
    for v in newl:
        if v.removesuffix(f"={pkg.pkgver}-r{pkg.pkgrel}") not in sold:
            ldiff.append((v, True))

    if len(ldiff) == 0:
        return

    ldiff.sort()

    pkg.log(f"changed {head}:")
    for v, isadd in ldiff:
        if isadd:
            log.out(f"\f[green]  +{v}")
        else:
            log.out(f"\f[red]  -{v}")


def _get_cmdline(
    pkg, arch, origin, desc, deps, provides, replaces, iif, signkey
):
    pargs = [
        "--info",
        f"name:{pkg.pkgname}",
        "--info",
        f"version:{pkg.pkgver}-r{pkg.pkgrel}",
        "--info",
        f"description:{desc}",
        "--info",
        f"arch:{arch}",
        "--info",
        f"license:{pkg.license}",
        "--info",
        f"origin:{origin}",
        "--info",
        f"maintainer:{pkg.rparent._maintainer}",
        "--info",
        f"url:{pkg.rparent.url}",
        "--info",
        f"build-time:{int(pkg.rparent.source_date_epoch)}",
    ]

    # only record commits in non-dirty repos
    if pkg.rparent.git_revision and not pkg.rparent.git_dirty:
        pargs += ["--info", f"repo-commit:{pkg.rparent.git_revision}"]

    if len(deps) > 0:
        pargs += ["--info", f"depends:{' '.join(deps)}"]

    if len(provides) > 0:
        pargs += ["--info", f"provides:{' '.join(provides)}"]

    if pkg.provider_priority > 0:
        pargs += ["--info", f"provider-priority:{pkg.provider_priority}"]

    if len(replaces) > 0:
        pargs += ["--info", f"replaces:{' '.join(replaces)}"]

    if pkg.replaces_priority > 0:
        pargs += ["--info", f"replaces-priority:{pkg.replaces_priority}"]

    if len(iif) > 0:
        pargs += ["--info", f"install-if:{' '.join(iif)}"]

    # scripts including trigger scripts
    sclist = []

    for f in (pkg.statedir / "scripts").glob(f"{pkg.pkgname}.*"):
        if f.is_file() and f.suffix in _scripts:
            sclist.append(f.suffix[1:])

    sclist.sort()

    for f in sclist:
        # get in-chroot path to that
        scp = pkg.rparent.chroot_statedir / f"scripts/{pkg.pkgname}.{f}"
        # pass it
        pargs += ["--script", f"{f}:{scp}"]

    # trigger paths
    for t in pkg.triggers:
        p = pathlib.Path(t)
        if not p or not p.is_absolute():
            pkg.error(
                f"invalid trigger path: {t}",
                hint="trigger declarations require absolute paths",
            )
        pargs += ["--trigger", t]

    # signing key
    if signkey:
        if pkg.rparent.stage > 0:
            pargs += ["--sign-key", f"/tmp/{signkey.name}"]
        else:
            pargs += ["--sign-key", signkey]

    # for stage 1, we have stage0 apk built without zstd
    if (pkg.stage > 1 and pkg.compression) or pkg.compression == "none":
        comp = pkg.compression
        dcomp = autil.get_compression()
        # some generic presets that respect user-set global config
        match comp:
            case "fast":
                if dcomp.startswith("zstd"):
                    comp = "zstd:3"
                elif dcomp.startswith("deflate"):
                    comp = "deflate:3"
            case "slow":
                if dcomp.startswith("zstd"):
                    comp = "zstd:19"
                elif dcomp.startswith("deflate"):
                    comp = "deflate:9"
            case "zstd:fast":
                comp = "zstd:3"
            case "zstd:slow":
                comp = "zstd:19"
            case "deflate:fast":
                comp = "deflate:3"
            case "deflate:slow":
                comp = "deflate:9"
        pargs += ["--compression", comp]
    else:
        pargs += ["--compression", autil.get_compression()]

    return pargs


def _invoke_mkpkg(pkg, repo, pargs, binpath, signkey, wscript):
    repon = repo.parent.relative_to(paths.stage_repository())
    logger.get().out_plain(
        f"  \f[green]apk:\f[] \f[orange]{binpath.name}\f[] in {repon}\f[]"
    )

    if pkg.rparent.stage == 0:
        cbpath = binpath
    else:
        srepo = paths.stage_repository()
        cbpath = pathlib.Path("/stagepkgs") / binpath.relative_to(srepo)

    # make repo if needed
    repo.mkdir(parents=True, exist_ok=True)

    # remove any potential outdated package
    binpath.unlink(missing_ok=True)

    # in stage 0 we need to use the host apk, avoid fakeroot while at it
    # we just use bwrap to pretend we're root and that's all we need
    if pkg.rparent.stage == 0:
        ret = subprocess.run(
            [
                paths.bwrap(),
                "--bind",
                "/",
                "/",
                "--uid",
                "0",
                "--gid",
                "0",
                "--",
                paths.apk(),
                "mkpkg",
                "--files",
                pkg.chroot_destdir,
                "--output",
                cbpath,
                *pargs,
            ],
            capture_output=True,
        )
    else:
        ret = chroot.enter(
            "apk",
            "mkpkg",
            "--files",
            pkg.chroot_destdir,
            "--output",
            cbpath,
            *pargs,
            capture_output=True,
            bootstrapping=False,
            ro_root=True,
            ro_build=True,
            ro_dest=False,
            unshare_all=True,
            mount_binpkgs=True,
            fakeroot=True,
            binpkgs_rw=True,
            signkey=signkey,
            wrapper=wscript,
        )

    if ret.returncode != 0:
        logger.get().out_plain(">> stderr:")
        logger.get().out_plain(ret.stderr.decode())
        pkg.error("failed to generate package")


def genpkg(pkg, repo, arch, binpkg, adesc=None):
    origin = pkg.origin
    if pkg.alternative:
        # extract from the name instead
        origin = f"alt:{pkg.alternative}"

    deps, provides, replaces, riif = _get_new_deps(pkg, origin)
    over, odeps, oprovides, oiif = _get_old_deps(pkg, arch)

    if pkg.subdesc:
        bpdesc = f"{pkg.pkgdesc} ({pkg.subdesc})"
    else:
        bpdesc = pkg.pkgdesc

    if adesc:
        pdesc = f"{bpdesc} ({adesc})"
    else:
        pdesc = bpdesc

    signkey = asign.get_keypath()
    pargs = _get_cmdline(
        pkg, arch, origin, pdesc, deps, provides, replaces, riif, signkey
    )

    _print_diff("dependencies", pkg, over, odeps, deps)
    _print_diff("providers", pkg, over, oprovides, provides)
    _print_diff("install-ifs", pkg, over, oiif, riif)

    # generate a wrapper script for fakeroot ownership
    wscript = """
#!/bin/sh
set -e
"""

    needscript = False

    # as fakeroot, add extended attributes and capabilities
    # this needs to be done BEFORE chowning, or fakeroot messes things up
    for f in pkg.file_xattrs:
        fpath = pkg.chroot_destdir / f
        attrs = pkg.file_xattrs[f]
        qfp = shlex.quote(str(fpath))
        for a in attrs:
            needscript = True
            av = attrs[a]
            if av is False:
                wscript += f"""setfattr -x {a} {qfp}\n"""
                continue
            if a == "security.capability":
                wscript += f"""setcap "{av}" {qfp}\n"""
                continue
            # regular attr set
            wscript += f"""setfattr -n {a} -v "{av}" {qfp}\n"""

    # at this point permissions are already applied, we just need owners
    for f in pkg.file_modes:
        fpath = pkg.chroot_destdir / f
        recursive = False
        if len(pkg.file_modes[f]) == 4:
            uname, gname, fmode, recursive = pkg.file_modes[f]
        else:
            uname, gname, fmode = pkg.file_modes[f]
        # avoid noops (except when xattring, then we need to re-chown)
        if (uname == "root" or uname == 0) and (gname == "root" or gname == 0):
            if f not in pkg.file_xattrs:
                continue
        # now we know it's needed
        needscript = True
        # handle recursive owner
        if recursive:
            chcmd = "chown -R"
        else:
            chcmd = "chown"
        wscript += f"""{chcmd} {uname}:{gname} {shlex.quote(str(fpath))}\n"""

    # execute what we were wrapping
    wscript += """exec "$@"\n"""

    if pkg.rparent.stage == 0 or not needscript:
        # disable wrapper script unless we have a real chroot
        wscript = None

    try:
        _invoke_mkpkg(pkg, repo, pargs, repo / binpkg, signkey, wscript)
    finally:
        pkg.rparent._stage[repo] = True


def generate(pkg):
    arch = pkg.rparent.profile().arch
    binpkg = f"{pkg.pkgname}-{pkg.pkgver}-r{pkg.pkgrel}.apk"

    stagebase = paths.stage_repository()
    repobase = stagebase / pkg.rparent.repository

    if pkg.pkgname.endswith("-dbg"):
        repo = repobase / "debug" / arch
    else:
        repo = repobase / arch

    genpkg(pkg, repo, arch, binpkg, adesc=pkg.autopkg)
