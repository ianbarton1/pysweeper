from neighbour import Neighbour


class Square:
    def __init__(self, is_mine:bool):
        self.is_mine:bool = is_mine
        self.neighbours:dict[Neighbour, Square|None] = {}

        for neighbour in Neighbour:
            self.neighbours[neighbour] = None

        self.is_opened: bool = False
        self.clue:int = 0
        self.calculate_clue()
        pass


    def calculate_clue(self):
        '''Recalcuate the clue value for this cell'''
        self.clue = 0
        #cycle through each neighbour and add to clue if it's a mine
        for neighbour in Neighbour:
            if self.neighbours[neighbour] and self.neighbours[neighbour].is_mine:
                self.clue += 1