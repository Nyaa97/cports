# real flamegraph name is for the original perl project; this also has a cargo
# plugin
pkgname = "cargo-flamegraph"
pkgver = "0.6.7"
pkgrel = 1
build_style = "cargo"
hostmakedepends = ["cargo-auditable"]
makedepends = ["rust-std"]
depends = ["perf"]
pkgdesc = "Perf-based flamegraph generator"
maintainer = "Orphaned <orphaned@chimera-linux.org>"
license = "Apache-2.0 OR MIT"
url = "https://github.com/flamegraph-rs/flamegraph"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "d7fa901673f4ece09226aeda416b98f919b7d946541ec948f1ef682bd6eec23b"
# no tests
options = ["!check"]


def post_build(self):
    for shell in ["bash", "fish", "zsh"]:
        with open(self.cwd / f"flamegraph.{shell}", "w") as f:
            self.do(
                f"./target/{self.profile().triplet}/release/flamegraph",
                "--completions",
                shell,
                stdout=f,
            )


def post_install(self):
    for shell in ["bash", "fish", "zsh"]:
        self.install_completion(f"flamegraph.{shell}", shell, "flamegraph")
    self.install_license("LICENSE-MIT")
