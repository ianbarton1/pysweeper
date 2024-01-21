from random import shuffle
from neighbour import Neighbour
from square import Square


class Grid:
    def __init__(self, x:int, y:int, m:int) -> None:
        self.grid:list[Square] = [Square(is_mine = i < m) for i in range(x*y)]

        self.x:int = x
        self.y:int = y
        self.m:int = m

        shuffle(self.grid)

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

            for cell in self.grid:
                cell.calculate_clue()
            

    def _set_neighbour(self, cell, cell_address, neighbour, offset_x, offset_y):
        cell.neighbours[neighbour] = self.get_cell_from_grid_ref(cell_address[0] + offset_x, cell_address[1] + offset_y)

    def __repr__(self) -> str:
        grid_str:str = ""

        for cell_index,cell in enumerate(self.grid):
            grid_str += "M" if cell.is_mine else str(cell.clue)
            if (cell_index + 1) % self.x == 0:
                grid_str += "\n"


        return grid_str
    
    def get_cell_from_grid_ref(self, x:int, y:int)->Square|None:
        if (x < 0 or x >= self.x or y < 0 or y >= self.y):
            return None
        
        new_address:int = y * self.x + x

        return self.grid[new_address]
    
    def get_xy_from_index(self, index:int)->tuple[int,int]|None:
        if index < 0 or index >= self.x * self.y:
            return None
        
        return (index % self.x, index // self.x)