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

    def min_manhattan_distance(self, percepts):
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
        return abs(x2 // STEP - x1 // STEP) + abs(y2 // STEP - y1 // STEP)


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

    def path_distance(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return (self.tour[y2//STEP][x2//STEP] - self.tour[y1//STEP][x1//STEP]) % GRID_SIZE


class ShortestPathSnakeAgent(Snake):

    def action(self, percepts):
        return self.min_manhattan_distance(percepts)


class HamCycleWithShortcutsSnakeAgent(HamCycleSnakeAgent):

    def action(self, percepts):
        # Find the coordinate that covers the most distance while ensuring all safety constraints are met.
        max_shortcut_distance = self.max_shortcut_distance()
        best_shortcut = None
        max_distance_covered = 0
        for coordinate in percepts:
            path_distance = self.path_distance(self.head.coordinate, coordinate)
            if max_shortcut_distance >= path_distance > max_distance_covered:
                best_shortcut = coordinate
                max_distance_covered = path_distance
        
        # If length of snake is one, follow the shortest path to apple.
        if len(self.snake) == 1:
            return self.min_manhattan_distance(percepts)
        
        # If a valid shortcut is found. Take it.
        if best_shortcut is not None:
            return best_shortcut

        # Otherwise, stick to the safe route (Normal HamCycle).
        return super(HamCycleWithShortcutsSnakeAgent, self).action(percepts)

    def max_shortcut_distance(self):
        if len(self.snake) >= GRID_SIZE / 2:  # Only take shortcuts if the snake covers less than half the grid
            return 0

        # Does not overtake tail.
        tail = self.tail.coordinate if self.tail.coordinate is not None else self.head.coordinate
        distance_to_tail = self.path_distance(self.head.coordinate, tail)
        max_shortcut_distance = distance_to_tail - 4  # Subtract 4 as a precaution.

        # Does not grow enough to catch up to tail.
        distance_to_apple = self.path_distance(self.head.coordinate, self.env.apple_coord)
        if distance_to_apple < distance_to_tail:
            # Take into consideration the amount the snake will grow (to avoid catching up to tail).
            max_shortcut_distance -= 1

            # Take into consideration that another apple might spawn on the path between the apple and tail
            # causing us to catch up to the tail.
            n_blocks_2nd_app_possible = self.path_distance(self.env.apple_coord, tail)
            # We use a multiplier of 4 as a precautionary buffer.
            n_blocks_2nd_app_possible *= 4
            # If the probability of spawn is greater than 25% subtract 10 as a precaution.
            if n_blocks_2nd_app_possible/len(self.env.available_coords) > 0.25:
                max_shortcut_distance -= 10

        # Does not overtake apple.
        max_shortcut_distance = min(max_shortcut_distance, distance_to_apple)

        return max(0, max_shortcut_distance)
