# SnakeAI

## Brief Description of the project:
This project is part of the CIIC 5010 course (Artificial Intelligence) and is an oportunity for students to apply some of the concepts discussed in class from the textbook (Artificial Intelligence: A Modern Approach, 3rd Edition, Russel and Norvig, 2010). The aim of this project is to create different AI agents which attempt to solve the snake game.

## The following files are included:

* requirements.txt: Contains the library dependencies needed to run the application. You can use your package manager of choice to install them. 

```bash
pip install -r requirements.txt
```

* main.py: Contains the code for the main program. Once this file is runned, the user will be prompted with a couple of options from which he/she can decide which of the different simulations the user wants to carry out.The user is also presented with the option of carrying a benchmark which would run the different simulations n times, being n provided by the user. Once the benchmarks finishes, on screen the performance results for each run and each simulation will be printed. These results will be saved in the output.txt file.

* agents.py: Implements three different agents to play the single player snake game. Each agent uses a different strategy to solve the game. The first, uses a greedy algorithm which always chooses the coordinate which minimizes the manhattan distance to the apple. This snake does not complete the game since, it is not always the best desicion to choose the closest coordinate. The second agent implements a hamiltonian cycle (goes through all coordinates only once and ends at the same place it started. This agent completes the game but is not optimal since it always sticks to the cycle. A final agent, which attempts to improve the optimality of the hamiltonian cycle by takin shortcuts is included.
The program is runned from the main.py file.

* environment.py: Contains all the code relevand to displaying and performing actions on the environment. The implementation is based on the abstract Environment class from: https://github.com/aimacode/aima-python/blob/master/agents.py

* conf.py: Contains global variables used throught the project. Can be edited to alter the window and grid size.

* ham_cycle.py: Contains the necessary code to generate a random hamiltonian cycle and store it on a 2d array. It is a python implementation of the C++ code provided by John Tapsell in https://johnflux.com/2015/05/02/nokia-6110-part-3-algorithms/

* output.txt: Stores the results of the benchmarks that can be ran in the program.

* LOG.txt: a detailed log of all pair programming sessions and the progress achieved in each meeting.

* SnakeAI.mp4: A short video demostration of the project. 
