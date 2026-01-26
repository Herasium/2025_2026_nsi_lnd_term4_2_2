from modules.ui import Window, EditorView, MainMenuView
from modules.data import data
from modules.data.loader import load_saves,load_tiles, load_font, load_textures
from modules.logger import Logger
import arcade
import os

arcade.enable_timings()
path = os.path.dirname(os.path.abspath(__file__)) 

data.current_path = path
data.loaded_chips = {}

logger = Logger("Main")

logger.print(f"Logic Box, v.{data.VERSION}.")
logger.print(f"Current path: {path}")

load_font()
logger.print("Loaded Font.")
load_tiles()
logger.print("Loaded Tiles.")

windows = Window()
data.window = windows
logger.print("Created Window.")

load_textures()
logger.print("Loaded textures.")

load_saves()
logger.print("Loaded saves files.")

view = MainMenuView()

windows.display(view)
windows.run()
