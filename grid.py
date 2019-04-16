from itertools import zip_longest

class Grid:
    def __init__(self, visit, start=(0,0)):
        self.grid = {}
        self.loc = start
        self._visit = visit
        self.grid[start] = self.visit()

    def visit(self):
        return self._visit(self.grid, self.loc)

    def setPos(self, loc):
        self.loc = loc
        self.grid[loc] = self.visit()

    def move(self, dloc):
        oldLoc = self.loc
        self.loc = tuple(sum(x) for x in zip_longest(self.loc, dloc, fillvalue=0))
        self.grid[self.loc] = self.visit()

    def up(self):
        self.move((1,))
    def down(self):
        self.move((-1,))
    def left(self):
        self.move((0,-1))
    def right(self):
        self.move((0,1))
    def forward(self):
        self.move((0,0,1))
    def backward(self):
        self.move((0,0,-1))
