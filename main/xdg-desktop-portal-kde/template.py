pkgname = "xdg-desktop-portal-kde"
pkgver = "6.3.0"
pkgrel = 0
build_style = "cmake"
make_check_env = {"QT_QPA_PLATFORM": "offscreen"}
make_check_wrapper = ["dbus-run-session"]
hostmakedepends = [
    "cmake",
    "extra-cmake-modules",
    "gettext",
    "ninja",
    "pkgconf",
]
makedepends = [
    "kconfig-devel",
    "kcoreaddons-devel",
    "kcrash-devel",
    "kglobalaccel-devel",
    "kguiaddons-devel",
    "ki18n-devel",
    "kiconthemes-devel",
    "kio-devel",
    "kirigami-devel",
    "knotifications-devel",
    "kstatusnotifieritem-devel",
    "kwayland-devel",
    "plasma-wayland-protocols",
    "qt6-qtbase-private-devel",  # qxkbcommon_p.h
    "qt6-qtdeclarative-devel",
    "qt6-qtwayland-devel",
    "wayland-protocols",
]
depends = [
    "kiconthemes",
    "kio-fuse",
    "plasma-workspace",
    "xdg-desktop-portal",
]
checkdepends = [
    "dbus",
    "python-gobject",
    *depends,
]
pkgdesc = "Backend implementation for xdg-desktop-portal using Qt/KF6"
maintainer = "Jami Kettunen <jami.kettunen@protonmail.com>"
license = "LGPL-2.0-or-later"
url = "https://invent.kde.org/plasma/xdg-desktop-portal-kde"
source = f"$(KDE_SITE)/plasma/{pkgver}/xdg-desktop-portal-kde-{pkgver}.tar.xz"
sha256 = "b30cf5716685bea9161b7ac3dcbaaa31156627399850d74592c06e9cd4dd0f51"
hardening = ["vis"]


def post_install(self):
    self.uninstall("usr/lib/systemd/user")
