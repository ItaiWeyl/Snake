############################################################################
# GLOBAL VARIABLES:
UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"
BLACK = "black"
BLUE = "blue"
GREEN = "green"
############################################################################


class SnakeNode:
    """
    The SnakeNode class represents a node in a linked list structure for creating a snake. It stores a coordinate
    value and a reference to the next node. The class provides methods to get and set the coordinate value, as well
    as to set and get the next node.
    """
    def __init__(self, coordinate, next_node=None):
        self.__coordinate = coordinate
        self.__next = next_node

    def get_coordinate(self):
        return self.__coordinate

    def set_new_coordinate(self, coordinate):
        self.__coordinate = coordinate

    def set_next(self, next_node):
        self.__next = next_node

    def get_next(self):
        return self.__next


class Snake:
    """
    this class is made out of snake nodes connected to each other, when initializing an object, it gets the coordinate
    of the head of the snake, and adds 2 body nodes to create a snake in the len of 3, it also has direction that
    snake will move to according
    """

    def __init__(self, head_x, head_y):
        self.head = SnakeNode((head_x, head_y))
        self.head.set_next(SnakeNode((head_x, head_y - 1), SnakeNode((head_x, head_y - 2))))
        self.tail = self.head.get_next().get_next()
        self.direction = UP
        self.color = BLACK
        self.grow_count = 0

    def get_head(self):
        """ returns the snake's head node"""
        return self.head

    def get_color(self):
        """returns the color of the snake"""
        return self.color

    def move_head(self):
        """ moves the head of the snake according to the snake's direction attribute. """
        head_coordinate = self.head.get_coordinate()
        head_x = head_coordinate[0]
        head_y = head_coordinate[1]
        if self.direction == UP:
            self.head.set_new_coordinate((head_x, head_y + 1))
        elif self.direction == DOWN:
            self.head.set_new_coordinate((head_x, head_y - 1))
        elif self.direction == RIGHT:
            self.head.set_new_coordinate((head_x + 1, head_y))
        elif self.direction == LEFT:
            self.head.set_new_coordinate((head_x - 1, head_y))

    def move_snake(self):
        """ moves the rest of the snake's body after moving the head by calling the move_head() function. each node
         gets the location of the node it points to """
        next_coordinates = self.head.get_coordinate()
        self.move_head()
        current_node = self.head.get_next()
        while current_node:
            current_coordinates = current_node.get_coordinate()
            current_node.set_new_coordinate(next_coordinates)
            current_node = current_node.get_next()
            next_coordinates = current_coordinates

    def change_direction(self, direction=None):
        """ changes the snake's direction to the new direction given """
        if self.direction == UP or self.direction == DOWN:
            if direction == RIGHT or direction == LEFT:
                self.direction = direction
        if self.direction == RIGHT or self.direction == LEFT:
            if direction == UP or direction == DOWN:
                self.direction = direction

    def cut_snake(self, coordinate):
        """ cuts the linked list of the snake at the snake node that holds the given coordinate as data"""
        current = self.head
        while current:
            if current.get_next().get_coordinate() == coordinate:
                current.set_next(None)
                self.tail = current
            current = current.get_next()

    def __len__(self):
        """ a function that changes the snake's length"""
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.get_next()
        return count

    def get_snake_coordinates(self, without_head):
        """ returns a list of coordinates representing the snake's location. given a bool expression - without_head,
         the list will include the head's location if without_head = False"""
        current = self.head.get_next()
        coordinates = []
        if without_head and current:
            current = current.get_next()
        while current:
            coordinates.append(current.get_coordinate())
            current = current.get_next()
        return coordinates

    def add2snake(self, tail_coordinate):
        """ ads a new node to the snake using the snake's tail coordinate"""
        self.tail.set_next(SnakeNode(tail_coordinate))
        self.tail = self.tail.get_next()
