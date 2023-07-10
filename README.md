# 8 Puzzle Solver

This is a Python program that solves the 8 Puzzle problem using the A* search algorithm with a priority queue. The program provides a graphical user interface (GUI) implemented using the tkinter module.

## Problem Description
The 8 Puzzle problem involves a 3x3 grid with eight numbered tiles and one blank tile. The goal is to rearrange the tiles from a given initial configuration to the goal state:

```
1 2 3
8 0 4
7 6 5
```

The tiles can be moved either vertically or horizontally into the adjacent blank space. The objective is to find the shortest sequence of moves that transforms the initial configuration into the goal state.

## Program Components
The program consists of the following components:

- `PuzzleState`: This class represents a state in the puzzle-solving process. It stores the current puzzle configuration, the parent state, the move made to reach this state, and the cost values for path finding.
- `PuzzleSolverGUI`: This class implements the graphical user interface for the puzzle solver. It provides a canvas widget for drawing the puzzle, generates the initial state, and handles the solve button click event.
- `solve_8_puzzle`: This function solves the 8 Puzzle problem using the A* search algorithm. It maintains an open set and a closed set of states, explores the states in order of their total cost, and backtracks to find the solution path.
- `main`: This section of the code creates an instance of the `PuzzleSolverGUI` class and runs the GUI.

## Dependencies
The program requires the following dependencies:
- `tkinter`: The tkinter module is used for creating the GUI.
- `queue.PriorityQueue`: The `PriorityQueue` class is used for implementing the priority queue.
- `random`: The `random` module is used for generating random numbers.
- `time`: The `time` module is used for timing the puzzle-solving process.

## Usage
To use the program, follow these steps:
1. Ensure you have Python installed on your system.
2. Install the required dependencies if necessary.
3. Run the program using the command: `python puzzle_solver.py`.
4. The GUI window will appear with the initial puzzle configuration displayed.
5. Click the "Solve" button to start solving the puzzle.
6. A message box will appear showing the solution moves and the elapsed time.

Note: The program generates a random initial state for each run. Therefore, the solution moves may vary for different runs.

## Contributing
If you would like to contribute to this project, you can fork the repository, make your changes, and submit a pull request. Contributions are welcome!

## License
This project is licensed under the [MIT License](LICENSE). Feel free to use and modify the code according to your needs.

## Acknowledgments
The implementation of the A* search algorithm and the GUI design were inspired by various online resources and tutorials.
