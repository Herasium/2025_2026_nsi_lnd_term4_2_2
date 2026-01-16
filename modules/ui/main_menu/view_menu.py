import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.editor.view import EditorView
from modules.ui.debug_display_all_tiles.view import DebugTilesView
from modules.ui.main_menu.in_progress_view import MainMenuView

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

        self.button_quit = Button(self.ui_tiles)
        self.button_quit.x = 120
        self.button_quit.y = 400
        self.button_quit.width = 340
        self.button_quit.height = 90
        self.button_quit.name = "Quitter"

        self.titre1 = arcade.Text(
            "Welcome to",
            x = 120,
            y = 760,
            color = arcade.color.BLOND,
            font_size = 60,
            font_name = "Press Start 2P"
        )
        self.shadow_titre1 = arcade.Text(
            "Welcome to",
            x = 120,
            y = 754,
            color = arcade.color.DEEP_SAFFRON,
            font_size = 60,
            font_name = "Press Start 2P"
        )
        self.titreL = arcade.Text(
            "LogicBox",
            x = 120,
            y = 640,
            color = arcade.color.BLOND,
            font_size = 60,
            font_name = "Press Start 2P"
        )
        self.shadow_titreL = arcade.Text(
            "LogicBox",
            x = 120,
            y = 634,
            color = arcade.color.DEEP_SAFFRON,
            font_size = 60,
            font_name = "Press Start 2P"
        )


    def reset(self):
        pass

    def on_draw(self):

        self.clear()
        self.button_play.draw()
        self.button_quit.draw()
        self.shadow_titre1.draw()
        self.titre1.draw()
        self.shadow_titreL.draw()
        self.titreL.draw()



    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        if key == 97: #"a"
            arcade.exit()


    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x,y)
        if self.button_play.rect.point_in_rect((x, y)):
            self.button_play.scale = 1.1
        else:
            self.button_play.scale = 1.0
        if self.button_quit.rect.point_in_rect((x, y)):
            self.button_quit.scale = 1.1
        else:
            self.button_quit.scale = 1.0

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.button_play.touched:
            data.window.hide()
            if key_modifiers == 16 or key_modifiers == 0:
                data.window.display(EditorView())
            elif key_modifiers == 17 or key_modifiers == 1:
                data.window.display(DebugTilesView())
            elif key_modifiers == 2 or key_modifiers == 18:
                data.window.display(MainMenuView())

            else:
                print(f"Modificator not found, defaulting to EditorView. ({key_modifiers})")
                data.window.display(EditorView())
        if self.button_quit.touched:
            arcade.exit()

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


