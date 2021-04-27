from ham_cycle import HamCycle
from conf import STEP, GRID_SIZE
from sys import maxsize


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
        self.env = None  # Environment should be set from the environment class.

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


class ShortestPathSnakeAgent(Snake):

    def action(self, percepts):
        min_distance = maxsize
        min_coord = None
        for coordinate in percepts:
            manhattan_distance = self.manhattan_distance(coordinate, self.env.apple_coord)
            if manhattan_distance < min_distance:
                min_distance = manhattan_distance
                min_coord = coordinate
        return min_coord

    @staticmethod
    def manhattan_distance(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return abs(x2//STEP - x1//STEP) + abs(y2//STEP - y1//STEP)
