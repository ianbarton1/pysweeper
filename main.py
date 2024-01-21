from grid import Grid
import tkinter as ui

main_window = ui.Tk()

grid = Grid(10, 10, 20, main_window)

main_window.mainloop()

print(grid)