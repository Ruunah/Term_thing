def run(self, args):
    if args:
        return self.insertPlainText("\n"+str(args)+"\n")
    else:
        return self.insertPlainText("\nNo arguments input\n")
