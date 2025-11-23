
import arcade

class Window():

    def __init__(self):
        
        self.width = 1920
        self.height = 1080
        self.title = "Starting Template"

        self.window = arcade.Window(self.width, self.height, self.title,fullscreen=True)

    def run(self):
        arcade.run()

    def display(self,view: arcade.View):
        self.window.show_view(view)

    def hide(self):
        self.window.hide_view()