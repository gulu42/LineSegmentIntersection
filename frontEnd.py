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

def empty_event(event):
   pass

def draw_point(event):
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

def button_clicked():
   print("Button was pressed")

def run_eval():
   print("Evaluation running")
   fh.close()
   sweep_obj = Sweeper("temp_data.txt")
   sweep_obj.run()
   print("Eval complete. Running animation")
   print(config.sweep_y)
   delay = 0
   n = config.drawing_board.create_oval(0,0,1,1)
   for y in config.sweep_y:
      config.drawing_board.after(delay,config.drawing_board.create_line,0,y,config.canvas_width-1,y)
      n += 1
      print(n)
      delay += 1000
      config.drawing_board.after(delay,config.drawing_board.delete,n)
      delay += 1000
      # sweep_line = config.drawing_board.create_line(0,y,config.canvas_width-1,y)
      # print(sweep_line)
      # time.sleep(time_sec)
      # config.drawing_board.after(time_sec*1000,config.drawing_board.delete,sweep_line)
      # config.drawing_board.after(time_sec*1000,None)
      # print("Deleting line",sweep_line)
      # config.drawing_board.delete(sweep_line)
   config.sweep_line = []
   print("Animation complete")
   # sys.exit(0)

config.master.title("Line Segment Intersection")
# drawing_board = Canvas(master,
#            width=canvas_width,
#            height=canvas_height) # create a canvas
# drawing_board.pack(expand = YES, fill = BOTH)
config.drawing_board.bind("<Button-1>",draw_point)

start_button = Button(config.master,text = "Start Evaluation",command = run_eval)
start_button.pack(side = LEFT)

mainloop()


# if __name__ == "__main__":
#     data_file = "data_2.txt"
#     sweep_obj = Sweeper(data_file)
#     sweep_obj.run()
