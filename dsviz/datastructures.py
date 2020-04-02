from dsviz.element import *

class VizNamedReference(HGroup):
    def __init__(self, name):
        txt = Boxed(Text(name))
        bpt = Boxed(Circle(5, style = '_point'))
        bpt.setwidth(25)
        super().__init__([txt, bpt])
        self.setanchor('source', self.elements[1].a('center'))

class VizList(HGroup):
    def __init__(self, L):
        super().__init__([Boxed(Text(str(item))) for item in L])

class VizTree(Group):
    def __init__(self, T):
        super().__init__()
        # Create the pieces
        children = [VizTree(c) for c in T.children]
        root = Circle(18, label = str(T.data))

        # Center the root.
        width = max(sum(c.width for c in children), root.width)
        root.halign('center', (width/2, 0))
        rootcenter = root.a('center')
        self.setanchor('root', rootcenter)

        # Align the subtrees and draw the lines.
        for i, child in enumerate(children):
            if i != 0:
                child.align('left', children[i-1].a('right'))
            child.valign('top', root.a('bottom'))
            self.addelement(Line(rootcenter, child.a('root')))
            self.addelement(child)
        self.addelement(root)

        # It seems to be handy to provide this kind of tree access.
        self.children = children
        self.root = root


class VizBST(Group):
    def __init__(self, n, position = (0,0)):
        super().__init__()
        self.position = position
        self.lefttree = VizBST(n.left) if n.left else Empty()
        self.righttree = VizBST(n.right) if n.right else Empty()
        self.root = Circle(22, label = str(n.key))
        self.root.halign('left', self.lefttree.a('right'))
        self.righttree.halign('left', self.root.a('right'))
        for ch in [self.righttree, self.lefttree]:
            ch.valign('top', self.root.a('bottom'))
        rootcenter = self.root.a('center')
        self.setanchor('root', rootcenter)
        for child in [self.lefttree, self.righttree]:
            if child:
                self.addelement(Line(rootcenter, child.a('root')))
                self.addelement(child)
        self.addelement(self.root)
