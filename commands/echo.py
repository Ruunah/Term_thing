def run(self, args):
    if args:
        self.insertPlainText("\n"+str(args)+"\n")
    else:
        self.insertPlainText("\nNo arguments input\n")
