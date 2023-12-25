import random


class Node:
    board = [["_", 1, 2],
             [3, 4, 5],
             [6, 7, 8]]
    g = 0
    h = 0
    f = 0

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
    return node


# checks inversion count of given node
def solvable(node):
    count = 0
    flat = [element for sublist in node.board for element in sublist]
    not_solvable = "Random Puzzle is not solvable - Please try again!"
    for x in range(len(flat) - 1):
        for y in range(x, len(flat)):
            if flat[x] == "_" or flat[y] == "_":
                continue  # ignores the blank space
            if flat[x] > flat[y]:
                count += 1

    if count % 2 == 0:  # if inversion count is even = solvable
        return True
    else: return print(not_solvable)


# prints the board of given node
def printNode(node):
    for x in range(3):
        for y in range(3):
            print(node.board[x][y], end=" ")
        print("")


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

    node.h = distance  # saves hamming heuristic of node
    node.f = node.g + node.h  # updates cost of path


if __name__ == '__main__':

    # testing
    initial = initialNode()
    if solvable(initial):
        printNode(initial)

        directions = ["up", "down", "left", "right"]
        for direction in directions:
            child = initial.childNode(direction)
            if child:
                printNode(child)
        #hamming(initial)
