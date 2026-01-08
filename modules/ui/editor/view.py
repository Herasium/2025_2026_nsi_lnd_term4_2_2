import arcade
from line_profiler import profile

from modules.ui.mouse import mouse
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.grid import Grid
from modules.ui.toolbox.id_generator import random_id

from modules.data.nodes.path import Path
from modules.data.nodes.gate import Gate
from modules.data.nodes.input import Input

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

        self.simulate_button = Entity()
        self.simulate_button.width = 100
        self.simulate_button.height = 100

        self.selected_cursor = 1

        # changed
        self.gates = {}   # id : Gate
        self.paths = {}   # id : Path

        self.moving_gate_offset = (0, 0)
        
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

    def reset(self):
        pass

    def on_draw(self):
        self.clear()
        self.simulate_button.draw()

        for p in self.paths.values():
            p.draw()

        for g in self.gates.values():
            g.draw()

        if self.current_path:
            self.current_path.draw()

        if self.selected_follower:
            self.selected_follower.draw()


    def on_update(self, delta_time):
        for gate in self.gates.values():
            gate.update()


    def on_key_press(self, key, key_modifiers):
        if key == 97:  # "a"
            arcade.exit()
        if key == 65307:  # ESC
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
            for path in self.paths.values():
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
        propagate_values(self.gates,self.paths)

    def on_mouse_press(self, x, y, button, key_modifiers):

        if self.simulate_button.touched:
            self.simulate()
            return

        # Clicked a gate?
        for g in self.gates.values():
            touched = g.touched
            if touched:
                if self.current_path is None:
                    # start new path
                    pid = random_id()
                    self.current_path = Path(pid)
                    self.current_path.add_path()

                    if touched[0] == 1:
                        self.current_path.outputs.append((1, g.id, touched[1], 1, self.current_path.current_branch_count))
                    else:
                        self.current_path.inputs.append((2, g.id, touched[1], 1, self.current_path.current_branch_count))
                    return

                else:
                    # finish existing path
                    if touched[0] == 1:
                        self.current_path.outputs.append((1, g.id, touched[1], 2, self.current_path.current_branch_count))
                    else:
                        self.current_path.inputs.append((2, g.id, touched[1], 2, self.current_path.current_branch_count))

                    self.current_path.finish()

                    if self.current_path.id not in self.paths:
                        self.paths[self.current_path.id] = self.current_path

                    self.current_path = None
                    return

        # Clicking on a path
        if not self.current_path:
            for p in self.paths.values():
                if p.touched:
                    p.add_path()
                    self.current_path = p
                    return
        else:
            for p in self.paths.values():
                if p.touched and p != self.current_path:
                    self.current_path.add_path()
                    p.merge(self.current_path)

                    if self.current_path.id in self.paths:
                        del self.paths[self.current_path.id]

                    self.current_path = None
                    return

            self.current_path.add_path()
            return

        # Move a gate
        if self.moving_gate is None:
            for g in self.gates.values():
                if g.entity.touched:
                    self.moving_gate_offset = (
                        mouse.cursor[0] - g.x,
                        mouse.cursor[1] - g.y
                    )
                    self.moving_gate = g
                    return

        # Place new gate
        if self.selected_follower is None:
            if self.selected_cursor == 0:
                self.selected_follower = Gate(random_id(),self.gate_tiles)
            elif self.selected_cursor == 1:
                self.selected_follower = Input(random_id(),self.gate_tiles)
            self.selected_follower.x = mouse.cursor[0] - self.grid_size / 2
            self.selected_follower.y = mouse.cursor[1] - self.grid_size / 2

        else:
            self.gates[self.selected_follower.id] = self.selected_follower
            self.selected_follower = None


    def on_mouse_release(self, x, y, button, key_modifiers):
        self.moving_gate = None
        self.moving_gate_offset = (0, 0)
