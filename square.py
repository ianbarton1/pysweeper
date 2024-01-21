from queue import Queue
import tkinter

from neighbour import Neighbour


class Square:
    def __init__(self, is_mine: bool, parent_grid: tkinter.Frame):
        self.is_mine: bool = is_mine
        self.neighbours: dict[Neighbour, Square | None] = {}

        for neighbour in Neighbour:
            self.neighbours[neighbour] = None

        self.is_opened: bool = False
        self.clue: int = 0
        self.is_flagged:bool = False
        self.calculate_clue()

        self.parent_grid = parent_grid
    
        self.button = tkinter.Button(parent_grid, width=1, height=2, text=self.clue if not self.is_mine and self.is_opened else '', font=(
            'arial', 12))
        
        self.button.bind("<Button-1>", self._cell_action)
        self.button.bind("<Button-2>", self._cell_flag)
        self.button.bind("<Button-3>", self._cell_flag)

        self.locked_reference_count:int = 0 #this will be used to check whether the square has been locked when implementing the guardian functionality

    def count_mines_around(self)->int:
        mine_count = 0
        # cycle through each neighbour and add to clue if it's a mine
        for neighbour in Neighbour:
            if self.neighbours[neighbour] and self.neighbours[neighbour].is_mine:
                mine_count += 1
        
        return mine_count


    def calculate_clue(self):
        '''Recalcuate the clue value for this cell'''

        self.clue = self.count_mines_around()
        

    def _cell_action(self, _):
        if self.is_flagged:
            return
        
        self.is_opened = True
        # button_location_x, button_location_y  = self.button.grid_location()

        if self.is_mine:
            pass

        self.button.configure(
            text=self.clue if not self.is_mine else 'X', state='normal', command=None)
        
        
        if self.clue == 0 and not self.is_mine:
            self.button.config(text="", state='disabled', background='blue')
            for neighbour in self.neighbours.values():
                if isinstance(neighbour, Square):
                    if not neighbour.is_opened:
                        neighbour._cell_action("")

    def _cell_flag(self, _):
        if self.is_opened:
            return

        self.is_flagged ^= True

        if self.is_flagged:
            self.button.configure(text="Flag")
        else:
            self.button.configure(text="")


