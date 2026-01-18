import arcade
import math

from modules.data.node import Node
from modules.ui.toolbox.poly_hitbox import PolyHitbox
from modules.ui.mouse import mouse
from modules.data import data

from line_profiler import profile

class Path(Node):

    def __init__(self, id):
        super().__init__(id)

        self.current_point = None
        self.points = []        

        self.branch_points = {}  
        self.branch_hitboxes = {} 

        self.inputs = []
        self.outputs = []
        self.grid_size = data.UI_EDITOR_GRID_SIZE
        
        self.current_branch_count = 0
        self.color = arcade.color.RED

        self.thickness = data.UI_EDITOR_GRID_SIZE /2 

        self.branch_points[0] = []
        self.branch_hitboxes[0] = []

        self.input_off_color = arcade.types.Color.from_hex_string(data.COLORS.VALUE_OFF)
        self.input_on_color = arcade.types.Color.from_hex_string(data.COLORS.VALUE_ON)

        self.current_value = False
        self.draw_hitboxes = False

        self.do_points = True

    @profile
    def project_point_onto_segments(self, x, y):
        closest = {
            "point": None,
            "branch": None,
            "index": None,
            "dist": float('inf')
        }

        for bid, pts in self.branch_points.items():
            if len(pts) < 2:
                continue

            for i in range(len(pts) - 1):
                x1, y1 = pts[i]
                x2, y2 = pts[i + 1]

                dx = x2 - x1
                dy = y2 - y1
                seg_len_sq = dx * dx + dy * dy

                if seg_len_sq == 0:
                    continue

                t = ((x - x1) * dx + (y - y1) * dy) / seg_len_sq
                t = max(0.0, min(1.0, t))

                px = x1 + t * dx
                py = y1 + t * dy

                dist_sq = (px - x)**2 + (py - y)**2

                if dist_sq < closest["dist"]:
                    closest = {
                        "point": (px, py),
                        "branch": bid,
                        "index": i,
                        "dist": dist_sq
                    }

        return closest

    @profile
    def recalculate_hitbox(self):
        
        for current in range(self.current_branch_count):

            if len(self.branch_points[current]) > 1:
                self.branch_hitboxes[current] = []
                for point in range(len(self.branch_points[current])-1):
                    current_point = self.branch_points[current][point]
                    next_point = self.branch_points[current][point+1]
                    left, right = self.generate_thick_line_polygon([current_point,next_point], thickness=self.thickness)
                    polygon = left + list(reversed(right))

                    self.branch_hitboxes[current].append(PolyHitbox(polygon))


    @profile
    def add_path(self):
        
        pt = None

        if self.current_point == None and self.current_branch_count > 0:
                snapped = self.project_point_onto_segments(mouse.cursor[0], mouse.cursor[1])
                pt = snapped["point"]
                self.branch_points[snapped["branch"]].insert(snapped["index"]+1,pt)

        if pt == None:
            pt = (mouse.cursor[0], mouse.cursor[1])
            
        self.points.append(pt)
        self.branch_points[self.current_branch_count].append(pt)

        self.recalculate_hitbox()

        self.current_point = mouse.cursor

    def finish(self):
        self.add_path()

        self.current_branch_count += 1
        self.current_point = None

        self.points = []

        self.branch_points[self.current_branch_count] = []
        self.branch_hitboxes[self.current_branch_count] = []

        self.recalculate_hitbox()

    def abort(self):
        self.current_point = None

        self.points = []

        self.branch_points[self.current_branch_count] = []
        self.branch_hitboxes[self.current_branch_count] = []

        self.recalculate_hitbox()


    def draw(self):

        self.color = self.input_on_color if self.current_value else self.input_off_color

        for bid, pts in self.branch_points.items():
            if len(pts) > 1:
                if self.do_points:
                    arcade.draw_circle_filled(center_x=pts[0][0],center_y=pts[0][1],radius=self.thickness,color=self.color)
                    arcade.draw_circle_filled(center_x=pts[-1][0],center_y=pts[-1][1],radius=self.thickness,color=self.color)
                arcade.draw_line_strip(
                    point_list=pts,
                    color=self.color,
                    line_width=self.thickness
                )

        if self.current_point:
            arcade.draw_line(
                self.current_point[0], self.current_point[1],
                mouse.cursor[0], mouse.cursor[1],
                color=self.color,
                line_width=self.thickness
            )

        if self.draw_hitboxes:
            for i in self.branch_hitboxes:
                for a in self.branch_hitboxes[i]:
                    a.draw()

    def merge(self,path):

        branch_offset = self.current_branch_count 

        last_point = path.branch_points[path.current_branch_count][-1] 
        snapped = self.project_point_onto_segments(last_point[0],last_point[1])

        pt = snapped["point"]
        self.branch_points[snapped["branch"]].insert(snapped["index"]+1,pt)

        path.branch_points[path.current_branch_count][-1]  = pt

        for i in path.branch_points:
            self.branch_points[self.current_branch_count] = path.branch_points[i]
            self.current_branch_count += 1

        for i in path.inputs:
            self.inputs.append([i[0],i[1],i[2],i[3],i[4] + branch_offset])

        for i in path.outputs:
            self.outputs.append([i[0],i[1],i[2],i[3],i[4] + branch_offset])

        self.current_branch_count -= 1
        self.finish()

    @profile
    def get_connected_points(self, target_id):
        connected_inputs = []
        connected_outputs = []

        for inp in self.inputs:
            if inp[1] == target_id:  
                connected_inputs.append(inp)

        for outp in self.outputs:
            if outp[1] == target_id:
                connected_outputs.append(outp)

        return connected_inputs,connected_outputs


    @property
    def touched(self):
        return any(hb.touched for group in self.branch_hitboxes.values() for hb in group)


    @profile
    def generate_thick_line_polygon(self, points, thickness):
        if len(points) < 2:
            return [], []

        half = thickness / 2

        left_points = []
        right_points = []

        def normalize(vx, vy):
            length = math.sqrt(vx * vx + vy * vy)
            if length == 0:
                return 0, 0
            return vx / length, vy / length

        for i in range(len(points)):
            p = points[i]

            if i == 0:
                dx = points[i+1][0] - p[0]
                dy = points[i+1][1] - p[1]
            elif i == len(points)-1:
                dx = p[0] - points[i-1][0]
                dy = p[1] - points[i-1][1]
            else:
                dx1 = points[i+1][0] - p[0]
                dy1 = points[i+1][1] - p[1]
                dx2 = p[0] - points[i-1][0]
                dy2 = p[1] - points[i-1][1]
                dx = dx1 + dx2
                dy = dy1 + dy2

            nx, ny = normalize(dx, dy)

            px = -ny
            py = nx

            left_points.append((p[0] + px * half, p[1] + py * half))
            right_points.append((p[0] - px * half, p[1] - py * half))

        return left_points, right_points

    def __str__(self):
        out = []
        out.append(f"Path(id={self.id})")
        out.append(f"  Current value: {self.current_value}")
        out.append(f"  Color: {self.color}")
        out.append(f"  Grid size: {self.grid_size}")
        out.append(f"  Thickness: {self.thickness}")
        out.append(f"  Current point: {self.current_point}")
        out.append(f"  Current branch index: {self.current_branch_count}")
        out.append("")
        out.append("  Inputs:")
        if self.inputs:
            for i, inp in enumerate(self.inputs):
                out.append(f"    [{i}] {inp}")
        else:
            out.append("    (none)")
        out.append("")
        out.append("  Outputs:")
        if self.outputs:
            for i, outp in enumerate(self.outputs):
                out.append(f"    [{i}] {outp}")
        else:
            out.append("    (none)")
        out.append("")
        out.append("  Branches:")
        for bid, pts in self.branch_points.items():
            out.append(f"    Branch {bid}:")
            out.append(f"      Points ({len(pts)}):")
            for p in pts:
                out.append(f"        {p}")

            hb = self.branch_hitboxes.get(bid)
            if hb:
                out.append("      Hitbox points:")
                for point in hb:
                        out.append(f"        {point}")
                else:
                    out.append("        (empty)")
            else:
                out.append("      Hitbox: (missing)")
            out.append("")
        return "\n".join(out)
