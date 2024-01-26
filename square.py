from queue import Empty, Queue
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
        try:
            if not self.is_opened:
                self.button.configure(
                text=self.clue if not self.is_mine else 'X', state='normal', foreground='black', background='yellow')
        except AttributeError:
            pass
        

    def _cell_action(self, _):
        if self.is_flagged:
            return
        
        self.is_opened = True
        # button_location_x, button_location_y  = self.button.grid_location()

        if self.is_mine:
            return_code:bool = guardian(self)
            print("Guardian ran (output was): ",return_code)

        self.button.configure(
            text=self.clue if not self.is_mine else 'X', state='normal', command=None, background='white')
        
        
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


def guardian(start_square:Square)->bool:
    '''

    
    
    '''
    if not start_square.is_mine:
        return

    start_square.is_mine = False
    start_square.locked_reference_count += 1

    constraints_to_satisfy:list[Square] = []
    # do something

    for neighbour in start_square.neighbours.values():
        if isinstance(neighbour,Square):
            if not neighbour.is_mine:
                if neighbour.is_opened:
                    constraints_to_satisfy.append(neighbour)
    
    # print("Before the first call", len(constraints_to_satisfy))

    if fix_constraint(0, constraints_to_satisfy):

        # print("after_calls:", len(constraints_to_satisfy))

        seen:set[Square] = set()
        to_be_done:Queue[Square]= Queue()

        to_be_done.put(start_square)
        seen.add(start_square)

        while to_be_done.not_empty:
            # print("qsize",to_be_done.qsize(), "seen", len(seen))
            try:
                this_square = to_be_done.get(block=False)
            except Empty:
                break
            

            for neighbour in this_square.neighbours.values():
                # print(neighbour, neighbour not in seen)
                if isinstance(neighbour, Square) and neighbour not in seen:
                    to_be_done.put(neighbour)
                    seen.add(neighbour)

            
            this_square.calculate_clue()
            if this_square.clue != this_square.count_mines_around():
                raise Exception('Clue square mismatch')

        return True


    start_square.is_mine = True
    start_square.locked_reference_count = 0

    return False


def fix_constraint(constraint_index:int, constraint_list:list)->bool:
    print("constraint_index:", constraint_index, len(constraint_list))
    try:
        current_square:Square = constraint_list[constraint_index]
    except IndexError:
        return True
    
    print(current_square.clue, current_square.is_mine, current_square.is_opened)
    
    target_count:int = current_square.clue
    current_count:int = current_square.count_mines_around()
    
    if target_count < current_count:
        mine_to_flip = True
    elif target_count > current_count:
        mine_to_flip = False
    else:

        for neighbour in current_square.neighbours.values():
            if isinstance(neighbour, Square):
                neighbour.locked_reference_count += 1

        if fix_constraint(constraint_index+1, constraint_list):
                for neighbour in current_square.neighbours.values():
                    if isinstance(neighbour, Square):
                        neighbour.locked_reference_count -= 1       
                return True
        else:
            for neighbour in current_square.neighbours.values():
                if isinstance(neighbour, Square):
                    neighbour.locked_reference_count -= 1
            return False


    for neighbour in current_square.neighbours.values():
        if isinstance(neighbour, Square):
            if neighbour.is_mine == mine_to_flip and neighbour.locked_reference_count == 0 and not neighbour.is_opened:
                neighbour.is_mine ^= True
                neighbour.locked_reference_count += 1

                new_constraints_added:int = 0

                #add neighbouring constraints (if not already in the constraint list)
                for new_constraint in neighbour.neighbours.values():
                    if isinstance(new_constraint, Square):
                        print(constraint_index, new_constraint.clue, new_constraint.locked_reference_count)
                        if not new_constraint.is_mine:
                            if new_constraint.is_opened and new_constraint not in constraint_list:
                                constraint_list.append(new_constraint)
                                new_constraints_added += 1

                if fix_constraint(constraint_index, constraint_list):
                    return True
                
                for i in range(new_constraints_added):
                    constraint_list.pop()
                
                neighbour.is_mine ^= True
                neighbour.locked_reference_count -= 1

    return False


    


    
