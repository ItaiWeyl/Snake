from typing import Optional
from game_display import GameDisplay
import game_utils
from walls import *
from snake_def import *

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


class SnakeGame:
    """ The SnakeGame class represents a snake game with walls and apples.It manages the game state, including
    the snake's movement, walls placement, and apples consumption. The class provides methods to read user input, update
    game objects, draw the game board, and check for game over conditions. It also handles the management of walls and
    apples, including adding and drawing them on the game display."""

    def __init__(self, width, height, debug) -> None:
        self.__x = width
        self.__y = height
        self.__key_clicked = None
        self.cells_list = self.cell_list()
        self.snake = Snake(width // 2, height // 2)
        self.walls = []
        self.apples = []
        self.game_over = False
        self.round = 0
        self.score = 0
        self.debug = debug
        if self.debug:
            self.snake = None

    def read_key(self, key_clicked: Optional[str]) -> None:
        """ reads the key typed by the user to later use it and move the snake accordingly"""
        if self.debug:  # in case in debug mode, no need for user input
            return None
        self.__key_clicked = key_clicked
        self.snake.change_direction(key_clicked)

    def update_objects(self, num_of_walls, num_of_apples) -> None:
        """

        :param num_of_walls:
        :param num_of_apples:
        :return:
        """
        if self.debug:  # go to debug mode in case debug is on
            self.debug_mode(num_of_walls, num_of_apples)
            return None
        if 0 < self.snake.grow_count:  # a counter that determines if the snake needs to grow
            self.snake.add2snake(self.snake.tail.get_coordinate())
            self.snake.grow_count -= 1
        self.snake.move_snake()
        if self.round % 2 == 0:
            for wall in self.walls:
                wall.move()
        self.is_apple_eaten()
        self.check_wall_apple()
        self.remove_walls_outbound()
        if num_of_walls > len(self.walls):
            self.add_wall()
        if num_of_apples > len(self.apples):
            self.add_apple()

    def debug_mode(self, num_of_walls, num_of_apples):
        """ runs the game in debug mode - with only apples and walls. removing the snake from the game, and update the
        relevant objects in each round """
        if self.round % 2 == 0:
            for wall in self.walls:
                wall.move()
        self.check_wall_apple()
        self.remove_walls_outbound()
        if num_of_walls > len(self.walls):
            self.add_wall()
        if num_of_apples > len(self.apples):
            self.add_apple()
        return None

    def first_turn(self, num_of_walls, num_of_apples):
        """ performs the first round of the game (round zero). attempts to add an apple and a wall, without moving
        the snake yet"""
        if self.debug:  # in case debug mode is on, removing the snake
            self.snake = None
        if num_of_walls != 0:
            self.add_wall()
            self.check_wall_placement()
        if num_of_apples != 0:
            self.add_apple()

    def draw_board(self, gd: GameDisplay) -> None:
        """ uses the drawing function of each of the objects - snake, wall and apple. integrates all of them and prints
         the whole board """
        if not self.debug:  # drawing the snake only if not in debug mode
            self.draw_snake(gd)
        self.draw_apples(gd)
        for wall in self.walls:
            self.draw_wall(wall, gd)

    def end_round(self) -> None:
        """ checks if the game should finish. if not, update the rounds count by 1"""
        if not self.debug:
            self.check_wall_cut()
            if len(self.snake) == 1:  # in case a wall cut all the snake body besides his head
                self.game_over = True
        self.round += 1

    def cell_list(self):
        """ returns a list of all the cells in the board """
        cells_list = []
        for i in range(self.__x):
            for j in range(self.__y):
                cells_list.append((i, j))
        return cells_list

    def is_over(self) -> None:
        """ checks if the game should finish - in case the snake hit a wall with his head, crashed into himself or
         got out of the borders"""
        if self.debug:
            return None
        if self.snake.head.get_coordinate() not in self.cells_list:
            self.game_over = True
            self.snake.head = self.snake.head.get_next()  # updating the snake head_node so the game can draw the board
        elif self.snake.head.get_coordinate() in self.snake.get_snake_coordinates(True):
            self.game_over = True
            self.snake.head = self.snake.head.get_next()
        elif self.over_by_wall():
            self.game_over = True
            self.snake.head = self.snake.head.get_next()
        elif len(self.snake) == 1:
            self.game_over = True

    def is_game_over(self):
        """returns the game over attribute"""
        return self.game_over

    def draw_snake(self, gd):
        """
        draws the snake on the board according to its coordinates
        """
        current_node = self.snake.head
        while current_node:
            gd.draw_cell(current_node.get_coordinate()[0], current_node.get_coordinate()[1], self.snake.get_color())
            current_node = current_node.get_next()

    # METHODS REGARDING THE WALLS
    def add_wall(self):
        """
        adds a wall object to the wall list. it creates a wall object with random values from game_utils class and then
        checks if the wall placement isn't already taken, if it is taken, removes the new wall
        """
        random_wall = game_utils.get_random_wall_data()
        self.walls.append(Wall(random_wall[0], random_wall[1], random_wall[2]))
        self.check_wall_placement()

    def draw_wall(self, wall, gd):
        """
         draws all the walls on the board, draws only the parts that are in the limits of the board
        """
        for cell in wall.get_cells():
            if cell in self.cells_list:
                gd.draw_cell(cell[0], cell[1], BLUE)

    def walls_in_board(self):
        """
        returns the number of walls currently in the game
        """
        return len(self.walls)

    def remove_walls_outbound(self):
        """
        checks for all the walls that are out of the board completely, and remove them from the walls list
        """
        walls_to_remove = []
        for wall in self.walls:
            in_board = False
            for coordinate in wall.get_cells():
                if coordinate in self.cells_list:
                    in_board = True
            if not in_board:
                walls_to_remove.append(wall)
        for i in walls_to_remove:
            self.walls.remove(i)

    def over_by_wall(self):
        """
         a function that checks specifically if the snake's head crashed into a wall
         """
        head = self.snake.get_head()
        for wall in self.walls:
            if head.get_coordinate() in wall.get_cells():
                return True
        return False

    def check_wall_cut(self):
        """
        checks if the snake is overrun by one of the walls, if it is calls a function that cuts the snake in that place
        """
        if self.debug:
            return None
        snake_body = self.snake.get_snake_coordinates(False)
        for wall in self.walls:
            for i in wall.get_cells():
                if i in snake_body:
                    self.snake.cut_snake(i)

    def check_wall_placement(self):
        """
        checks if the wall that is pending to be added can use his location, or if the place is occupied
        """
        last_wall = self.walls[-1]
        for wall in self.walls[:-1]:
            for cor in last_wall.get_cells():
                if cor in wall.get_cells():
                    self.walls.remove(last_wall)
                    return None
        for cor in last_wall.get_cells():
            if cor in self.apples:
                self.walls.remove(last_wall)
                return None
        if not self.debug:
            snake_body = self.snake.get_snake_coordinates(False)
            for i in last_wall.get_cells():
                if i in snake_body:
                    self.walls.remove(last_wall)
                    return None

    # METHODS REGARDING THE APPLES
    def add_apple(self):
        """
        adds apple to the game, if the apple is in taken cell it doesn't add it
        """
        random_loc = game_utils.get_random_apple_data()
        new_apple = Apple(random_loc)
        if not self.debug:
            if new_apple.get_location() not in self.snake.get_snake_coordinates(False):
                if new_apple.get_location() not in self.apples:
                    self.apples.append(new_apple.get_location())
        else:
            self.apples.append(new_apple.get_location())

    def draw_apples(self, gd):
        """
        draw the apples in the board
        """
        for apple in self.apples:
            gd.draw_cell(apple[0], apple[1], GREEN)

    def is_apple_eaten(self):
        """
        checks if an apple was eaten by a snake this turn, if it is, remove the apple from the apples list, change the
        growing count of the snake and the score accordingly.
        """
        snake_head = self.snake.get_head().get_coordinate()
        for apple in self.apples:
            if apple[0] == snake_head[0] and apple[1] == snake_head[1]:
                self.apples.remove(apple)
                self.score += (len(self.snake) ** 0.5).__floor__()
                self.snake.grow_count += 3
                return True
        return False

    def check_wall_apple(self):
        """
        checks if an apple is run over by a wall and if it is, removes it from the apples list of the game
        """
        for wall in self.walls:
            for apple_loc in self.apples:
                if apple_loc in wall.get_cells():
                    self.apples.remove(apple_loc)
                    return True
        return False
