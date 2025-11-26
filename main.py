from modules.ui import Window, EditorView, GameView
import platform
import os

def start():

    windows = Window()
    view = GameView()

    windows.display(view)
    windows.run()

if __name__ == "__main__":
    start()