from copy import copy
from square import Square


class GuessChecker():
    def __init__(self):
        self.to_be_tested:set[Square] = set()
        self.known_squares:set[Square] = set()
        self.known_mines:set[Square] = set()
        self.unknown_squares:set[Square] = set()
        self.open_list:set[Square] = set()
    
    def test_square(self, square:Square)->bool:
        self.open_list.add(square)

        self.known_squares.clear()
        self.unknown_squares.clear()
        self.known_mines.clear()
        self.to_be_tested.clear()

        for test_square in square.all_squares.grid:
            if not isinstance(test_square, Square):
                continue

            if test_square.is_opened:
                self.open_list.add(test_square)
                for neighbour in test_square.neighbours.values():
                    if isinstance(neighbour,Square) and neighbour not in self.to_be_tested and not neighbour.is_opened:
                        self.to_be_tested.add(neighbour)
        
        # print(len(self.to_be_tested), " squares to be tested")

        changed_set:set[Square] = set()

        for test_square in self.to_be_tested:
            
            changed_set.clear()

            if test_square in self.unknown_squares:
                continue

            if test_square.require_guess(changed_squares=changed_set):
                self.unknown_squares.add(test_square)

                # print(f"Changed set size: {len(changed_set)}")
                # prev_length = len(self.unknown_squares)

                self.unknown_squares.update(changed_set)
                    
                # new_length = len(self.unknown_squares)

                # if new_length > prev_length:
                    # print(f"Memoisation added {new_length-prev_length}")



            else:
                if test_square.is_mine:
                    self.known_mines.add(test_square)
                else:
                    self.known_squares.add(test_square)
                


        # print("Guess Checker Status:", len(self.to_be_tested), len(self.known_squares), len(self.unknown_squares), square in self.known_squares)

        return self.check_guess_status()
        
    def check_guess_status(self)->bool:
        guess_required:bool = len(self.known_squares) == 0 or len(self.to_be_tested) == 0
        for square in self.open_list:
            square.enable_button()

        for square in self.known_squares.union(self.known_mines):
            square.change_solve_status(True)
            square.enable_button()
            if guess_required and not square.is_flagged:
                square._cell_flag('')


        maximum_clue_cells_around_unknown = 0

        unknown_cells:set[Square] = set()
        if guess_required:
            for square in self.unknown_squares:
                this_square_unopened_count:int = 0
                for neighbour in square.neighbours.values():
                    if isinstance(neighbour, Square) and not neighbour.is_mine and neighbour.is_opened:
                        this_square_unopened_count += 1
                if this_square_unopened_count == maximum_clue_cells_around_unknown:
                    unknown_cells.add(square)
                elif this_square_unopened_count > maximum_clue_cells_around_unknown:
                    maximum_clue_cells_around_unknown = this_square_unopened_count
                    unknown_cells.clear()
                    unknown_cells.add(square)
                


            
        for square in self.unknown_squares:
            square.change_solve_status(False)
            if guess_required and square in unknown_cells:
                square.enable_button()
            else:
                square.disable_button()

        return guess_required
