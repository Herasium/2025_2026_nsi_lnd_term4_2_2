import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.editor.view import EditorView
from modules.ui.debug_display_all_tiles.view import DebugTilesView

from modules.data import data

from pyglet.graphics import Batch

class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.JET

        self.ui_sheet = arcade.SpriteSheet("assets/ui_grid.png")

        self.ui_tiles = self.ui_sheet.get_texture_grid(
            size = (32, 32),
            columns = 23,
            count = 9*23,
        )
        
        self.button_play = Button(self.ui_tiles)
        self.button_play.x = 120
        self.button_play.y = 540
        self.button_play.width = 340
        self.button_play.height = 90
        self.button_play.name = "Jouer"
        self.button_play._text_obj.x = 280
        self.button_play._text_obj.y = 495

        self.button_quit = Button(self.ui_tiles)
        self.button_quit.x = 120
        self.button_quit.y = 400
        self.button_quit.width = 340
        self.button_quit.height = 90
        self.button_quit.name = "Quitter"
        self.button_quit._text_obj.x = 280
        self.button_quit._text_obj.y = 355

        self.titre = arcade.Text(
            "LogicBox",
            x = 120,
            y = 700,
            color = arcade.color.BLOND,
            font_size = 50,
            font_name = "Press Start 2P"
        )
        self.shadow_titre = arcade.Text(
            "LogicBox",
            x = 120,
            y = 694,
            color = arcade.color.DEEP_SAFFRON,
            font_size = 50,
            font_name = "Press Start 2P"
        )


    def reset(self):
        pass

    def on_draw(self):

        self.clear()
        self.button_play.draw()
        self.button_quit.draw()
        self.shadow_titre.draw()
        self.titre.draw()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        if key == 97: #"a"
            arcade.exit()
        if key == 65307: #echap
            self.current_path = None
            self.selected_follower = None

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x,y)
        if self.button_play.rect.point_in_rect((x, y)):
            self.button_play.scale = 1.1
        else:
            self.button_play.scale = 1.0

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.button_play.touched:
            data.window.hide()
            data.window.display(DebugTilesView())

        if self.button_quit.touched:
            arcade.exit()

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass