import enum
from queue import Empty, Queue
import tkinter

from neighbour import Neighbour

class SquareSolveState(enum.Enum):
    Solveable = {'flag': 'F_KNOWN', 'normal': 'X_KNOWN'}
    NotSolveable = {'flag': 'F_UNKNOWN', 'normal': 'X_UNKNOWN'}
    Indeterminate = {'flag': 'F', 'normal': 'X'} 


class Square:
    def __init__(self, is_mine: bool, parent_grid: tkinter.Frame, grid, square_index, images, image_size:int, enabled:bool):
        self.is_mine: bool = is_mine
        self.neighbours: dict[Neighbour, Square | None] = {}
        self.square_index = square_index
        self.all_squares = grid

        self.images = images
        self.solve_status = SquareSolveState.Indeterminate
        self.skip_check = False

        for neighbour in Neighbour:
            self.neighbours[neighbour] = None

        self.is_opened: bool = False
        self.clue: int = 0
        self.is_flagged:bool = False
        self.calculate_clue()

        self.parent_grid = parent_grid
        self.button_frame = tkinter.Frame(parent_grid)
        self.button = tkinter.Button(self.button_frame,image=self.images['X'], width=image_size, height=image_size, compound='c', state='normal')
        self.button.pack(padx=0,pady=0)

        self.enabled = not enabled

        if enabled:
            self.enable_button()
        else:
            self.disable_button()

        self.locked_reference_count:int = 0  #this will be used to check whether the square has been locked when implementing the guardian functionality

    def enable_button(self):
        if self.enabled:
            return    
        self.enabled = True

        self.button.bind("<Button-1>", self._cell_action)
        self.button.bind("<Button-2>", self._cell_guardian)
        self.button.bind("<Button-3>", self._cell_flag)

        self.button.configure(state='normal')

    def disable_button(self):
        if not self.enabled:
            return
        self.enabled = False

        self.button.unbind("<Button-1>")
        self.button.unbind("<Button-2>")
        self.button.unbind("<Button-3>")
        self.button.configure(state='disabled')

    def count_mines_around(self)->int:
        mine_count = 0
        # cycle through each neighbour and add to clue if it's a mine
        for neighbour in Neighbour:
            if self.neighbours[neighbour] and self.neighbours[neighbour].is_mine:
                mine_count += 1
        
        return mine_count
    
    def count_flags_around(self)->int:
        flag_count = 0
        # cycle through each neighbour and add to clue if it's a mine
        for neighbour in Neighbour:
            if self.neighbours[neighbour] and self.neighbours[neighbour].is_flagged:
                flag_count += 1
        
        return flag_count


    def calculate_clue(self):
        '''Recalcuate the clue value for this cell'''

        self.clue = self.count_mines_around()
        # try:
        #     if not self.is_opened:
        #         self.button.configure(
        #         text=self.clue if not self.is_mine else 'X', state='normal', foreground='black', background='yellow')
        # except AttributeError:
        #     pass
    

    def _cell_guardian(self, _):
        if True:
            return_code:bool = guardian(self, False)
            print("Guardian ran (output was): ",return_code)


    def _cell_action(self, arg):
        if self.is_flagged:
            return
        # button_location_x, button_location_y  = self.button.grid_location()

        # print(self.is_opened,self.count_flags_around(), self.clue)

        if self.is_opened and self.clue > 0 and self.count_flags_around() == self.clue:
            for neighbour in self.neighbours.values():
                if isinstance(neighbour, Square) and not neighbour.is_opened:
                    neighbour._cell_action("")
            return
        
        if self.is_opened:
            return
        
        if not self.skip_check:
            self.all_squares.guess_checker.test_square(self)
                
        if self.is_mine and not self.skip_check:
            # guardian_is_active = self.require_guess()
            guardian_is_active = self.all_squares.guess_checker.check_guess_status()
            print("Guardian Status: ",guardian_is_active)
            if guardian_is_active:
                print("Guardian process ran Status: ",guardian(self, True))

        if self.is_mine:
            self.all_squares.uncover_all_mines()

        self.is_opened = True

        

        # self.button.configure(
        #     image = self.images[self.clue] if not self.is_mine else self.images['M'], state='normal', command=None)
        
        if self.clue == 0 and not self.is_mine:
            self.button.config(image=self.images[0], state='disabled')
            self.skip_check = True
            for neighbour in self.neighbours.values():
                if isinstance(neighbour, Square):
                    if not neighbour.is_opened:
                        neighbour.enable_button()
                        neighbour.skip_check = True
                        neighbour._cell_action(None)
                        neighbour.skip_check = False
            self.skip_check = False

        
        if arg is not None and not self.skip_check:
            self.all_squares.guess_checker.test_square(self)

        
        # print("Is Guess Required: ", self.all_squares.guess_checker.check_guess_status())
        self.skip_check = False

        # print("Is Guess Required: ", self.require_guess())

        self.update_tile()
        
        

    def require_guess(self):
        # guess_required:bool = True

        # last_square_check:bool = True
        # for cell_ind,cell in enumerate(self.all_squares.grid):
        #     if isinstance(cell, Square) and not cell.is_opened and not cell.is_mine:
        #         last_square_check = False
        #         if not guardian(cell, False):
        #             guess_required = False
        #             break
        
        # if last_square_check:
        #     guess_required = False

        
        return guardian(self, False)
            

    def _cell_flag(self, _):
        if self.is_opened:
            return

        self.is_flagged ^= True

        self.update_tile()


    def _open_mines(self):
        for square in self.all_squares.grid:
            if isinstance(square, Square):
                if square.is_mine and square.is_opened:
                    self._cell_action(None)

    def change_solve_status(self, known:bool|None):
        if known:
            self.solve_status = SquareSolveState.Solveable
        elif not known and known is not None:
            self.solve_status = SquareSolveState.NotSolveable
        else:
            self.solve_status = SquareSolveState.Indeterminate

        self.update_tile()

    def update_tile(self):
        if not self.is_opened:
            if self.is_flagged:
                self.button.configure(image = self.images[self.solve_status.value['flag']])
            else:
                self.button.configure(image = self.images[self.solve_status.value['normal']])
        else:
            if self.is_mine:
                self.button.configure(image = self.images['M'])
            else:
                self.button.configure(image = self.images[self.clue])

    def opening_value(self)->int:
        '''Return how many squares will be opened by this square'''

        if self.is_mine:
            return 0
        elif self.clue > 0:
            return 1
        
        opened_squares:set[Square] = set()

        to_be_opened_queue:Queue[Square] = Queue()
        to_be_opened_queue.put(self)

        queue_hit_test:set[Square] = set()
        queue_hit_test.add(self)

        while to_be_opened_queue.not_empty:
            try:
                current_square = to_be_opened_queue.get_nowait()
            except Empty:
                break
            
            print(to_be_opened_queue.qsize())
            opened_squares.add(current_square)

            for neighbour in current_square.neighbours.values():
                if isinstance(neighbour,Square):
                    if neighbour not in opened_squares.union(queue_hit_test):
                        if neighbour.clue == 0:
                            to_be_opened_queue.put(neighbour)
                            queue_hit_test.add(neighbour)
                        else:
                            opened_squares.add(neighbour)

        return len(opened_squares)
                        
    
        

