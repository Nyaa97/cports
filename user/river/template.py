pkgname = "river"
pkgver = "0.4.0_git250220"
_commit = "866c8166a3"
pkgrel = 0
build_style = "zig"
prepare_after_patch = True
zig_build_args = [
    "-Dxwayland"
]
hostmakedepends = [
    "zig-git",
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
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "8ea9ce2287672206af6e59bbae8841363658bcded32448ef1164e1d44adb9d53"

hardening = ["!pie"]
