import arcade
from line_profiler import profile
from PIL import Image
import time

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
from modules.data.gate_index import gate_types

from modules.engine.logic import propagate_values


class EditorView(arcade.View):

    def __init__(self):
        super().__init__()

        self.follower = Entity()
        self.follower.height = data.UI_EDITOR_GRID_SIZE
        self.follower.width = data.UI_EDITOR_GRID_SIZE

        self.bottom_zone_collider = Entity()
        self.bottom_zone_collider.x = 0
        self.bottom_zone_collider.y = 0
        self.bottom_zone_collider.width = 1920
        self.bottom_zone_collider.height = 3*64

        self.selected_follower = None
        self.moving_gate = None
        self.current_path = None

        self.chip = Chip("fihzfp")

        self.moving_gate_offset = (0, 0)

        self._real_camera_position = (0,0)
        self.camera_position = (0,0)

        self.bottom_gates = []
        self.bottom_gate_bar()

        self.background_color = arcade.types.Color.from_hex_string("121212")

        self.camera_hold = False
        self.fps = 0
        self.delta_time = 1
        self.frame_count = 0
        self.last_time = 1

        self.stress_test = False

        if self.stress_test:
            self.perf_graph_list = arcade.SpriteList()

            graph = arcade.PerfGraph(400, 400, graph_data="FPS")
            graph.position = 200, 200
            self.perf_graph_list.append(graph)

    def bottom_bar_width_sum(self):
        result = 0
        for i in self.bottom_gates:
            result += i.tile_width
        return result

    def bottom_gate_bar(self):

        for i in gate_types:
           
            position = (self.bottom_bar_width_sum()+len(self.bottom_gates))*data.UI_EDITOR_GRID_SIZE + 64 + data.UI_EDITOR_GRID_SIZE
            self.bottom_gates.append(gate_types[i](f"bottom_gate_{random_id()}"))
            self.bottom_gates[-1].camera = (0,0)
            self.bottom_gates[-1].y = (1*data.UI_EDITOR_GRID_SIZE)
            self.bottom_gates[-1].x = position
            

    def get_hovered_bottom_gate(self):
        for i in self.bottom_gates:
            if i.entity.touched :
                return i.gate_type

    def draw_bottom_gates(self):
        for i in self.bottom_gates:
            i.draw()

    def draw_tile(self,id,x,y):
            
            rect = arcade.XYWH(
                x=x,
                y=y,
                width=64,
                height=64,
                anchor=arcade.Vec2(0,0)
            )

            arcade.draw_texture_rect(data.ui_border_tiles[id],rect)


    def reset(self):
        pass

    def draw_frame_border(self):

        rect = arcade.XYWH(
                x=0,
                y=1080-(14*64),
                width=1920,
                height=14*64,
                anchor=arcade.Vec2(0,0)
            )

        arcade.draw_texture_rect(data.editor_border_texture,rect)

    def draw_frame_background(self):

        rect = arcade.XYWH(
                x=0,
                y=0,
                width=1920,
                height=1088,
                anchor=arcade.Vec2(0,0)
            )

        arcade.draw_texture_rect(data.background_grid_texture,rect)

    def draw_frame_border_small(self):

        rect = arcade.XYWH(
                x=0,
                y=0,
                width=1920,
                height=3*64,
                anchor=arcade.Vec2(0,0)
            )

        arcade.draw_texture_rect(data.editor_border_texture_small,rect)

    def draw_frame_background_small(self):

        rect = arcade.XYWH(
                x=0,
                y=0,
                width=1920,
                height=3*64,
                anchor=arcade.Vec2(0,0)
            )

        arcade.draw_texture_rect(data.background_grid_texture_small,rect)



    def draw_debug_text(self):

        debug_list = [
            f"Camera: {self.camera_position}",
            f"FPS: {self.fps} / {round(self.delta_time*100000)/100} ms / {self.frame_count}",
            f"Objects: {len(self.chip.gates.keys())}g/{len(self.chip.paths.keys())}p"
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

        self.draw_frame_background_small()
        self.draw_frame_border_small()
        self.draw_debug_text()
        self.draw_frame_border()
        self.draw_bottom_gates()

        if self.stress_test:
            self.perf_graph_list.draw()

        self.frame_count += 1
        self.delta_time = time.time() - self.last_time
        self.last_time = time.time()
        
    def on_update(self, delta_time):
        self.fps = 1/self.delta_time*10000//10000
        self.simulate()


    def on_key_press(self, key, key_modifiers):

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
            hovered = self.get_hovered_bottom_gate()
            if hovered in gate_types:
                self.selected_follower =  gate_types[hovered](random_id())
                self.selected_follower.camera = self.camera
                self.selected_follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[0]
                self.selected_follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[1]



    def on_mouse_release(self, x, y, button, key_modifiers):
        
        if button == 2:
            self.camera_hold = False

            for g in self.chip.gates:
                self.chip.gates[g].camera = self.camera_position

        else:
            if not self.selected_follower is None:

                if self.bottom_zone_collider.touched:
                    self.selected_follower = None
                else:
                    self.chip.gates[self.selected_follower.id] = self.selected_follower
                    self.selected_follower.camera = self.camera
                    self.selected_follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[0]
                    self.selected_follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2 - self.camera_position[1]
                    self.selected_follower = None

        self.moving_gate = None
        self.moving_gate_offset = (0, 0)
