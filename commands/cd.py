import os
import pathlib

def run(self, args):
    if args:
        self.insertPlainText("\n")
        if isinstance(args, str):
            if args != "..":
                if args.startswith("~/"):
                    start = self.vfs.home
                    args = args[2:]

                elif args.startswith("/"):
                    start = self.vfs.root
                    args = args[1:]

                else:
                    start = self.vfs.cwd

                args = args.strip().split("/")
                if len(args)<=1:
                    self.vfs.cwd = pathlib.Path(os.path.join(start, args[0]))

                else:
                    result = start
                    for part in args:
                        result = os.path.join(result, part)

                    self.vfs.cwd = pathlib.Path(result)

            else:
                if self.vfs.cwd != self.vfs.root:
                    self.vfs.cwd = self.vfs.cwd.parent
