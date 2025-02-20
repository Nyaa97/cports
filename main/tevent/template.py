pkgname = "tevent"
pkgver = "0.16.2"
pkgrel = 0
build_style = "waf"
configure_script = "buildtools/bin/waf"
configure_args = [
    "--disable-rpath",
    "--disable-rpath-install",
    "--builtin-libraries=replace",
    "--bundled-libraries=NONE",
]
hostmakedepends = [
    "pkgconf",
    "python",
    "gettext",
    "docbook-xsl-nons",
    "libxslt-progs",
]
makedepends = [
    "python-devel",
    "talloc-devel",
    "cmocka-devel",
    "gettext-devel",
]
pkgdesc = "Event system based on talloc"
maintainer = "q66 <q66@chimera-linux.org>"
license = "LGPL-3.0-or-later"
url = "https://tevent.samba.org"
source = f"https://download.samba.org/pub/tevent/tevent-{pkgver}.tar.gz"
sha256 = "f0bbd29dfabbcbbce9f4718fc165410cdd4f7d8ee1f3dfc54618d4c03199cea3"
# we don't want their makefile
env = {"PYTHONHASHSEED": "1", "WAF_MAKE": "1"}
# FIXME check fails in some envs
options = ["!cross", "!check", "linkundefver"]


@subpackage("tevent-devel")
def _(self):
    return self.default_devel()


@subpackage("tevent-python")
def _(self):
    self.subdesc = "Python bindings"
    self.depends += ["python"]

    return ["usr/lib/python*"]
