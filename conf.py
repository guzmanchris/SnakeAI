"""
Configuration file: Contains all global variables for the project.
"""

SCREEN_WIDTH = 400  # The width (in pixels) of the screen window.
SCREEN_HEIGHT = 400  # The height (in pixels) of the screen window.
STEP = 40  # The number of pixels the snake travels with each action. It should be a factor of both width and height
GRID_WIDTH = SCREEN_WIDTH//STEP
GRID_HEIGHT = SCREEN_HEIGHT//STEP
GRID_SIZE = GRID_WIDTH * GRID_HEIGHT
