import arcade
import math

from modules.data.node import Node
from modules.ui.toolbox.poly_hitbox import PolyHitbox
from modules.ui.mouse import mouse
from modules.data import data


class Path(Node):

    def __init__(self, id):
        super().__init__(id)

        self.current_point = None
        self.points = []          # active branch points

        self.branch_points = {}   # { branch_id: [ (x,y), (x,y) ] }
        self.branch_hitboxes = {} # { branch_id: PolyHitbox }

        self.inputs = []
        self.outputs = []
        self.grid_size = data.UI_EDITOR_GRID_SIZE
        
        self.current_branch_count = 0
        self.color = arcade.color.RED

        self.thickness = 10

        # create initial branch
        self.branch_points[0] = []
        self.branch_hitboxes[0] = PolyHitbox()


    def add_path(self):

        pt = (mouse.cursor[0], mouse.cursor[1])
        self.points.append(pt)
        self.branch_points[self.current_branch_count].append(pt)

        if len(self.points) > 1:
            left, right = self.generate_thick_line_polygon(self.points, thickness=self.thickness)
            polygon = left + list(reversed(right))

            self.branch_hitboxes[self.current_branch_count].points = polygon

        self.current_point = mouse.cursor

    def finish(self):
        # finalize the active segment
        self.add_path()

        # move to new branch
        self.current_branch_count += 1
        self.current_point = None

        # reset active points list
        self.points = []

        # register a new branch
        self.branch_points[self.current_branch_count] = []
        self.branch_hitboxes[self.current_branch_count] = PolyHitbox()


    def draw(self):

        self.color = arcade.color.BLUE if self.touched else arcade.color.RED

        # Draw ALL branch lines
        for bid, pts in self.branch_points.items():
            if len(pts) > 1:
                arcade.draw_line_strip(
                    point_list=pts,
                    color=self.color,
                    line_width=self.thickness
                )

        # Draw active "rubber band" segment
        if self.current_point:
            arcade.draw_line(
                self.current_point[0], self.current_point[1],
                mouse.cursor[0], mouse.cursor[1],
                color=self.color,
                line_width=self.thickness
            )



    @property
    def touched(self):
        return any(hb.touched for hb in self.branch_hitboxes.values())


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
