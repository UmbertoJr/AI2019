from src import *
import pandas as pd
from time import time as t


def run(show_plots=False, verbose=False):
    # names = [name_ for name_ in os.listdir("./problems") if "tsp" in name_]
    names = ["eil76.tsp", "kroA100.tsp"]
    methods = Solver_TSP.available_methods.keys()
    results = []
    index = []
    for name in names:
        filename = f"problems/{name}"
        instance = Instance(filename)
        if verbose:
            print("\n\n#############################")
            instance.print_info()
        if show_plots:
            instance.plot_data()

        for method in methods:
            solver = Solver_TSP(method)
            start = t()
            solver(instance, return_value=False, verbose=verbose)
            end = t()

            if verbose:
                print(f"the total length for the solution found is {solver.found_length}",
                      f"while the optimal length is {instance.best_sol}",
                      f"the gap is {solver.gap}%",
                      f"the solution is found in {np.round(end - start, 5)} seconds", sep="\n")

            index.append((name, method))
            results.append([solver.found_length, instance.best_sol, solver.gap, end - start])

            if show_plots:
                solver.plot_solution()

        if instance.exist_opt:
            solver.solution = np.concatenate([instance.optimal_tour, [instance.optimal_tour[0]]])
            solver.method = "optimal"
            solver.plot_solution()

    index = pd.MultiIndex.from_tuples(index, names=['problem', 'method'])

    return pd.DataFrame(results, index=index, columns=["tour length", "optimal solution", "gap", "time to solve"])


if __name__ == '__main__':
    run(show_plots=True, verbose=True).to_csv("./results.csv")
