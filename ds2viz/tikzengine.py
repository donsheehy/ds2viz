from ds2viz.primitives import *
from ds2viz.imageengine import ImageEngine, styledefaults

scale = .02 

def rgbtotikz(rgb):
    if rgb is None:
        return 'none'
    else:
        red,green,blue = rgb
#        if red == 1 and green == 1 and blue == 1:
#            return 'white'
#        else:
        return f'{{rgb,1:red,{red};green,{green};blue,{blue}}}'

def tikzpt(pt):
        x,y = pt
        return f'({x*scale:.2f}, {-y*scale:.2f})'

def tikzprops(props):
    tpropslist = []
    if 'fill' in props.keys():
        tpropslist.append(f'fill={props["fill"]}')
    if 'stroke' in props.keys():
        tpropslist.append(f'stroke={props["stroke"]}')
    if 'stroke_width' in props.keys():
        tpropslist.append(f'line width={props["stroke_width"]/2:.2f}')
    return ", ".join(tpropslist)

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
                output[prop] = rgbtotikz(props[prop])
            else:
                output[prop] = props[prop]
        return output

    def draw_circle(self, circle):
        props = self.props(circle.props, 'stroke', 'fill', 'stroke_width')
        tprops = tikzprops(props)
        center = tikzpt(circle.center)
        radius = circle.radius * scale
        tcircle = f'\\draw[{tprops}] {center} circle ({radius:.2f});\n'
        self.tikz += tcircle

    def draw_polyline(self, polyline):
        props = self.props(polyline.props, 'stroke', 'fill', 'stroke_width')
        tprops = tikzprops(props)
        points = list(tikzpt(p) for p in polyline.points)
        tpolyline = f'\\draw[{tprops}] ' + ' -- '.join(points) + ';\n'
        self.tikz += tpolyline

    def draw_polygon(self, polygon):
        props = self.props(polygon.props, 'stroke', 'fill', 'stroke_width')
        tprops = tikzprops(props)
        points = list(tikzpt(p) for p in polygon.points)
        points.append(points[0])
        tpolyline = f'\\draw[{tprops}]' + ' -- '.join(points) + ';\n'
        self.tikz +=  tpolyline

    def draw_bezier(self, bezier):
        props = self.props(bezier.props, 'stroke', 'fill', 'stroke_width')
        tprops = tikzprops(props)
        points = [tikzpt(p) for p in bezier.points]
        controls = points[1:-1]
        first = points[0]
        last = points[-1]
        tbezier = f'\\draw[{tprops}] {first} .. controls ' + ' and '.join(controls) + f' .. {str(last)};\n'
        self.tikz += tbezier

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
        tprops = tikzprops(props)
        string = text.text
        position = tikzpt(text.position)
        ttext = f'\\draw[{tprops}] {position} node {{{text.text}}};\n'
        self.tikz += ttext

    def __str__(self):
        return '\\begin{tikzpicture}\n' + self.tikz + '\\end{tikzpicture}'
