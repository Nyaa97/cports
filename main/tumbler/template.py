pkgname = "tumbler"
pkgver = "4.20.0"
pkgrel = 0
build_style = "gnu_configure"
hostmakedepends = [
    "automake",
    "gettext-devel",
    "gtk-doc-tools",
    "pkgconf",
    "slibtool",
    "xfce4-dev-tools",
]
makedepends = [
    "freetype-devel",
    "gdk-pixbuf-devel",
    "glib-devel",
    "gst-plugins-base-devel",
    "curl-devel",
    "libgsf-devel",
    "libjpeg-turbo-devel",
    "libopenraw-devel",
    "libpng-devel",
    "libxfce4util-devel",
    "poppler-devel",
    # TODO: libgepub, if/when it moves off libsoup2
]
depends = ["cover-thumbnailer"]
pkgdesc = "Xfce implementation of the thumbnail management D-Bus spec"
maintainer = "triallax <triallax@tutanota.com>"
license = "GPL-2.0-or-later"
url = "https://docs.xfce.org/xfce/tumbler/start"
source = f"$(XFCE_SITE)/xfce/tumbler/{pkgver[:-2]}/tumbler-{pkgver}.tar.bz2"
sha256 = "74b1647d55926547e98bfac70838ff63c5a84299a5e10c81c38d1fab90e25880"


def post_install(self):
    self.uninstall("usr/lib/systemd/user")


@subpackage("tumbler-devel")
def _(self):
    return self.default_devel()