def guardian(start_square:Square, make_changes:bool = True)->bool:
    '''

    
    
    '''
    mine_count_change:int = 0

    start_square.is_mine ^= True

    if start_square.is_mine:
        mine_count_change = 1
    else:
        mine_count_change = -1

    start_square.locked_reference_count += 1

    constraints_to_satisfy:list[Square] = []
    # do something

    for neighbour in start_square.neighbours.values():
        if isinstance(neighbour,Square):
            if not neighbour.is_mine:
                if neighbour.is_opened:
                    constraints_to_satisfy.append(neighbour)
    
    # print("Before the first call", len(constraints_to_satisfy))

    if fix_constraint(0, constraints_to_satisfy, mine_count_change, start_square, make_changes):

        # print("after_calls:", len(constraints_to_satisfy))

        if not make_changes:
            start_square.is_mine ^= True
        start_square.locked_reference_count = 0

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
            
            if this_square.locked_reference_count != 0:
                print (Exception(f'{this_square.square_index} cell remains locked!'))
            
        

        return True


    start_square.is_mine ^= True
    start_square.locked_reference_count = 0

    return False


def fix_constraint(constraint_index:int, constraint_list:list, mine_count_change:int, ref_square:Square, make_changes:bool)->bool:
    # print("constraint_index:", constraint_index, len(constraint_list), mine_count_change)
    try:
        current_square:Square = constraint_list[constraint_index]
    except IndexError:
        if correct_mine(ref_square, mine_count_change, make_changes):
            return True
        
        return False
       
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

        if fix_constraint(constraint_index+1, constraint_list, mine_count_change, ref_square, make_changes):
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

                if neighbour.is_mine:
                    mine_count_change += 1
                else:
                    mine_count_change -= 1

                new_constraints_added:int = 0

                #add neighbouring constraints (if not already in the constraint list)
                for new_constraint in neighbour.neighbours.values():
                    if isinstance(new_constraint, Square):
                        if not new_constraint.is_mine:
                            if new_constraint.is_opened and new_constraint not in constraint_list:
                                constraint_list.append(new_constraint)
                                new_constraints_added += 1

                if fix_constraint(constraint_index, constraint_list, mine_count_change,ref_square, make_changes):
                    if not make_changes:
                        neighbour.is_mine ^= True
                    
                    neighbour.locked_reference_count -= 1

                    return True
                
                for i in range(new_constraints_added):
                    constraint_list.pop()
                
                neighbour.is_mine ^= True
                neighbour.locked_reference_count -= 1
                
                if neighbour.is_mine:
                    mine_count_change += 1
                else:
                    mine_count_change -= 1

    return False

