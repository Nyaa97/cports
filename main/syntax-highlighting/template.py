pkgname = "syntax-highlighting"
pkgver = "6.8.0"
pkgrel = 0
build_style = "cmake"
hostmakedepends = [
    "cmake",
    "extra-cmake-modules",
    "ninja",
    "perl",
    "pkgconf",
]
makedepends = [
    "qt6-qtdeclarative-devel",
    "qt6-qttools-devel",
]
pkgdesc = "KDE Syntax highlighting engine for structured text and code"
maintainer = "Jami Kettunen <jami.kettunen@protonmail.com>"
license = "MIT"
url = "https://api.kde.org/frameworks/syntax-highlighting/html"
source = f"$(KDE_SITE)/frameworks/{pkgver[:pkgver.rfind('.')]}/syntax-highlighting-{pkgver}.tar.xz"
sha256 = "ed3c7d3d92c154d9af39a1aba39166b07e6411c18c3100116208f3a4423b1257"
hardening = ["vis"]


def post_install(self):
    self.install_license("LICENSES/MIT.txt")


@subpackage("syntax-highlighting-devel")
def _(self):
    return self.default_devel()
