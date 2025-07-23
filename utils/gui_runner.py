import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from window.window import main as window_main

if __name__ == "__main__":
    window_main()
