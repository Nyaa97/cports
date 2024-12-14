pkgname = "river"
pkgver = "0.3.5"
pkgrel = 0
build_style = "zig"
zig_build_args = [
    "-Dxwayland"
]
hostmakedepends = [
    "zig",
    "pkgconf",
    "scdoc",
]
makedepends = [
    "wayland-devel",
    "wayland-protocols",
    "wlroots0.18-devel",
    "libxkbcommon-devel",
    "libevdev-devel",
    "pixman-devel",
]
pkgdesc = "Dynamic tiling Wayland compositor"
maintainer = "nyaah <nyaah@ewry.one>"
license = "GPL-3.0-or-later"
url = "https://codeberg.org/river/river"
source = f"{url}/archive/v{pkgver}.tar.gz"
sha256 = "572885eea1e689f582ff327eaf2f74a8f11f562a781695d18d8650ccab161d11"

hardening = ["!pie"]
