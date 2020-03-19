from ds_viz.element import *

class VizList(Group):
    def __init__(self, L):
        super().__init__()
        self.L = HGroup([Boxed(Text(str(item))) for item in L])
        self.width = self.L.width
        self.height = self.L.height
        self.setboxanchors()
        self.addelement(self.L)


class VizBST(Group):
    def __init__(self, n, position = (0,0)):
        super().__init__()
        self.position = position
        self.left = VizBST(n.left) if n.left else Empty()
        self.right = VizBST(n.right) if n.right else Empty()
        self.root = Circle(22, label = str(n.key))
        self.root.halign('left', self.left, 'right')
        self.right.halign('left', self.root, 'right')
        for ch in [self.right, self.left]:
            ch.valign('top', self.root, 'bottom')
            # ch.position.y += 20 # Optionally stretch the tree vertically.
            # This should use the padding in the style.
        root = self.root.a('center')
        self.addanchor('root', root)
        for child in [self.left, self.right]:
            if child:
                childroot = child.a('root')
                self.addelement(Line(root, childroot))
                self.addelement(child)
        self.addelement(self.root)

        # The following three lines should be one function call.
        self.width = self.left.width + self.right.width + self.root.width
        self.height = max(self.left.height, self.right.height) + self.root.height
        self.setboxanchors()
