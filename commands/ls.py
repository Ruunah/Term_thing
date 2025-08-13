from pathlib import Path as path

def run(self, args):
    if args:
        if isinstance(args, str):
            if args.startswith("~/"):
                target_path = self.vfs.home / args
            elif args.startswith("/"):
                target_path = self.vfs.cwd / args
        
        else:
            for i in range(len(args)):
                if args.startswith("~/"):
                    target_path = self.vfs.home / args[i]
                elif args.startswith("/"):
                    target_path = self.vfs.cwd / args[i]
    else:
        target_path = self.vfs.cwd
        
    self.insertPlainText("\n")

    files=[]
    dirs=[]
    for item in target_path.iterdir():
        if path.is_file(item):
            files+=(str(item)[len(str(target_path))+1:]+"\n")

        elif path.is_dir(item): 
            dirs+=(str(item)[len(str(target_path))+1:]+"/\n")

        else:
            return self.insertPlainText("Error, file "+str(item)[len(str(target_path))+1:]+" doesnt exist"+"\n")

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