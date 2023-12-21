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
    distance = 0
    goal = [["_", 1, 2],
            [3, 4, 5],
            [6, 7, 8]]

    for x in range(3):
        for y in range(3):
            if node.board[x][y] != "_" and node.board[x][y] != goal[x][y]:
                distance += 1

    node.h = distance # saves hamming heuristic of node
    node.f = node.g + node.h # updates cost of path


if __name__ == '__main__':

    # testing
    initial = initialNode()
    if solvable(initial):
        printNode(initial)
        hamming(initial)