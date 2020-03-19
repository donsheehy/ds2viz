import gizeh
from ds_viz.primitives import *

styledefaults = {'radius': 3,
                 'fill': (1,1,1),
                 'stroke': (0,0,0),
                 'stroke_width' : 0,
                 'font_size': 24,
                 'font_family' : 'monospace',
                 'font_weight': 'normal',
                 'text_anchor' : 'middle',
                 'dominant_baseline' : 'central',
                }

stylerenames = {'font_weight': 'fontweight',
             'font_size' : 'fontsize',
             'font_family' : 'fontfamily',
}

class GizehEngine:
    def __init__(self, canvas, filename = None):
        for p in canvas.primitives():
            if isinstance(p, DP_Circle):
                self.draw_circle(p)
            elif isinstance(p, DP_Line):
                self.draw_line(p)
            elif isinstance(p, DP_Polygon):
                self.draw_polygon(p)
            elif isinstance(p, DP_Text):
                self.draw_text(p)
            else:
                raise TypeError('The drawing primitive has an unknown type.')

    def props(self, props, *required_props):
        output = {}
        for prop in required_props:
            if prop not in props:
                props[prop] = styledefaults[prop]
            # if prop in ['stroke', 'fill']:
            #     output[prop] = rgbtohex(props[prop])
            if prop in stylerenames:
                output[stylerenames[prop]] = props[prop]
            else:
                output[prop] = props[prop]
        return output


    def draw_circle(self, circle):
        props = self.props(circle.props, 'stroke', 'fill', 'stroke_width')
        center = list(circle.center)
        radius = circle.radius
        gcircle = gizeh.circle(r = radius, xy = center, **props)
        gcircle.draw(self.surface)

    def draw_line(self, line):
        props = self.props(line.props, 'stroke', 'stroke_width')
        start = list(line.start)
        end = list(line.end)
        gline = gizeh.polyline(points=[start, end], **props)
        gline.draw(self.surface)

    def draw_polygon(self, polygon):
        props = self.props(polygon.props, 'stroke', 'fill', 'stroke_width')
        points = list(list(p) for p in polygon.points)
        gpolygon = gizeh.polyline(points = points, close_path = True, **props)
        gpolygon.draw(self.surface)

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
        gtext = gizeh.text(text.text, xy = text.position, **props)
        gtext.draw(self.surface)

    def __str__(self):
        return self.surface.get_html_embed_code()


class PNGEngine(GizehEngine):
    def __init__(self, canvas, filename = None):
        self.filename = filename
        self.surface = gizeh.Surface(width=canvas.width,
                                     height=canvas.height)
        GizehEngine.__init__(self, canvas)

    def pngsave(self):
        if self.filename is not None:
            self.surface.write_to_png(self.filename)
        else:
            raise RuntimeError("No filename given for canvas.")

class PDFEngine(GizehEngine):
    def __init__(self, canvas, filename):
        self.surface = gizeh.PDFSurface(filename,
                                        width=canvas.width,
                                        height=canvas.height)
        GizehEngine.__init__(self, canvas)

    def pdfsave(self):
        self.surface.finish()
        self.surface.flush()
