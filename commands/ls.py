def run(self, args):
    result=[]
    if args:
        for i in range(len(args())):
            if args.startswith("~/"):
                target_path = args[i]
            elif args.startswith("/"):
                target_path = self.vfs.cwd / args[i]
    else:
        target_path = self.vfs.cwd
    
    for item in target_path.interdir():
        self.insertPlainText(item)
