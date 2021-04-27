import numpy as np
from random import randint
from conf import GRID_HEIGHT, GRID_WIDTH


class HamCycle:
    """
    This class contains the necessary code to generate a random hamiltonian cycle in the rectangular grid. It is
    heavily based on the C++ code created by John Tapsell and available in:
    https://johnflux.com/2015/05/02/nokia-6110-part-3-algorithms/comment-page-1/

    Many thanks to John for designing and making publicly available his ingenious algorithm.
    """

    class Node:

        def __init__(self):
            self.visited = False
            self.can_go_right = False
            self.can_go_down = False

    def __init__(self):
        self.nodes = np.empty((GRID_HEIGHT // 2, GRID_WIDTH // 2), dtype=self.Node)
        self.tour = np.zeros((GRID_HEIGHT, GRID_WIDTH))

        for x in range(GRID_HEIGHT // 2):
            for y in range(GRID_HEIGHT//2):
                self.nodes[x][y] = self.Node()

        self.generate_maze(-1, -1, 0, 0)
        self.generate_tour()

    def mark_visited(self, x, y):
        self.nodes[x][y].visited = True

    def mark_can_go_right(self, x, y):
        self.nodes[x][y].can_go_right = True

    def mark_can_go_down(self, x, y):
        self.nodes[x][y].can_go_down = True

    def can_go_right(self, x, y):
        return self.nodes[x][y].can_go_right

    def can_go_down(self, x, y):
        return self.nodes[x][y].can_go_down

    def can_go_left(self, x, y):
        return self.nodes[x-1][y].can_go_right

    def can_go_up(self, x, y):
        return self.nodes[x][y-1].can_go_down

    def is_visited(self, x, y):
        return self.nodes[x][y].visited

    def generate_maze(self, fromx, fromy, x, y):
        if x < 0 or y < 0 or x >= GRID_WIDTH/2 or y >= GRID_HEIGHT/2 or self.is_visited(x, y):
            return

        self.mark_visited(x, y)

        if fromx != -1:
            if fromx < x:
                self.mark_can_go_right(fromx, fromy)
            elif fromx > x:
                self.mark_can_go_right(x, y)
            elif fromy < y:
                self.mark_can_go_down(fromx, fromy)
            elif fromy > y:
                self.mark_can_go_down(x, y)

        # We visit two of the four connected nodes randomly and then visit all non-randomly. It's ok to visit the
        # same node twice.
        for _ in range(2):
            case = randint(1, 4)
            if case == 1:
                self.generate_maze(x, y, x-1, y)
            elif case == 2:
                self.generate_maze(x, y, x+1, y)
            elif case == 3:
                self.generate_maze(x, y, x, y-1)
            elif case == 4:
                self.generate_maze(x, y, x, y+1)

        self.generate_maze(x, y, x - 1, y)
        self.generate_maze(x, y, x + 1, y)
        self.generate_maze(x, y, x, y - 1)
        self.generate_maze(x, y, x, y + 1)

    def find_next_direction(self, x, y, dir):
        if dir == 'Right':
            if self.can_go_up(x, y):
                return 'Up'
            elif self.can_go_right(x, y):
                return 'Right'
            elif self.can_go_down(x, y):
                return 'Down'
            else:
                return 'Left'
        elif dir == 'Down':
            if self.can_go_right(x, y):
                return 'Right'
            elif self.can_go_down(x, y):
                return 'Down'
            elif self.can_go_left(x, y):
                return 'Left'
            else:
                return 'Up'
        elif dir == 'Left':
            if self.can_go_down(x, y):
                return 'Down'
            elif self.can_go_left(x, y):
                return 'Left'
            elif self.can_go_up(x, y):
                return 'Up'
            else:
                return 'Right'
        elif dir == 'Up':
            if self.can_go_left(x, y):
                return 'Left'
            elif self.can_go_up(x, y):
                return 'Up'
            elif self.can_go_right(x, y):
                return 'Right'
            else:
                return 'Down'

    def set_tour_number(self, x, y, number):
        if self.tour[x][y] != 0:
            return
        self.tour[x][y] = number

    def generate_tour(self):
        x = y = 0
        start_dir = 'Up' if self.can_go_down(x, y) else 'Left'
        dir = start_dir
        number = 0
        while True:
            next_dir = self.find_next_direction(x, y, dir)
            if dir == 'Right':
                self.set_tour_number(x * 2, y * 2, number)
                number += 1
                if next_dir == dir or next_dir == 'Down' or next_dir == 'Left':
                    self.set_tour_number(x * 2 + 1, y * 2, number)
                    number += 1
                if next_dir == 'Down' or next_dir == 'Left':
                    self.set_tour_number(x * 2 + 1, y * 2 + 1, number)
                    number += 1
                if next_dir == 'Left':
                    self.set_tour_number(x * 2, y * 2 + 1, number)
                    number += 1
            elif dir == 'Down':
                self.set_tour_number(x * 2 + 1, y * 2, number)
                number += 1
                if next_dir == dir or next_dir == 'Left' or next_dir == 'Up':
                    self.set_tour_number(x * 2 + 1, y * 2 + 1, number)
                    number += 1
                if next_dir == 'Left' or next_dir == 'Up':
                    self.set_tour_number(x * 2, y * 2 + 1, number)
                    number += 1
                if next_dir == 'Up':
                    self.set_tour_number(x * 2, y * 2, number)
                    number += 1
            elif dir == 'Left':
                self.set_tour_number(x * 2 + 1, y * 2 + 1, number)
                number += 1
                if next_dir == dir or next_dir == 'Up' or next_dir == 'Right':
                    self.set_tour_number(x * 2, y * 2 + 1, number)
                    number += 1
                if next_dir == 'Up' or next_dir == 'Right':
                    self.set_tour_number(x * 2, y * 2, number)
                    number += 1
                if next_dir == 'Right':
                    self.set_tour_number(x * 2 + 1, y * 2, number)
                    number += 1
            elif dir == 'Up':
                self.set_tour_number(x * 2, y * 2 + 1, number)
                number += 1
                if next_dir == dir or next_dir == 'Right' or next_dir == 'Down':
                    self.set_tour_number(x * 2, y * 2, number)
                    number += 1
                if next_dir == 'Right' or next_dir == 'Down':
                    self.set_tour_number(x * 2 + 1, y * 2, number)
                    number += 1
                if next_dir == 'Down':
                    self.set_tour_number(x * 2 + 1, y * 2 + 1, number)
                    number += 1

            dir = next_dir
            if next_dir == 'Right':
                x += 1
            elif next_dir == 'Left':
                x -= 1
            elif next_dir == 'Down':
                y += 1
            elif next_dir == 'Up':
                y -= 1

            if number >= GRID_WIDTH * GRID_HEIGHT - 1:
                break

    def print_maze(self):
        for y in range(GRID_HEIGHT // 2):
            print('#', end='')
            for x in range(GRID_WIDTH // 2):
                if self.can_go_right(x, y) and self.can_go_down(x, y):
                    print('+', end='')
                elif self.can_go_right(x, y):
                    print('-', end='')
                elif self.can_go_down(x, y):
                    print('|', end='')
                else:
                    print(' ', end='')
            print('#')


if __name__ == '__main__':
    cycle = HamCycle()

    cycle.print_maze()
    print(cycle.tour)
