pkgname = "hplip"
pkgver = "3.24.4"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-doc-build",
    "--disable-fax-build",
    "--disable-gui-build",
    "--disable-imageProcessor-build",
    # net-snmp
    "--disable-network-build",
    "--enable-cups-drv-install",
    "--enable-cups-ppd-install",
]
make_dir = "."
# libtool relink is racy..
make_install_args = ["-j1"]
hostmakedepends = [
    "automake",
    "libtool",
    "pkgconf",
    "python-devel",
]
makedepends = [
    "cups-devel",
    "dbus-devel",
    "libjpeg-turbo-devel",
    "libusb-devel",
    "python-devel",
    "sane-backends-devel",
]
depends = [
    "python-dbus",
    "python-gobject",
]
pkgdesc = "Drivers for HP printers"
maintainer = "Orphaned <orphaned@chimera-linux.org>"
license = "GPL-2.0-only AND BSD-3-Clause AND MIT"
url = "https://developers.hp.com/hp-linux-imaging-and-printing"
source = f"https://downloads.sourceforge.net/hplip/hplip-{pkgver}.tar.gz"
sha256 = "5d7643831893a5e2addf9d42d581a5dbfe5aaf023626886b8762c5645da0f1fb"
# nuh uh
hardening = ["!vis"]
# TODO: probably ignores CC
options = ["!cross"]

tool_flags = {"CFLAGS": ["-D_GNU_SOURCE"]}


def post_extract(self):
    # the reconf fails because these files are "required"; just quickly make them all
    for f in ["NEWS", "README", "AUTHORS", "ChangeLog", "INSTALL"]:
        (self.cwd / f).touch()


def post_install(self):
    from cbuild.util import python

    python.precompile(self, "usr/share/hplip")

    self.install_license("COPYING")
    self.uninstall("usr/lib/systemd")
    # rename default dll.conf that conflicts with sane-backends to own name,
    # loads hpaio
    self.rename("etc/sane.d/dll.conf", "dll.d/hpaio")
    self.rename("etc/udev", "usr/lib/udev")

    # move elfs to libexec
    for f in ["locatedriver", "dat2drv"]:
        self.rename(
            f"usr/share/hplip/{f}", f"usr/libexec/hplip/{f}", relative=False
        )
        self.install_link(f"usr/share/hplip/{f}", f"../../libexec/hplip/{f}")
