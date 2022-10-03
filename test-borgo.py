import os
import sys
from io import BytesIO
from time import sleep, time
from collections import deque
from typing import Any, Iterable, Tuple, List

import irsdk
import PIL.Image
import PySimpleGUI as sg


class Value():
    """Class to store a value from the iRacing SDK and relative metadata for its rendering within the UI"""
    def __init__(self, name: str, color: str = 'white', range: Tuple[Any,Any] = (None,None), initial_value: Any = 0.0, type: Any = int, buffer_size: int = 1):
        self._name = name.strip()
        self._color = color.strip()
        self._range = (min(range), max(range)) if range[0] and range[1] else range
        self._type = type
        self._values = deque([self._clamp(initial_value)] * buffer_size, maxlen=buffer_size)

    def _clamp(self, value):
        "Restrict a value to the range and type defined at initialization"
        if not isinstance(value, self.type):
            raise TypeError(f"Value {value} is not of type {self.type}")
        if self.range[1] is not None:
            value = min(self.range[1], value)
        if self.range[0] is not None:
            value = max(self.range[0], value)
        return value

    @property
    def name(self) -> str:
        """Return the name of the attribute"""
        return self._name

    @property
    def color(self) -> str:
        """Return the color of the rendered graph lines"""
        return self._color

    @property
    def buffer_size(self) -> int:
        """Return the size of the buffer array"""
        return len(self.values)

    @property
    def is_buffered(self) -> bool:
        """Check if the value has a buffer size greater than 1"""
        return self.buffer_size > 1

    @property
    def range(self) -> Tuple[Any,Any]:
        """Return the value range"""
        return self._range

    @property
    def type(self):
        """Return the data type of the value"""
        return self._type

    @property
    def values(self) -> List[Any]:
        """Return the buffer containing all the values"""
        return self._values

    @values.setter
    def values(self, value: Iterable[Any]) -> None:
        """Set n values in the buffer, extra values will be discarded"""
        for e in value:
            self.values.append(self._clamp(e))

    @property
    def value(self) -> Any:
        """Return the last value in the buffer"""
        return self.values[-1]

    @value.setter
    def value(self, value: Any) -> None:
        """Set the last value in the buffer"""
        self.values = [value]


# iRating SDK initialization
ir = irsdk.IRSDK()

# Literal values
UI_SCALING = 1
FONT = {'name': 'Mont Heavy DEMO',
        'size': 22,
        'color': '#FFFFFF'}

# Tracked values
_values = [Value('Throttle',           color='green',        type=float, range=(0,100),    buffer_size=100),
            Value('Brake',              color='red',         type=float, range=(0,100),    buffer_size=100),
            Value('Clutch',             color='blue',        type=float, range=(0,100),    buffer_size=100),
            Value('SteeringWheelAngle', color='white',       type=float, range=(-180,180), buffer_size=100),
            Value('Speed',              initial_value=0,     type=int,   range=(0, None)),
            Value('Gear',               initial_value='N',   type=str),
            Value('DisplayUnits',       initial_value="kph", type=str)]
values = {v.name: v for v in _values}
columns: Tuple[Value, Value, Value] = (values['Throttle'], values['Brake'], values['Clutch'])

# GUI elements
image_bg = PIL.Image.open("./res/bg.png")
image_wheel = PIL.Image.open("./res/wheel.png")
background_layout = [[sg.Image(image_bg.filename,   key='bg')]]
top_layout = [[sg.Graph((524,193),(0,-1),(1048-1,386+1), key='graph',   pad=((76,0),(13,0))),
                sg.Graph((44,198),(0,0),(1,100+22), key='column1',      pad=((17,0),(0,0))),
                sg.Graph((44,198),(0,0),(1,100+22), key='column2',      pad=((3,0),(0,0))),
                sg.Graph((44,198),(0,0),(1,100+22), key='column3',      pad=((2,0),(0,0))),
                sg.Graph((70,178),(0,0),(70,178),   key='text_overlay', pad=((3,0),(28,0))),
                sg.Image(image_wheel.filename,      key='wheel',        pad=((0,0),(0,0)))]]


