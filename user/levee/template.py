pkgname = "levee"
pkgver = "0.1.4"
pkgrel = 0
build_style = "zig"
hostmakedepends = [
    "zig",
    "pkgconf",
]
makedepends = [
    "wayland-devel",
    "wayland-protocols",
    "pixman-devel",
    "fcft-devel",
    "libpulse-devel",
    "udev-devel",
]
pkgdesc = "Statusbar for the river wayland compositor"
maintainer = "nyaah <nyaah@ewry.one>"
license = "MIT"
url = "https://git.sr.ht/~andreafeletto/levee"
source = f"{url}/archive/v{pkgver}.tar.gz"
sha256 = "d3230e5a5afee6d80dee00e14e53ce149628d2c65bc101f7241bc3596822df34"
hardening = ["!pie"]

def post_install(self):
    self.install_license("LICENSE")
