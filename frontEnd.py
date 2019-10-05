from utils import Point,Line
from logicBlock import Sweeper
from tkinter import *
import sys

canvas_width = 500
canvas_height = 500

# 0 if all points are paired
# 1 if there is an un-paired point
points_modulo = 0
px = 0
py = 0

fh = open("data_files/temp_data.txt","w+")

def empty_event(event):
   pass

def draw_point(event):
   python_green = "#476042"
   global points_modulo,px,py

   print("Mouse position:",event.x,event.y)
   x1, y1 = ( event.x - 1 ), ( event.y - 1 )
   x2, y2 = ( event.x + 1 ), ( event.y + 1 )
   drawing_board.create_oval( x1, y1, x2, y2, fill = python_green )

   if points_modulo == 0:
      px,py = event.x,event.y
      points_modulo = 1
   else:
      points_modulo = 0
      drawing_board.create_line(px,py,event.x,event.y)
      fh.write(str(px) + " " + str(py) + " " + str(event.x) + " " + str(event.y) + "\n")
      # write the line correcting for x and y

def button_clicked():
   print("Button was pressed")

def run_eval():
   print("Evaluation running")
   fh.close()
   sweep_obj = Sweeper("temp_data.txt")
   sweep_obj.run()
   print("Eval complete")
   sys.exit(0)

def draw_sweep_line():
   print("Call to update the sweep line position")

def draw_intersection_point():
   print("call to draw a new intersection point")

master = Tk()
master.title("Line Segment Intersection")
drawing_board = Canvas(master,
           width=canvas_width,
           height=canvas_height) # create a canvas
drawing_board.pack(expand = YES, fill = BOTH)
drawing_board.bind("<Button-1>",draw_point)

start_button = Button(master,text = "Start Evaluation",command = run_eval)
start_button.pack(side = LEFT)

mainloop()


# if __name__ == "__main__":
#     data_file = "data_2.txt"
#     sweep_obj = Sweeper(data_file)
#     sweep_obj.run()
