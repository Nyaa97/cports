pkgname = "libaec"
pkgver = "1.1.3"
pkgrel = 1
build_style = "cmake"
hostmakedepends = [
    "cmake",
    "ninja",
]
pkgdesc = "Adaptive entropy coding library"
maintainer = "Orphaned <orphaned@chimera-linux.org>"
license = "BSD-2-Clause"
url = "https://gitlab.dkrz.de/k202009/libaec"
source = f"{url}/-/archive/v{pkgver}.tar.gz"
sha256 = "453de44eb6ea2500843a4cf4d2e97d1be251d2df7beae6c2ebe374edcb11e378"


def post_install(self):
    self.install_license("LICENSE.txt")
    self.rename("usr/cmake", "lib/cmake")


@subpackage("libaec-devel")
def _(self):
    return self.default_devel()
