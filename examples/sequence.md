# Drawing Sequences

Given a sequence, we'd like to lay it out on a kind of tape.
This is most useful for arrays.

```python {cmd output=html}
from ds_viz.canvas import Canvas
from ds_viz.vizsequence import drawlist

canvas = Canvas()

L = [1,2,3, '\'hello\'', '\'goodbye\'', 234]
drawlist(L, (30, 30), canvas)

L.append('more!')
drawlist(L, (30, 80), canvas)
print(canvas.tohtml())
```

```python {cmd output=none}
from ds_viz.gizehcanvas import Canvas
from ds_viz.vizsequence import drawlist
canvas = Canvas(300, 60)

L = [1,2,3]
L.append(400)
drawlist(L, (10,10), canvas)
canvas.surface.write_to_png('list_example.png')
```

![A simple list](./list_example.png)
