import os
import pathlib

def run(self, args):
    if args:
        self.insertPlainText("\n")
        if isinstance(args, str):
            if args != "..":
                args = args.strip().split("/")
                if len(args)<=1:
                    self.vfs.cwd = pathlib.Path(os.path.join(self.vfs.cwd, args[0]))

                else:
                    result = self.vfs.cwd
                    for part in args:
                        result = os.path.join(result, part)

                    self.vfs.cwd = pathlib.Path(result)

            else:
                if self.vfs.cwd != self.vfs.root:
                    self.vfs.cwd = self.vfs.cwd.parent
