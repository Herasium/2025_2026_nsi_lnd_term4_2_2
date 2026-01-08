import arcade
from line_profiler import profile

from modules.ui.mouse import mouse
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.grid import Grid
from modules.ui.toolbox.id_generator import random_id

from modules.data.nodes.path import Path
from modules.data.nodes.gate import Gate
from modules.data.nodes.input import Input

from modules.data import data

from modules.engine.logic import propagate_values


class DebugTilesView(arcade.View):

    def __init__(self):
        super().__init__()

        self.grid_size = data.UI_EDITOR_GRID_SIZE

        self.follower = Entity()
        self.follower.height = self.grid_size
        self.follower.width = self.grid_size
        
        TILE_W = 27
        TILE_H = 27
        ROWS = 6
        COLS = 6
        COUNT = ROWS * COLS 

        self.gate_sheet = arcade.SpriteSheet("assets/gate_grid.png")

        self.tiles = self.gate_sheet.get_texture_grid(
            size=(TILE_W, TILE_H),
            columns=COLS,
            count=COUNT
        )

        self.ui_sheet = arcade.SpriteSheet("assets/ui_grid.png")

        
        self.ui_tiles = self.ui_sheet.get_texture_grid(
            size = (32, 32),
            columns = 23,
            count = 9*23,
        )

        self.hovered_index = None
  
    def on_mouse_motion(self, x, y, delta_x, delta_y):
            self.hovered_index = None  # Reset every frame

            ui_grid_x = (x - 500) // self.grid_size
            ui_grid_y = (y - 500) // self.grid_size

            if 0 <= ui_grid_x < 23 and 0 <= ui_grid_y < 9:
                self.hovered_index = f"UI Tile: {int(ui_grid_y * 23 + ui_grid_x)}"
                return
            
            gate_grid_x = (x - 500) // self.grid_size
            gate_grid_y = (y - 900) // self.grid_size

            if 0 <= gate_grid_x < 6 and 0 <= gate_grid_y < 6:
                self.hovered_index = f"Gate Tile: {int(gate_grid_y * 6 + gate_grid_x)}"
                return
            
    def reset(self):
        pass

    def on_draw(self):
    
        self.clear()

        current = 0
        for y in range(9):
            for x in range(23):

                tile_x = x * self.grid_size + 500
                tile_y = y * self.grid_size + 500

                rect = arcade.XYWH(
                    x=tile_x,
                    y=tile_y,
                    width=self.grid_size,
                    height=self.grid_size,
                    anchor=arcade.Vec2(0,0)
                )


                arcade.draw_texture_rect(self.ui_tiles[current],rect)
                current += 1

        current = 0
        for y in range(6):
            for x in range(6):

                tile_x = x * self.grid_size + 500
                tile_y = y * self.grid_size + 900

                rect = arcade.XYWH(
                    x=tile_x,
                    y=tile_y,
                    width=self.grid_size,
                    height=self.grid_size,
                    anchor=arcade.Vec2(0,0)
                )


                arcade.draw_texture_rect(self.tiles[current],rect)
                current += 1
            
        if self.hovered_index is not None:
                    arcade.draw_text(
                        f"Hovered Index: {self.hovered_index}",
                        10,
                        10,
                        arcade.color.WHITE,
                        16
                    )


    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        if key == 97:  # "a"
            arcade.exit()
        if key == 65307:  # ESC
            self.current_path = None
            self.selected_follower = None


    def on_key_release(self, key, key_modifiers):
        pass


    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass