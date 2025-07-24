from commands import command_registry

def run(self, args=""):
    if not args:
        bleb = "\n"
        for key in command_registry:
            bleb += str(command_registry[key])+"\n"
        print(self.insertPlainText(bleb))
        return self.insertPlainText(bleb)
