```python {cmd output="html"}
from ds_viz.element import *
from ds_viz.canvas import Canvas
from ds_viz.vector import Vector

atext = Text('top')
a = Boxed(atext)
b = Boxed(Text('middle'))
c = Boxed(Text('bottom'))
d = Boxed(Text('other!!!!'))
# g = VGroup([HGroup([a,b]), c])
e = VGroup([a,b,c])
f = HGroup([e, d])
g = VGroup([Boxed(Text(str(i))) for i in range(4)] + [f])
# g = VGroup([a])
atext.align('center', a, 'center')

# g = VGroup([a,b,c])

canvas = Canvas(600,400)
g.position = Vector(200,100)
g.draw(canvas)
# atext.drawanchors(canvas)

line = Line(Vector(40, 50), Vector(130, 200))
# line.position = Vector(100, 100)
line.draw(canvas)
line.drawanchors(canvas)

print(canvas.svgout())
```
