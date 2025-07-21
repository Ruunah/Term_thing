from commands import command_registry
def run(args=""):
    if not args:
        for key in command_registry:
            print(key)