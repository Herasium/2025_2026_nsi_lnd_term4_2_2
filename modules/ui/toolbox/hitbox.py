import arcade
from modules.ui.mouse import mouse

class HitBox:

    def __init__(self,x=0,y=0,width=0,height=0):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        
        self._recalculate_rect()

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self._recalculate_rect()

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self._recalculate_rect()

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        self._recalculate_rect()

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
        self._recalculate_rect()


    def _recalculate_rect(self):
        self.rect = arcade.XYWH(
            x=self._x,
            y=self._y,
            width=self._width,
            height=self._height,
            anchor=arcade.Vec2(0,0)
        )

    def draw(self):
        arcade.draw_rect_outline(self.rect, arcade.color.ALLOY_ORANGE)

    @property
    def touched(self):
        mouse_x, mouse_y = mouse.cursor
        return (
            self.rect.left   <= mouse_x <= self.rect.right and
            self.rect.bottom <= mouse_y <= self.rect.top
        )
    
    def __repr__(self):
        return (f"HitBox(x={self._x}, y={self._y}, "
                f"width={self._width}, height={self._height})")

    def __str__(self):
        return (f"HitBox at ({self._x}, {self._y}) "
                f"size=({self._width}×{self._height})")
