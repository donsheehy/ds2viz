from collections import namedtuple


# The Drawing Primitives
Circle = namedtuple('Circle', ['center', 'radius', 'props'])
Line = namedtuple('Line', ['start', 'end', 'props'])
Polygon = namedtuple('Polygon', ['points', 'props'])
Text = namedtuple('Text', ['text', 'position', 'props'])

if False:

    styledefaults = {'radius': 3,
                     'fill': (1,1,1),
                     'stroke': (0,0,0),
                     'stroke_width' : 0,
                     'font_size': '24pt',
                     'font_family' : 'monospace',
                     'font_weight': 'normal',
                    }



    def rgbtohex(rgb):
        colors = [hex(int(x * 255 + 256))[-2:] for x in rgb]
        return "#" + "".join(colors[:3])

    class Primitive:
        def __init__(self, properties = (), **kwargs):
            self.props = dict(styledefaults)
            self.props.update(kwargs)
            self.props = {k: self.props[k] for k in self.properties}

        def svg(self):
            for p in ['fill', 'stroke']:
                if p in self.props:
                    self.props[p] = rgbtohex(self.props[p])

    class Point(Primitive):
        properties = ['radius', 'stroke', 'fill', 'stroke_width']

        def __init__(self, point, **kwargs):
            super().__init__(**kwargs)
            self.props['center'] = point

        def svg(self, engine):
            super().svg()
            engine.draw_circle(**self.props)

    class Line(Primitive):
        properties = ['stroke', 'stroke_width']

        def __init__(self, a, b, **kwargs):
            super().__init__(**kwargs)

            self.a = a
            self.b = b

        def svg(self, engine):
            super().svg()
            engine.draw_line(list(self.a), list(self.b), **self.props)

    class Circle(Primitive):
        properties = ['radius', 'stroke', 'fill', 'stroke_width']

        def __init__(self, c, r, **kwargs):
            super().__init__(**kwargs)
            self.props['center'] = c
            self.props['radius'] = r

        def svg(self, engine):
            super().svg()
            engine.draw_circle(**self.props)

    class Rectangle(Primitive):
        properties = ['stroke', 'stroke_width', 'fill']

        def __init__(self, topleft, width, height, **kwargs):
            super().__init__(**kwargs)
            self.topleft = topleft
            self.width = width
            self.height = height

        def svg(self, engine):
            super().svg()
            engine.draw_rect(self.topleft,
                             self.width,
                             self.height,
                             **self.props
                            )

    class Text(Primitive):
        properties = ['stroke',
                      'fill',
                      'font_size',
                      'font_family',
                      'font_weight'
                      ]

        def __init__(self, text, location, **kwargs):
            super().__init__(**kwargs)
            self.text = text
            self.center = location

        def svg(self, engine):
            super().svg()
            engine.draw_text_center(self.text, self.center, **self.props)
