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


class Wall:
    """The Wall class represents a structure in a grid. It is used to create walls within the grid. The wall
     is initialized with a position (x, y) and a direction, which determines its orientation. The wall consists
     of three cells arranged either horizontally or vertically, depending on the direction."""
    def __init__(self, x, y, direction):
        self.__direction = direction
        self.__cells = []
        if self.__direction == RIGHT or self.__direction == LEFT:
            self.__cells.append((x - 1, y))
            self.__cells.append((x, y))
            self.__cells.append((x + 1, y))
        else:
            self.__cells.append((x, y - 1))
            self.__cells.append((x, y))
            self.__cells.append((x, y + 1))

    def move(self):
        """ moves the wall according to the direction attribute"""
        if self.__direction == RIGHT:
            self.__cells[0] = self.__cells[1]
            self.__cells[1] = self.__cells[2]
            self.__cells[2] = (self.__cells[2][0] + 1, self.__cells[2][1])
        elif self.__direction == LEFT:
            self.__cells[2] = self.__cells[1]
            self.__cells[1] = self.__cells[0]
            self.__cells[0] = (self.__cells[0][0] - 1, self.__cells[0][1])
        elif self.__direction == UP:
            self.__cells[0] = self.__cells[1]
            self.__cells[1] = self.__cells[2]
            self.__cells[2] = (self.__cells[2][0], self.__cells[2][1] + 1)
        elif self.__direction == DOWN:
            self.__cells[2] = self.__cells[1]
            self.__cells[1] = self.__cells[0]
            self.__cells[0] = (self.__cells[0][0], self.__cells[0][1] - 1)

    def get_cells(self):
        """
        returns the coordinates of the wall
        """
        return self.__cells


class Apple:
    """ The Apple class represents an apple in the game. It contains a location coordinate that represents the position
         of the apple on the game grid. The Apple class also has a color attribute. It provides a method to retrieve the
          location of the apple."""

    def __init__(self, location):
        self.location = location
        self.color = GREEN

    def get_location(self):
        """ return a tuple of the apple's location"""
        return self.location
