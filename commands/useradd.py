from utils import module_registry



def run(window_self, args):
    if not args:
        self.insertPlainText("\nNo argument input\n")
    else:
        if isinstance(args, list):
            for i in len(args-1)
                if args[i].startswith("-"):
                    arg = args[i]
                    match arg[1:]:
                        case "g":
                            if args[i+1] in vfs_reference("root/etc/group"): 


        else args.startswith("-"):
            self.insertPlainText("\nUsername cannot start with -\n")
