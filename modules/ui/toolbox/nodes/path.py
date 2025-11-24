import arcade

from modules.ui.toolbox.node import Node
from modules.ui.toolbox.hitbox import HitBox
from modules.ui.mouse import mouse
from modules.data import data

class Path(Node):

    def __init__(self, id):
        super().__init__(id)

        self.current_point = None
        self.paths = []
        self.hitboxs = []
        self.inputs = []
        self.outputs = []
        self.grid_size = data.UI_EDITOR_GRID_SIZE
        
    def click(self):

        if self.current_point == None:
            self.current_point = mouse.cursor
        else:

            horizontal_path = (self.current_point, (mouse.cursor[0], self.current_point[1]))
            vertical_path = ((mouse.cursor[0], self.current_point[1]), mouse.cursor)

            horizontal_hitbox = HitBox()
            horizontal_hitbox.x = min(self.current_point[0], mouse.cursor[0])
            horizontal_hitbox.y = self.current_point[1]
            horizontal_hitbox.width = abs(mouse.cursor[0] - self.current_point[0])
            horizontal_hitbox.height = 1 

            vertical_hitbox = HitBox()
            vertical_hitbox.x = mouse.cursor[0]
            vertical_hitbox.y = min(self.current_point[1], mouse.cursor[1])
            vertical_hitbox.width = 1  
            vertical_hitbox.height = abs(mouse.cursor[1] - self.current_point[1])


            self.paths.append(horizontal_path)
            self.paths.append(vertical_path)
            self.hitboxs.append(horizontal_hitbox)
            self.hitboxs.append(vertical_hitbox)
            self.current_point = mouse.cursor

    def finish(self):
        self.click()
        self.current_point = None

    def draw(self):
        
        for i in self.paths:
            arcade.draw_line(i[0][0], i[0][1], i[1][0], i[1][1], arcade.color.RED, 5)

        if self.current_point != None:
            arcade.draw_line(self.current_point[0], self.current_point[1], mouse.cursor[0], mouse.cursor[1], arcade.color.RED, 5)

        for a in self.hitboxs:
            a.draw()

    @property
    def touched(self):

        result = False

        for i in self.hitboxs:
            if i.touched:
                result = True

        return result