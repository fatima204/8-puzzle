import random


class Node:
    board = [["_", 1, 2],
             [3, 4, 5],
             [6, 7, 8]]
    g = 0
    h = 0
    f = 0


# creates a shuffled initial node
def initialNode():
    node = Node()
    flat = [element for sublist in node.board for element in sublist]  # flatten nested list using list comprehension
    random.shuffle(flat)  # shuffle the flattened list
    node.board = [flat[i:i + 3] for i in range(0, 9, 3)]  # recompose into nested list
    return node

# def initialNode():
#     node = Node()
#     node.board = [
#         [2, 3, 1],
#         [4, 5, 6],
#         [7, 8, "_"]
#     ]
#     return node

def goalNode():
    node = Node()
    node.board = [
        ["_", 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]
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


# prints the board of given node
def printNode(node):
    for x in range(3):
        for y in range(3):
            print(node.board[x][y], end=" ")
        print("")


# returns the blank space of given board
def findBlank(node):
    for x in range(3):
        for y in range(3):
            if node.board[x][y] == "_":
                return x, y


# counts the number of misplaced tiles
def hamming(node):
    misplaced_tiles = 0
    goal = [["_", 1, 2],
            [3, 4, 5],
            [6, 7, 8]]

    for x in range(3):
        for y in range(3):
            if node.board[x][y] != "_" and node.board[x][y] != goal[x][y]:
                misplaced_tiles += 1

    return misplaced_tiles

    # node.h = distance # saves hamming heuristic of node
    # node.f = node.g + node.h # updates cost of path


def findCoordinates(node, tile):
    for x in range(3):
        for y in range(3):
            if node.board[x][y] == tile:
                return x, y


def manhattan(node):  # calculates how many moves that are needed to move tiles from the initial node to goal node
    goal = goalNode()
    total_distance = 0

    for value in range(1, 9):  # for the tiles from 1 to 8
        initial_coordinates = findCoordinates(initial, value)  # finds coordinates of initial value
        goal_coordinates = findCoordinates(goal, value)  # finds coordinates of goal value
        # calculates total difference of row from initial node to goal node
        row_difference = abs(initial_coordinates[0] - goal_coordinates[0])
        # calculates total difference of col from initial node to goal node
        col_difference = abs(initial_coordinates[1] - goal_coordinates[1])

        # calculates distance of current tile
        distance = row_difference + col_difference  # sums up difference of row and col
        total_distance += distance  # sums up each additional distance when there is are new row and col differences

    return total_distance

if __name__ == '__main__':

    # testing
    initial = initialNode()
    goal = goalNode()
    print("Initial Node:")
    printNode(initial)
    print("---------------")
    print("Goal Node:")
    printNode(goal)
    print("---------------")
    manhattan = manhattan(initial)
    hamming = hamming(initial)
    print(f"Total Manhattan distance: {manhattan}")
    print(f"Total Hamming distance: {hamming}")
    # if solvable(initial):
    #     printNode(initial)
    #     hamming(initial)