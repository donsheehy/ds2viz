from ds2viz.primitives import *
from ds2viz.imageengine import ImageEngine, styledefaults

def rgbtohex(rgb):
    if rgb is None:
        return 'none'
    colors = [hex(int(x * 255 + 256))[-2:] for x in rgb]
    return "#" + "".join(colors[:3])

class TikzEngine(ImageEngine):
    def __init__(self, canvas, filename = None):
        self.tikz = ""
        super().__init__(canvas, filename)

    def props(self, props, *required_props):
        output = {}
        for prop in required_props:
            if prop not in props:
                props[prop] = styledefaults[prop]
            if prop in ['stroke', 'fill']:
                output[prop] = rgbtohex(props[prop])
            else:
                output[prop] = props[prop]
        return output

    def draw_circle(self, circle):
        props = self.props(circle.props, 'stroke', 'fill', 'stroke_width')
        center = list(circle.center)
        radius = circle.radius
        tcircle = f'\\draw {center} circle {radius};\n'
        self.tikz.append(tcircle)

    def draw_polyline(self, polyline):
        props = self.props(polyline.props, 'stroke', 'fill', 'stroke_width')
        points = list(list(p) for p in polyline.points)
        tpolyline = '\\draw' + ' -- '.join(points) + ';\n'
        self.tikz.append(tpolyline)

    def draw_polygon(self, polygon):
        props = self.props(polygon.props, 'stroke', 'fill', 'stroke_width')
        fill = props['fill']
        points = list(list(p) for p in polygon.points)
        tpolyline = '\\filldraw[{fill}]' + ' -- '.join(points) + ';\n'
        self.tikz.append(tpolyline)

    def draw_bezier(self, bezier):
        props = self.props(bezier.props, 'stroke', 'fill', 'stroke_width')
        # points = list(tuple(p) for p in bezier.points)
        points = ['('+x+','+y+')' for x,y in bezier.points
        controls = points[1:-2]
        first = points[0]
        last = points[-1]
        
        tbezier = '\\draw {first} .. controls' + ' and '.join(controls) + '.. {str(last)};\n'
        self.tikz.append(tbezier)

    def draw_text(self, text):
        props = self.props(text.props,
                           'stroke',
                           'fill',
                           'font_size',
                           'font_family',
                           'font_weight',
                           # 'dominant_baseline',
                           # 'text_anchor',
                           )
        string = text.text
        print(string)
        ttext = f'\node[draw] at {text.position} {text.text};\n'
        selk.tikz.append(ttext)

    def __str__(self):
        return self.tikz
