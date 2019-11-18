from src import *
import pandas as pd



def run(show_plots=False, verbose=False):
    # names = [name_ for name_ in os.listdir("./problems") if "tsp" in name_]
    names = ["eil76.tsp", "kroA100.tsp"]
    initializers = Solver_TSP.available_initializers.keys()
    improvements = Solver_TSP.available_improvements.keys()
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

        for init in initializers:
            solver = Solver_TSP(init)
            for improve in improvements:
                solver.bind(improve)
                end - start
                solver(instance, return_value=False, verbose=verbose)

                if verbose:
                    print(f"the total length for the solution found is {solver.found_length}",
                          f"while the optimal length is {instance.best_sol}",
                          f"the gap is {solver.gap}%",
                          f"the solution is found in {solver.time_to_solve} seconds", sep="\n")

                index.append((name, solver.name_method))
                results.append([solver.found_length, instance.best_sol, solver.gap, solver.time_to_solve])

                if show_plots:
                    solver.plot_solution()

        if instance.exist_opt:
            solver.solution = np.concatenate([instance.optimal_tour, [instance.optimal_tour[0]]])
            solver.method = "optimal"
            solver.plot_solution()

    index = pd.MultiIndex.from_tuples(index, names=['problem', 'method'])

    return pd.DataFrame(results, index=index, columns=["tour length", "optimal solution", "gap", "time to solve"])


if __name__ == '__main__':
    run(show_plots=False, verbose=True).to_csv("./results.csv")
