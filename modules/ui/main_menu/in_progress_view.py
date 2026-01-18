import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.editor.view import EditorView
from modules.ui.debug_display_all_tiles.view import DebugTilesView

from modules.data.nodes.path import Path

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
        self.name_banner_sprite = arcade.Sprite("assets/name_banner.png")

        self.ui_sheet = arcade.SpriteSheet("assets/ui_grid.png")

        self.ui_tiles = self.ui_sheet.get_texture_grid(
            size = (32, 32),
            columns = 23,
            count = 9*23,
        )

        self.play_button = Button(self.ui_tiles)
        self.play_button.x = 1920 / 2 - 768 / 2 + 35
        self.play_button.y = 260 + 320 + 100 + 768 / 6 - 25
        self.play_button.width = 768 - 85
        self.play_button.height = 768 / 3 - 50
        self.play_button.scale = 1
 
        self.paths = []
        self.add_paths()

    def add_paths(self):

        branches = [
            {0: [(945, 702), (594, 702), (594, 837), (270, 837), (270, 891)], 1: []},
            {0: [(945, 702), (945, 648), (540, 648), (540, 540), (243, 540), (243, 648), (81, 648)], 1: []},
            {0: [(945, 702), (945, 459), (675, 459), (675, 351), (189, 351), (189, 270), (81, 270)], 1: []},
            {0: [(945, 702), (945, 351), (729, 351), (729, 216), (297, 216), (297, 81)], 1: []},
            {0: [(945, 702), (972, 675), (972, 648), (1161, 648), (1161, 351), (1026, 351), (1026, 189), (918, 189), (918, 81)], 1: []},
            {0: [(945, 702), (1188, 702), (1188, 297), (1350, 297), (1350, 135), (1512, 135), (1512, 81)], 1: []},
            {0: [(945, 702), (1269, 702), (1269, 351), (1674, 351), (1674, 297), (1836, 297)], 1: []},
            {0: [(945, 702), (1377, 702), (1377, 729), (1836, 729)], 1: []},
            {0: [(945, 702), (1026, 729), (1296, 729), (1296, 891)], 1: []}
        ]

        for branch in branches:

            self.paths.append(Path(""))
            self.paths[len(self.paths)-1].do_points = False
            self.paths[len(self.paths)-1].branch_points = branch

    def draw_paths(self):

        for i in self.paths:
            i.draw()

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
        self.clear(arcade.color.BLACK)
        
        start_x = 32
        start_y = 865

        self.draw_tile(0,start_x,start_y)
        for i in range(27):
            self.draw_tile(1,start_x + (i+1)*64,start_y)
        self.draw_tile(3,start_x+28*64,start_y)

        y_len = 13

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
        self.draw_paths()
        rect = arcade.XYWH(
                x = 1920 / 2,
                y = 260 + 320 + 100,
                width = 768,
                height = 768,
                anchor = arcade.Vec2(0.5,0.5)
        )

        arcade.draw_sprite_rect(self.play_button_sprite,rect)

        rect = arcade.XYWH(
                x=0,
                y=1080-128,
                width=1920,
                height=128,
                anchor=arcade.Vec2(0,0)
        )

        arcade.draw_sprite_rect(self.name_banner_sprite,rect)
        

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x,y)
        if self.play_button.rect.point_in_rect((x, y)):
            print (f"soiris")
        else:
            pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        print(x,y)
        if self.play_button.touched:
            data.window.hide()
            print (f"Bouton préssé")
            if key_modifiers == 16 or key_modifiers == 0:
                data.window.display(EditorView())
            elif key_modifiers == 17 or key_modifiers == 1:
                data.window.display(DebugTilesView())
            elif key_modifiers == 2 or key_modifiers == 18:
                data.window.display(MainMenuView())

            else:
                print(f"Modificator not found, defaulting to EditorView. ({key_modifiers})")
                data.window.display(EditorView())