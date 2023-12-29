import copy
import random


class Node:
    board = [["_", 1, 2],
             [3, 4, 5],
             [6, 7, 8]]
    g = 0
    h = 0
    f = 0
    heuristic = 0 # 0 = hamming, 1 = manhattan


    def childNode(self, direction):
        # Copy the current board to create a new node
        new_board = [row.copy() for row in self.board]
        # find coordinates of blank space
        blank_x, blank_y = self.findBlank()

        # Find new coordinates after blank space is swapped
        if direction == "up" and blank_x > 0:
            new_x, new_y = blank_x - 1, blank_y
        elif direction == "down" and blank_x < 2:
            new_x, new_y = blank_x + 1, blank_y
        elif direction == "left" and blank_y > 0:
            new_x, new_y = blank_x, blank_y - 1
        elif direction == "right" and blank_y < 2:
            new_x, new_y = blank_x, blank_y + 1
        else:
            return None  # Invalid direction

        # Swap the blank space with the tile in the specified direction
        new_board[blank_x][blank_y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[blank_x][blank_y]

        # Create a new node with the updated board
        new_node = Node()
        new_node.board = new_board
        new_node.g = copy.deepcopy(self.g) + 1  # copies the parent's g value and increments by 1
        new_node.h = copy.deepcopy(self.heuristic)  # copies parent's heuristic approach

        if new_node.heuristic == 1:
            manhattan(new_node)
        else:
            hamming(new_node)

        return new_node


    # returns the blank space of given board
    def findBlank(self):
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == "_":
                    return x, y


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


def goalNode():
    node = Node()
    node.board = [["_", 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]
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
        print("")


def findCoordinates(node, tile):
    for x in range(3):
        for y in range(3):
            if node.board[x][y] == tile:
                return x, y


# counts the number of misplaced tiles
def hamming(node):
    goal = goalNode()
    ham_distance = 0

    for x in range(3):
        for y in range(3):
            if node.board[x][y] != "_" and node.board[x][y] != goal.board[x][y]:
                ham_distance += 1

    node.h = ham_distance  # saves hamming heuristic of node
    node.f = node.g + node.h  # updates cost of path


# calculates how many moves are needed from initial to goal node
def manhattan(node):
    goal = goalNode()
    man_distance = 0

    for value in range(1, 9):  # for the tiles from 1 to 8
        initial_coordinates = findCoordinates(initial, value)  # finds coordinates of initial value
        goal_coordinates = findCoordinates(goal, value)  # finds coordinates of goal value
        row_difference = abs(initial_coordinates[0] - goal_coordinates[0])  # calculates total difference of row from initial node to goal node
        col_difference = abs(initial_coordinates[1] - goal_coordinates[1])  # calculates total difference of col from initial node to goal node

        man_distance += row_difference + col_difference  # sums up difference of row and col

    node.h = man_distance
    node.f = node.g + node.h


# main process
def solvePuzzle(node):
    print("Start Puzzle")
    printNode(initial)  # prints shuffled start node
    print()

    child_nodes = []
    directions = ["up", "down", "left", "right"]

    for direction in directions:  # loops the print of all child nodes for each possible direction
        child = node.childNode(direction)
        if child:
            child_nodes.append(child)
            print("child:")
            printNode(child)
            print("f: ", child.f)  # for testing
            print(" ")

    child_nodes.sort(key=lambda element: element.f)  # sorts the list of child nodes by f value

    for obj in child_nodes:
        print(obj.f)  # for testing - prints the sorted f values


if __name__ == '__main__':

    # testing
    initial = initialNode()
    if solvable(initial):
        solvePuzzle(initial)
