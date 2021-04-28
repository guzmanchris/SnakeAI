import sys
from agents import *
from environment import SnakeEnvironment


def run_benchmarks(n):
    result = ''
    agents = [ShortestPathSnakeAgent, HamCycleSnakeAgent, HamCycleWithShortcutsSnakeAgent]
    for agent in agents:
        result += f'{agent.verbose_name()}\n'
        result += '%s %12s %22s %27s %22s\n' % ('n', 'PM', 'total_steps', 'avg_steps_to_app', 'completed?')
        for i in range(n):
            agnt = agent()
            SnakeEnvironment(agnt, benchmark=True).run()
            avg = agnt.total_steps//agnt.apples_eaten
            result += '%s %12s %22s %27s %22s\n' % (i+1, agnt.performance, agnt.total_steps, avg, agnt.completed_game)
        result += '\n'
    return result


if __name__ == '__main__':
    print('Welcome to the Snake AI game.')
    while True:
        option = int(input('''
What would you like to do?
    1. Run and display a single game.
    2. Run a benchmark.
    3. Exit program.
:'''))
        if option == 1:
            while True:
                option2 = int(input('''
Which strategy would you like your agent to follow?
    1. Choose the coordinate with the minimum distance to the apple (Use a greedy algorithm which uses
       the manhattan distance as a heuristic).
    2. Always follow a predetermined hamiltonian cycle.
    3. Follow a hamiltonian cycle with the possibility of taking shortcuts.
:'''))
                if option2 == 1:
                    agent = ShortestPathSnakeAgent()
                elif option2 == 2:
                    agent = HamCycleSnakeAgent()
                elif option2 == 3:
                    agent = HamCycleWithShortcutsSnakeAgent()
                else:
                    print('Please enter a number between 1 and 3\n')
                    continue

                SnakeEnvironment(agent).run()
                print('Successfully completed game?', 'Yes' if agent.completed_game else 'No')
                print('Its performance measure for this game was:', agent.performance)
                print('The total steps the snake took were:', agent.total_steps)
                print('The average steps taken to reach the apple was:', agent.total_steps//agent.apples_eaten)
                print('\n')
                break

        elif option == 2:
            n = int(input('Enter the amount of simulations you want to run per agent (Try to keep the number small): '))
            print('Please wait while the process completes...')
            result = run_benchmarks(n)
            print(result)
            original = sys.stdout
            sys.stdout = open('output.txt', 'wt')
            print(result)
            sys.stdout = original
            print('The results have been stored in the output.txt file')
        elif option == 3:
            exit()
        else:
            print('Please enter a number between 1 and 3\n')
            continue
