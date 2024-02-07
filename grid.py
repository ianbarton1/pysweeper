from random import shuffle
from tkinter import Tk
import tkinter
from guess_checker import GuessChecker
from neighbour import Neighbour

import square


class Grid:
    def __init__(self, x:int, y:int, m:int, window:Tk, grid_string:str|None = None, open_string:str|None = None) -> None:
        self.tkinter_widget = tkinter.Frame(window)

        SUB_SAMPLE_SIZE:int = 5
        self.images_array:dict[tkinter.PhotoImage] = {i : tkinter.PhotoImage(file = f"assets/Minesweeper/MINESWEEPER_{i}.png").subsample(SUB_SAMPLE_SIZE,SUB_SAMPLE_SIZE) for i in range(9)}

        self.images_array['F'] = tkinter.PhotoImage(file=f"assets/Minesweeper/MINESWEEPER_F.png").subsample(SUB_SAMPLE_SIZE,SUB_SAMPLE_SIZE)
        self.images_array['M'] = tkinter.PhotoImage(file=f"assets/Minesweeper/MINESWEEPER_M.png").subsample(SUB_SAMPLE_SIZE,SUB_SAMPLE_SIZE)
        self.images_array['X'] = tkinter.PhotoImage(file=f"assets/Minesweeper/MINESWEEPER_X.png").subsample(SUB_SAMPLE_SIZE,SUB_SAMPLE_SIZE)

        self.images_array['F_KNOWN'] = tkinter.PhotoImage(file=f"assets/Minesweeper/MINESWEEPER_F_KNOWN.png").subsample(SUB_SAMPLE_SIZE,SUB_SAMPLE_SIZE)
        self.images_array['F_UNKNOWN'] = tkinter.PhotoImage(file=f"assets/Minesweeper/MINESWEEPER_F_UNKNOWN.png").subsample(SUB_SAMPLE_SIZE,SUB_SAMPLE_SIZE)

        self.images_array['X_KNOWN'] = tkinter.PhotoImage(file=f"assets/Minesweeper/MINESWEEPER_X_KNOWN.png").subsample(SUB_SAMPLE_SIZE,SUB_SAMPLE_SIZE)
        self.images_array['X_UNKNOWN'] = tkinter.PhotoImage(file=f"assets/Minesweeper/MINESWEEPER_X_UNKNOWN.png").subsample(SUB_SAMPLE_SIZE,SUB_SAMPLE_SIZE)



        img_size = self.images_array['X'].width()
        self.grid:list[square.Square] = [square.Square(is_mine = i < m, parent_grid = self.tkinter_widget, grid = self, square_index= i, images = self.images_array, image_size=img_size, enabled=False) for i in range(x*y)]

        if grid_string is not None and isinstance(grid_string, str) and len(grid_string) == x * y:
            for grid_index, grid_char in enumerate(grid_string):
                self.grid[grid_index].is_mine = bool(int(grid_char))
        else:
            shuffle(self.grid)

        for ind, cell in enumerate(self.grid):
            if isinstance(cell, square.Square):
                cell.square_index = ind

        self.x:int = x
        self.y:int = y
        self.m:int = m   
        
        #join neighbouring cells together baby
        for cell_index,cell in enumerate(self.grid):
            cell_address:tuple[int,int]|None = self.get_xy_from_index(cell_index)

            if cell_address is None:
                raise Exception('cell is not valid')

            for neighbour in Neighbour:
                match neighbour:
                    case Neighbour.TOP_LEFT:
                        self._set_neighbour(cell, cell_address, neighbour, -1, -1)
                    case Neighbour.TOP_MIDDLE:
                        self._set_neighbour(cell, cell_address, neighbour, 0, -1)
                    case Neighbour.TOP_RIGHT:
                        self._set_neighbour(cell, cell_address, neighbour, 1, -1)
                    case Neighbour.LEFT:
                        self._set_neighbour(cell, cell_address, neighbour, -1, 0)
                    case Neighbour.RIGHT:
                        self._set_neighbour(cell, cell_address, neighbour, 1, 0)
                    case Neighbour.BOTTOM_LEFT:
                        self._set_neighbour(cell, cell_address, neighbour, -1, 1)
                    case Neighbour.BOTTOM:
                        self._set_neighbour(cell, cell_address, neighbour, 0, 1)
                    case Neighbour.BOTTOM_RIGHT:
                        self._set_neighbour(cell, cell_address, neighbour, 1, 1)

        for cell_index,cell in enumerate(self.grid):
            this_x, this_y = self.get_xy_from_index(cell_index)
            # cell.button.grid(column=this_x, row=this_y,padx=2,pady=2)
            cell.button_frame.grid(column=this_x,row=this_y,padx=0,pady=0)
            # cell.button.place(x=this_x*10,y=this_y*10, width=1000,height=1000)

        for cell in self.grid:
            cell.calculate_clue()

        #find square with best opening:
        best_square:square.Square|None = None
        best_score:int = 0

        for index,current_square in enumerate(self.grid):
            this_score = current_square.opening_value()

            print(index,this_score)

            if best_square is None:
                best_square = current_square
                best_score = this_score
            
            if this_score > best_score:
                best_square = current_square
                best_score = this_score
        

        print(f'best score {best_score}')
        best_square.enable_button()            



        self.tkinter_widget.pack()
        self.guess_checker:GuessChecker = GuessChecker()

        self.uncovering_mines:bool = False

        if open_string is not None and isinstance(open_string, str) and len(open_string) == x * y:
            for open_index, open_char in enumerate(open_string):
                if bool(int(open_char)):
                    self.grid[open_index]._cell_action('')

    def _set_neighbour(self, cell, cell_address, neighbour, offset_x, offset_y):
        cell.neighbours[neighbour] = self.get_cell_from_grid_ref(cell_address[0] + offset_x, cell_address[1] + offset_y)

    def __repr__(self) -> str:
        grid_str:str = ""

        for cell_index,cell in enumerate(self.grid):
            grid_str += "M" if cell.is_mine else str(cell.clue)
            if (cell_index + 1) % self.x == 0:
                grid_str += "\n"


        return grid_str
    
    def get_cell_from_grid_ref(self, x:int, y:int)->square.Square|None:
        if (x < 0 or x >= self.x or y < 0 or y >= self.y):
            return None
        
        new_address:int = y * self.x + x

        return self.grid[new_address]
    
    def get_xy_from_index(self, index:int)->tuple[int,int]|None:
        if index < 0 or index >= self.x * self.y:
            return None
        
        return (index % self.x, index // self.x)
    
    def uncover_all_mines(self):
        if self.uncovering_mines:
            return
        
        self.uncovering_mines = True

        for squarex in self.grid:
            if not isinstance(squarex, square.Square):
                continue

            if squarex.is_mine and not squarex.is_flagged and not squarex.is_opened:
                squarex.enable_button()
                squarex.skip_check = True
                squarex._cell_action('')
                squarex.skip_check = False

        self.uncovering_mines = False

        return None