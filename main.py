import pygame as game

WIDTH = 400
HEIGHT = 400
STEP = 40
POSITIONS = int((WIDTH/STEP) * (HEIGHT/STEP))

game.init()


surface = game.display.set_mode((WIDTH, HEIGHT), game.HWSURFACE)
game.display.set_caption('Snake AI')
surface.fill((0, 0, 0))


def dfs(initial):
    frontier = [initial]
    explored = dict()

    while frontier:
        point = frontier.pop()
        explored[point] = False
        x, y = point

        north = (x, y - STEP/2)
        west = (x - STEP/2, y)
        south = (x, y + STEP/2)
        east = (x + STEP/2, y)

        if y - STEP/2 > 0 and explored.get(north, True):
            frontier.append(north)
        if x - STEP/2 > 0 and explored.get(west, True):
            frontier.append(west)
        if y + STEP/2 < HEIGHT and explored.get(south, True):
            frontier.append(south)
        if x + STEP/2 < WIDTH and explored.get(east, True):
            frontier.append(east)

    return explored.keys()


def hamiltonian_cycle_helper(path, pos, count=1):

    # Base case: all positions included in path
    if count == POSITIONS:
        return True

    x, y = pos
    north = (x, y - STEP)
    west = (x - STEP, y)
    south = (x, y + STEP)
    east = (x + STEP, y)
    for point in [north, west, south, east]:
        x, y = point
        if 0 < x < WIDTH and 0 < y < HEIGHT and path.get(point, True):
            print(x, y)
            path[point] = False

            if hamiltonian_cycle_helper(path, point, count + 1):
                return True

            path.pop(point)

    return False


def hamiltonian_cycle():
    path = dict()
    pos = (20, 20)
    path[pos] = False

    hamiltonian_cycle_helper(path, pos)

    return list(path.keys())


def hardcoded_ham_cycle():
    path = []
    for row in range(20, HEIGHT, STEP):

        for i in range(20, WIDTH, STEP):
            path.append((i, 20))

    path.append()


line_color = (100, 100, 100)
# for i in range(STEP, WIDTH, STEP):
#     game.draw.line(surface, line_color, (0, i), (WIDTH, i))
# for j in range(STEP, HEIGHT, STEP):
#     game.draw.line(surface, line_color, (j, 0), (j, HEIGHT))

path = hamiltonian_cycle()
print(path)
print(len(path))
game.draw.lines(surface, line_color, False, path, 3)

game.display.flip()

while True:
    pass