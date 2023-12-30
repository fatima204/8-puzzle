import copy
import random


class Node:
    board = [["_", 1, 2],
             [3, 4, 5],
             [6, 7, 8]]
    g = 0
    h = 0
    f = 0
    heuristic = 1 # 0 = hamming, 1 = manhattan
    parent = 0


    def childNode(self, direction):
        new_board = [row.copy() for row in self.board]  # copy the current node board
        blank_x, blank_y = self.findBlank()  # find coordinates of blank space

        # find new coordinates after blank space is swapped
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

        # create a new node with the updated board
        new_node = Node()
        new_node.parent = self
        new_node.board = new_board
        new_node.g = copy.deepcopy(self.g) + 1  # copy the parent's g value and increment by 1
        new_node.h = copy.deepcopy(self.heuristic)  # copy parent's heuristic approach

        if new_node.heuristic == 1:
            manhattan(new_node)
        else:
            hamming(new_node)

        if check_loops(new_node) == 0:
            return 0

        return new_node


    # returns the blank space of given board
    def findBlank(self):
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == "_":
                    return x, y


def compare_boards(node1, node2):
    for x in range(3):
        for y in range(3):
            if node1.board[x][y] != node2.board[x][y]:
                return 0
    return 1


def check_loops(node):
    parent_node = node.parent
    while parent_node != 0:
        if compare_boards(node, parent_node) == 1:
            return 0
        parent_node = parent_node.parent
    return 1


# creates a shuffled initial node
def initialNode():
    node = Node()
    flat = [element for sublist in node.board for element in sublist]  # flatten nested list using list comprehension
    random.shuffle(flat)  # shuffle the flattened list
    node.board = [flat[i:i + 3] for i in range(0, 9, 3)]  # recompose into nested list

    if node.heuristic == 1:
        manhattan(node)
    else:
        hamming(node)

    return node


def goal_node():
    node = Node()
    node.board = [["_", 1, 2],
                  [3, 4, 5],
                  [6, 7, 8]]
    return node


# checks inversion count of given node
def solvable(node):
    count = 0
    flat = [element for sublist in node.board for element in sublist]

    for x in range(len(flat) - 1):
        for y in range(x, len(flat)):
            if flat[x] == "_" or flat[y] == "_":
                continue  # ignores the blank space
            if flat[x] > flat[y]:
                count += 1

    if count % 2 == 0:  # if inversion count is even = solvable
        return True
    else:
        return print("Random puzzle is not solvable! - Please try again!")


# prints the board of given node
def printNode(node):
    for x in range(3):
        for y in range(3):
            print(node.board[x][y], end=" ")
        print()


def find_coordinates(node, tile):
    for x in range(3):
        for y in range(3):
            if node.board[x][y] == tile:
                return x, y


# counts the number of misplaced tiles
def hamming(node):
    goal = goal_node()
    ham_distance = 0

    for x in range(3):
        for y in range(3):
            if node.board[x][y] != "_" and node.board[x][y] != goal.board[x][y]:
                ham_distance += 1

    node.h = ham_distance  # saves hamming heuristic of node
    node.f = node.g + node.h  # updates cost of path


# calculates how many moves are needed from initial to goal node
def manhattan(node):
    goal = goal_node()
    man_distance = 0

    for value in range(1, 9):
        initial_coordinates = find_coordinates(node, value)  # finds coordinates of initial value
        goal_coordinates = find_coordinates(goal, value)  # finds coordinates of goal value

        # check if find_coordinates returned valid coordinates
        if initial_coordinates is not None and goal_coordinates is not None:
            row_difference = abs(initial_coordinates[0] - goal_coordinates[0])  # calculates total difference of row from initial node to goal node
            col_difference = abs(initial_coordinates[1] - goal_coordinates[1])  # calculates total difference of col from initial node to goal node

            man_distance += row_difference + col_difference  # sums up difference of row and col

    node.h = man_distance
    node.f = node.g + node.h


# main process
def createChildren(node):
    child_nodes = []
    directions = ["up", "down", "left", "right"]

    for direction in directions:  # loops the print of all child nodes for each possible direction
        child = node.childNode(direction)
        if child:
            child_nodes.append(child)
            #print("child:")
            #printNode(child)
            #print("h: ", child.h)  # for testing
            #print()

    #child_nodes.sort(key=lambda element: element.f)  # sorts the list of nodes by f value

    #for obj in child_nodes:
        #print(obj.f)  # for testing - prints the sorted f values

    return child_nodes


def solvePuzzle():
    initial = initialNode()
    node_count = 1  # initial node is first node
    step_count = 0  # total step count
    open_nodes = []  # list of all nodes to be traversed
    visited_nodes = []  # list of already visited nodes

    if solvable(initial):
        open_nodes.append(initial)

        while True:
            current_node = open_nodes[0]  # set current node

            # does not work yet
            if current_node in visited_nodes:
                continue  # avoid repetition

            # testing/debugging
            print("step ", step_count, ": ")
            print()
            printNode(current_node)
            print("-> g: ", current_node.g, " h: ", current_node.h, " f: ", current_node.f)
            print()

            if current_node.h == 0:
                break  # stop loop when heuristic of current node reaches 0

            child_nodes = createChildren(current_node)  # create children of current node

            for child in child_nodes:
                open_nodes.append(child)  # add every child to list
                node_count += 1

            visited_nodes.append(current_node)  # add current node to visited nodes

            del open_nodes[0]  # delete current node
            open_nodes.sort(key=lambda element: element.f, reverse=False)  # sorts the list of nodes by f value
            step_count += 1





if __name__ == '__main__':

    # testing
    solvePuzzle()