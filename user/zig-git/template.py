pkgname = "zig-git"
pkgver = "0.14.0_git1702"
_pkgver = "0.14.0-dev.1702+26d35cc11"
pkgrel = 0
build_style = "cmake"
configure_args = [
    "-DZIG_PIE=ON",
    "-DZIG_SHARED_LLVM=ON",
    "-DZIG_TARGET_MCPU=native",
]
hostmakedepends = [
    "cmake",
    "ninja",
]
makedepends = [
    "clang-devel",
    "linux-headers",
    "lld-devel",
    "llvm-devel",
    "ncurses-devel",
    "zlib-ng-compat-devel",
    "zstd-devel",
]
pkgdesc = "Zig programming language toolchain"
maintainer = "psykose <alice@ayaya.dev>"
license = "MIT"
url = "https://github.com/ziglang/zig"
source = f"https://ziglang.org/builds/zig-{_pkgver}.tar.xz"
sha256 = "8d69b7eb9cd1bbcc44d166d77126486f7f4912ae8c7a5f0d2d664ff59c1604ab"
# lighten up the build, only applies to bootstrap and just slows down the build
tool_flags = {"CFLAGS": ["-U_FORTIFY_SOURCE"]}
hardening = ["!int", "!scp", "!ssp", "!var-init"]
options = ["!lto"]

restricted = "work in progress (needs to either not need llvm or for us to multiversion llvm)"

match self.profile().arch:
    case "x86_64" | "aarch64":
        pass
    case _:
        # disable tests on other archs, a lot of them fail
        options += ["!check"]


def check(self):
    self.do(
        self.make_dir + "/stage3/bin/zig",
        "build",
        "test",
        "--summary",
        "all",
        "-Dcpu=native",
        "-Dskip-debug",
        "-Dskip-non-native",
        "-Dskip-release-safe",
        "-Dskip-release-small",
    )


def post_install(self):
    self.install_license("LICENSE")
