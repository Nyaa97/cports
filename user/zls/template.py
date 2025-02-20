pkgname = "zls"
pkgver = "0.14.0_git3241"
_pkgver = "0.14.0-dev.3241+55c46870b"
_commit = "7f367a64106d4eb2dc3656e24a1a4370358080ec"
pkgrel = 0
build_style = "zig"
zig_build_args = [
    f"-Dversion-string={_pkgver}"
]
hostmakedepends = [
    "zig-git",
]
pkgdesc = "Zig language server supporting Zig developers"
maintainer = "nyaah <nyaah@ewry.one>"
license = "MIT"
url = "https://github.com/zigtools/zls"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "409fae63c81a0b5b66083f6dd7ee8ad1a578c200cbdaf13e4c9340bdd666023a"

def post_install(self):
    self.install_license("LICENSE")