# Utility functions
def _make_borderless_window(layout, title):
    """Create a borderless window given a layout and a title"""
    return sg.Window(title,layout,no_titlebar=True,keep_on_top=True,grab_anywhere=True,resizable=False,alpha_channel=0.8,transparent_color=sg.theme_background_color(),margins=(0, 0),element_padding=(0,0))

def _darken_color(color : str):
    """Darken a color by 50% (str format should be '#RRGGBB' or 'RRGGBB')"""
    return '#'+hex(int((int(color[1:] if color.startswith('#') else color,16)+int('6f6f6f',16))/2))[2:]

def _image_to_bytes(image: PIL.Image):
    """Convert a PIL.Image to bytes"""
    bio = BytesIO()
    image.save(bio, format="PNG")
    return bio.getvalue()

def update_values():
    """Update dictionary values with the ones from iRacing"""
    for v in values:
        continue #TODO: remove continue once iracing integration is finished
        v.value = ir[v.name]

def update_gui(top_window : sg.Window):
    """Draw the new frame"""
    # Erase every graph's canvas
    [e.erase() for e in top_window.AllKeysDict.values() if isinstance(e, sg.Graph)]

    # Draw all buffered values on the main graph
    graph: sg.Graph = top_window['graph']
    for v in [v for v in values.values() if v.is_buffered]:
        scaling = {'x': graph.TopRight[0]/(v.buffer_size-1), 'y': graph.TopRight[1]/(sum(abs(x) for x in v.range))}
        lines = [(i * scaling['x'], (v.values[i] + abs(v.range[0])) * scaling['y']) for i in range(v.buffer_size)]
        graph.draw_lines(lines, color=v.color, width=4)

    # Draw Throttle, Brake and Clutch on their own column graphs
    for v, g in zip([values['Throttle'], values['Brake'], values['Clutch']], [top_window['column1'], top_window['column2'], top_window['column3']]):
        scaling = {'x': g.TopRight[0]/2, 'y': (g.TopRight[1]-22)/(sum(abs(x) for x in v.range))}
        g.draw_text(str(int(v.value)), (scaling['x'], (g.TopRight[1] - 100*scaling['y'])/2 + 100*scaling['y']), color=FONT['color'] if int(v.value) >= v.range[1] else _darken_color(FONT['color']), font=(FONT['name'], int(g.CanvasSize[0]/2.8)))
        g.draw_line((scaling['x'], 0), (scaling['x'], scaling['y'] * v.value), color=v.color, width=30)

    # Draw Gear, Unit and Speed on text_overlay graph
    graph = top_window['text_overlay']
    graph.draw_text(str(values["Gear"].value), (1, graph.TopRight[1]), color=FONT['color'], font=(FONT['name'],int(FONT['size'])+8), text_location=sg.TEXT_LOCATION_TOP_LEFT)
    graph.draw_text(str(values['DisplayUnits'].value), (0, FONT['size']+FONT['size']/2.8), color=FONT['color'], font=(FONT['name'],int(FONT['size']/1.4)), text_location=sg.TEXT_LOCATION_BOTTOM_LEFT)
    graph.draw_text(str(values['Speed'].value), (FONT['size']*2, 0), color=FONT['color'], font=(FONT['name'],FONT['size']), text_location=sg.TEXT_LOCATION_BOTTOM_RIGHT)

    # Rotate wheel image
    image: sg.Image = top_window['wheel']
    image.update(_image_to_bytes(image_wheel.rotate(values['SteeringWheelAngle'].value or 0)))

    # Render new frame
    top_window.refresh()


def main():
    # Setup GUI
    sg.Window._move_all_windows = True
    background_window = _make_borderless_window(background_layout, 'Background')
    top_window = _make_borderless_window(top_layout, 'Telemetry')
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