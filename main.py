import os
import sys
import time

from irsdk import IRSDK
from gui import Gui
from value import Value

DEBUG: bool = True # set to True to run without iRacing

# Literal values
UI_SCALE = 1
LINE_WIDTH = 4
TRANSPARENCY = 0.8
FONT = {'name': 'Mont Heavy DEMO',
        'size': 22,
        'color': '#FFFFFF'}

# iRacing values to be tracked, buffered values will be rendered in a graph
_values = [ Value('Throttle',           color='green',       type=float, range=(0.0,100.0),    buffer_size=50),
            Value('Brake',              color='red',         type=float, range=(0.0,100.0),    buffer_size=50),
            Value('Clutch',             color='blue',        type=float, range=(0.0,100.0),    buffer_size=50),
            Value('SteeringWheelAngle', color='white',       type=float, range=(-180.0,180.0), buffer_size=50),
            Value('Speed',              initial_value=0,     type=int,   range=(0, None)),
            Value('Gear',               initial_value='N',   type=str),
            Value('DisplayUnits',       initial_value="kph", type=str)]
# Values dictionary
values = {v.name: v for v in _values}
# Tuple of 3 Values to be displayed in columns
columns = (values['Throttle'], values['Brake'], values['Clutch'])

def main():
    # Setup iRacing SDK
    ir = IRSDK() if not DEBUG else type('irsdk.IRSDK', (object,), {'__getitem__': lambda self, value: getattr(self, value),'startup': lambda self: True,'is_initialized': True,'is_connected': True,'FrameRate': 60,'Throttle': 100.0,'Brake': 93.0,'Clutch': 15.0,'SteeringWheelAngle': 168.0,'Speed': 200,'Gear': '3','DisplayUnits': 'kmh',})()
    print("Waiting for iRacing...")
    sys.stdout = open(os.devnull, "w")      # suppress irsdk output
    while not ir.startup(): time.sleep(0.5) # wait for sdk to connect
    sys.stdout = sys.__stdout__             # restore stdout
    print("Startup successful")

    # Setup GUI
    gui = Gui(UI_SCALE, LINE_WIDTH, FONT, TRANSPARENCY)
    gui.show()

    # Main loop
    framerate = ir['FrameRate']
    while ir.is_connected:
        start = time.time()                                # start frame calculation time
        for v in _values: v.value = ir[v.name]             # update values from iRacing
        gui.update(values, columns)                        # update GUI with new values
        stop = time.time()                                 # stop frame time
        time.sleep(max(1/framerate-(stop-start), 0))       # sleep until next frame

        if DEBUG:                                          # DEBUG: print frame times
            if round(stop-start,6) > round(1/framerate,6):
                print(f"Frame took too long to render: {((stop-start)*1000):.4f}ms (should be < {((1/framerate)*1000):.4f}ms) - {(1/(stop-start)):.0f}fps")
            else:
                print(f"{((stop-start)*1000):.0f}ms - {(1/(stop-start)):.0f}fps")
    print("iRacing disconnected, exiting...")


if __name__ == '__main__':
    main()