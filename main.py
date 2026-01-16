from modules.ui import Window, EditorView, GameView
from modules.data import data
import arcade

arcade.load_font("assets/press_start.ttf")

windows = Window()
data.window = windows

view = GameView()

windows.display(view)
windows.run()
