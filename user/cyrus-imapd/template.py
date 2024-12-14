pkgname = "cyrus-imapd"
pkgver = "3.10.0"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--enable-autocreate",
    "--enable-afs",
    "--enable-idled",
    "--enable-calalarmd",
    "--enable-backup",
    "--enable-jmap",
    "--enable-xapian",
    "--enable-http",
    "--with-openssl=yes"
    "--with-ldap",
    "--with-libcap",
]
hostmakedepends = [
    "pkgconf",
    "byacc",
    "bison",
    "flex",
    "rsync",
    "xxd",
    "perl",
]
makedepends = [
    "sqlite-devel",
    "openssl-devel",
    "jansson-devel",
    "icu-devel",
    "libsasl-devel",
    "xapian-core-devel",
    "libxml2-devel",
    "libical-devel",
    "chimerautils-devel",
]
depends = [
    "rsync",
]
pkgdesc = "Cyrus IMAP is an email, contacts and calendar server"
maintainer = "nyaah <nyaah@ewry.one>"
license = "BSD-3-Clause-Attribution"
url = "https://cyrusimap.org"
source = f"https://github.com/cyrusimap/{pkgname}/releases/download/{pkgname}-{pkgver}/{pkgname}-{pkgver}.tar.gz"
sha256 = "bef0fefa776862629c17cdde268c9b8d17ae1ae6fd087a4c5e52524c66c33a23"

def post_install(self):
    self.install_license("COPYING")

tool_flags = {"LDFLAGS": ["-lfts"]}
configure_gen = []
