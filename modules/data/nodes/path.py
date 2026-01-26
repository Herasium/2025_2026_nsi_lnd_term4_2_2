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
        self._camera = (0,0)
 
    
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

    
    def recalculate_hitbox(self):
        
        for current in range(len(self.branch_hitboxes.keys())):

            if len(self.branch_points[current]) > 1:
                self.branch_hitboxes[current] = []
                for point in range(len(self.branch_points[current])-1):
                    current_point = self.branch_points[current][point]
                    current_point = (current_point[0] + self._camera[0], current_point[1] + self._camera[1])
                    next_point = self.branch_points[current][point+1]
                    next_point = (next_point[0] + self._camera[0], next_point[1] + self._camera[1])
                    left, right = self.generate_thick_line_polygon([current_point,next_point], thickness=self.thickness)
                    polygon = left + list(reversed(right))

                    self.branch_hitboxes[current].append(PolyHitbox(polygon))

    def clean_out_single_branch(self,depth = 0):

        if depth > 100:
            print("Max depth on branch clean out.")
            return

        branch_counts = [0 for i in range(len(self.branch_points.keys()))]

        for i in (self.inputs+self.outputs):
            branch_counts[i[4]] += 1

        to_delete = []

        for index in range(len(branch_counts)):
            i = branch_counts[index]
            if i <= 1:
                to_delete.append(index)

        to_delete.sort()
        to_delete.reverse()

        for i in to_delete:
            self.remove_branch(i)

        if len(to_delete) > 1:
            self.clean_out_single_branch(depth=depth+1)
        else:
            if len(to_delete) >0:
                if to_delete[0] != len(self.branch_points)-1:
                    self.clean_out_single_branch(depth=depth+1)
            
    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self,value):
        self._camera = value
        self.recalculate_hitbox()


    @property
    def empty(self):
        value = len(self.branch_points.keys())
        if 0 in self.branch_points:
            value += len(self.branch_points[0])

        return value <= 1
    def remove_branch(self,branch):
        
        for index in range(branch,len(self.branch_points)-1):
            self.branch_points[index] = self.branch_points[index+1]
            self.branch_hitboxes[index] = self.branch_hitboxes[index+1]

        del self.branch_hitboxes[len(self.branch_hitboxes)-1] 
        del self.branch_points[len(self.branch_points)-1] 

        self.current_branch_count = len(self.branch_hitboxes.keys()) 

        if len(self.branch_points) > 0:
            if len(self.branch_points[len(self.branch_points)-1]) != 0:
                self.branch_points[len(self.branch_points)] = []
                self.branch_hitboxes[len(self.branch_hitboxes)] = []
        else:
            self.branch_points[len(self.branch_points)] = []
            self.branch_hitboxes[len(self.branch_hitboxes)] = []

        to_delete = []

        for index in range(len(self.inputs)):
            if self.inputs[index][4] == branch:
                to_delete.append(index)
            elif self.inputs[index][4] > branch:
                self.inputs[index][4] -= 1

        to_delete.sort()
        to_delete.reverse()
 
        for i in to_delete:
            del self.inputs[i]

        to_delete = []

        for index in range(len(self.outputs)):
            if self.outputs[index][4] == branch:
                to_delete.append(index)
            elif self.outputs[index][4] > branch:
                self.outputs[index][4] -= 1

        to_delete.sort()
        to_delete.reverse()
 
        for i in to_delete:
            del self.outputs[i]

    
    def add_path(self):
        
        pt = None

        if self.current_point == None and self.current_branch_count > 0:
                snapped = self.project_point_onto_segments(mouse.cursor[0]- self._camera[0], mouse.cursor[1]- self._camera[1])
                pt = snapped["point"]
                pt = (pt[0], pt[1])
                self.branch_points[snapped["branch"]].insert(snapped["index"]+1,pt)

        if pt == None:
            pt = (mouse.cursor[0]-self._camera[0], mouse.cursor[1]-self._camera[1])
        

        pt = (pt[0], pt[1])
        self.points.append(pt)
        self.branch_points[self.current_branch_count].append(pt)

        self.recalculate_hitbox()

        self.current_point = (mouse.cursor[0]- self._camera[0], mouse.cursor[1]- self._camera[1])

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

    @profile
    def draw(self):

        self.color = self.input_on_color if self.current_value else self.input_off_color

        for bid, pts in self.branch_points.items():
            if len(pts) > 1:

                new_pts = []
                for i in pts:
                    new_pts.append((i[0] + self._camera[0], i[1] + self._camera[1]))

                if self.do_points:
                    if bid > 0:
                        arcade.draw_circle_filled(center_x=pts[0][0] + self._camera[0],center_y=pts[0][1] + self._camera[1],radius=self.thickness,color=self.color)
                        #arcade.draw_circle_filled(center_x=pts[-1][0] + self._camera[0],center_y=pts[-1][1] + self._camera[1],radius=self.thickness,color=self.color)
                arcade.draw_line_strip(
                    point_list=new_pts,
                    color=self.color,
                    line_width=self.thickness
                )

        if self.current_point:
            arcade.draw_line(
                self.current_point[0] + self._camera[0], self.current_point[1] + self._camera[1],
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

    @property
    def get_touched_branch(self):
        for index in self.branch_hitboxes:
            group = self.branch_hitboxes[index]
            if any(hb.touched for hb in group):
                return index

    
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
        return f"Path {self.id}"
    
    def save_hitboxes(self):
        result = {}
        for id in self.branch_hitboxes:
            result[id] = []
            for i in self.branch_hitboxes[id]:
                result[id].append(i.save())
        return result

    def save(self):
        return {
            "type": "path",
            "inputs": self.inputs,
            "outputs": self.outputs,
            "id": self.id,
            "branch_points": self.branch_points,
            "branch_hitboxes": self.save_hitboxes(),
            "current_branch_count": self.current_branch_count
        }
    
    def load_hitboxes(self,hitboxes):
        result = {}
        for index in hitboxes: 
            count = len(result.keys())
            result[count] = []
            for hit in hitboxes[index]:
                result[count].append(PolyHitbox(hit["points"]))
        return result

    def load(self,data):

        self.inputs = data["inputs"]
        self.outputs = data["outputs"]
        self.id = data["id"]
        self.branch_points = {}
        for key in data["branch_points"]:
            self.branch_points[int(key)] = data["branch_points"][key]
        self.branch_hitboxes = self.load_hitboxes(data["branch_hitboxes"])
        self.current_branch_count = data["current_branch_count"]
