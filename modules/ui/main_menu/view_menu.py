import arcade
from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.editor.view import EditorView
from modules.data import data
from pyglet.graphics import Batch

class GameView(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.JET

        self.button_play = Button()
        self.button_play.x = 120
        self.button_play.y = 540
        self.button_play.width = 340
        self.button_play.height = 90
        self.button_play.color = arcade.color.WHITE
        self.button_play.name = "Jouer"
        self.button_play.text.x = 280
        self.button_play.text.y = 495

        self.button_quit = Button()
        self.button_quit.x = 120
        self.button_quit.y = 400
        self.button_quit.width = 340
        self.button_quit.height = 90
        self.button_quit.color = arcade.color.WHITE
        self.button_quit.name = "Quitter"
        self.button_quit.text.x = 280
        self.button_quit.text.y = 355

        self.titre = arcade.Text(
            "Hello",
            x = 120,
            y = 700,
            font_size = 50,
            font_name = "Press Start 2P"
        )

        self.ui_sheet = arcade.SpriteSheet("assets/ui_grid.png")

        self.ui_tiles = self.ui_sheet.get_texture_grid(
            size=(32, 32),
            columns=28,
            count=7*28,
        )


    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.button_play.draw()
        self.button_quit.draw()
        self.titre.draw()

        arcade.draw_texture_rect(self.ui_tiles[38],arcade.XYWH(
                        x=0,
                        y=0,
                        width=64,
                        height=64,
                        anchor=arcade.Vec2(0,0)
                    ))



    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == 97: #"a"
            arcade.exit()
        if key == 65307: #echap
            self.current_path = None
            self.selected_follower = None

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        mouse.position = (x,y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if self.button_play.touched:
            data.window.hide()
            data.window.display(EditorView())

        if self.button_quit.touched:
            arcade.exit()

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


