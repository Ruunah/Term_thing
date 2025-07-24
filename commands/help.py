from commands import command_registry

def run(self, args=""):
    if not args:
        bleb="\n"
        for key in command_registry:
            bleb += f"{key}\n"
        return self.insertPlainText(bleb)
