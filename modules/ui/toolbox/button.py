import arcade
from modules.ui.toolbox.hitbox import HitBox
from modules.data import data


class Button:

    def __init__(self, tiles):

        self._x = 0
        self._y = 0

        self._width = 0
        self._height = 0

        self._color = arcade.color.BLUE
        self.hitbox = HitBox()

        self._name = ""
        self._text = ""

        self.grid_size = data.UI_EDITOR_GRID_SIZE
        self.tiles = tiles


    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self._recalculate_rect()

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self._recalculate_rect()    

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        self._recalculate_rect()

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
        self._recalculate_rect()

    def _recalculate_rect(self):

        self.rect = arcade.XYWH(
            x=self._x,
            y=self._y,
            width=self._width,
            height=self._height,
            anchor=arcade.Vec2(0,0)
        )
        self._update_hitbox()
        self._text = arcade.Text(
            self._name,
            self._x,
            self._y,
            arcade.color.BLACK,
            18, 
            anchor_x = "center",
            anchor_y = "center",
            font_name = "Press Start 2P"
        )
        self.text.x = self.x + self.width /2
        self.text.y = self.y + self.height /2

    def draw_tiles(self):
    
        gate_tile_pattern = [7,6,6,0,6,8,26,10,10,1,10,19,31,13,13,13,13,25,28,2,2,2,2,27]
        width = 6
        height = 4

        current = 0
        for y in range(height):
            for x in range(width):

                tile_x = x * self.grid_size + self.x
                tile_y = y * self.grid_size + self.y

                rect = arcade.XYWH(
                    x=tile_x,
                    y=tile_y,
                    width=self.grid_size,
                    height=self.grid_size,
                    anchor=arcade.Vec2(0,0)
                )


                arcade.draw_texture_rect(self.tiles[gate_tile_pattern[current]],rect)
                current += 1

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        self._recalculate_rect()

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        self._recalculate_rect()

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        self._recalculate_rect
    
    def _update_hitbox(self):
        self.hitbox.x = self._x
        self.hitbox.y = self._y-self._height
        self.hitbox.width = self._width
        self.hitbox.height = self._height

    def draw(self):
        self.draw_tiles()
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self._x, self._y, self._width, self._height,anchor=arcade.Vec2(0,1)),
            self._color,
        )
        self.text.draw()

    @property
    def touched(self):
        return self.hitbox.touched