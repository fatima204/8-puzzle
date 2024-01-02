import copy
import random
import time  # runtime
import psutil  # memory usage
import statistics


class Node:
    board = [["_", 1, 2],
             [3, 4, 5],
             [6, 7, 8]]
    g = 0  # level of node in puzzle
    h = 0  # heuristic value
    f = 0  # overall costs
    heuristic = 0  # 0 = hamming (default), 1 = manhattan
    parent = 0


    # generates new child node
    def child_node(self, direction):
        new_board = [row.copy() for row in self.board]  # copy the current node board
        blank_x, blank_y = self.find_blank()  # find coordinates of blank space

        # find new coordinates after blank space is swapped # in specified direction
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

        # swap the blank space with the tile in the specified direction
        new_board[blank_x][blank_y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[blank_x][blank_y]

        # create a new node with the updated board and values
        new_node = Node()
        new_node.board = new_board
        new_node.parent = self
        new_node.g = copy.deepcopy(self.g) + 1  # copy the parent's g value and increment by 1
        new_node.heuristic = copy.deepcopy(self.heuristic)  # copy parent's heuristic approach

        if new_node.heuristic == 1:
            manhattan(new_node)
        else:
            hamming(new_node)

        if new_node.check_loops() == 0:  # same board state detected
            return None

        return new_node


    # returns the blank space of given board (needed for child_node)
    def find_blank(self):
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == "_":
                    return x, y


    # creates new child nodes according to possible directions of movable tiles
    def create_children(self):
        child_nodes = []
        directions = ["up", "down", "left", "right"]

        for direction in directions:
            child = self.child_node(direction)  # for every possible direction, generate child node
            if child:
                child_nodes.append(child)  # if child node generated, add to list

        return child_nodes


    # compares two node boards (needed for check_loops)
    def compare_boards(self, node):
        for x in range(3):
            for y in range(3):
                if self.board[x][y] != node.board[x][y]:
                    return 0
        return 1  # if boards not identical, return True


    # prevent algorithm from revisiting previously encountered states (needed for child_node)
    def check_loops(self):
        parent_node = self.parent  # set node to be compared as given node's parent
        while parent_node != 0:  # while node to be compared has parent
            if self.compare_boards(parent_node) == 1:  # if both identical, return False
                return 0
            parent_node = parent_node.parent  # otherwise set checked node's parent as node to be checked next
        return 1  # if nodes not identical, return True


    # prints the board of given node
    def print_node(self):
        for x in range(3):
            for y in range(3):
                print(self.board[x][y], end=" ")
            print()


    # prints whole path of given nodes
    def print_path(self):
        path = []  # array to store the nodes that leads from initial node to goal node
        node = self

        while node:
            path.append(node)  # append node to array path
            node = node.parent  # node is the parent of the node

        path.reverse()  # reverse the nodes in the array

        for step, step_node in enumerate(path):
            print(f"Step {step + 1}:")
            step_node.print_node()  # prints nodes of path
            print("-> g: ", step_node.g, " h: ", step_node.h, " f: ", step_node.f)
            print()


# generate a solvable random initial node
def initial_node(heuristic_type):
    while True:
        inv_count = 0

        # create new shuffled node
        node = Node()
        node.heuristic = heuristic_type

        flat = [element for sublist in node.board for element in sublist]  # flatten nested list using list comprehension
        random.shuffle(flat)  # shuffle the flattened list
        node.board = [flat[i:i + 3] for i in range(0, 9, 3)]  # recompose into nested list

        # inversion counter for solvability check
        for x in range(len(flat) - 1):
            for y in range(x, len(flat)):
                if flat[x] == "_" or flat[y] == "_":
                    continue  # ignores blank space
                if flat[x] > flat[y]:
                    inv_count += 1

        if inv_count % 2 == 0:  # if inversion count is even = solvable
            break
        else:
            continue

    if node.heuristic == 1:
        manhattan(node)
    else:
        hamming(node)

    return node


# generate goal state
def goal_node():
    node = Node()
    node.board = [["_", 1, 2],
                  [3, 4, 5],
                  [6, 7, 8]]
    return node


# Hamming Distance - counts the number of misplaced tiles
def hamming(node):
    goal = goal_node()
    ham_distance = 0

    for x in range(3):
        for y in range(3):
            if node.board[x][y] != "_" and node.board[x][y] != goal.board[x][y]:
                ham_distance += 1

    node.h = ham_distance  # saves hamming heuristic of node
    node.f = node.g + node.h  # updates cost of path


# calculates coordinates of tiles (needed for Manhattan distance)
def find_coordinates(node, tile):
    for x in range(3):
        for y in range(3):
            if node.board[x][y] == tile:
                return x, y


# Manhattan Distance - calculates how many moves are needed from initial to goal node
def manhattan(node):
    goal = goal_node()
    man_distance = 0

    for value in range(1, 9):
        initial_coordinates = find_coordinates(node, value)  # finds coordinates of initial value
        goal_coordinates = find_coordinates(goal, value)  # finds coordinates of goal value

        # checks if the funtion find_coordinates returned valid coordinates
        if initial_coordinates is not None and goal_coordinates is not None:
            row_difference = abs(initial_coordinates[0] - goal_coordinates[0])  # row difference of initial node and goal node tile
            col_difference = abs(initial_coordinates[1] - goal_coordinates[1])  # col difference of initial node and goal node tile

            man_distance += row_difference + col_difference  # sums up difference of row and col

    node.h = man_distance
    node.f = node.g + node.h


# solves puzzle from initial state to goal state
def solve_puzzle(heuristic_type):
    initial = initial_node(heuristic_type)  # random start node
    node_count = 1  # initial node is first node
    step_count = 0  # total step count
    open_nodes = [initial]  # list of all nodes to be traversed, initial node being the first

    while True:
        current_node = open_nodes[0]

        if current_node.h == 0:
            break  # stop loop when heuristic of current node reaches 0

        child_nodes = current_node.create_children()  # create children of current node

        for child in child_nodes:
            open_nodes.append(child)  # add every child to list
            node_count += 1

        del open_nodes[0]  # delete current node
        open_nodes.sort(key=lambda element: element.f, reverse=False)  # sorts the list of nodes by f value
        step_count += 1

    current_node.print_path()

    return node_count, step_count


# prompting user to choose heuristic
def choose_heuristic():
    # heuristic input by user
    heuristic_choice = int(input("Choose heuristic: 0 for Hamming, 1 for Manhattan: "))

    # ensure input validity
    if heuristic_choice not in [0, 1]:
        print("Invalid choice. Defaulting to Hamming (0).")
        heuristic_choice = 0

    # create new puzzle & solve it with chosen heuristic
    solve_puzzle(heuristic_choice)


# run A* search for each random state with either heuristic - to calculate statistics
def calc_statistics():
    random_states = 50  # number of random states to generate
    measure_count = 0  # counter for measurements readability
    runtimes = [] # stores all runtimes for statistic calculations
    memoryusages = [] # stores all memory usages for statistic calculations
    node_list = [] # stores memory usages (nodes)
    step_list = [] # stores algorithm complexities (steps)

    # prompts user to choose heuristic approach
    heuristic_choice = int(input("Statistics - Choose 0 for Hamming, 1 for Manhattan: "))

    if heuristic_choice == 0:
        print("Hamming Heuristic Statistics")
    elif heuristic_choice == 1:
        print("Manhattan Heuristic Statistics")

    for _ in range(random_states):
        # measure run time
        start_time = time.time()
        node_count, step_count = solve_puzzle(heuristic_choice)  # capture the returned values
        end_time = time.time()
        elapsed_time = end_time - start_time
        runtimes.append(elapsed_time)

        # measure memory usage
        process = psutil.Process()
        memory_usage = process.memory_info().rss
        memoryusages.append(memory_usage)

        node_list.append(node_count)
        step_list.append(step_count)

        measure_count += 1

        print(f"""{measure_count}.
        Runtime: {elapsed_time} seconds
        Memory Usage: {memory_usage} bytes
        Nodes generated (memory usage): {node_count}
        Steps needed (algorithm complexity): {step_count}""")

    # print() with multiline strings
    print(f"""----------------------------------
    Runtime - mean: {statistics.mean(runtimes)}
    Runtime - standard deviation: {statistics.stdev(runtimes)}
    Memory Usage - mean: {statistics.mean(memoryusages)}
    Memory Usage - standard deviation: {statistics.stdev(memoryusages)}

    nodes - mean: {statistics.mean(node_list)}
    nodes - standard deviation: {statistics.stdev(node_list)}
    steps - mean: {statistics.mean(step_list)}
    steps - standard deviation: {statistics.stdev(step_list)}""")


if __name__ == '__main__':

    choose_heuristic()
    #calc_statistics()


