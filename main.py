from modules.ui import Window, EditorView, GameView
import platform
import os
from modules.data import data

windows = Window()
data.window = windows

view = GameView()

windows.display(view)
windows.run()
