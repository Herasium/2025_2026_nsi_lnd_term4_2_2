class COLORS:
    VALUE_ON = "DC2626"
    VALUE_OFF = "D9D9D9"
        
class ImageBuffer():
    def __init__(self):

        self.buffer = {}

    def add_gate_type(self,id):
        self.buffer[id] = {
            "complete": False,
            "textures": {}
        }

    def add_texture(self,id,texture_id,texture):
        self.buffer[id]["textures"][texture_id] = texture

    def get_texture(self,id,texture_id):
        return self.buffer[id]["textures"][texture_id]

    def complete_gate(self,id):
        self.buffer[id]["complete"] = True

    def is_complete_gate(self,id):
        return self.buffer[id]["complete"]


class Data:
    def __init__(self):
        self.WINDOW_WIDTH = 1920
        self.WINDOW_HEIGHT = 1080
        self.WINDOW_FULLSCREEN = True
        self.UI_EDITOR_GRID_SIZE = 27
        self.COLORS = COLORS
        self.IMAGE = ImageBuffer()

data = Data()