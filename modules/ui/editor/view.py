import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.grid import Grid

from modules.ui.toolbox.nodes.path import Path
from modules.ui.toolbox.nodes.gate import Gate

class EditorView(arcade.View):

    def __init__(self):
        super().__init__()
        self.follower = Entity()
        self.follower.height = 20
        self.follower.width = 20

        self.path = Path("0000")
        self.gate = Gate("0001")


    def reset(self):
        pass

    def on_draw(self):
        self.clear()
        self.path.draw()
        self.gate.draw()
        self.follower.draw()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        if key == 97:
            arcade.exit()

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.x = x
        mouse.y = y

        self.follower.x = round(mouse.x / 20) * 20
        self.follower.y = round(mouse.y / 20) * 20


    def on_mouse_press(self, x, y, button, key_modifiers):
        self.path.click()
    def on_mouse_release(self, x, y, button, key_modifiers):
        pass

