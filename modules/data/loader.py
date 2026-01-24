from os import listdir
from os.path import isfile, join, isdir
import zlib
import json
from modules.data import data
from modules.data.chip import Chip
import arcade
import traceback
from modules.data.gate_index import gate_types
from PIL import Image,ImageFont,ImageDraw

def load_saves():

    saves = join(data.current_path,"saves")

    if not isdir(saves):
         return 

    files = [f for f in listdir(saves) if isfile(join(saves, f))]
    read = []

    for file_path in files:
        complete = join(saves,file_path)
        try: 
            with open(complete,"rb") as file:
                raw= file.read()
                file.close()

            dump = zlib.decompress(raw).decode()
            loaded = json.loads(dump)
            read.append(loaded)
        except Exception as e:
            print(f"Failed to read file {complete} ({e})")

    for i in read:
        try:
            new = Chip("default_id")
            new.load(i)
            data.loaded_chips[i["id"]] = new
        except Exception as e: 
             print(f"Failed to load chip \n\n{i}\n\n")
             print(traceback.format_exc())

def load_tiles():
        
        ui_border_sheet = arcade.SpriteSheet("assets/ui_border_grid.png")

        ui_border_tiles = ui_border_sheet.get_texture_grid(
            size = (64, 64),
            columns = 4,
            count = 4*4,
        )

        data.ui_border_tiles = ui_border_tiles

        gate_sheet = arcade.SpriteSheet("assets/gate_grid.png")

        gate_tiles = gate_sheet.get_texture_grid(
            size=(data.UI_EDITOR_GRID_SIZE, data.UI_EDITOR_GRID_SIZE),
            columns=6,
            count=6*6
        )

        data.gate_tiles = gate_tiles

def load_font():
     arcade.load_font("assets/press_start.ttf")
     

def bake_background_grid_texture():
    start_x = 0
    y_len = int(1088/64)
    start_y = 1088

    new = Image.new("RGBA",(1920,1088))

    for i in range(y_len):
        for a in range(int(1920/64)):
            new.paste(data.ui_border_tiles[9].image, (start_x + (a)*64,start_y- (i+1)*64))
        
    data.background_grid_texture = arcade.Texture(new)

def render_gate_image(gate):
    width = gate.tile_width
    height = 4

    current = 0
    new = Image.new("RGBA",(width*data.UI_EDITOR_GRID_SIZE,height*data.UI_EDITOR_GRID_SIZE))
    myFont = ImageFont.truetype('assets/press_start.ttf', 32)

    for y in range(height):
        for x in range(width):

            tile_x = x * data.UI_EDITOR_GRID_SIZE
            tile_y = ((height-1)-y) * data.UI_EDITOR_GRID_SIZE
            tile = gate.tiles[gate.gate_tile_pattern[current]].image.copy()

            tile.resize((data.UI_EDITOR_GRID_SIZE,data.UI_EDITOR_GRID_SIZE))
            new.paste(tile,(tile_x,tile_y))

            current += 1

    I1 = ImageDraw.Draw(new)

    text_x = gate.width/2 
    text_y = (4*data.UI_EDITOR_GRID_SIZE) - (gate.height /1.6 + data.UI_EDITOR_GRID_SIZE/4)

    bg_text_x = text_x - 2
    bg_text_y = text_y - 4

    I1.text((bg_text_x, bg_text_y), gate.name, font=myFont, fill="#5f556a", anchor = "mm")
    I1.text((text_x, text_y), gate.name, font=myFont, fill="#b45252", anchor = "mm")

    return new
    
def bake_gate_texture(gate_id):

    gate = gate_types[gate_id]("default_id")
    size = len(gate.inputs)+len(gate.outputs)
    power = 2 ** (size)
    data.IMAGE.add_gate_type(gate_id)

    for current in range(power):
        values = [bool(current & (1 << i)) for i in range(size)]
        gate.inputs = values[:len(gate.inputs)]
        gate.outputs = values[len(gate.inputs):]

        gate.gen_tile_pattern()
        new = render_gate_image(gate)
        data.IMAGE.add_texture(gate_id,current,arcade.Texture(new))

    data.IMAGE.complete_gate(gate_id)

def bake_textures():
    print("Baking Textures")
    bake_background_grid_texture()

    for i in gate_types:
        bake_gate_texture(i)

    print(data.IMAGE.buffer)
def load_textures():
    bake_textures()