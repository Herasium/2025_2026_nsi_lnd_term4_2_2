import arcade
from line_profiler import profile

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

        self.grid_size = data.UI_EDITOR_GRID_SIZE

        self.follower = Entity()
        self.follower.height = self.grid_size
        self.follower.width = self.grid_size

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

        self.chip = Chip()

        self.moving_gate_offset = (0, 0)

        self.camera_position = ()
        
        TILE_W = 27
        TILE_H = 27
        ROWS = 6
        COLS = 6
        COUNT = ROWS * COLS 

        self.gate_sheet = arcade.SpriteSheet("assets/gate_grid.png")

        self.gate_tiles = self.gate_sheet.get_texture_grid(
            size=(TILE_W, TILE_H),
            columns=COLS,
            count=COUNT
        )

        self.numpad_key_list = [65456,65457,65458,65459,65460,65461,65462,65463,65464,65465]
        self.add_side_bar()

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

    def on_draw(self):
        self.clear()

        for p in self.chip.paths.values():
            p.draw()

        for g in self.chip.gates.values():
            g.draw()

        if self.current_path:
            self.current_path.draw()

        if self.selected_follower:
            self.selected_follower.draw()

        self.render_side_bar()

    def on_update(self, delta_time):
        self.simulate()


    def on_key_press(self, key, key_modifiers):

        if key in self.numpad_key_list:
            self.selected_cursor = self.numpad_key_list.index(key)

        if key == 101:
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


    def on_key_release(self, key, key_modifiers):
        pass


    @profile
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x, y)

        self.follower.x = mouse.cursor[0] - self.grid_size / 2
        self.follower.y = mouse.cursor[1] - self.grid_size / 2

        if self.selected_follower:
            self.selected_follower.x = mouse.cursor[0] - self.grid_size / 2
            self.selected_follower.y = mouse.cursor[1] - self.grid_size / 2

        if self.moving_gate:
            self.moving_gate.x = mouse.cursor[0] - self.moving_gate_offset[0]
            self.moving_gate.y = mouse.cursor[1] - self.moving_gate_offset[1]

            # update connected paths
            for path in self.chip.paths.values():
                connected_inputs, connected_outputs = path.get_connected_points(self.moving_gate.id)
                modified = False

                for i in connected_inputs:
                    modified = True
                    if i[3] == 1:
                        path.branch_points[i[4]][0] = self.moving_gate.outputs_position[i[2]]
                    elif i[3] == 2:
                        path.branch_points[i[4]][-1] = self.moving_gate.outputs_position[i[2]]

                for i in connected_outputs:
                    modified = True
                    if i[3] == 1:
                        path.branch_points[i[4]][0] = self.moving_gate.inputs_position[i[2]]
                    elif i[3] == 2:
                        path.branch_points[i[4]][-1] = self.moving_gate.inputs_position[i[2]]

                if modified:
                    path.recalculate_hitbox()

    def simulate(self):
        propagate_values(self.chip)

    def on_mouse_press(self, x, y, button, key_modifiers):

        # Clicked a gate?
        for g in self.chip.gates.values():
            touched = g.touched
            if touched:
                if self.current_path is None:
                    # start new path
                    pid = random_id()
                    self.current_path = Path(pid)
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
            self.selected_follower =  self.cursors[self.selected_cursor](random_id(),self.gate_tiles)
            self.selected_follower.x = mouse.cursor[0] - self.grid_size / 2
            self.selected_follower.y = mouse.cursor[1] - self.grid_size / 2

        else:
            self.chip.gates[self.selected_follower.id] = self.selected_follower
            self.selected_follower = None


    def on_mouse_release(self, x, y, button, key_modifiers):
        self.moving_gate = None
        self.moving_gate_offset = (0, 0)
