import os
import sys
import time
import math

from gui import Gui
from value import Value

DEBUG: bool = True # set to True to run without iRacing and print debug info
if DEBUG:
    from debugirsdk import IRSDK
else:
    from irsdk import IRSDK

# Literal values
UI_SCALE = 1
LINE_WIDTH = 4
TRANSPARENCY = 0.8
FONT = {'name': 'Mont Heavy DEMO',
        'size': 22,
        'color': '#FFFFFF'}

def main():
    # Setup iRacing SDK
    ir = IRSDK()
    print("Waiting for iRacing...")
    sys.stdout = open(os.devnull, "w")      # suppress irsdk output
    while not ir.startup(): time.sleep(0.5) # wait for sdk to connect
    sys.stdout = sys.__stdout__             # restore stdout
    print("Startup successful")

    # iRacing values to be tracked, buffered values will be rendered in a graph
    buff_size = 100
    _values = [ Value('Throttle',           color='green', type=float, range=(0.0, 1.0), buffer_size=buff_size),
                Value('Brake',              color='red',   type=float, range=(0.0, 1.0), buffer_size=buff_size),
                Value('Clutch',             color='blue',  type=float, range=(0.0, 1.0), buffer_size=buff_size, convert_func=lambda v: 1-v),
                Value('SteeringWheelAngle', color='white', type=float, buffer_size=buff_size, convert_func=lambda v: math.degrees(v)),
                Value('Speed',              type=int, range=(0, None)),
                Value('Gear',               type=str, convert_func=lambda v: {'0':'N','-1':'R'}.get(v,v)),
                Value('DisplayUnits',       type=str, convert_func=lambda v: {'0':'mph','1':'kph'}.get(v,v))]
    # Values dictionary
    values = {v.name: v for v in _values}
    # Tuple of 3 Values to be displayed in columns
    columns = (values['Throttle'], values['Brake'], values['Clutch'])

    # Setup GUI
    gui = Gui(UI_SCALE, LINE_WIDTH, FONT, TRANSPARENCY)
    gui.show()

    # Main loop
    while ir.is_connected:
        framerate = ir['FrameRate']
        values['SteeringWheelAngle'].range = (math.degrees(-ir['SteeringWheelAngleMax']/2), math.degrees(ir['SteeringWheelAngleMax']/2))
        start = time.time()                                 # start frame calculation time
        for v in _values: v.value = ir[v.name]              # update values from iRacing
        gui.update(values, columns)                         # update GUI with new values
        stop = time.time()                                  # stop frame time
        time.sleep(1/framerate - time.time() % 1/framerate) # sleep until next frame

        if DEBUG:                                           # print debug info
            print(f"{((stop-start)*1000):.3f}ms - {(1/(stop-start)):.0f}fps", f"- Frame took too long to render (should be < {((1/framerate)*1000):.3f}ms)" if round(stop-start,3) > round(1/framerate,3) else "")
    print("iRacing disconnected, exiting...")

if __name__ == '__main__':
    main()