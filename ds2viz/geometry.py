""" Visualization Utilities

This module is used to describe the geometry of a drawing.  Currently
this module contains a single class VizPoint and a series of utility functions
used to describe a convex hull.
"""

from ds2viz.element import Circle

class VizPoint(Circle):
  """
  This class is used to describe a visible point drawn on a diagram using a ds2viz circle primitive.
  This class inherits Circle from the super class ds2viz.element
  """
  def __init__(self, x, y, radius=1):
    """
    Parameters
    ----------
    x: float
      The x coordinate of this point.
    y: float
      The y coordinate of this point.
    radius: float
      The radius of this point. (default 1)
    """
    super().__init__(radius)
    self.x, self.y = x, y
    self.align('center', (x, y))

  def dist(self, other):
    """
    Calculates the distance between this point and the parameterized 
    other point.
    Parameters
    ----------
    other: VizPoint
      The point to calculate the distance too.
    Return
    ----------
    The distance from this point to other point.
    """
    return sum((a - b) ** 2 for a, b in zip(self, other)) ** (0.5)

  def __iter__(self):
    yield self.x
    yield self.y

  def __eq__(self, other):
    return list(self) == list(other)

  def __hash__(self):
    return hash((self.x, self.y))

  def __str__(self):
    return f"({self.x}, {self.y})"

#######################################################################################
# UTILITIES
#######################################################################################

def convexhull(P):
  """ Returns the convex hull of P as a list of points

  The first point is repeated as the last point.
  This makes it easier to draw.
  """
  P = list(P)
  return lowerhull(P)[:-1] + upperhull(P)

def ccw(a,b,c):
  return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x) > 0

def lowerhull(P):
  P.sort(key = lambda p: (p.x, p.y))
  return grahamscan(P)

def upperhull(P):
  P.sort(key = lambda p: (-p.x, -p.y))
  return grahamscan(P)

def grahamscan(P):
  stack = []
  for p in P:
    while len(stack) >= 2 and not ccw(stack[-2], stack[-1], p):
      stack.pop()
    stack.append(p)
  return stack