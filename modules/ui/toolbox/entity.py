import arcade
from modules.ui.toolbox.hitbox import HitBox
from modules.data import data

class Entity:

    def __init__(self):

        self._x = 0
        self._y = 0

        self._width = 10
        self._height = 10

        self.hitbox = HitBox()
        self._update_hitbox()

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
        self._update_hitbox()

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
        self._update_hitbox()

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        self._width = value
        self._update_hitbox()

    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        self._height = value
        self._update_hitbox()

    def _update_hitbox(self):
        self.hitbox.x = self._x
        self.hitbox.y = self._y
        self.hitbox.width = self._width
        self.hitbox.height = self._height

    def draw(self):
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self._x, self._y, self._width, self._height,anchor=arcade.Vec2(0,0)),
            arcade.color.BLUE,
        )

    @property
    def touched(self):
        return self.hitbox.touched