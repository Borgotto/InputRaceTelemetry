import os
import sys
from typing import Any, Tuple
import irsdk
import numpy as np
import PySimpleGUI as sg
import PIL.Image
from io import BytesIO
from time import sleep, time



# Literal values
BUFFER_SIZE = 100                           # Number of values to store in the buffer
VALUE_RANGE = (0,100)                       # Range of values for the graphs
LINE_WIDTH = 4                              # Graph line width
UI_SCALING = 1                              # Resize the whole UI window
FONT = ('Mont Heavy DEMO', 22, '#FFFFFF')   # This only changes the Gear and Speed text size (not the Throttle, Brake and Clutch graph values)

class Value():
    """Class to store a value from the iRacing SDK and relative metadata for its rendering within the UI"""
    def __init__(self, name: str, color: str = 'white', initial_value: Any = 0, type: np.dtype = np.int32, value_range: Tuple[Any,Any] = (0,100), buffer_size: int = 1):
        self._name = name
        self._color = color
        self._initial_value = initial_value
        self._type = type
        self._value_range = value_range
        self._buffer_size = buffer_size
        self._values = np.full(self._buffer_size, max(min(max(self._value_range), self._initial_value), min(self._value_range)), dtype=self._type)

    def update(self, value: np.dtype):
        """Shift the buffer and add the new value"""
        self._value = np.roll(self._value, -1)
        self._value[-1] = max(min(max(self._value_range), value), min(self._value_range))

    def get(self) -> np.dtype:
        """Return the last value in the buffer"""
        return self._value[-1]

    def get_all_values(self) -> np.ndarray:
        """Return the buffer containing all the values"""
        return self._value

    def get_range(self) -> Tuple[Any,Any]:
        """Return the value range"""
        return self._value_range

values = {'Throttle': np.random.rand(BUFFER_SIZE)*50,
            'Brake': np.zeros(BUFFER_SIZE, dtype=np.int32)+100,
            'Clutch': np.zeros(BUFFER_SIZE, dtype=np.int32)+10,
            'SteeringWheelAngle': np.zeros(BUFFER_SIZE, dtype=np.float32)
            }
colors = {'Throttle': 'red',
            'Brake': 'blue',
            'Clutch': 'green',
            'SteeringWheelAngle': 'yellow'}

# iRating SDK initialization
ir = irsdk.IRSDK()

# GUI elements
image_bg = PIL.Image.open("bg.png")
image_wheel = PIL.Image.open("wheel.png")
background_layout = [[sg.Image("bg.png", key='bg')]]
top_layout = [[sg.Graph((524,193),(0,VALUE_RANGE[0]-1),(BUFFER_SIZE-1,VALUE_RANGE[1]+1), key='graph', pad=((76,0),(13,0))),
                sg.Graph((44,198),(0,VALUE_RANGE[0]),(1,VALUE_RANGE[1]+22), key='graph2', pad=((17,0),(0,0))),
                sg.Graph((44,198),(0,VALUE_RANGE[0]),(1,VALUE_RANGE[1]+22), key='graph3', pad=((3,0),(0,0))),
                sg.Graph((44,198),(0,VALUE_RANGE[0]),(1,VALUE_RANGE[1]+22), key='graph4', pad=((2,0),(0,0))),
                sg.Graph((70,178),(0,0),(70,178), key='text_overlay', pad=((3,0),(28,0))),
                sg.Image("wheel.png", key='wheel', pad=((0,0),(0,0)))]]



# Utility functions
def make_borderless_window(layout, title):
    """Create a borderless window given a layout and a title"""
    return sg.Window(title,layout,no_titlebar=True,keep_on_top=True,grab_anywhere=True,resizable=False,alpha_channel=0.8,transparent_color=sg.theme_background_color(),margins=(0, 0),element_padding=(0,0))

def darken_color(color : str):
    """Darken a color by 50% (str format should be '#RRGGBB')"""
    return '#'+hex(int((int(color[1:],16)+int('6f6f6f',16))/2))[2:]

