
import arcade
from modules.data import data



class  Grid():

    def __init__(self):
        
        self.size = data.UI_EDITOR_GRID_SIZE

    def draw(self):

        for y in range(0,720,self.size):
            for x in range(0,1280,self.size):
                arcade.draw_point(x, y, arcade.color.DARK_BLUE_GRAY, 5)
