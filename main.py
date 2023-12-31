import copy
import random
import time
import psutil


class Node:
    board = [["_", 1, 2],
             [3, 4, 5],
             [6, 7, 8]]
    g = 0 # --------------------------------------------------------
    h = 0  # hamming heuristic
    f = 0  # overall cost
    heuristic = 1  # 0 = hamming, 1 = manhattan
    parent = 0

    # Generates new Child Node
    def child_node(self, direction):
        new_board = [row.copy() for row in self.board]  # new copy of current node board
        blank_x, blank_y = self.find_blank()  # blank space coordinates

        # New coordinates after blank space is swapped
        if direction == "up" and blank_x > 0:
            new_x, new_y = blank_x - 1, blank_y
        elif direction == "down" and blank_x < 2:
            new_x, new_y = blank_x + 1, blank_y
        elif direction == "left" and blank_y > 0:
            new_x, new_y = blank_x, blank_y - 1
        elif direction == "right" and blank_y < 2:
            new_x, new_y = blank_x, blank_y + 1
        else:
            return None  # invalid direction

        # Swap the blank space with the tile in the specified direction
        new_board[blank_x][blank_y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[blank_x][blank_y]

        # Create a new node with the updated board & cost
        new_node = Node()
        new_node.parent = self
        new_node.board = new_board
        new_node.g = copy.deepcopy(self.g) + 1
        new_node.h = copy.deepcopy(self.heuristic)

        if new_node.heuristic == 1:
            manhattan(new_node)
        else:
            hamming(new_node)

        # Checks if state already occured
        if check_loops(new_node) == 0:
            return 0  # same state detected ------------------------------?

        return new_node

    # Returns the blank space of given board
    def find_blank(self):
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == "_":
                    return x, y


# Creates a solvable random initial node
def initial_node():
    solvable = False
    while not solvable:

        # Create new shuffled board
        node = Node()
        count = 0
        flat = [element for sublist in node.board for element in sublist]
        random.shuffle(flat)
        node.board = [flat[i:i + 3] for i in range(0, 9, 3)]

        # Inversion counter for solvability check
        for x in range(len(flat) - 1):
            for y in range(x, len(flat)):
                if flat[x] == "_" or flat[y] == "_":
                    continue  # ignores blank space
                if flat[x] > flat[y]:
                    count += 1

        if count % 2 == 0:
            solvable = True
        else:
            solvable = False
        if solvable:
            break

    if node.heuristic == 1:
        manhattan(node)
    else:
        hamming(node)

    return node


# Goal state
def goal_node():
    node = Node()
    node.board = [["_", 1, 2],
                  [3, 4, 5],
                  [6, 7, 8]]
    return node


# Hamming Distance - counts the number of misplaced tiles
def hamming(node):
    goal = goal_node()

    for y in range(3):
        if node.board[x][y] != "_" and node.board[x][y] != goal.board[x][y]:
            ham_distance += 1

    node.h = ham_distance
    node.f = node.g + node.h


# Manhatten Distance - calculates how many moves are needed from initial to goal node
def manhattan(node):
    goal = goal_node()
    man_distance = 0

    for value in range(1, 9):
        initial_coordinates = find_coordinates(node, value)
        goal_coordinates = find_coordinates(goal, value)

        if initial_coordinates is not None and goal_coordinates is not None:
            row_difference = abs(initial_coordinates[0] - goal_coordinates[
                0])  # row difference of initial node and goal node tile
            col_difference = abs(initial_coordinates[1] - goal_coordinates[
                1])  # col difference of initial node and goal node tile

            man_distance += row_difference + col_difference

    node.h = man_distance
    node.f = node.g + node.h


# Creates amount of new child nodes in regard of possible direction
def create_children(node):
    child_nodes = []
    directions = ["up", "down", "left", "right"]

    for direction in directions:  # ? loops the print of all child nodes for each possible direction ---------------------
        child = node.child_node(direction)
        if child:
            child_nodes.append(child)

    return child_nodes

# Überschriften?---------------------------------------
# Solves Puzzle from Initial state till Goal state
def solve_puzzle():
    initial = initial_node()
    node_count = 1
    step_count = 1
    open_nodes = []  # lists all nodes to be traversed
    visited_nodes = []

    open_nodes.append(initial)

    while True:
        current_node = open_nodes[0]

        # does not work yet
        if current_node in visited_nodes:
            continue  # avoid repetition

        # testing/debugging
        print("step ", step_count, ": ")
        print()
        print_node(current_node)
        print("-> g: ", current_node.g, " h: ", current_node.h, " f: ", current_node.f)
        print()

        if current_node.h == 0:
            break  # stop loop when heuristic of current node reaches 0

        child_nodes = create_children(current_node)

        for child in child_nodes:
            open_nodes.append(child)
            node_count += 1

        visited_nodes.append(current_node)

        del open_nodes[0]
        open_nodes.sort(key=lambda element: element.f, reverse=False)
        step_count += 1


# Checks for identical boards in check_loops
def compare_boards(node1, node2):
    for x in range(3):
        for y in range(3):
            if node1.board[x][y] != node2.board[x][y]:
                return 0
    return 1


# Prevent algorithm from revisiting previously encountered states
def check_loops(node):
    parent_node = node.parent
    while parent_node != 0:
        if compare_boards(node, parent_node) == 1:
            return 0
        parent_node = parent_node.parent
    return 1


# Prints the board of given node
def print_node(node):
    for x in range(3):
        for y in range(3):
            print(node.board[x][y], end=" ")
        print()


# For calculation of Manhatten Distance
def find_coordinates(node, tile):
    for x in range(3):
        for y in range(3):
            if node.board[x][y] == tile:
                return x, y


random_states = 100


# Run A* search for each random state with both heuristics --------------------
def statistics():
    for _ in range(random_states):

        initial_state = initial_node()
        goal_state = goal_node()

        # Measure Runtime
        start_time = time.time()
        heuristic = 1  # Choose Hamming=0 or Manhattan=1 heuristic
        solve_puzzle()
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Measure memory usage & print Statistics
        if heuristic == 0:
            print(f"Hamming Heuristic - Run Time: {elapsed_time} seconds")
            process = psutil.Process()
            memory_usage = process.memory_info().rss
            print(f"Hamming Heuristic - Memory Usage: {memory_usage} bytes")
        elif heuristic == 1:
            print(f"Manhattan Heuristic - Run Time: {elapsed_time} seconds")
            process = psutil.Process()
            memory_usage = process.memory_info().rss
            print(f"Manhattan Heuristic - Memory Usage: {memory_usage} bytes")


if __name__ == '__main__':
    """
    initial_state = initial_node()
    create_children(initial_state)
    """
    solve_puzzle()
    # statistics()
