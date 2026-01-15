import arcade
from modules.ui.toolbox.entity import Entity
from modules.data import data

class DebugTilesView(arcade.View):

    def __init__(self):
        super().__init__()

        self.grid_size = data.UI_EDITOR_GRID_SIZE

        self.follower = Entity()
        self.follower.height = self.grid_size
        self.follower.width = self.grid_size

        self.tilesets = [
            {
                "name": "Gate Grid",
                "path": "assets/gate_grid.png",
                "tile_w": 27,
                "tile_h": 27,
                "columns": 6,
                "count": 6 * 6, 
                "textures": []  
            },
            {
                "name": "UI Grid",
                "path": "assets/ui_grid.png",
                "tile_w": 32,
                "tile_h": 32,
                "columns": 23,
                "count": 9 * 23,
                "textures": []
            },
            {
                "name": "UI Border Grid",
                "path": "assets/ui_border_grid.png",
                "tile_w": 64,
                "tile_h": 64,
                "columns": 4,
                "count": 4 * 4,
                "textures": []
            }
        ]

        self.load_tilesets()

        self.current_index = 0
        self.hovered_index = None

        self.display_start_x = 500
        self.display_start_y = 500

    def load_tilesets(self):
        for ts in self.tilesets:
            try:
                sheet = arcade.SpriteSheet(ts["path"])
                ts["textures"] = sheet.get_texture_grid(
                    size=(ts["tile_w"], ts["tile_h"]),
                    columns=ts["columns"],
                    count=ts["count"]
                )
            except Exception as e:
                print(f"Error loading tileset {ts['name']}: {e}")
                ts["textures"] = []

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.hovered_index = None
        
        current_set = self.tilesets[self.current_index]
        cols = current_set["columns"]
        total_count = current_set["count"]

        grid_x = (x - self.display_start_x) // self.grid_size
        grid_y = (y - self.display_start_y) // self.grid_size

        import math
        rows = math.ceil(total_count / cols)

        if 0 <= grid_x < cols and 0 <= grid_y < rows:
            index = int(grid_y * cols + grid_x)
            if 0 <= index < total_count:
                self.hovered_index = f"{current_set['name']} Index: {index}"

    def on_draw(self):
        self.clear()

        current_set = self.tilesets[self.current_index]
        textures = current_set["textures"]
        cols = current_set["columns"]

        arcade.draw_text(
            f"Current Set: {current_set['name']} (Arrow Keys to Switch)",
            self.display_start_x,
            self.display_start_y + (len(textures) // cols * self.grid_size) + 50,
            arcade.color.WHITE,
            14
        )

        for i, texture in enumerate(textures):
            column_x = i % cols
            row_y = i // cols

            tile_x = column_x * self.grid_size + self.display_start_x
            tile_y = row_y * self.grid_size + self.display_start_y

            rect = arcade.XYWH(
                x=tile_x,
                y=tile_y,
                width=self.grid_size,
                height=self.grid_size,
                anchor=arcade.Vec2(0, 0)
            )

            arcade.draw_texture_rect(texture, rect)

        if self.hovered_index is not None:
            arcade.draw_text(
                f"Hovered: {self.hovered_index}",
                10,
                10,
                arcade.color.CYAN,
                16
            )

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            self.current_path = None
            self.selected_follower = None

        elif key == arcade.key.A:
            arcade.exit()

        elif key == arcade.key.RIGHT:
            self.current_index = (self.current_index + 1) % len(self.tilesets)
            print(f"Switched to: {self.tilesets[self.current_index]['name']}")

        elif key == arcade.key.LEFT:
            self.current_index = (self.current_index - 1) % len(self.tilesets)
            print(f"Switched to: {self.tilesets[self.current_index]['name']}")

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass