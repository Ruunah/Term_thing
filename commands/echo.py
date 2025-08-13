def run(self, args=""):
    if args:
        if len(args) == 1:
            self.insertPlainText(f"\n{args[0]}\n")
        else:
            self.insertPlainText("\nToo many arguments\n")
    else:
        self.insertPlainText("\nNo arguments input\n")