def image_to_bytes(image: PIL.Image):
    """Convert a PIL.Image to bytes"""
    bio = BytesIO()
    image.save(bio, format="PNG")
    return bio.getvalue()

def update_values():
    """Update dictionary values with the ones from iRacing"""
    for k, v in values.items():
        values[k] = np.roll(v, -1)
        values[k][-1] = VALUE_RANGE[1]
        values[k][-1] = abs( values[k][-2] + np.random.rand(1)*VALUE_RANGE[1]/4 - VALUE_RANGE[1]/8 ) % VALUE_RANGE[1]
        #values[k][-1] = ir[k]

def update_gui(top_window : sg.Window):
    """Draw the new frame"""
    # Erase previous frame
    for graph in [top_window['graph'], top_window['graph2'], top_window['graph3'], top_window['graph4'], top_window['text_overlay']]:
        graph.erase()

    # Draw all values on main graph
    graph: sg.Graph = top_window['graph']
    for k, v in values.items():
        graph.draw_lines([(i, v[i]) for i in range(v.size)], color=colors[k], width=LINE_WIDTH)

    # Draw Throttle, Brake and Clutch on their own graphs
    for k, g in zip(['Throttle', 'Brake', 'Clutch'], [top_window['graph2'], top_window['graph3'], top_window['graph4']]):
        g.draw_text(str(int(values[k][-1])), (g.TopRight[0]/2, (g.TopRight[1]-VALUE_RANGE[1])/2+VALUE_RANGE[1]), color=FONT[2] if int(values[k][-1]) == VALUE_RANGE[1] else darken_color(FONT[2]), font=(FONT[0], int(g.CanvasSize[0]/2.8)))
        g.draw_line((g.TopRight[0]/2, 0), (g.TopRight[0]/2, values[k][-1]), color=colors[k], width=30)

    # Draw Gear and Speed on text_overlay graph
    graph: sg.Graph = top_window['text_overlay']
    graph.draw_text(str(int(np.random.rand()*10%7+1)), (1, graph.TopRight[1]), color=FONT[2], font=(FONT[0],int(FONT[1])+8), text_location=sg.TEXT_LOCATION_TOP_LEFT)
    graph.draw_text("mph" if np.random.rand() > 0.5 else "kph", (0, FONT[1]+FONT[1]/2.8), color=FONT[2], font=(FONT[0],int(FONT[1]/1.4)), text_location=sg.TEXT_LOCATION_BOTTOM_LEFT)
    graph.draw_text(str(int(np.random.rand()*200+1)), (FONT[1]*2, 0), color=FONT[2], font=(FONT[0],FONT[1]), text_location=sg.TEXT_LOCATION_BOTTOM_RIGHT)

    # Rotate wheel image
    image: sg.Image = top_window['wheel']
    image.update(image_to_bytes(image_wheel.rotate(np.random.rand(1)*360)))

    # Render new frame
    top_window.refresh()



def main():
    # Setup GUI
    sg.Window._move_all_windows = True
    background_window = make_borderless_window(background_layout, 'Background')
    top_window = make_borderless_window(top_layout, 'Telemetry')
    # Show windows
    background_window.finalize()
    top_window.finalize()
    top_window.move(background_window.current_location()[0], background_window.current_location()[1])

    while True:
        update_gui(top_window)
        update_values()
        sleep(0.0167)

    # wait for iracing to start and connect to it through the SDK
    print("Waiting for iRacing...")
    sys.stdout = open(os.devnull, "w")          # suppress irsdk output
    while not ir.startup(): sleep(0.5)          # wait for sdk to connect
    sys.stdout = sys.__stdout__                 # restore stdout
    print("Startup successful")

    while ir.is_connected:
        start = time()                          # start frame calculation time
        update_values()                         # update values from iRacing
        update_gui()                            # update GUI with new values
        stop = time()                           # stop frame time
        sleep(1/ir['FrameRate'] - (stop-start)) # sleep until next frame

    print("iRacing disconnected, exiting...")


if __name__ == '__main__':
    main()