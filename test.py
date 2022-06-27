#!/usr/bin/env python
from time import sleep
import PySimpleGUI as sg
from matplotlib.pyplot import pause

# Usage of Graph element.

layout = [[sg.Graph(canvas_size=(500, 100), graph_bottom_left=(0, 0), graph_top_right=(2000, 2000), background_color='white', enable_events=True, key='graph')]]

window = sg.Window('Graph test', layout, finalize=True, no_titlebar=True,
                   grab_anywhere=True,)

graph = window['graph']         # type: sg.Graph

i=0
direction=1
lastpoint=(0,0)
while True:

    if( i == 2000) :
        direction == -1
    else :
        if( i == 0) :
            direction == 1

    sleep(0.1)

    i += direction
    graph.draw_line((i,i), lastpoint)
    lastpoint = (i,i)

    print(i)

window.close()