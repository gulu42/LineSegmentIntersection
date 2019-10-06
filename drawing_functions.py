import config
import tkinter as tk
import time

def to_canvas_y(logic_y):
   return config.canvas_height - logic_y

def to_logic_y(canvas_y):
   return config.canvas_height - canvas_y

def draw_sweep_line(y):
   print("Call to update the sweep line position")
   config.sweep_y.append(y)
   # canv_y = to_canvas_y(y)
   # sweep_line = config.drawing_board.create_line(0,y,config.canvas_width-1,y)
   # print(sweep_line)
   # time_sec = 5
   # time.sleep(time_sec)
   # config.drawing_board.after(time_sec * 1000,config.drawing_board.delete,sweep_line)

def draw_intersection_point():
   print("call to draw a new intersection point")
