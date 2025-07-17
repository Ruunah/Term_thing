import os
import sys
import subprocess
from commands.clear import run as clear
from datetime import datetime
from commands import command_registry

def main():
    while True:
            try:
                command_input = input("-->").strip()
                if not command_input:
                    continue

                if command_input in command_registry:
                    command_execution()

                if "exit" == command_input:
                    clear()
                    print("Exiting...")
                    break

            except(KeyboardInterrupt, EOFError):
                clear()
                print("Exiting...")
                break

def command_execution(command_input):

if __name__ == "__main__":
    main()
