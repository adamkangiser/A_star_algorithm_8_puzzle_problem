# Course:               CS7375-W02 Artificial Intelligence
# Student name:         Adam Kangiser
# Student ID:           000681701
# Assignment number:    2
# Due Date:             July 10, 2023
# Signature:            Adam Kangiser
# Score:


import tkinter as tk  # Import the tkinter module for GUI
from tkinter import messagebox  # Import the messagebox submodule for displaying messages
from queue import PriorityQueue  # Import the PriorityQueue class for implementing the priority queue
import random  # Import the random module for generating random numbers
import time  # Import the time module for timing the puzzle-solving process


# Define the goal state
goal_state = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]


class PuzzleState:
    def __init__(self, puzzle, parent=None, move=""):
        self.puzzle = puzzle  # Current puzzle configuration
        self.parent = parent  # Parent state
        self.move = move  # Move made to reach this state
        self.g = 0  # Cost from start node to current node
        self.h = 0  # Heuristic value (estimated cost from current node to goal)
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f  # Comparison function for the priority queue

    def __eq__(self, other):
        return self.puzzle == other.puzzle  # Comparison function for equality

    def __hash__(self):
        return hash(str(self.puzzle))  # Hash function for set membership

    def find_blank(self):
        # Find the row and column index of the blank tile (0)
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] == 0:
                    return i, j

    def get_neighbors(self):
        row, col = self.find_blank()
        neighbors = []

        # Move the blank tile up
        if row > 0:
            new_puzzle = [row[:] for row in self.puzzle]  # Create a new puzzle configuration as a copy of the current one
            new_puzzle[row][col], new_puzzle[row - 1][col] = new_puzzle[row - 1][col], new_puzzle[row][col]  # Swap the blank tile with the tile above it
            neighbors.append(PuzzleState(new_puzzle, self, "Up"))

        # Move the blank tile down
        if row < 2:
            new_puzzle = [row[:] for row in self.puzzle]  # Create a new puzzle configuration as a copy of the current one
            new_puzzle[row][col], new_puzzle[row + 1][col] = new_puzzle[row + 1][col], new_puzzle[row][col]  # Swap the blank tile with the tile below it
            neighbors.append(PuzzleState(new_puzzle, self, "Down"))

        # Move the blank tile left
        if col > 0:
            new_puzzle = [row[:] for row in self.puzzle]  # Create a new puzzle configuration as a copy of the current one
            new_puzzle[row][col], new_puzzle[row][col - 1] = new_puzzle[row][col - 1], new_puzzle[row][col]  # Swap the blank tile with the tile to its left
            neighbors.append(PuzzleState(new_puzzle, self, "Left"))

        # Move the blank tile right
        if col < 2:
            new_puzzle = [row[:] for row in self.puzzle]  # Create a new puzzle configuration as a copy of the current one
            new_puzzle[row][col], new_puzzle[row][col + 1] = new_puzzle[row][col + 1], new_puzzle[row][col]  # Swap the blank tile with the tile to its right
            neighbors.append(PuzzleState(new_puzzle, self, "Right"))

        return neighbors

    def calculate_heuristic(self):
        # Manhattan distance heuristic
        h = 0
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] != 0:
                    goal_row, goal_col = (self.puzzle[i][j] - 1) // 3, (self.puzzle[i][j] - 1) % 3  # Calculate the goal row and column for the current tile value
                    h += abs(i - goal_row) + abs(j - goal_col)  # Calculate the Manhattan distance and add it to the heuristic value
        self.h = h

    def update_cost(self):
        self.g = self.parent.g + 1  # Update the cost from start to current node (g)
        self.f = self.g + self.h  # Update the total cost (f) as the sum of the cost from start to current node and the heuristic value

    def is_goal_state(self):
        return self.puzzle == goal_state  # Check if the current puzzle configuration matches the goal state


