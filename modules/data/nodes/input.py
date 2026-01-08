import arcade
import math

from modules.data.node import Node
from modules.ui.toolbox.hitbox import HitBox
from modules.ui.toolbox.entity import Entity
from modules.ui.mouse import mouse
from modules.data import data
from modules.engine.logic import calculate_output

from line_profiler import profile

class Input(Node):

    def __init__(self, id, tiles):
        super().__init__(id)

        self.grid_size = data.UI_EDITOR_GRID_SIZE

        self._x = 0 + self.grid_size/2
        self._y = 0 + self.grid_size/2

        self.outputs = [True]

        self._name = "INPUT"

        self.bg = Entity()
        self.bg.color = arcade.types.Color.from_hex_string("0F3FA8")
        self.entity.color = arcade.types.Color.from_hex_string("2563EB")

        self.input_off_color = arcade.types.Color.from_hex_string(data.COLORS.VALUE_OFF)
        self.input_on_color = arcade.types.Color.from_hex_string(data.COLORS.VALUE_ON)

        self.text = arcade.Text(
                    self._name,
                    self.x,
                    self.y,
                    arcade.types.Color.from_hex_string("b45252"),
                    24, 
                    anchor_x="center",
                    anchor_y="center",
                    font_name="Press Start 2P"
                )

        self.bg_text = arcade.Text(
                    self._name,
                    self.x,
                    self.y,
                    arcade.types.Color.from_hex_string("5f556a"),
                    24, 
                    anchor_x="center",
                    anchor_y="center",
                    font_name="Press Start 2P"
                )

        self.tiles = tiles

 
        self.calculate_display()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        if self._name == "NOT":
            self.inputs = [False]
        else:
            self.inputs = [False, False]

        if hasattr(self, "text"):
            self.text.text = self._name
            self.bg_text.text = self._name

        if hasattr(self, "grid_size"):
            self.calculate_display()

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self,value):
        self._x = value
        self.calculate_display()

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self,value):
        self._y = value
        self.calculate_display()    

    @profile
    def calculate_display(self):

        self.width = (math.ceil(self.text.content_width / self.grid_size)+2) * self.grid_size
        self.height = 4*self.grid_size
        self.max = len(self.outputs) +1 

        self.text.x = self.x + self.grid_size * 3 + 1 
        self.text.y = self.y + self.height /1.6 + self.grid_size/4

        self.bg_text.x = self.x + self.grid_size * 3 - 1
        self.bg_text.y = self.y + self.height /1.6 + self.grid_size/4 + 2


        self.entity.x = self.x
        self.entity.y = self.y
        self.entity.width = self.width
        self.entity.height = self.height

        self.bg.x = self.x-5
        self.bg.y = self.y-5
        self.bg.width = self.width+10
        self.bg.height = self.height+10

        self.outputs_position = []

        self.outputs_hitboxes = []

        for i in range(len(self.outputs)):

            y = self.y 
            x = self.x + self.grid_size * (i+2)

            self.outputs_position.append((x + self.grid_size/2, y + self.grid_size/2))
            self.outputs_hitboxes.append(
                HitBox(x=x, y=y, width=self.grid_size, height=self.grid_size)
            )

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
            

    @profile
    def draw(self):

        self.draw_tiles()
        self.bg_text.draw()
        self.text.draw()
        for i in self.outputs_hitboxes:
            i.draw()
        self.entity.hitbox.draw()

    def update(self):
        pass


    @property
    def touched(self):

        touched = False

        for a in range(len(self.outputs_hitboxes)):
            i = self.outputs_hitboxes[a]
            if i.touched:
                touched = (2,a)

        return touched
