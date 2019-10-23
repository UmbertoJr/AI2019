from code import *


def run():
    names = [name_ for name_ in os.listdir("./problems") if "tsp" in name_]
    for name in names:
        filename = f"problems/{name}"
        instance = Instance(filename)
        instance.print_info()
        print(" ---  ")
        instance.plot_data()

        solver = Solver_TSP('random')
        naive_solution = solver(instance)
        solver.plot_solution()
        print(f"the total length for the solution found is {solver.evaluate_solution()}",
              f"while the optimal length is {instance.best_sol}",
              f"the gap is {solver.gap} %", sep="\n")


if __name__ == '__main__':
    run()