class PuzzleSolverGUI:
    def __init__(self):
        self.root = tk.Tk()  # Create the main window
        self.root.title("8 Puzzle Solver")  # Set the title of the window
        self.canvas = tk.Canvas(self.root, width=300, height=300, borderwidth=0, highlightthickness=0)  # Create a canvas widget for drawing the puzzle
        self.canvas.pack()  # Pack the canvas widget to make it visible

        self.buttons = []  # Initialize a list to store the button widgets
        self.button_values = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Initialize a 2D list to store the values of the buttons
        for i in range(3):
            row = []  # Initialize an inner list to store the buttons in each row
            for j in range(3):
                button = tk.Button(self.canvas, text="", width=10, height=5, state=tk.DISABLED)  # Create a button widget
                button.grid(row=i, column=j, padx=1, pady=1)  # Grid the button in the canvas at the specified row and column with padding
                row.append(button)  # Add the button to the current row list
            self.buttons.append(row)  # Add the row list to the buttons list

        self.generate_initial_state()  # Generate a random initial state for the puzzle

        solve_button = tk.Button(self.root, text="Solve", command=self.solve_puzzle)  # Create a solve button widget
        solve_button.pack()  # Pack the solve button widget to make it visible

    def generate_initial_state(self):
        initial_state = self.generate_random_state()  # Generate a random initial state for the puzzle
        for i in range(3):
            for j in range(3):
                self.button_values[i][j] = initial_state[i][j]  # Update the button values with the initial state
                self.buttons[i][j].config(text=initial_state[i][j] if initial_state[i][j] != 0 else "")  # Set the text of the buttons with the initial state values

    def generate_random_state(self):
        numbers = random.sample(range(1, 9), 8)  # Generate a list of random numbers from 1 to 8
        numbers.append(0)  # Add 0 (blank tile) to the list
        random.shuffle(numbers)  # Shuffle the list randomly
        return [numbers[:3], numbers[3:6], numbers[6:9]]  # Return the 2D list representation of the randomized numbers

    def update_puzzle(self, state):
        for i in range(3):
            for j in range(3):
                value = state.puzzle[i][j]  # Get the value of the puzzle at the current position
                self.button_values[i][j] = value  # Update the button values with the puzzle values
                self.buttons[i][j].config(text=value if value != 0 else "")  # Set the text of the buttons with the puzzle values (blank tile represented as "")

    def solve_puzzle(self):
        initial_state = self.button_values  # Get the current button values as the initial state of the puzzle

        start_time = time.time()  # Start timing the puzzle-solving process

        solution = solve_8_puzzle(initial_state)  # Solve the 8 puzzle problem with the initial state

        end_time = time.time()  # Stop timing the puzzle-solving process
        elapsed_time = end_time - start_time  # Calculate the elapsed time

        if solution is None:
            messagebox.showinfo("No Solution", "No solution found.")  # Show a message box indicating that no solution was found
        else:
            messagebox.showinfo("Solution Found", f"Solution found in {len(solution)} moves:\n{', '.join(solution)}\n\nElapsed time: {elapsed_time:.6f} seconds")  # Show a message box with the solution moves and the elapsed time

    def run(self):
        self.root.mainloop()  # Start the main event loop of the GUI


def solve_8_puzzle(initial_state):
    open_set = PriorityQueue()  # Create a priority queue to store the open states
    closed_set = set()  # Create a set to store the closed states

    # Create the initial state and calculate its heuristic value
    initial_state = PuzzleState(initial_state)
    initial_state.calculate_heuristic()
    open_set.put(initial_state)

    while not open_set.empty():
        current_state = open_set.get()  # Get the state with the lowest total cost from the priority queue

        if current_state.is_goal_state():
            # Backtrack to get the solution path
            moves = []
            while current_state.parent:
                moves.append(current_state.move)
                current_state = current_state.parent
            moves.reverse()
            return moves  # Return the solution moves

        closed_set.add(current_state)  # Add the current state to the closed set

        for neighbor in current_state.get_neighbors():
            if neighbor in closed_set:
                continue  # Skip the neighbor if it is already in the closed set

            if neighbor not in open_set.queue:
                neighbor.calculate_heuristic()  # Calculate the heuristic value for the neighbor
                neighbor.update_cost()  # Update the cost values (g and f) for the neighbor
                open_set.put(neighbor)  # Add the neighbor to the open set
            else:
                # Check if the current path is better than the previous one
                new_g = current_state.g + 1  # Calculate the new cost from start to neighbor (g)
                if new_g < neighbor.g:
                    neighbor.parent = current_state  # Update the parent of the neighbor
                    neighbor.g = new_g  # Update the cost from start to neighbor (g)
                    neighbor.f = new_g + neighbor.h  # Update the total cost (f)
                    open_set.put(neighbor)  # Add the neighbor to the open set

    return None  # Return None if no solution is found


if __name__ == "__main__":
    gui = PuzzleSolverGUI()  # Create an instance of the GUI
    gui.run()  # Run the GUI
