pkgname = "gopass"
pkgver = "1.15.15"
pkgrel = 0
build_style = "go"
hostmakedepends = ["go"]
checkdepends = ["git", "gnupg"]
pkgdesc = "Pass-compatible password manager with more features"
maintainer = "Orphaned <orphaned@chimera-linux.org>"
license = "MIT"
url = "https://www.gopass.pw"
source = (
    f"https://github.com/gopasspw/gopass/archive/refs/tags/v{pkgver}.tar.gz"
)
sha256 = "00ad6a32f89fe64760b70b9424af19b88d671673a66424d59d80cfa97deb75d3"
# needs initialising git config
options = ["!check"]


def post_install(self):
    self.install_man("gopass.1")
    self.install_license("LICENSE")
    self.install_completion("bash.completion", "bash")
    self.install_completion("zsh.completion", "zsh")
    self.install_completion("fish.completion", "fish")
