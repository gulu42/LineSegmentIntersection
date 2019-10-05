from utils import Point,Line
from logicBlock import Sweeper

if __name__ == "__main__":
    data_file = "data_1.txt"
    sweep_obj = Sweeper(data_file)
    sweep_obj.run()
