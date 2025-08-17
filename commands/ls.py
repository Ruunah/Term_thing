from pathlib import Path as path

def run(self, args):
    if args:
        if isinstance(args, str):
            args = args.strip()
            if args.startswith("~/"):
                target_path = self.vfs.home / args[2:]

            elif args.startswith("/"):
                target_path = self.vfs.root / args[1:]

            else:
                target_path = self.vfs.cwd / args
        
        else:
            arg = args[0].strip()
            if arg.startswith("~/"):
                target_path = self.vfs.home / arg[2:]

            elif arg.startswith("/"):
                target_path = self.vfs.root / arg[1:]

            else:
                target_path = self.vfs.cwd / arg

    else:
        target_path = self.vfs.cwd

    self.insertPlainText("\n")

    files=[]
    dirs=[]
    try:
        for item in target_path.iterdir():
            if path.is_file(item):
                files.append(str(item)[len(str(target_path))+1:]+"\n")

            elif path.is_dir(item): 
                dirs.append(str(item)[len(str(target_path))+1:]+"/\n")


        if isinstance(files, list):
            for key in files:
                self.insertPlainText(key)
        else:
            self.insertPlainText(files)

        if isinstance(dirs, list):
            for key in dirs:
                self.insertPlainText(key)
        else:
            self.insertPlainText(dirs)

    except:
        self.insertPlainText("Error, input path is invalid\n")
