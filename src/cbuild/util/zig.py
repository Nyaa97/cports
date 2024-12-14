from cbuild.util import zonpy

def prepare(pkg):
    zon = zonpy.load(pkg.cwd / "build.zig.zon")
    for obj in zon['dependencies'].values():
        pkg.do(
            "zig",
            "fetch",
            "--global-cache-dir",
            ".zig-cache",
            obj["url"],
            allow_network = True,
        )


def build(pkg, extra_args=[]):
    profile = pkg.profile()
    sysroot = profile.sysroot
    with open(pkg.cwd / "cbuild_zig_libc.txt", mode="w") as f:
        f.write(
            f"""include_dir={sysroot}/usr/include
sys_include_dir={sysroot}/usr/include
crt_dir={sysroot}/lib
msvc_lib_dir=
kernel32_lib_dir=
gcc_dir=

"""
        )

    zig_arch = None
    zig_cpu = None
    match profile.arch:
        # TODO other architectures
        case "x86_64" | "aarch64":
            zig_arch = profile.arch
            zig_cpu = "native"

    # The Zig build system only has a single install step, there is no
    # way to build artifacts for a given prefix and then install those artifacts
    # to that prefix at some later time. Therefore, we build and install to the zig-out
    # directory and later copy the artifacts to the destdir in do_install().
    # We use zig-out to avoid path conflicts as it is the default install
    # prefix used by the zig build system.
    pkg.do(
        "zig",
        "build",
        "-j" + str(pkg.make_jobs),
        "--sysroot",
        sysroot,
        "--libc",
        "cbuild_zig_libc.txt",
        "--search-prefix",
        "/usr",
        "--prefix",
        "/usr",
        "--system",
        ".zig-cache/p",
        "--release=safe",
        f"-Dtarget={zig_arch}-linux-musl",
        f"-Dcpu={zig_cpu}",
        *extra_args,
        env={"DESTDIR": "zig-out"},
    )


def install(pkg):
    for x in (pkg.cwd / "zig-out").iterdir():
        pkg.install_files(x, ".")
