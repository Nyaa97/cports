pkgname = "kumomta"
pkgver = "2024.09.02"
_pkgrev = "c5476b89"
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
]
pkgdesc = "First Open-Source high-performance MTA developed from the ground-up"
maintainer = "nyaah <nyaah@ewry.one>"
license = "Apache-2.0"
url = "https://github.com/KumoCorp/kumomta"
source = f"{url}/archive/refs/tags/{pkgver}-{_pkgrev}.tar.gz"
sha256 = "daead10dd9f1846b95c1be1a9981cbed296da34adf5b32ef2f178a697a936a41"

