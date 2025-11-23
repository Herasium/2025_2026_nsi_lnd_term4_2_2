import arcade
import math

from modules.ui.toolbox.node import Node
from modules.ui.toolbox.hitbox import HitBox
from modules.ui.mouse import mouse
from modules.data import data

class Gate(Node):

    def __init__(self, id):
        super().__init__(id)

        self.grid_size = data.UI_EDITOR_GRID_SIZE

        self.x = 100
        self.y = 200

        self.inputs = [0,1]
        self.outputs = [0]

        self.name = "AND"

        self.text = arcade.Text(
            self.name,
            self.x,
            self.y,
            arcade.color.BLACK,
            24, 
            anchor_x="center",
            anchor_y="center",
        )

        self.width = math.ceil(self.text.content_width / self.grid_size) * self.grid_size
        self.height = max((len(self.inputs)*2+1)*self.grid_size,(len(self.outputs)*2+1)*self.grid_size)

        self.text.x = self.x + self.width /2
        self.text.y = self.y + self.height /2

        self.entity.x = self.x
        self.entity.y = self.y
        self.entity.width = self.width
        self.entity.height = self.height

        self.inputs_position = []

        for i in range(len(self.inputs)):
            self.inputs_position.append((self.x-self.grid_size,self.y + self.height - ((i*2+1)*self.grid_size)))

        self.outputs_position = []

        for i in range(len(self.outputs)):
            self.outputs_position.append((self.x+self.width,self.y + self.height - ((i*2+1)*self.grid_size)))

    def draw(self):
        self.entity.draw()
        self.text.draw()

        for i in self.inputs_position:
            arcade.draw_rect_filled(arcade.XYWH(i[0],i[1],self.grid_size,self.grid_size,anchor=arcade.Vec2(0,0)),color=arcade.color.AMARANTH_PINK)

        for i in self.outputs_position:
            arcade.draw_rect_filled(arcade.XYWH(i[0],i[1],self.grid_size,self.grid_size,anchor=arcade.Vec2(0,0)),color=arcade.color.CANDY_APPLE_RED)

