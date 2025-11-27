
from modules.ui.toolbox.entity import Entity

class Node():

    def __init__(self,id):
        
        self.entity = Entity()
        self.type = "DefaultNode"
        self.id = id
        self.name = f"{self.type} ({self.id})"


    def draw(self):

        self.entity.draw()
