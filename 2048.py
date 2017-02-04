"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = sort_zeros(list(line))
    for index in range(1, len(result)):
        if result[index] == result[index - 1]:
            result[index - 1] = result[index - 1] * 2
            result[index] = 0
    
    result = sort_zeros(result)
    return result

def sort_zeros(unsorted):
    """
    Helper function to aid in sorting of result list.
    Moves zeros to end of list
    """
    count = 0
    for element in list(unsorted):
        if element == 0:
            unsorted.remove(element)
            count += 1
    sorted_list = unsorted + [0]*count     
    return sorted_list


                
class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height = 4, grid_width = 4):
        """
        Initialization method
        """
        self._grid_rows = grid_height
        self._grid_columns = grid_width
        
        #List of initial tiles for each direction
        self._up_list = [(0,col_element) for col_element in range(self._grid_columns)]
        self._down_list = [(self._grid_rows - 1, col_element) for col_element in range(self._grid_columns)]
        self._left_list = [(row_element, 0) for row_element in range(self._grid_rows)]
        self._right_list = [(row_element, self._grid_columns - 1) for row_element in range(self._grid_rows)]
        
        self._initials = {UP: self._up_list, DOWN: self._down_list,
                          LEFT: self._left_list, RIGHT: self._right_list}
        
        
        self.reset()
        

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._grid_columns)]
                for dummy_row in range(self._grid_rows)]
        
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string = ''
        for dummy_index in range(self._grid_rows):
            string += str(self._grid[dummy_index]) + '\n'
        return string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_rows

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_columns
    
    def traverse_grid(self, start_cell, direction, num_steps):
        """
        Function that linearly traverses through cells
        in a grid in given direction.
        """
        tiles = []
        
        for step in range(num_steps):
            row = start_cell[0] + step * direction[0]
            col = start_cell[1] + step * direction[1]
            tiles.append([row, col])
        return tiles    

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        
        self._grid_before = str(self._grid)
        grid_ends = {UP: self._grid_rows, DOWN: self._grid_rows,
                     LEFT: self._grid_columns, RIGHT: self._grid_columns}
        
        linear_list = []
        coord_list = []
        
        self._initial_tiles = self._initials[direction]            
        
        for tile in self._initial_tiles:
            coord_list.append(self.traverse_grid(tile, OFFSETS[direction], grid_ends[direction]))
        #print coord_list 
        
        for coord_set in coord_list:
            temp_list = []
            for coord in coord_set:
                temp_list.append(self._grid[coord[0]][coord[1]])
            
            linear_list.append(temp_list)
            
        #print linear_list                         
        
        merged_list = []
        for line in list(linear_list):
            merged_list.append(merge(line))
            
        #print merged_list    
        merged_sum = []
        
        for line in merged_list:
            merged_sum += line
        #print merged_sum    
        
        coord_sum = []
        for coord_set in coord_list:
            coord_sum += coord_set
        #print coord_sum    
        
        for index in range(len(coord_sum)):
            self.set_tile(coord_sum[index][0], coord_sum[index][1], merged_sum[index])
                
        gridlist = []
        for line in self._grid:
            gridlist += line
            
       

        if 0 in gridlist and self._grid_before != str(self._grid):
            self.new_tile()
        #print gridlist    
        

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        
        #Get indices of squares which are empty
        zero_indices = [[(row,col) for col in range(self._grid_columns) if self._grid[row][col] == 0]
                for row in range(self._grid_rows)]

        zeros = []

        for element in range(self._grid_rows):
            zeros += zero_indices[element]
    
        #Select random empty square in grid
        random_square = random.choice(zeros)
        
        #Set random aquare to be either 2 or 4,
        #depending on probability distribution
        
        chance = random.random()
        if chance < 0.9:
            self.set_tile(random_square[0], random_square[1], 2)
            
        elif chance >= 0.9:
            self.set_tile(random_square[0], random_square[1], 4)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

#item = TwentyFortyEight(4,4)
#print item
#item.move(3)
#print item


#import user40_PMwU4nFmik_2 as test_2048
#test_2048.run_test(TwentyFortyEight)
poc_2048_gui.run_gui(TwentyFortyEight(5, 3))
