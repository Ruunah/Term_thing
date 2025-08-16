def run(self, args=""):
    if args:
        if isinstance(args, str):
            self.insertPlainText(f"\n{args}\n")
        else:
            self.insertPlainText("\n")
            for key in args:
                self.insertPlainText(f"{key}\n")
    else:
        self.insertPlainText("\nNo arguments input\n")
