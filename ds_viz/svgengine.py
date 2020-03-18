import svgwrite
from ds_viz.primitives import *

styledefaults = {'radius': 3,
                 'fill': (1,1,1),
                 'stroke': (0,0,0),
                 'stroke_width' : 0,
                 'font_size': '24pt',
                 'font_family' : 'monospace',
                 'font_weight': 'normal',
                 'text_anchor' : 'middle',
                 'dominant_baseline' : 'central',
                }

def rgbtohex(rgb):
    colors = [hex(int(x * 255 + 256))[-2:] for x in rgb]
    return "#" + "".join(colors[:3])

class SVGEngine:
    def __init__(self, canvas, filename = None):
        size = (canvas.width, canvas.height)
        self.svg_doc = svgwrite.Drawing(None, size)
        for p in canvas.primitives():
            if isinstance(p, Circle):
                self.draw_circle(p)
            elif isinstance(p, Line):
                self.draw_line(p)
            elif isinstance(p, Polygon):
                self.draw_polygon(p)
            elif isinstance(p, Text):
                self.draw_text(p)
            else:
                raise TypeError('The drawing primitive has an unknown type.')

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
        svgcircle = self.svg_doc.circle(center, r = radius, **props)
        self.svg_doc.add(svgcircle)

    def draw_line(self, line):
        props = self.props(line.props, 'stroke', 'stroke_width')
        svgline = self.svg_doc.line(line.start, line.end, **props)
        self.svg_doc.add(svgline)

    def draw_polygon(self, polygon):
        props = self.props(polygon.props, 'stroke', 'stroke_width', 'fill')
        points = polygon.points
        svgpolygon = self.svg_doc.path(**props)
        svgpolygon.push("M%f %f" % tuple(points[0]))
        for i, p in enumerate(points):
            svgpolygon.push("L%f %f" % tuple(p))
        svgpolygon.push("L%f %f" % tuple(points[0]))
        self.svg_doc.add(svgpolygon)

    def draw_text(self, text):
        props = self.props(text.props,
                           'stroke',
                           'fill',
                           'font_size',
                           'font_family',
                           'font_weight',
                           'dominant_baseline',
                           'text_anchor',
                           )
        svgtext = self.svg_doc.text(text.text, text.position, **props)
        self.svg_doc.add(svgtext)

    def __str__(self):
        return self.svg_doc.tostring()
