from src import *
import os


def run(show_plots=False):
    names = [name_ for name_ in os.listdir("./problems") if "tsp" in name_]
    for name in names:
        print("\n\n#############################")
        filename = f"problems/{name}"
        instance = Instance(filename)
        instance.print_info()

        solver = Solver_TSP('random')
        solver(instance, return_value=False)

        print(f"the total length for the solution found is {solver.evaluate_solution()}",
              f"while the optimal length is {instance.best_sol}",
              f"the gap is {solver.gap} %", sep="\n")
        if show_plots:
            instance.plot_data()
            solver.plot_solution()


if __name__ == '__main__':
    run()
