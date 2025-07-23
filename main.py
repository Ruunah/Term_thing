import os
import sys
import subprocess
from window.window import main as window
from commands.clear import run as clear
from commands import command_registry


def command_execution(command_name, args):
    command_registry[command_name](*args)

def main():
    clear()

    gui_process = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "utils", "gui_runner.py")])


    while True:
            try:
                command_input = input("-->").split()
                command_name=command_input[0]
                args=command_input[1:]

                if not command_input:
                    continue

                if command_name in command_registry:
                    command_execution(command_name, args)

                if "exit" == command_name:
                    clear()
                    print("Exiting...")
                    break

            except(KeyboardInterrupt, EOFError):
                clear()
                print("Exiting...")
                break

            finally:
                gui_process.terminate()
                gui_process.wait

if __name__ == "__main__":
    main()
