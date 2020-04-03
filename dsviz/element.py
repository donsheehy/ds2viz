from dsviz.vector import Vector
from collections import defaultdict, namedtuple

Box = namedtuple('Box', ['top', 'right', 'bottom', 'left'])

class Element:
    def __init__(self):
        self._position = Vector(0,0)
        self._box = Box(0, 0, 0, 0)
        self.anchor = defaultdict(Vector)
        self.tags = set()
        self.style = []
        self.parent = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, x, y = None):
        self._position = Vector(x, y)

    @property
    def _top(self):
        return self._box.top

    @property
    def _right(self):
        return self._box.right

    @property
    def _bottom(self):
        return self._box.bottom

    @property
    def _left(self):
        return self._box.left

    @property
    def top(self):
        return self._top + self.position.y

    @property
    def right(self):
        return self._right + self.position.x

    @property
    def bottom(self):
        return self._bottom + self.position.y

    @property
    def left(self):
        return self._left + self.position.x

    @property
    def width(self):
        return self._right - self._left

    @property
    def height(self):
        return self._bottom - self._top

    def globalposition(self):
        if self.parent is None:
            return self.position
        else:
            return self.position + self.parent.globalposition()

    def setanchor(self, label, v):
        self.anchor[label] = Vector(v)

    def _align(self, anchor, point):
        return Vector(point) - self._a(anchor)

    def align(self, anchor, point):
        self.position = self._align(anchor, point)

    def valign(self, anchor, point):
        self.position.y = self._align(anchor, point).y

    def halign(self, anchor, point):
        self.position.x = self._align(anchor, point).x

    def setwidth(self, width):
        t, r, b, l = self._box
        dwidth = width - self.width
        self._box = Box(t, r + dwidth, b, l)

    def setheight(self, height):
        t, r, b, l = self._box
        dheight = height - self.height
        self._box = Box(t, r, b + dheight, l)

    def drawbox(self, canvas):
        position = self.globalposition()
        anchors = ['top', 'right', 'bottom', 'left', 'topleft', 'topright',
                   'bottomleft', 'bottomright', 'center']
        lines = [('topleft', 'topright'),
                 ('topright', 'bottomright'),
                 ('bottomright', 'bottomleft'),
                 ('bottomleft', 'topleft')]
        for start, end in lines:
            canvas.line(position + self._a(start), position + self._a(end))
        for anchor in anchors:
            canvas.point(position + self._a(anchor))

    def _a(self, anchor):
        verticalcenter = (self._top + self._bottom) / 2
        horizontalcenter = (self._left + self._right) / 2
        self.setanchor('top', (horizontalcenter, self._top))
        self.setanchor('topright', (self._right, self._top))
        self.setanchor('right',(self._right, verticalcenter))
        self.setanchor('bottomright', (self._right, self._bottom))
        self.setanchor('bottom', (horizontalcenter, self._bottom))
        self.setanchor('bottomleft', (self._left, self._bottom))
        self.setanchor('left', (self._left, verticalcenter))
        self.setanchor('topleft', (self._left, self._top))
        self.setanchor('center', (horizontalcenter, verticalcenter))
        return self.anchor[anchor]

    def a(self, anchor):
        return self.position + self._a(anchor)

class Text(Element):
    def __init__(self, text, style = '_text'):
        super().__init__()
        self.style = style
        self.text = text
        # The size will depend on the fontfamily and size.
        self._box = Box(0, 17 * len(text), 30, 0)

    def draw(self, canvas):
        pos = self.globalposition() + self._a('center')
        canvas.text(self.text, pos, self.style)

class Empty(Element):
    def __init__(self):
        super().__init__()

    def draw(self, canvas):
        pass

    def __bool__(self):
        return False

class Boxed(Element):
    def __init__(self, element, style = '_polygon'):
        super().__init__()
        self.element = element
        self.style = style
        element.parent = self
        self.padding = 5
        self.margin = 0
        # If the margin is not zero, we also have to change how to draw it.
        assert(self.margin == 0)
        vshift = self.margin + self.padding
        hshift = self.margin + self.padding
        self._box = Box(0,
                        element.width + 2 * hshift,
                        element.height + 2 * vshift,
                        0)
        self.alignelement()

    def draw(self, canvas):
        topleft = self.globalposition() + self._a('topleft') + Vector(self.margin, self.margin)
        canvas.rectangle(topleft,
                             self.width,
                             self.height,
                             self.style
                             )
        self.element.draw(canvas)

    def alignelement(self):
        self.element.align('center', self._a('center'))

    def setwidth(self, width):
        super().setwidth(width)
        self.alignelement()

    def setheight(self, width):
        super().setheight(width)
        self.alignelement()

class Circle(Element):
    def __init__(self, radius = 20, label = None, style = '_circle'):
        super().__init__()
        margin = 5
        size = 2 * (radius + margin)
        self._box = Box(0, size, size, 0)
        self.style = style
        if label is not None:
            self.label = Text(str(label))
            self.label.parent = self
            self.label.align('center', self._a('center'))
        else:
            self.label= None
        self.radius = radius

    def draw(self, canvas):
        center = self.globalposition() + self._a('center')
        canvas.circle(center, self.radius, self.style)
        if self.label is not None:
            self.label.draw(canvas)

class Line(Element):
    def __init__(self, a, b, style = '_path'):
        super().__init__()
        self.style = style
        start = Vector(a)
        end = Vector(b)
        self._box = Box(min(start.y, end.y),
                        max(start.x, end.x),
                        max(start.y, end.y),
                        min(start.x, end.x)
                       )
        self.setanchor('start', start)
        self.setanchor('end', end)

    def draw(self, canvas):
        pos = self.globalposition()
        a = pos + self._a('start')
        b = pos + self._a('end')
        canvas.line(a, b, self.style)

class SCurve(Line):
    def draw(self, canvas):
        right = Vector(60, 0)
        pos = self.globalposition()
        a = pos + self._a('start')
        b = pos + self._a('end')
        u = a + right
        v = b - right
        canvas.bezier([a, u, v, b])

class Group(Element):
    def __init__(self, elements = ()):
        super().__init__()
        self.elements = []
        for e in elements:
            self.addelement(e)

    def alignelements(self, anchor1, anchor2):
        for i in range(1, len(self.elements)):
            self.elements[i].align(anchor1, self.elements[i-1].a(anchor2))

    def draw(self, canvas):
        for e in self.elements:
            e.draw(canvas)

    def addelement(self, element):
        self.elements.append(element)
        element.parent = self

    @property
    def _top(self):
        return min(e.top for e in self)

    @property
    def _right(self):
        return max(e.right for e in self)

    @property
    def _bottom(self):
        return max(e.bottom for e in self)

    @property
    def _left(self):
        return min(e.left for e in self)

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        return iter(self.elements)

class HGroup(Group):
    def __init__(self, elements):
        super().__init__(elements)
        for e in self.elements:
            e.setheight(self.height)
        self.alignelements('left', 'right')

class VGroup(Group):
    def __init__(self, elements):
        super().__init__(elements)
        for e in self.elements:
            e.setwidth(self.width)
        self.alignelements('top', 'bottom')