def correct_mine(start_square:Square, mine_difference:int, make_changes:bool)->bool:
    '''
        attempt to correct a mine difference by hiding/removing mine elsewhere
    '''
    
    # print("correct_mine", mine_difference)
    if mine_difference == 0:
        return True
    
    if mine_difference < 0:
        mine_to_flip:bool = False
    elif mine_difference > 0:
        mine_to_flip:bool = True
    
    seen:set[Square] = set()
    to_be_done:Queue[Square]= Queue()

    to_be_done.put(start_square)
    seen.add(start_square)

    while to_be_done.not_empty:
        try:
            this_square = to_be_done.get(block=False)
        except Empty:
            break
        
        this_square_valid:bool = True

        if not this_square.is_opened and this_square.is_mine == mine_to_flip and this_square != start_square:
            this_square_valid = True
        else:
            this_square_valid = False


        for neighbour in this_square.neighbours.values():
            # print(neighbour, neighbour not in seen)
            if isinstance(neighbour, Square) and neighbour not in seen:
                to_be_done.put(neighbour)
                seen.add(neighbour)

            if isinstance(neighbour, Square) and neighbour.is_opened:
                this_square_valid = False

        if this_square_valid:
            # print(this_square.button)
            this_square.is_mine ^= True
            this_square.locked_reference_count += 1

            if this_square.is_mine:
                mine_difference += 1
            else:
                mine_difference -= 1

            if correct_mine(start_square, mine_difference, make_changes):
                if not make_changes:
                    this_square.is_mine ^= True

                this_square.locked_reference_count -= 1
                return True
            else:
                this_square.is_mine ^= True
                this_square.locked_reference_count -= 1
    
    return False
    


    
