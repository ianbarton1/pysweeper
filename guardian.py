import square
from queue import Queue


def run_guardian_process(start_square:square.Square):
    '''
        Given a starting square automagically move mines away from the player
        if it is possible.

        Two parts will be required, a recursive solver for the "frontier"
        and a way to give/borrow mines back to the "unexplored" areas of the playfield.
   
    '''

    constraints_to_be_fixed:Queue[square.Square] = Queue()
    constraints_seen:set[square.Square] = set()

    #pre
    start_square.locked_reference_count += 1
    change_mine_state(start_square)
    constraints_seen.add(start_square)

    #recurse
    for neighbour in start_square.neighbours.values():
        if isinstance(neighbour, square.Square):
            if neighbour.is_opened and not neighbour.is_mine:
                constraints_to_be_fixed.put(neighbour)

    # print(constraints_to_be_fixed)
    input()

    #post
    start_square.locked_reference_count -= 1
    constraints_seen.remove(start_square)
    change_mine_state(start_square)


def fix_constraint(constraint_square:square.Square):
    '''
        Takes a square which has the following properties.

        1.) Is a clue square (i.e. a constraint)
        2.) Is open (the player can see this clue square)
        3.) Has been put into an inconsitent state from another constraint being fixed.
   
        Attempts to fix this constraint and continues until all constraints are either solved
   '''
    
def change_mine_state(square:square.Square):
    '''
        Flips the square to the other state i.e. a mine will become a free space, a free space becomes a mine.
    
    '''
    square.is_mine ^= True