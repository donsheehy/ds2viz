# Basic Elements

### Circle (no label)

```python {cmd output="html" hide}
from ds_viz.element import *
from ds_viz.canvas import Canvas

canvas = Canvas(600,100)
circle = Circle(40)
circle.position = (5, 5)
circle.draw(canvas)
circle.drawbox(canvas)
print(canvas.svgout())
```

### Text

```python {cmd output="html" hide}
from ds_viz.element import *
from ds_viz.canvas import Canvas

canvas = Canvas(600,100)
text = Text('Hello, world!')
text.position = (30, 5)
text.draw(canvas)
text.drawbox(canvas)
print(canvas.svgout())
```

### Circle (with label)

```python {cmd output="html" hide}
from ds_viz.element import *
from ds_viz.canvas import Canvas

canvas = Canvas(600, 100)
circle = Circle(20, 'X')
circle.position = (30, 5)
circle.draw(canvas)
circle.drawbox(canvas)
print(canvas.svgout())
```

### Boxed Text

```python {cmd output="html" hide}
from ds_viz.element import *
from ds_viz.canvas import Canvas

canvas = Canvas(600, 100)
box = Boxed(Text('hi!'))
box.position = (30, 5)
box.draw(canvas)
box.drawbox(canvas)
print(canvas.svgout())
```

### Lines

```python {cmd output="html" hide}
from ds_viz.element import *
from ds_viz.canvas import Canvas

canvas = Canvas(600, 100)
line = Line((20,20), (150, 40))
line.draw(canvas)
line.drawbox(canvas)
print(canvas.svgout())
```


### SCurve

```python {cmd output="html" hide}
from ds_viz.element import SCurve
from ds_viz.canvas import Canvas

c = SCurve((20, 20), (200, 90))
canvas = Canvas(600, 130)

c.draw(canvas)
c.drawbox(canvas)
print(canvas.svgout())
```


### Aligned Groups

```python {cmd output="html" hide}
from ds_viz.element import *
from ds_viz.canvas import Canvas

canvas = Canvas(600, 200)
vg = VGroup([Boxed(Text(txt)) for txt in ['a', 'bb', 'cccc']])
vg.position = (110, 10)
vg.draw(canvas)

stack = VGroup([Text(str(i)) for i in range(5)])
hg = HGroup([Boxed(Text('xoxo')), stack])
hg.position = (250, 10)
hg.draw(canvas)

vg.drawbox(canvas)
print(canvas.svgout())
```

# Data Structures

### VizList

```python {cmd output="html" hide}
from ds_viz.datastructures import VizList
from ds_viz.canvas import Canvas


canvas = Canvas(600, 100)
L = VizList([1,2,3,'abc'])
L.position = (10,10)
L.draw(canvas)

print(canvas.svgout())
```

### VizNamedReference

```python {cmd output="html" hide}
from ds_viz.element import Line
from ds_viz.datastructures import VizNamedReference
from ds_viz.canvas import Canvas

canvas = Canvas(600, 100)
ref = VizNamedReference('objectname')
ref.position = (10,10)
ref.draw(canvas)
ref.drawbox(canvas)

line = Line(ref.a('source'), (300,2))
line.draw(canvas)
print(canvas.svgout())
```

### VizTree

```python {cmd output="html" hide}
from ds2.tree import Tree
from ds_viz.datastructures import VizTree
from ds_viz.canvas import Canvas

T = Tree([7, [4, [2, [1], [1], [1]], [5]], [1], [13, ['x'], ['y']]])
# T = Tree([2, [1, [0]], [1], [1]])

canvas = Canvas(600, 250)
mytree = VizTree(T)
mytree.position = (40, 40)
# for c in mytree.children:
#     c.drawbox(canvas)

mytree.draw(canvas)
mytree.drawbox(canvas)
# mytree.root.drawbox(canvas)

print(canvas.svgout())
print(canvas.pngout())
```



### VizBST

```python {cmd output="html" hide}
from ds2.orderedmapping import BSTMapping as BST
from ds_viz.datastructures import VizBST
from ds_viz.canvas import Canvas

T = BST()
for i in [7,2,1,4,3,6,11,9,10,8]:
    T[i] = i

canvas = Canvas(600, 400)
mytree = VizBST(T._root, (20, 10))
mytree.draw(canvas)
# mytree.left.drawanchors(canvas)
mytree.drawbox(canvas)

print(canvas.svgout())
print(canvas.pngout())
```
