class Vector:
    def __init__(self, x = (0,0), y = None):
        if y is None:
            self.x, self.y = x
        else:
            self.x = x
            self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def midpoint(self, other):
        return Vector((self.x + other.x) / 2, (self.y + other.y) /2)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError

    def __len__(self):
        return 2
