from os import path
from io import BytesIO
from typing import Tuple, Dict, Union
import PIL.Image
import PySimpleGUI as sg
import pyglet
from value import Value

class Gui():
    def __init__(self, scale: Union[float,int] = 1.0, line_width: Union[float,int] = 4, font: Dict[str,Union[int,str]] = {'name': 'Mont Heavy DEMO', 'size': 22, 'color': '#FFFFFF'}, transparency: Union[float,int] = 0.8):
        # try to import custom font
        try: pyglet.font.add_file(path.join(path.dirname(__file__), 'res', 'Mont-HeavyDEMO.otf'))
        except: pass
        # vars
        self.scale = abs(scale)
        self.line_width = line_width * self.scale
        self.font = {'name': font['name'].strip(), 'size': int(font['size']*self.scale), 'color': font['color'].strip()}
        self.transparency = max(min(1.0, transparency), 0.01)
        self.image_bg = Gui.transform(path.join(path.dirname(__file__),    'res', "background.png"), scale=self.scale)
        self.image_wheel = Gui.transform(path.join(path.dirname(__file__), 'res', "wheel.png"),      scale=self.scale)
        # gui layouts
        graph_dim = (int(524*self.scale), int(193*self.scale)), (int(1048*self.scale), int(386*self.scale))
        column_dim = (int(44*self.scale), int(198*self.scale)), (1, int((100+22)*self.scale))
        text_overlay_dim = (int(70*self.scale), int(178*self.scale))
        background_layout = [[sg.Image(self.image_bg, key='bg', enable_events=True)]]
        top_layout = [[ sg.Graph(graph_dim[0],     (0,-self.line_width), graph_dim[1],     key='graph',        pad=((round(76*self.scale), 0),(round(13*self.scale),0))),
                        sg.Graph(column_dim[0],    (0,0),                column_dim[1],    key='column1',      pad=((round(17*self.scale), 0),(0,0))),
                        sg.Graph(column_dim[0],    (0,0),                column_dim[1],    key='column2',      pad=((round(2.6*self.scale),0),(0,0))),
                        sg.Graph(column_dim[0],    (0,0),                column_dim[1],    key='column3',      pad=((round(1.4*self.scale),0),(0,0))),
                        sg.Graph(text_overlay_dim, (0,0),                text_overlay_dim, key='text_overlay', pad=((round(3*self.scale),  0),(round(28*self.scale),0))),
                        sg.Image(self.image_wheel, key='wheel')]]
        # gui windows
        sg.Window._move_all_windows = True
        self.foreground_window = sg.Window('Telemetry', top_layout,       no_titlebar=True,keep_on_top=True,grab_anywhere=True,resizable=False,alpha_channel=self.transparency,transparent_color=sg.theme_background_color(),margins=(0, 0),element_padding=(0,0))
        self.background_window = sg.Window('background',background_layout,no_titlebar=True,keep_on_top=True,grab_anywhere=True,resizable=False,alpha_channel=self.transparency,transparent_color=sg.theme_background_color(),margins=(0, 0),element_padding=(0,0))

    def transform(file_or_bytes: Union[str, bytes], rotate: float = None, resize: Tuple[int,int] = None, scale: float = None):
        """Transform an image (file path or bytes) and return the bytes"""
        if isinstance(file_or_bytes, str):
            img = PIL.Image.open(file_or_bytes)
        else:
            img = PIL.Image.open(BytesIO(file_or_bytes))

        cur_width, cur_height = img.size
        if resize:
            new_width, new_height = resize
            scale = min(new_height / cur_height, new_width / cur_width)
        if scale:
            img = img.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS)
        if rotate:
            img = img.rotate(rotate, resample=PIL.Image.BICUBIC)
        with BytesIO() as bio:
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()

    def darken_color(color: str):
        """Darken a color by 50% (str format should be '#RRGGBB' or 'RRGGBB')"""
        return '#'+hex(int((int(color[1:] if color.startswith('#') else color,16)+int('6f6f6f',16))/2))[2:]

    def show(self):
        """Show the gui windows"""
        self.background_window.finalize()
        self.foreground_window.finalize()
        self.foreground_window.move(self.background_window.current_location()[0], self.background_window.current_location()[1])

    def hide(self):
        """Hide the gui windows"""
        self.background_window.hide()
        self.foreground_window.hide()

    def update(self, values: Dict[str,Value], columns: Tuple[Value,Value,Value]):
        """Update the gui with new data"""
        window = self.foreground_window
        font = self.font

        # Erase every graph's canvas
        [e.erase() for e in [window['graph'], window['column1'], window['column2'], window['column3'], window['text_overlay']]]

        # Draw all buffered values on the main graph
        graph: sg.Graph = window['graph']
        for v in [v for v in values.values() if v.is_buffered]:
            scaling = {'x': graph.TopRight[0]/(v.buffer_size-1), 'y': (graph.TopRight[1]-self.line_width)/(sum(abs(x) for x in v.range))}
            lines = [(i * scaling['x'], (v.values[i] + abs(v.range[0])) * scaling['y']) for i in range(v.buffer_size)]
            graph.draw_lines(lines, color=v.color, width=abs(round(self.line_width)))

        # Draw passed columns Values on the ui columns
        for v, g in zip(columns, [window['column1'], window['column2'], window['column3']]):
            scaling = {'x': g.TopRight[0]/2, 'y': (g.TopRight[1]-round(22*self.scale))/(sum(abs(x) for x in v.range))}
            g.draw_text(int(v.value),      (scaling['x'], (g.TopRight[1] - 100*scaling['y'])/2 + 100*scaling['y']), color=font['color'] if int(v.value) >= v.range[1] else Gui.darken_color(font['color']), font=(font['name'], int(g.CanvasSize[0]/2.8)))
            g.draw_line((scaling['x'], 0), (scaling['x'], scaling['y'] * v.value),                                  color=v.color, width=round(30*self.scale))

        # Draw Gear, Unit and Speed on text_overlay graph
        graph: sg.Graph = window['text_overlay']
        graph.draw_text(values["Gear"].value,         (0, graph.TopRight[1]), color=font['color'], font=(font['name'],font['size']+int(8*self.scale)), text_location=sg.TEXT_LOCATION_TOP_LEFT)
        graph.draw_text(values['DisplayUnits'].value, (0, font['size']*1.5),  color=font['color'], font=(font['name'],int(font['size']/1.5 )),         text_location=sg.TEXT_LOCATION_BOTTOM_LEFT)
        graph.draw_text(values['Speed'].value,        (font['size']*2.5, 0),  color=font['color'], font=(font['name'],font['size']),                   text_location=sg.TEXT_LOCATION_BOTTOM_RIGHT)

        # Rotate wheel image
        image: sg.Image = window['wheel']
        image.update(Gui.transform(self.image_wheel, rotate=values['SteeringWheelAngle'].value))

        # Render new frame
        window.refresh()

        # Check for window events
        self.event_handler(self.background_window.read(timeout=0)[0])

    def event_handler(self, e):
        if e == 'bg':
            self.foreground_window.bring_to_front()
        if e in (sg.WIN_CLOSED, 'Exit'):
            quit()