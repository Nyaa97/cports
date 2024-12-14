pkgname = "zls"
pkgver = "0.13.0"
pkgrel = 0
build_style = "zig"
zig_build_args = [
    f"-Dversion_data_path=ref/langref.html.in"
]
hostmakedepends = [
    "zig",
]
pkgdesc = "Zig language server supporting Zig developers"
maintainer = "nyaah <nyaah@ewry.one>"
license = "MIT"
url = "https://github.com/zigtools/zls"
source = [
    f"{url}/archive/{pkgver}.tar.gz",
    f"https://raw.githubusercontent.com/ziglang/zig/{pkgver}/doc/langref.html.in"
]
source_paths = [".", "ref"]
sha256 = [
    "2e8046b6b0de765a4bf4bb828345e2badc8b828bc257dc931d0f56b147684d9f",
    "5d43f599f56a1ee0246958552545d13ee4ddeb7c705c05a432554d5eff6e1902"
]

def post_install(self):
    self.install_license("LICENSE")
