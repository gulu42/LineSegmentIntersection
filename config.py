from tkinter import Tk,Canvas,YES,BOTH

canvas_width = 500
canvas_height = 500

master = Tk()
drawing_board = Canvas(master,
           width=canvas_width,
           height=canvas_height) # create a canvas
drawing_board.pack(expand = YES, fill = BOTH)

sweep_y = []
