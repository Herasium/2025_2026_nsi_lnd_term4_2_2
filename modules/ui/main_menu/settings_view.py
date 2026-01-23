import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.debug_display_all_tiles.view import DebugTilesView

from modules.data.nodes.path import Path

from modules.data import data

from pyglet.graphics import Batch
import sys


class SettingView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.JET

        self.ui_border_sheet = arcade.SpriteSheet("assets/ui_border_grid.png")

        self.ui_border_tiles = self.ui_border_sheet.get_texture_grid(
            size = (64, 64),
            columns = 4,
            count = 4*4,
        )

        self.ui_sheet = arcade.SpriteSheet("assets/ui_grid.png")

        self.ui_tiles = self.ui_sheet.get_texture_grid(
            size = (32, 32),
            columns = 23,
            count = 9*23,
        )

        self.back_button = Button(self.ui_tiles)
        self.back_button.x = 192 / 2.5
        self.back_button.y = 1010
        self.back_button.width = 150
        self.back_button.height = 100


    def on_key_press(self, key, key_modifiers):
        if key == 97: #"a"
            arcade.exit()

    def draw_tile(self,id,x,y):
        self.back_button.draw()

    def on_draw(self):
       self.clear()
       self.back_button.draw()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x,y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.back_button.touched :
            from modules.ui.main_menu.in_progress_view import MainMenuView
            data.window.display(MainMenuView())
