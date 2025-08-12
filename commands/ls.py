from pathlib import Path as path

def run(self, args):
    try:
        if args:
            if isinstance(args, str):
                if args.startswith("~/"):
                    target_path = args
                elif args.startswith("/"):
                    target_path = self.vfs.cwd / args

            else:
                for i in range(len(args)):
                    if args.startswith("~/"):
                        target_path = args[i]
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

        self.insertPlainText(files)
        self.insertPlainText(dirs)

    except:
        self.insertPlainText("Error\n")
