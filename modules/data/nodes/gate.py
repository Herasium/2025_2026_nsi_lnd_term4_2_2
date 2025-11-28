import arcade
import math

from modules.data.node import Node
from modules.ui.toolbox.hitbox import HitBox
from modules.ui.mouse import mouse
from modules.data import data

class Gate(Node):

    def __init__(self, id):
        super().__init__(id)

        self.grid_size = data.UI_EDITOR_GRID_SIZE

        self._x = 0 + self.grid_size/2
        self._y = 0 + self.grid_size/2

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

    def calculate_display(self):
        self.text.x = self.x + self.width /2
        self.text.y = self.y + self.height /2

        self.entity.x = self.x
        self.entity.y = self.y
        self.entity.width = self.width
        self.entity.height = self.height

        self.inputs_position = []
        self.outputs_position = []

        self.inputs_hitboxes = []
        self.outputs_hibtoxes = []

        for i in range(len(self.inputs)):

            y = self.y + self.height - ((i * 2 + 1) * self.grid_size)
            x = self.x - self.grid_size

            self.inputs_position.append((x, y))
            self.inputs_hitboxes.append(
                HitBox(x=x, y=y, width=self.grid_size, height=self.grid_size)
            )

        for i in range(len(self.outputs)):

            y = self.y + self.height - ((i * 2 + 1) * self.grid_size)
            x = self.x + self.width

            self.outputs_position.append((x, y))
            self.outputs_hibtoxes.append(
                HitBox(x=x, y=y, width=self.grid_size, height=self.grid_size)
            )


    def draw(self):
        self.entity.draw()
        self.text.draw()

        for a in range(len(self.inputs_position)):
            i = self.inputs_position[a]
            arcade.draw_rect_filled(arcade.XYWH(i[0],i[1],self.grid_size,self.grid_size,anchor=arcade.Vec2(0,0)),color=arcade.color.AMARANTH_PINK)
            self.inputs_hitboxes[a].draw()

        for a in range(len(self.outputs_position)):
            i = self.outputs_position[a]
            arcade.draw_rect_filled(arcade.XYWH(i[0],i[1],self.grid_size,self.grid_size,anchor=arcade.Vec2(0,0)),color=arcade.color.CANDY_APPLE_RED)
            self.outputs_hibtoxes[a].draw()


    @property
    def touched(self):

        touched = False

        for a in range(len(self.inputs_hitboxes)):
            i = self.inputs_hitboxes[a]
            if i.touched:
                touched = (1,a)


        for a in range(len(self.outputs_hibtoxes)):
            i = self.outputs_hibtoxes[a]
            if i.touched:
                touched = (2,a)

        return touched