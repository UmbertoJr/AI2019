from src import *
from concorde.tsp import TSPSolver


def run(show_plots=False):
    # names = [name_ for name_ in os.listdir("./problems") if "tsp" in name_]
    names = ["ch130.tsp"]

    for name in names:
        print("\n\n#############################")
        filename = f"problems/{name}"
        instance = Instance(filename)
        instance.print_info()
        if show_plots:
            instance.plot_data()

        solver = TSPSolver.from_data(
            instance.points[:, 1]*100,
            instance.points[:, 2]*100,
            norm="EUC_2D"
        )
        solution = solver.solve(verbose=False)
        tour_opt = np.copy(solution.tour)


        for method in ["random", "nearest_neighbors", "best_nn"]:
            solver = Solver_TSP(method)
            solver(instance, return_value=False)

            print(f"the total length for the solution found is {solver.found_length}",
                  f"while the optimal length is {instance.best_sol}",
                  f"the gap is {solver.gap} %", sep="\n")
            if show_plots:
                solver.plot_solution()

        solver.method = "optimal"
        solver.solution = np.concatenate([tour_opt, [tour_opt[0]]])
        solver.solved = True
        solver.plot_solution()
        print(solver.evaluate_solution(return_value=True))


if __name__ == '__main__':
    run(show_plots=True)
