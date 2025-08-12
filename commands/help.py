from commands import command_registry

def run(self, args=""):
    if not args:
        self.insertPlainText("\n")
        for key in command_registry:
            self.insertPlainText(key+"\n")
