pkgname = "krdc"
pkgver = "24.08.3"
pkgrel = 1
build_style = "cmake"
configure_args = ["-DWITH_RDP3=ON", "-DWITH_RDP=OFF"]
hostmakedepends = [
    "cmake",
    "extra-cmake-modules",
    "freerdp",
    "gettext",
    "ninja",
    "pkgconf",
]
makedepends = [
    "freerdp-devel",
    "kbookmarks-devel",
    "kcmutils-devel",
    "kcompletion-devel",
    "kconfig-devel",
    "kdnssd-devel",
    "kdoctools-devel",
    "ki18n-devel",
    "kiconthemes-devel",
    "kio-devel",
    "knotifications-devel",
    "knotifyconfig-devel",
    "kstatusnotifieritem-devel",
    "kwallet-devel",
    "kwidgetsaddons-devel",
    "kwindowsystem-devel",
    "kxmlgui-devel",
    "libssh-devel",
    "libvncserver-devel",
    "plasma-activities-devel",
    "qt6-qtbase-devel",
    "qt6-qtwayland-devel",
]
depends = ["freerdp"]
pkgdesc = "KDE remote desktop client"
maintainer = "Jami Kettunen <jami.kettunen@protonmail.com>"
license = "GPL-2.0-or-later"
url = "https://apps.kde.org/krdc"
source = f"$(KDE_SITE)/release-service/{pkgver}/src/krdc-{pkgver}.tar.xz"
sha256 = "2f04a408434702aee49caf9c0193c3471a049f341b0e8a36a773e7ed93810af0"


@subpackage("krdc-devel")
def _(self):
    return self.default_devel()
