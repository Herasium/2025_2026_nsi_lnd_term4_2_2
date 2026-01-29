
import arcade
from modules.data import data

class Window():

    def __init__(self):
        
        self.width = data.WINDOW_WIDTH
        self.height = data.WINDOW_HEIGHT
        self.title = "LogicBox"

        self.window = arcade.Window(self.width, self.height, self.title,fullscreen=data.WINDOW_FULLSCREEN, update_rate = 0.00001, draw_rate = 0.00001)

    def run(self):
        arcade.run()

    def display(self,view: arcade.View):
        self.window.show_view(view)

    def hide(self):
        self.window.hide_view()