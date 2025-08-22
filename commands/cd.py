import os
import pathlib

def run(self, args):
    self.insertPlainText("\n")
    if args:
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
                    result = pathlib.Path(os.path.join(start, args[0]))
                    if result.is_dir():
                        self.vfs.cwd = result

                    else:
                        self.insertPlainText("Error: Input path is invalid\n")

                else:
                    result = start
                    for part in args:
                        result = os.path.join(result, part)

                    if result.is_dir():
                        self.vfs.cwd = result

                    else:
                        self.insertPlainText("Error: Input path is invalid\n")

            else:
                if self.vfs.cwd != self.vfs.root:
                    self.vfs.cwd = self.vfs.cwd.parent
