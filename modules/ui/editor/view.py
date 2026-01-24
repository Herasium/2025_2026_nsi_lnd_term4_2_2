import arcade
from line_profiler import profile
from PIL import Image

from modules.ui.mouse import mouse
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.grid import Grid
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.id_generator import random_id

from modules.data.nodes.path import Path

from modules.data.nodes.nand import Nand
from modules.data.nodes.gand import And
from modules.data.nodes.gor import Or
from modules.data.nodes.gnot import Not
from modules.data.nodes.xor import Xor
from modules.data.nodes.nor import Nor

from modules.data.nodes.input import Input
from modules.data.nodes.output import Output
from modules.data.chip import Chip

from modules.data import data

from modules.engine.logic import propagate_values


class EditorView(arcade.View):

    def __init__(self):
        super().__init__()

        self.follower = Entity()
        self.follower.height = data.UI_EDITOR_GRID_SIZE
        self.follower.width = data.UI_EDITOR_GRID_SIZE

        self.selected_follower = None
        self.moving_gate = None
        self.current_path = None

        self.selected_cursor = 0
        self.cursors = [
            Nand,And,Or,Not,Xor,Nor,Input,Output
        ]
        self.cursors_names = [
            "Nand",'And',"Or","Not","Xor","Nor","Input","Output"
        ]

        self.chip = Chip("fihzfp")

        self.moving_gate_offset = (0, 0)

        self._real_camera_position = (0,0)
        self.camera_position = (0,0)

        self.numpad_key_list = [65456,65457,65458,65459,65460,65461,65462,65463,65464,65465]
        self.add_side_bar()
        self.background_color = arcade.types.Color.from_hex_string("121212")

        self.camera_hold = False
        self.fps = 0

        self.bake_textures()


    def bake_textures(self):

        start_x = 0
        y_len = int(1088/64)
        start_y = 1088

        new = Image.new("RGBA",(1920,1088))

        for i in range(y_len):
            for a in range(int(1920/64)):
                new.paste(data.ui_border_tiles[9].image, (start_x + (a)*64,start_y- (i+1)*64))
        
        self.background_grid_texture = arcade.Texture(new)


    def draw_tile(self,id,x,y):
            
            rect = arcade.XYWH(
                x=x,
                y=y,
                width=64,
                height=64,
                anchor=arcade.Vec2(0,0)
            )

            arcade.draw_texture_rect(data.ui_border_tiles[id],rect)


    def add_side_bar(self):
        self.side_texts = []

        for i in self.cursors_names:
            new = Text()
            new.name = f"{len(self.side_texts)}: {str(i)}"
            new.x = 1700
            new.y = 1080-50*(len(self.side_texts)+1)
            new.align = ("left","center")
            self.side_texts.append(new)

    def render_side_bar(self):

        for i in range(len(self.side_texts)):
            text = self.side_texts[i]
            if i == self.selected_cursor:
                text.color = arcade.color.RED
            else:
                text.color = arcade.color.WHITE

            text.draw()

    def reset(self):
        pass

    def draw_frame_border(self):
        start_x = 0
        start_y = 1080-64

        self.draw_tile(0,start_x,start_y)
        for i in range(28):
            self.draw_tile(1,start_x + (i+1)*64,start_y)
        self.draw_tile(3,start_x+29*64,start_y)

        y_len = 13

        for i in range(y_len-1):
            self.draw_tile(4,start_x,start_y - (i+1)*64)
            self.draw_tile(7,start_x+29*64,start_y - (i+1)*64)


        self.draw_tile(12,start_x,start_y - y_len*64)
        self.draw_tile(13,start_x + 64,start_y- y_len*64)
        self.draw_tile(5,start_x + 2*64,start_y- y_len*64)
        self.draw_tile(6,start_x + 3*64,start_y- y_len*64)
        self.draw_tile(10,start_x + 4*64,start_y- y_len*64)
        for i in range(24):
            self.draw_tile(13,start_x + (i+5)*64,start_y- y_len*64)
        self.draw_tile(15,start_x+29*64,start_y- y_len*64)

    def draw_frame_background(self):

        rect = arcade.XYWH(
                x=0,
                y=0,
                width=1920,
                height=1088,
                anchor=arcade.Vec2(0,0)
            )

        arcade.draw_texture_rect(self.background_grid_texture,rect)


    def draw_debug_text(self):

        debug_list = [
            f"Camera: {self.camera_position}",
            f"FPS: {self.fps}",
        ]

        start_y = 1080-70
        
        for index, item in enumerate(debug_list):
            arcade.draw_text(
                item, 
                64,  
                start_y - (index * 25), 
                arcade.color.WHITE,  
                14,
                font_name="Press Start 2P",
            )

    @profile
    def on_draw(self):
        self.clear()


        self.draw_frame_background()
        for p in self.chip.paths.values():
            p.draw()

        for g in self.chip.gates.values():
            g.draw()

        if self.current_path:
            self.current_path.draw()

        if self.selected_follower:
            self.selected_follower.draw()

        self.render_side_bar()
        self.draw_frame_border()
        self.draw_debug_text()

    def on_update(self, delta_time):
        self.fps = 1/delta_time*100//100
        self.simulate()

    def on_key_press(self, key, key_modifiers):

        if key in self.numpad_key_list:
            self.selected_cursor = self.numpad_key_list.index(key)

        if key == 101: #e
            for g in self.chip.gates.values():
                if g.entity.touched and g.type == "Input":
                    g.switch()

        if key == 97:  # "a"
            arcade.exit()
        if key == 65307:  # ESC
            if self.current_path:
                self.current_path.abort()
            self.current_path = None
            self.selected_follower = None

        if key == 115: # s
            self.chip.save()

        if key == 65288:
            self.delete()

    def delete_gate(self,id):
        to_delete = []
        for index in self.chip.paths.keys():
            p = self.chip.paths[index]

            for input in p.inputs:
                if input[1] == id:
                    p.remove_branch(input[4])
                    if p.empty:
                        to_delete.append(index)
                        continue
                    p.clean_out_single_branch()

            for output in p.outputs:
                if output[1] == id:
                    p.remove_branch(output[4])
                    if p.empty:
                        to_delete.append(index)
                        continue
                    p.clean_out_single_branch()

        del self.chip.gates[id]
        for i in to_delete:
            del self.chip.paths[i]

    def delete(self):

        for g in self.chip.gates.values():
            if g.entity.touched:
                self.delete_gate(g.id)
                break

        for p in self.chip.paths.values():
            if p.touched:
                p.remove_branch(p.get_touched_branch)
                if p.empty:
                    del self.chip.paths[p.id]
                    break
                p.clean_out_single_branch()
                break


    def on_key_release(self, key, key_modifiers):
        pass


    @property
    def camera(self):
        return self.camera_position

    @camera.setter
    
    def camera(self,value):
        self._real_camera_position = value
        self.camera_position = ((self._real_camera_position[0] // data.UI_EDITOR_GRID_SIZE) * data.UI_EDITOR_GRID_SIZE,(self._real_camera_position[1] // data.UI_EDITOR_GRID_SIZE) * data.UI_EDITOR_GRID_SIZE)
        for g in self.chip.gates:
            self.chip.gates[g].camera_moving(self.camera_position)
        for p in self.chip.paths:
            self.chip.paths[p].camera = self.camera_position
        if self.current_path:
            self.current_path.camera = self.camera_position

    
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x, y)
        
        self.follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2
        self.follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2

        if self.camera_hold:
            self.camera = (self._real_camera_position[0] + delta_x, self._real_camera_position[1] + delta_y)
            #self.camera = (self.camera_position[0] + delta_x, self.camera_position[1] + delta_y)


        if self.selected_follower:
            self.selected_follower._camera = (0,0)
            self.selected_follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2 
            self.selected_follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2 

        if self.moving_gate:
            self.moving_gate.x = mouse.cursor[0] - self.moving_gate_offset[0] 
            self.moving_gate.y = mouse.cursor[1] - self.moving_gate_offset[1] 

            # update connected paths
            for path in self.chip.paths.values():
                connected_inputs, connected_outputs = path.get_connected_points(self.moving_gate.id)
                modified = False

                for i in connected_inputs:
                    modified = True
                    position = self.moving_gate.outputs_position[i[2]]
                    position = (position[0]- self.camera_position[0] ,position[1] - self.camera_position[1] )
                    if i[3] == 1:
                        path.branch_points[i[4]][0] = position
                    elif i[3] == 2:
                        path.branch_points[i[4]][-1] = position

                for i in connected_outputs:
                    modified = True
                    position = self.moving_gate.inputs_position[i[2]]
                    position = (position[0] - self.camera_position[0] ,position[1] - self.camera_position[1] )
                    if i[3] == 1:
                        path.branch_points[i[4]][0] = position
                    elif i[3] == 2:
                        path.branch_points[i[4]][-1] = position

                if modified:
                    path.recalculate_hitbox()

    def simulate(self):
        propagate_values(self.chip)

    def on_mouse_press(self, x, y, button, key_modifiers):

        if button == 2:
            self.camera_hold = True
            return
        if self.camera_hold:
            return

        # Clicked a gate?
        for g in self.chip.gates.values():
            touched = g.touched
            if touched:
                if self.current_path is None:
                    # start new path
                    pid = random_id()
                    self.current_path = Path(pid)
                    self.current_path.camera = self.camera
                    self.current_path.add_path()

                    if touched[0] == 1: #Input touched
                        self.current_path.outputs.append([1, g.id, touched[1], 1, self.current_path.current_branch_count])
                    else: #Output touched
                        self.current_path.inputs.append([2, g.id, touched[1], 1, self.current_path.current_branch_count])
                    return

                else:
                    # finish existing path
                    if touched[0] == 1:#Input touched
                        self.current_path.outputs.append([1, g.id, touched[1], 2, self.current_path.current_branch_count])
                    else:#Output touched
                        self.current_path.inputs.append([2, g.id, touched[1], 2, self.current_path.current_branch_count])
                    self.current_path.camera = self.camera
                    self.current_path.finish()
                    if self.current_path.id not in self.chip.paths:
                        self.chip.paths[self.current_path.id] = self.current_path

                    self.current_path = None
                    return

        # Clicking on a path
        if not self.current_path:
            for p in self.chip.paths.values():
                if p.touched:
                    p.add_path()
                    self.current_path = p
                    return
        else:
            for p in self.chip.paths.values():
                if p.touched and p != self.current_path:
                    self.current_path.add_path()
                    p.merge(self.current_path)

                    if self.current_path.id in self.chip.paths:
                        del self.chip.paths[self.current_path.id]

                    self.current_path = None
                    return

            self.current_path.add_path()
            return

        # Move a gate
        if self.moving_gate is None:
            for g in self.chip.gates.values():
                if g.entity.touched:
                    self.moving_gate_offset = (
                        mouse.cursor[0] - g.x,
                        mouse.cursor[1] - g.y
                    )
                    self.moving_gate = g
                    return

        # Place new gate
        if self.selected_follower is None:
            self.selected_follower =  self.cursors[self.selected_cursor](random_id())
            self.selected_follower.camera = self.camera
            self.selected_follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[0]
            self.selected_follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[1]

        else:
            self.chip.gates[self.selected_follower.id] = self.selected_follower
            self.selected_follower.camera = self.camera
            self.selected_follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[0]
            self.selected_follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[1]
            self.selected_follower = None


    def on_mouse_release(self, x, y, button, key_modifiers):
        
        if button == 2:
            self.camera_hold = False

            for g in self.chip.gates:
                self.chip.gates[g].camera = self.camera_position

        self.moving_gate = None
        self.moving_gate_offset = (0, 0)
