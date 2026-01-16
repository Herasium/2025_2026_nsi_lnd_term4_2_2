import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.editor.view import EditorView
from modules.ui.debug_display_all_tiles.view import DebugTilesView

from modules.data import data

from pyglet.graphics import Batch

class MainMenuView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.JET

        self.ui_border_sheet = arcade.SpriteSheet("assets/ui_border_grid.png")

        self.ui_border_tiles = self.ui_border_sheet.get_texture_grid(
            size = (64, 64),
            columns = 4,
            count = 4*4,
        )

        self.play_button_sprite = arcade.Sprite("assets/play_button.png")

    def on_key_press(self, key, key_modifiers):
        if key == 97: #"a"
            arcade.exit()

    def draw_tile(self,id,x,y):
            
            rect = arcade.XYWH(
                x=x,
                y=y,
                width=64,
                height=64,
                anchor=arcade.Vec2(0,0)
            )

            arcade.draw_texture_rect(self.ui_border_tiles[id],rect)

    def on_draw(self):
        self.clear()
        
        start_x = 32
        start_y = 900

        self.draw_tile(0,start_x,start_y)
        for i in range(27):
            self.draw_tile(1,start_x + (i+1)*64,start_y)
        self.draw_tile(3,start_x+28*64,start_y)

        y_len = 11

        for i in range(y_len-1):
            self.draw_tile(4,start_x,start_y - (i+1)*64)
            for a in range(27):
                self.draw_tile(9,start_x + (a+1)*64,start_y- (i+1)*64)
            self.draw_tile(7,start_x+28*64,start_y - (i+1)*64)


        self.draw_tile(12,start_x,start_y - y_len*64)
        self.draw_tile(13,start_x + 64,start_y- y_len*64)
        self.draw_tile(5,start_x + 2*64,start_y- y_len*64)
        self.draw_tile(6,start_x + 3*64,start_y- y_len*64)
        self.draw_tile(10,start_x + 4*64,start_y- y_len*64)
        for i in range(23):
            self.draw_tile(13,start_x + (i+5)*64,start_y- y_len*64)
        self.draw_tile(15,start_x+28*64,start_y- y_len*64)

        rect = arcade.XYWH(
                x=1920/2,
                y=260+320+100,
                width=768,
                height=768,
                anchor=arcade.Vec2(0.5,0.5)
        )

        arcade.draw_sprite_rect(self.play_button_sprite,rect)