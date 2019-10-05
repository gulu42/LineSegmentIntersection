from utils import Point,Line
from logicBlock import Sweeper
from tkinter import *

canvas_width = 500
canvas_height = 500


if __name__ == "__main__":
    data_file = "data_2.txt"
    sweep_obj = Sweeper(data_file)
    sweep_obj.run()
