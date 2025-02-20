pkgname = "kumomta"
pkgver = "2024.11.08"
_pkgrev = "d383b033"
pkgrel = 0
build_style = "cargo"
hostmakedepends = [
    "cargo",
    "rust-bindgen",
    "pkgconf",
    "cmake",
]
makedepends = [
    "zstd-devel",
    "libgit2-devel",
    "linux-headers",
]
pkgdesc = "First Open-Source high-performance MTA developed from the ground-up"
maintainer = "nyaah <nyaah@ewry.one>"
license = "Apache-2.0"
url = "https://github.com/KumoCorp/kumomta"
source = f"{url}/archive/refs/tags/{pkgver}-{_pkgrev}.tar.gz"
sha256 = "90056a2fcc21d588a96c391be4002a58cb391149579add5078c62a12ecbe3066"

