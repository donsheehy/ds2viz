from collections import namedtuple

# The Drawing Primitives
DP_Circle = namedtuple('Circle', ['center', 'radius', 'props'])
DP_Line = namedtuple('Line', ['start', 'end', 'props'])
DP_Polygon = namedtuple('Polygon', ['points', 'props'])
DP_Text = namedtuple('Text', ['text', 'position', 'props'])
