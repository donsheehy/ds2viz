```python {cmd output="html"}
from ds_viz.canvas import Canvas
from ds_viz.svgengine import SVGEngine
from ds_viz.default_styles import default_styles


c = Canvas(600, 480, default_styles)
c.point((30,30), 'ps')
c.point((50,30), 'doublepoint')
c.circle((100,100), 40, 'stark')
c.rectangle((250,20), 100, 200)
c.line((100,200), (300, 150))
c.text('hello', (140, 300))
print(c.svgout())
# print(SVGEngine(c))
```
