pkgname = "meson"
pkgver = "1.7.0"
pkgrel = 0
build_style = "python_pep517"
hostmakedepends = [
    "python-build",
    "python-devel",
    "python-installer",
    "python-setuptools",
]
depends = ["python", "ninja"]
pkgdesc = "Meson build system"
maintainer = "q66 <q66@chimera-linux.org>"
license = "Apache-2.0"
url = "https://mesonbuild.com"
source = f"https://github.com/mesonbuild/meson/releases/download/{pkgver}/meson-{pkgver}.tar.gz"
sha256 = "08efbe84803eed07f863b05092d653a9d348f7038761d900412fddf56deb0284"
# meson is early in our bootstrap path but has a million checkdepends
options = ["!check"]


def post_install(self):
    # vim syntax
    self.install_dir("usr/share/vim/vimfiles")
    for f in ["ftdetect", "ftplugin", "indent", "syntax"]:
        self.install_files(
            f"data/syntax-highlighting/vim/{f}", "usr/share/vim/vimfiles"
        )
    with self.pushd("data/shell-completions"):
        self.install_completion("bash/meson", "bash")
        self.install_completion("zsh/_meson", "zsh")
