# Drawing Binary Search Trees

Let's draw a binary search tree.  It should have the property that the left to right ordering of the nodes corresponds to the inorder traversal.

We should be able to highlight the path taken by a search.

```python {cmd output=html}
from ds_viz.gizehcanvas import Canvas
from ds_viz.vizbst import drawtree, drawpathtoroot
from ds2.orderedmapping import BSTMapping as BST

canvas = Canvas(height= 200)

T = BST()
for i in [7,2,1,4,3,6,11,12,9,10,8]:
    T[i] = None

drawpathtoroot(T, 2.5, canvas)
drawtree(T, canvas)

print(canvas.tohtml())
```

```python {cmd output="html"}
from ds_viz.element import *

class VizBST(Group):
    def __init__(self, n):
        super().__init__()
        self.left = VizBST(n.left) if n.left else Empty()
        self.right = VizBST(n.right) if n.right else Empty()
        self.root = Circle(22, label = str(n.key))
        self.root.halign('left', self.left, 'right')
        self.right.halign('left', self.root, 'right')
        for ch in [self.right, self.left]:
            ch.valign('top', self.root, 'bottom')
            # ch.position.y += 20 # Optionally stretch the tree vertically.
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

from ds2.orderedmapping import BSTMapping as BST
from ds_viz.canvas import Canvas

T = BST()
for i in [7,2,1,4,3,16,11,12,9,10,8]:
    T[i] = i

canvas = Canvas(600, 400)
mytree = VizBST(T._root)
mytree.position = Vector(100, 100)
mytree.draw(canvas)
mytree.left.drawanchors(canvas)

print(canvas.svgout())
```


## Some features to add

- **Draw an entire subtree as a triangle.**
