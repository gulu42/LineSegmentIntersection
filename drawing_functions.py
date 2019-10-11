import config
import tkinter as tk
import time

def to_canvas_y(logic_y):
   return config.canvas_height - logic_y

def to_logic_y(canvas_y):
   return config.canvas_height - canvas_y

def draw_sweep_line(p):
   config.sweep_y.append(p)
