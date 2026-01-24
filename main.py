from modules.ui import Window, EditorView, MainMenuView
from modules.data import data
from modules.data.loader import load_saves,load_tiles, load_font, load_textures
import arcade
import os

version = "0.12"
path = os.path.dirname(os.path.abspath(__file__)) 

data.current_path = path
data.loaded_chips = {}

print(f"Logic Box, v{version}.")
print(f"Current path: {path}")

load_font()
print("Loaded Font.")
load_tiles()
print("Loaded Tiles.")

windows = Window()
data.window = windows
print("Created Window.")

load_textures()
print("Loaded textures.")

load_saves()
print("Loaded saves files.")

view = MainMenuView()

windows.display(view)
windows.run()
