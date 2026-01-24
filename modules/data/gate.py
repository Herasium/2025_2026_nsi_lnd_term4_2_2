import arcade
import math

from modules.data.node import Node
from modules.ui.toolbox.hitbox import HitBox
from modules.ui.toolbox.entity import Entity
from modules.ui.mouse import mouse
from modules.data import data

from line_profiler import profile

class Gate(Node):

    def __init__(self, id):
        super().__init__(id)

        self._x = 0 + data.UI_EDITOR_GRID_SIZE/2
        self._y = 0 + data.UI_EDITOR_GRID_SIZE/2

        self.inputs = []
        self.outputs = []

        self._name = "Default Gate"
        self.type = "Gate"
        self.gate_type = "Default"

        self.bg = Entity()
        self.bg.color = arcade.types.Color.from_hex_string("0F3FA8")
        self.entity.color = arcade.types.Color.from_hex_string("2563EB")

        self._camera = (0,0)

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

        self.tiles = data.gate_tiles
        self.draw_hitboxes = True
        self.exceptional_size_offset = 0

        self.calculate_display()
        self.gen_tile_pattern()
        

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

    
    def calculate_display_lite(self):
        self.text.x = self.x + self.width/2 + self._camera[0]
        self.text.y = self.y + self.height /1.6 + data.UI_EDITOR_GRID_SIZE/4 + self._camera[1]

        self.bg_text.x = self.text.x - 1
        self.bg_text.y = self.text.y + 2

        self.entity._x = self.x + self._camera[0]
        self.entity._y = self.y + self._camera[1]
        self.entity._width = self.width
        self.entity._height = self.height

        self.bg._x = self.x-5
        self.bg._y = self.y-5
        self.bg._width = self.width+10
        self.bg._height = self.height+10
    
    def calculate_display(self):
        self.both = len(self.inputs) > 0 and len(self.outputs) > 0

        self.tile_width = 2 + len(self.inputs) + len(self.outputs) + self.exceptional_size_offset
        self.tile_width += self.both*1

        self.width = self.tile_width * data.UI_EDITOR_GRID_SIZE
        self.height = 4*data.UI_EDITOR_GRID_SIZE
        self.max = max(len(self.inputs),len(self.outputs)) +1 

        self.text.x = self.x + self.width/2 + self._camera[0]
        self.text.y = self.y + self.height /1.6 + data.UI_EDITOR_GRID_SIZE/4 + self._camera[1]

        self.bg_text.x = self.text.x - 1
        self.bg_text.y = self.text.y + 2

        self.entity.x = self.x + self._camera[0]
        self.entity.y = self.y + self._camera[1]
        self.entity.width = self.width
        self.entity.height = self.height

        self.bg.x = self.x-5
        self.bg.y = self.y-5
        self.bg.width = self.width+10
        self.bg.height = self.height+10

        self.inputs_position = []
        self.outputs_position = []

        self.inputs_hitboxes = []
        self.outputs_hitboxes = []

        for i in range(len(self.inputs)):

            y = self.y + self._camera[1]
            x = self.x + data.UI_EDITOR_GRID_SIZE * (i+1 + self.exceptional_size_offset//2) + self._camera[0]

            self.inputs_position.append((x + data.UI_EDITOR_GRID_SIZE/2, y + data.UI_EDITOR_GRID_SIZE/2))
            self.inputs_hitboxes.append(
                HitBox(x=x, y=y, width=data.UI_EDITOR_GRID_SIZE, height=data.UI_EDITOR_GRID_SIZE)
            )

        for i in range(len(self.outputs)):

            y = self.y + self._camera[1]
            x = self.x + data.UI_EDITOR_GRID_SIZE * (i+1+self.both*1+len(self.inputs)+ self.exceptional_size_offset//2) + self._camera[0]

            self.outputs_position.append((x + data.UI_EDITOR_GRID_SIZE/2, y + data.UI_EDITOR_GRID_SIZE/2))
            self.outputs_hitboxes.append(
                HitBox(x=x, y=y, width=data.UI_EDITOR_GRID_SIZE, height=data.UI_EDITOR_GRID_SIZE)
            )


    @property
    def camera(self):
        return self._camera

    @camera.setter
    
    def camera(self,value):
        self._camera = value
        self.calculate_display()
    
    def camera_moving(self,value):
        self._camera = value
        self.calculate_display_lite()


    def gen_tile_pattern(self):

        gate_tile_pattern = []

        #Bottom Row
        gate_tile_pattern.append(7)
        for _ in range(len(self.inputs)):
            gate_tile_pattern.append(6)
        if self.both:
            gate_tile_pattern.append(0)
        for _ in range(len(self.outputs)):
            gate_tile_pattern.append(6)
        gate_tile_pattern.append(8)

        #First Row
        gate_tile_pattern.append(26)
        for i in self.inputs:
            if i:
                gate_tile_pattern.append(15)
            else:
                gate_tile_pattern.append(21)
        if self.both:
            gate_tile_pattern.append(1)
        for i in self.outputs:
            if i:
                gate_tile_pattern.append(15)
            else:
                gate_tile_pattern.append(21)
        gate_tile_pattern.append(19)

        #Second Row
        gate_tile_pattern.append(31)
        for _ in range(self.tile_width-2):
            gate_tile_pattern.append(13)
        gate_tile_pattern.append(25)

        #Top Row
        gate_tile_pattern.append(28)
        for _ in range(self.tile_width-2):
            gate_tile_pattern.append(2)
        gate_tile_pattern.append(27)

        self.gate_tile_pattern = gate_tile_pattern

    @profile
    def draw_tiles(self):
    
        width = self.tile_width
        height = 4
        out = self.outputs.copy()
        inp = self.inputs.copy()

        out.reverse()
        inp.reverse()

        current = int(''.join(map(str, map(int, (out+inp)))), 2)

        tile_x = self.x + self._camera[0]
        tile_y = self.y + self._camera[1]

        rect = arcade.XYWH(
                    x=tile_x,
                    y=tile_y,
                    width=width * data.UI_EDITOR_GRID_SIZE,
                    height=height * data.UI_EDITOR_GRID_SIZE,
                    anchor=arcade.Vec2(0,0)
        )

        arcade.draw_texture_rect(data.IMAGE.get_texture(self.gate_type,current),rect)

    @profile
    def draw(self):

        self.draw_tiles()
        self.bg_text.draw()
        self.text.draw()

        if self.draw_hitboxes:
            for i in self.inputs_hitboxes:
                i.draw()
            for i in self.outputs_hitboxes:
                i.draw()
            self.entity.hitbox.draw()

    @property
    def touched(self):

        touched = False

        for a in range(len(self.inputs_hitboxes)):
            i = self.inputs_hitboxes[a]
            if i.touched:
                touched = (1,a)


        for a in range(len(self.outputs_hitboxes)):
            i = self.outputs_hitboxes[a]
            if i.touched:
                touched = (2,a)

        return touched


    def save(self):
        return {
            "x": self.x,
            "y": self.y,
            "type": self.type,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "gate": self.gate_type,
            "id": self.id
        }
    
    def load(self, data):

        self.type = data["type"]
        self.inputs = data.get("inputs",[])
        self.outputs = data.get("outputs",[])
        self.gate_type = data.get("gate","")
        self.id = data["id"]
        self.x = data["x"]
        self.y = data["y"]

    def __str__(self):
        result = f"Gate {self._name} (#{self.id}), {len(self.inputs)} Inputs ({self.inputs}), {len(self.outputs)} Outputs ({self.outputs})"
        return result