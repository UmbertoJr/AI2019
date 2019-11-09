import os

if 'AI' in os.getcwd():
    from src.utils import *
    from src.TSP_solver import *
    from src.io_tsp import *
else:
    from AI2019.src.utils import *
    from AI2019.src.TSP_solver import *
    from AI2019.src.io_tsp import *
