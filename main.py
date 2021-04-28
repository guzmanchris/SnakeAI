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
    # for _ in range(50):
    #     agent = HamCycleWithShortcutsSnakeAgent()
    #     environment = SnakeEnvironment(agent, benchmark=True)
    #     environment.run()
    result = run_benchmarks(10)
    print(result)
    sys.stdout = open('output.txt', 'wt')
    print(result)



