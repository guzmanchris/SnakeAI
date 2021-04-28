import pygame as game
import random
import time
from agents import *
from conf import *


class SnakeEnvironment:

    def __init__(self, agent):
        self.agent = agent
        self.agent.env = self

        # Initialize pygame
        game.init()
        self.surface = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), game.HWSURFACE)
        game.display.set_caption('Snake AI')
        self.background_color = (0, 0, 0)
        self.surface.fill(self.background_color)

        # Draw grid lines
        line_color = (100, 100, 100)
        self.line_width = 1
        for i in range(STEP, SCREEN_WIDTH, STEP):
            game.draw.line(self.surface, line_color, (0, i), (SCREEN_WIDTH, i), self.line_width)
        for j in range(STEP, SCREEN_HEIGHT, STEP):
            game.draw.line(self.surface, line_color, (j, 0), (j, SCREEN_HEIGHT), self.line_width)

        # Draw snake
        x, y = self.agent.head.coordinate
        self.snake_color = (79, 132, 55)
        self.draw_rect(x, y)

        # Store available coords for apple placement.
        self.available_coords = dict()
        for x in range(0, SCREEN_WIDTH, STEP):
            for y in range(0, SCREEN_HEIGHT, STEP):
                coord = (x, y)
                if not self.agent.snake.get(coord, False):
                    self.available_coords[coord] = coord

        # Draw apple
        self.apple_color = (150, 0, 0)
        self.apple_coord = None
        self.generate_apple()

        # Update Display
        game.display.flip()

    def percept(self, agent):
        valid_steps = []
        x, y = agent.head.coordinate

        north = (x, y - STEP)
        west = (x - STEP, y)
        south = (x, y + STEP)
        east = (x + STEP, y)

        if y - STEP >= 0 and not agent.snake.get(north, False):
            valid_steps.append(north)
        if x - STEP >= 0 and not agent.snake.get(west, False):
            valid_steps.append(west)
        if y + STEP < SCREEN_HEIGHT and not agent.snake.get(south, False):
            valid_steps.append(south)
        if x + STEP < SCREEN_WIDTH and not agent.snake.get(east, False):
            valid_steps.append(east)

        return valid_steps

    def execute_action(self, agent, action):
        if action is None:
            return

        # Add new head
        self.agent.head.next = Body(action, None)
        self.agent.head = self.agent.head.next
        self.agent.snake[action] = self.agent.head
        self.draw_rect(*action)
        del self.available_coords[action]

        if self.agent.head.coordinate == self.apple_coord:
            self.generate_apple()
            if self.agent.tail.coordinate is None:
                self.agent.tail.coordinate = self.agent.tail.next.coordinate
                self.agent.tail.next = self.agent.head
        else:
            # Remove tail from body
            try:
                del self.agent.snake[self.agent.tail.coordinate]
                self.available_coords[self.agent.tail.coordinate] = self.agent.tail.coordinate
                self.delete_rect(*self.agent.tail.coordinate)
                prev_tail = self.agent.tail
                self.agent.tail = self.agent.tail.next
                prev_tail.coordinate = None
                prev_tail.next = None
                prev_tail = None
            except KeyError:
                # The coordinate of tail is None (snake body only of length 1)
                self.available_coords[self.agent.tail.next.coordinate] = self.agent.tail.next.coordinate
                self.delete_rect(*self.agent.tail.next.coordinate)
                del self.agent.snake[self.agent.tail.next.coordinate]
                self.agent.tail.next = self.agent.head

        game.display.flip()

    def step(self):
        if self.agent.alive:
            self.execute_action(self.agent, self.agent.action(self.percept(self.agent)))

    def run(self):
        while self.agent.alive:
            self.step()
            time.sleep(100 / 1000)

    def new_rect(self, x, y):
        lw = self.line_width
        return x + lw, y + lw, STEP - lw, STEP - lw

    def draw_rect(self, x, y):
        color = self.snake_color
        game.draw.rect(self.surface, color, self.new_rect(x, y))

    def delete_rect(self, x, y):
        game.draw.rect(self.surface, self.background_color, self.new_rect(x, y))

    def generate_apple(self):
        if len(self.available_coords) == 0:
            x, y = self.apple_coord
            self.draw_rect(x, y)
            print('Done!')
        else:
            self.apple_coord = random.choice(list(self.available_coords.keys()))
            x, y = self.apple_coord
            game.draw.rect(self.surface, self.apple_color, self.new_rect(x, y))
