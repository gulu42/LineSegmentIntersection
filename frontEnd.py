from utils import Point,Line
from logicBlock import Sweeper
from tkinter import *
import sys
import time
import config
from optparse import OptionParser
import random

# 0 if all points are paired
# 1 if there is an un-paired point
points_modulo = 0
px = 0
py = 0
num = 0
epsi = 0.01

INP_FILE = "data_files/input_data.txt"

fh = open(INP_FILE,"w+")

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
      dir = []
      for i in range(4):
         dir.append(random.choice([-1,1]))
      config.drawing_board.create_line(px,py,event.x,event.y)
      if py == event.y: #it's a line parallel to the x axis
         dir[1] = 1
         dir[3] = -1
      fh.write(str(px+(dir[0] * epsi)) + " " + str(py+(dir[1] * epsi)) + " " + str(event.x+(dir[2] * epsi)) + " " + str(event.y+(dir[3] * epsi)) + "\n")
      print("Saving line: " + str(px+(dir[0] * epsi)) + " " + str(py+(dir[1] * epsi)) + " " + str(event.x+(dir[2] * epsi)) + " " + str(event.y+(dir[3] * epsi)) + "\n")
      # write the line correcting for x and y

def draw_sweep_line(p):
   config.drawing_board.create_line(0,p.y,config.canvas_width-1,p.y,fill="green")
   draw_point(p.x,p.y)

def run_eval(delay_param=200):
   print("Evaluation running")
   fh.close()

   # sweep_obj = Sweeper("temp_testing.txt")
   sweep_obj = Sweeper(INP_FILE)
   sweep_obj.run()
   print("Eval complete. Running animation")
   for p in config.sweep_y:
      print(p)

   delay = 0
   delay_amount =delay_param
   num_artifacts = 2#drawing two things and the first one is the line
   n = config.drawing_board.create_oval(0,0,1,1)
   points_drawn = dict()
   for p in config.sweep_y:
      print(p)
      if p not in points_drawn:
         config.drawing_board.after(delay,draw_sweep_line,p)
         n += num_artifacts
         points_drawn[p] = True # since the point isn't hashable
         delay += delay_amount
         config.drawing_board.after(delay,config.drawing_board.delete,n - (num_artifacts - 1))
         delay += delay_amount
   config.sweep_y = []
   print("Animation complete")

def clear_canvas():
   global fh
   fh.close()
   global INP_FILE
   INP_FILE = "data_files/input_data.txt"
   fh = open(INP_FILE,"w")

   global points_modulo
   points_modulo = 0

   config.drawing_board.delete("all")

   config.sweep_y = []

def save_input():
   global num

   print("num = ",num)

   with open("data_files/input_data.txt") as f:
      with open("data_files/examples/tc_"+str(num)+".txt","w") as f1:
         for l in f:
            print(l)
            f1.write(l)

   clear_canvas()
   num += 1

if __name__ == "__main__":


   parser = OptionParser()

   parser.add_option('--inp',dest='inp_file',type=str,help='File from which input is to be loaded')
   parser.add_option('-n',dest='test_case_num',type=int,help='The number to be assigned to the testcase file where the input will be saved')
   parser.add_option('--disp_delay',dest='disp_delay',type=int,help='The delay between two positions of the sweep line on the GUI')

   options, otherjunk = parser.parse_args(sys.argv[1:])
   if len(otherjunk) != 0:
       raise Exception('Command line input not understood: ' + str(otherjunk))
   print(options.inp_file,type(options.inp_file))

   if options.disp_delay is None:
      options.disp_delay = 200

   if options.test_case_num is None:
      num = 0
   else:
      num = options.test_case_num

   # Draw board
   config.master.title("Line Segment Intersection")
   config.drawing_board.bind("<Button-1>",input_lines)
   # config.drawing_board.bind("<Button-1>",temp_testing)

   start_button = Button(config.master,text = "Start Evaluation",command = lambda: run_eval(delay_param=options.disp_delay))
   start_button.pack(side = LEFT)

   clear_all_button = Button(config.master,text = "Clear Screen",command = clear_canvas)
   clear_all_button.pack(side = LEFT)

   print(options.test_case_num)

   save_button = Button(config.master,text = "Save Input",command = save_input)
   save_button.pack(side = LEFT)

   if options.inp_file is None:
      print("loading from gui")
      mainloop()
   else:
      print("loading from file")
      # load_file = "data_files/bad_cases/" + options.inp_file
      load_file = "data_files/examples/" + options.inp_file
      fh_temp = open(load_file ,"r")
      t = fh_temp.readlines()
      for row in t:
         x1,y1,x2,y2 = map(float,row.split(' '))
         config.drawing_board.create_line(x1,y1,x2,y2)
         print("drawing line:",x1,y1,x2,y2)
      fh_temp.close()
      # global INP_FILE
      INP_FILE = load_file
      # run_eval()
      mainloop()
