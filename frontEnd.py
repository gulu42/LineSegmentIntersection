from utils import Point,Line
from logicBlock import Sweeper
from tkinter import *
import sys
import time
import config

# 0 if all points are paired
# 1 if there is an un-paired point
points_modulo = 0
px = 0
py = 0

fh = open("data_files/temp_data.txt","w+")

def draw_point(x,y):
   c = 'deep pink'
   size = 3
   x1, y1 = ( x - size ), ( y - size )
   x2, y2 = ( x + size ), ( y + size )
   config.drawing_board.create_oval( x1, y1, x2, y2, fill = c )

def empty_event(event):
   pass

def input_lines(event):
   python_green = "#476042"
   global points_modulo,px,py

   print("Mouse position:",event.x,event.y)
   x1, y1 = ( event.x - 1 ), ( event.y - 1 )
   x2, y2 = ( event.x + 1 ), ( event.y + 1 )
   config.drawing_board.create_oval( x1, y1, x2, y2, fill = python_green )

   if points_modulo == 0:
      px,py = event.x,event.y
      points_modulo = 1
   else:
      points_modulo = 0
      config.drawing_board.create_line(px,py,event.x,event.y)
      fh.write(str(px) + " " + str(py) + " " + str(event.x) + " " + str(event.y) + "\n")
      # write the line correcting for x and y

def draw_sweep_line(p):
   config.drawing_board.create_line(0,p.y,config.canvas_width-1,p.y,fill="green")
   draw_point(p.x,p.y)

def run_eval(button_obj):

   # hide the button after its been clicked
   button_obj.pack_forget() #passed as param
   print("Evaluation running")
   fh.close()

   # sweep_obj = Sweeper("temp_testing.txt")
   sweep_obj = Sweeper("temp_data.txt")
   sweep_obj.run()
   print("Eval complete. Running animation")
   print(config.sweep_y)

   delay = 0
   delay_amount =200
   num_artifacts = 2#drawing two things and the first one is the line
   n = config.drawing_board.create_oval(0,0,1,1)
   for p in config.sweep_y:
      print(p)
      config.drawing_board.after(delay,draw_sweep_line,p)
      n += num_artifacts
      print(n)
      delay += delay_amount
      config.drawing_board.after(delay,config.drawing_board.delete,n - (num_artifacts - 1))
      delay += delay_amount
   config.sweep_line = []
   print("Animation complete")

def temp_testing(event):
   print("entered")
   fh_temp = open("data_files/temp_testing.txt","r")
   t = fh_temp.readlines()
   for row in t:
      x1,y1,x2,y2 = map(float,row.split(' '))
      config.drawing_board.create_line(x1,y1,x2,y2)
      print("drawing line:",x1,y1,x2,y2)
   fh_temp.close()
   run_eval()

# Draw board
config.master.title("Line Segment Intersection")
config.drawing_board.bind("<Button-1>",input_lines)
# config.drawing_board.bind("<Button-1>",temp_testing)

start_button = Button(config.master,text = "Start Evaluation")
start_button.configure(command = lambda: run_eval(start_button))
start_button.pack(side = LEFT)
# this is so that the button can be hidden after clicking

mainloop()
