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
        
        print(len(self.to_be_tested), " squares to be tested")

       

        for test_square in self.to_be_tested:
            if test_square.require_guess():
                self.unknown_squares.add(test_square)
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
            
        for square in self.unknown_squares:
            square.change_solve_status(False)
            if guess_required:
                square.enable_button()
            else:
                square.disable_button()


        return guess_required
