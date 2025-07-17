import os
import sys
from datetime import datetime
from commands import command_registry

def main():
    while true:
            try:
                command_input = input("~~>").strip()
                if not command_input:
                    continue
                if exit == command_input:
                    break
            except(KeyboardInterrupt, EOFError):
                print("Exiting...")
                break