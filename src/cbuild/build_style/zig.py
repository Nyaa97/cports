from cbuild.util import zig

def prepare(self):
    zig.prepare(self)

def build(self):
    zig.build(self, self.zig_build_args)

def install(self):
    zig.install(self)

def use(tmpl):
    tmpl.prepare = prepare
    tmpl.build = build
    tmpl.install = install
