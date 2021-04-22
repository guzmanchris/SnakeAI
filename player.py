from ham_cycle import HamCycle
from conf import STEP, GRID_SIZE


class Body:
    def __init__(self, coordinate, next):
        self.coordinate = coordinate
        self.next = next

    def __eq__(self, other):
        return self.coordinate == other.coordinate

    def __str__(self):
        return str(self.coordinate)


class Snake:

    def __init__(self):
        self.head = Body((0, 0), None)
        self.tail = Body(None, self.head)
        self.snake = {self.head.coordinate: self.head}
        self.snake_color = (79, 132, 55)
        self.alive = True

    def action(self, percepts):
        raise NotImplementedError("Actions has not been implemented.")


class HamCycleSnakeAgent(Snake):

    def __init__(self):
        super(HamCycleSnakeAgent, self).__init__()
        # Calculate a random hamiltonian cycle and store it in self.tour
        self.tour = HamCycle().tour

    def action(self, percepts):
        x, y = self.head.coordinate
        next_pos = (self.tour[y//STEP][x//STEP] + 1) % GRID_SIZE
        for coordinate in percepts:
            x, y = coordinate
            if self.tour[y//STEP][x//STEP] == next_pos:
                return coordinate
