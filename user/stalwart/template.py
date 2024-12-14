pkgname = "stalwart"
pkgver = "0.10.4"
pkgrel = 0
build_style = "cargo"
hostmakedepends = [
    "cargo",
    "pkgconf",
]
makedepends = [
    "zstd-devel",
    "sqlite-devel",
    "linux-headers",
]
pkgdesc = "Secure & Modern All-in-One Mail Server - IMAP, JMAP, POP3, SMTP"
maintainer = "nyaah <nyaah@ewry.one>"
license = "AGPL-3.0-only OR custom:Stalwart"
url = "https://github.com/stalwartlabs/mail-server"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "ab2d5db7eed3c223d7f0ca686a475cdde946dd8481b64e6d978b8012352748a2"

def build(self):
    from cbuild.util import cargo
    cargo.Cargo(self).build(args=["--manifest-path=crates/main/Cargo.toml"])

def install(self):
    from cbuild.util import cargo
    retv = cargo.Cargo(self)._invoke(
        "install",
        [
            "--root",
            str(self.chroot_destdir / "usr"),
            "--path",
            "crates/main",
            "--no-track",
            *self.make_install_args,
            None,
        ],
        None,
        True,
        self.make_install_env,
        {},
        None,
        self.make_install_wrapper,
        [],
    )

    self.install_license("LICENSES/AGPL-3.0-only.txt")
    self.install_license("LICENSES/LicenseRef-SEL.txt")

    return retv
