pkgname = "kde-gtk-config"
pkgver = "6.3.1"
pkgrel = 0
build_style = "cmake"
hostmakedepends = [
    "cmake",
    "extra-cmake-modules",
    "gettext",
    "ninja",
    "pkgconf",
    "sassc",
]
makedepends = [
    "gsettings-desktop-schemas-devel",
    "kcolorscheme-devel",
    "kconfig-devel",
    "kcoreaddons-devel",
    "kdbusaddons-devel",
    "kdecoration-devel",
    "kguiaddons-devel",
    "kwindowsystem-devel",
    "qt6-qtbase-devel",
    "qt6-qtsvg-devel",
]
pkgdesc = "KDE settings synchronization for GTK applications"
maintainer = "Jami Kettunen <jami.kettunen@protonmail.com>"
license = "GPL-2.0-only OR GPL-3.0-only"
url = "https://invent.kde.org/plasma/kde-gtk-config"
source = f"$(KDE_SITE)/plasma/{pkgver}/kde-gtk-config-{pkgver}.tar.xz"
sha256 = "e3972732a69697672c8933dea21fdc32885b28a47071bbcfd8791270d582d62a"
