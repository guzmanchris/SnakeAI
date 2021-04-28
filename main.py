from agents import *
from environment import SnakeEnvironment

if __name__ == '__main__':
    agent = HamCycleWithShortcutsSnakeAgent()
    print(agent.tour)
    environment = SnakeEnvironment(agent)
    environment.run()
