from ds_viz.vector import Vector
# from ds_viz.style import bigpoint, blackline, jeffeline
# from ds_viz.default_styles import default_styles
from collections import defaultdict

class Element:
    def __init__(self):
        self._position = Vector(0,0)
        self.width = 0
        self.height = 0
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

    def globalposition(self):
        if self.parent is None:
            return self.position
        else:
            return self.position + self.parent.globalposition()

    def addanchor(self, label, v):
        self.anchor[label] = Vector(v)

    def _align(self, anchor, other, otheranchor):
        if self.parent is None:
            parentposition = Vector(0,0)
        else:
            parentposition = self.parent.globalposition()
        otherposition = other.globalposition() + other.anchor[otheranchor]
        return otherposition - self.anchor[anchor] - parentposition

    def align(self, anchor, other, otheranchor):
        self.position = self._align(anchor, other, otheranchor)

    def valign(self, anchor, other, otheranchor):
        self.position.y = self._align(anchor, other, otheranchor).y

    def halign(self, anchor, other, otheranchor):
        self.position.x = self._align(anchor, other, otheranchor).x

    def setboxanchors(self):
        self.addanchor('left', (0, self.height/2))
        self.addanchor('right', (self.width, self.height/2))
        self.addanchor('top', (self.width/2, 0))
        self.addanchor('bottom', (self.width/2, self.height))
        self.addanchor('center', (self.width/2, self.height/2))
        self.addanchor('topleft', (0, 0))

    def setwidth(self, width):
        self.width = width
        self.setboxanchors()

    def setheight(self, height):
        self.height = height
        self.setboxanchors()

    def drawanchors(self, canvas):
        position = self.globalposition()
        for a in self.anchor.values():
            canvas.point(position + a)

    def a(self, element, anchor):
        parent = element
        position = element.anchor[anchor]
        while parent is not self and parent is not None:
            # if parent is None:
            #     raise TypeError("asking for None anchor!", anchor, parent, self)
            position += parent.position
            parent = parent.parent
        return position

class Text(Element):
    def __init__(self, text, style = '_text'):
        super().__init__()
        self.style = style
        self.text = text
        # These really will depend on the fontfamily and size.
        self.width = 20 * len(text)
        self.height = 30
        self.setboxanchors()

    def draw(self, canvas):
        pos = self.globalposition() + self.anchor['center']
        canvas.text(self.text, pos, self.style)

class Empty(Element):
    def __init__(self):
        super().__init__()
        self.setboxanchors()

    def draw(self, canvas):
        pass

    def __bool__(self):
        return False

class Boxed(Element):
    def __init__(self, element, style = '_rectangle'):
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
        self.width = element.width + 2 * hshift
        self.height = element.height + 2 * vshift
        self.setboxanchors()
        element.align('center', self, 'center')

    def draw(self, canvas):
        topleft = self.globalposition() + self.anchor['topleft'] + Vector(self.margin, self.margin)
        canvas.rectangle(topleft,
                             self.width,
                             self.height,
                             self.style
                             )
        self.element.draw(canvas)

class Circle(Element):
    def __init__(self, radius = 20, label = None, style = '_circle'):
        super().__init__()
        self.width = self.height = 2 * radius
        self.setboxanchors()
        self.style = style
        if label is not None:
            self.label = Text(str(label))
            self.label.parent = self
            self.label.align('center', self, 'center')
        else:
            self.label= None
        self.radius = radius

    def draw(self, canvas):
        center = self.globalposition() + self.anchor['center']
        canvas.circle(center, self.radius, self.style)
        if self.label is not None:
            self.label.draw(canvas)

class Line(Element):
    def __init__(self, a, b, style = '_line'):
        super().__init__()
        self.style = style
        self.anchor['a'] = a
        self.anchor['b'] = b

    def draw(self, canvas):
        pos = self.globalposition()
        a = pos + self.anchor['a']
        b = pos + self.anchor['b']
        canvas.line(a, b, self.style)

class Group(Element):
    def __init__(self, elements = ()):
        super().__init__()
        self.elements = []
        for e in elements:
            self.addelement(e)

    def alignelements(self, anchor1, anchor2):
        for i in range(1, len(self.elements)):
            self.elements[i].align(anchor1, self.elements[i-1], anchor2)

    def draw(self, canvas):
        for e in self.elements:
            e.draw(canvas)

    def addelement(self, element):
        self.elements.append(element)
        element.parent = self

    def __len__(self):
        return len(self.elements)

class HGroup(Group):
    def __init__(self, elements):
        super().__init__(elements)
        self.width = sum(e.width for e in elements)
        self.height = max(e.height for e in elements)
        self.setboxanchors()
        for e in elements:
            e.setheight(self.height)
        self.alignelements('left', 'right')

class VGroup(Group):
    def __init__(self, elements):
        super().__init__(elements)
        self.width = max(e.width for e in elements)
        self.height = sum(e.height for e in elements)
        self.setboxanchors()
        for e in elements:
            e.setwidth(self.width)
        self.alignelements('top', 'bottom')
