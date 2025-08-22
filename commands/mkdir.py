def run(self, args):
    self.insertPlainText("\n")
    if isinstance(args, list):
        self.insertPlainText("Too many arguments input\n")

    else:
        if args.split("/") != args:
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
