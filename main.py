import os
import sys
import subprocess
from commands.clear import run as clear
from datetime import datetime
from commands import command_registry

def main():
    while True:
            try:
                command_input = input("-->").split()
                if not command_input:
                    continue
                command_name=command_input[0]
                args=command_input[1:]

                if command_name in command_registry:
                    command_execution()

                if "exit" == command_name:
                    clear()
                    print("Exiting...")
                    break

            except(KeyboardInterrupt, EOFError):
                clear()
                print("Exiting...")
                break

def command_execution(command_input, args):
    command_registry[command_name](*args)

if __name__ == "__main__":
    main()
