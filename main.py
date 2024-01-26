from grid import Grid
import tkinter as ui

main_window = ui.Tk()

# grid = Grid(10, 10, 20, main_window)
#first_guess_scenario https://minesweepergame.com/strategy/guessing.php
# grid = Grid(7, 4, 0, main_window, "0000000011111000010000000000", "0000000000000011101111110111")
#second_scenario https://minesweepergame.com/strategy/guessing.php
# grid = Grid(5, 5, 0, main_window, "0000001010110100001000000", "0000000001001011110111111")


#thirda 1 mine
# grid = Grid(5, 5, 0, main_window, "0000001000001000000000000", "0011100111110111111111111")
# third 2 mine
# grid = Grid(5, 5, 0, main_window, "0100010000001000000000000", "0011100111110111111111111")
#third 3 mine
grid = Grid(5, 5, 0, main_window, "1100010000001000000000000", "0011100111110111111111111")

#


main_window.mainloop()

print(grid)