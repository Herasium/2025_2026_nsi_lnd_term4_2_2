
from arcade import Vec2
from modules.data import data

class _Mouse():

    def __init__(self):
        
        self._x = 0
        self._y = 0

        self._grid_size = data.UI_EDITOR_GRID_SIZE

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self,value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self,value):
        self._y = value

    @property
    def cursor(self):
        return Vec2(round(self._x / self._grid_size)*self._grid_size,round(self._y / self._grid_size)*self._grid_size)
    
    @property
    def grid_size(self):
        return self._grid_size

    @grid_size.setter
    def grid_size(self,value):
        self._grid_size = value

mouse = _Mouse()