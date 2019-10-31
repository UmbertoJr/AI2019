import os

if 'AI' in os.getcwd():
    from src.TSP_solver import *
    from src.io_tsp import *
else:
    from AI2019.code.TSP_solver import *
    from AI2019.code.io_tsp import *