import os
import sys

from controller.controller import Controller

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    controller = Controller()
    controller.run()
