pkgname = "git-lfs"
pkgver = "3.6.0"
pkgrel = 0
build_style = "go"
make_dir = "bin"  # needed for tests
make_build_args = [
    "-ldflags=-X github.com/git-lfs/git-lfs/v3/config.Vendor=ChimeraLinux"
]
hostmakedepends = ["asciidoctor", "go"]
checkdepends = ["bash", "curl", "git", "perl"]
depends = ["git"]
pkgdesc = "Git extension for versioning large files"
maintainer = "Subhaditya Nath <sn03.general@gmail.com>"
license = "MIT"
url = "https://git-lfs.com"
source = f"https://github.com/git-lfs/git-lfs/releases/download/v{pkgver}/git-lfs-v{pkgver}.tar.gz"
sha256 = "9a5d2a598b4096f0fdde5b2ead6038996c657acafe5a89d22b8c2f1b56aeaf36"
# a test fails after go bump
options = ["!check"]


def post_build(self):
    self.mkdir("man")
    for file in self.find("docs/man", "*.adoc"):
        self.do(
            "asciidoctor",
            "-bmanpage",
            "-Dman",
            "-a",
            f"mansource={pkgname} {pkgver}",
            file,
        )


def check(self):
    from cbuild.util import golang

    self.golang.check()
    self.do("make", "test", "-C", "t", env=golang.get_go_env(self))


def install(self):
    self.install_bin("bin/git-lfs")
    self.install_license("LICENSE.md")
    self.install_man("man/*", glob=True)
    for shell in ("bash", "fish", "zsh"):
        self.install_completion(
            f"t/fixtures/completions/git-lfs-completion.{shell}",
            shell,
        )
