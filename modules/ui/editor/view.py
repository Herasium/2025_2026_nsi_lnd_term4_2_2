import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.grid import Grid

from modules.data.nodes.path import Path
from modules.data.nodes.gate import Gate

from modules.data import data

class EditorView(arcade.View):

    def __init__(self):
        super().__init__()

        self.grid_size = data.UI_EDITOR_GRID_SIZE

        self.follower = Entity()
        self.follower.height = self.grid_size
        self.follower.width = self.grid_size

        self.selected_follower = None

        self.gates = []

        self.paths = []

        self.current_path = None


    def reset(self):
        pass

    def on_draw(self):
        self.clear()

        for i in self.paths:
            i.draw()

        for i in self.gates:
            i.draw()

        if self.current_path != None:
            self.current_path.draw()

        if self.selected_follower != None:
            self.selected_follower.draw()

    

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        if key == 97: #"a"
            arcade.exit()
        if key == 65307: #echap
            self.current_path = None
            self.selected_follower = None
        
      

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
 
        mouse.position = (x,y)


        self.follower.x = mouse.cursor[0] - self.grid_size/2
        self.follower.y = mouse.cursor[1] - self.grid_size/2

        if self.selected_follower != None:
                self.selected_follower.x = mouse.cursor[0] - self.grid_size/2
                self.selected_follower.y = mouse.cursor[1] - self.grid_size/2

 
    def on_mouse_press(self, x, y, button, key_modifiers):
        
        done = False

        for i in self.gates:
            touched = i.touched
            if touched != False and done == False:
                if self.current_path == None:

                    self.current_path = Path("0002")
                    self.current_path.add_path()

                    if touched[0] == 1:
                        self.current_path.outputs.append((1,i.id,touched[1]))
                    if touched[0] == 2:
                        self.current_path.inputs.append((1,i.id,touched[1]))

                else:
                    self.current_path.finish()
                    if not self.current_path in self.paths:
                        self.paths.append(self.current_path)
                    self.current_path = None
                    done = True                


        if done == False:
            if not self.current_path:
                for i in self.paths:
                    if i.touched:
                        i.add_path()
                        self.current_path = i
                        done = True

            else:

                self.current_path.add_path()
                done = True

        if done == False:
            if self.selected_follower == None:
                self.selected_follower = Gate("001")
            else:
                self.gates.append(self.selected_follower)
                self.selected_follower = None
            done == True

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass

