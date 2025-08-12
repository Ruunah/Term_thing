def run(self, args):
    try:
        if args:
            if isinstance(args, str):
                if args.startswith("~/"):
                    target_path = args
                elif args.startswith("/"):
                    target_path = self.vfs.cwd / args

            for i in range(len(args)):
                if args.startswith("~/"):
                    target_path = args[i]
                elif args.startswith("/"):
                    target_path = self.vfs.cwd / args[i]
        else:
            target_path = self.vfs.cwd
        
        self.insertPlainText("\n")
        for item in target_path.iterdir():
            self.insertPlainText(str(item)[len(str(target_path))+1:]+"\n")
    except:
        self.insertPlainText(Error)
