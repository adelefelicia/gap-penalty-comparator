import sys
import os


from controller.controller_copy import Controller

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    controller = Controller()
    controller.run()
