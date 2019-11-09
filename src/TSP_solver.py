import numpy as np
from matplotlib import pyplot as plt
from numpy.core._multiarray_umath import ndarray
import os
if 'AI' in os.getcwd():
    from src.utils import *
else:
    from AI2019.src.utils import *



class Solver_TSP:

    solution: ndarray
    found_length: float
    available_methods = {"random": lambda x: x, "nearest_neighbors": lambda x: x,
                         "best_nn": lambda x: x, "multi_fragment": lambda x: x}

    def __init__(self, method):
        self.available_methods = {"random": self.random_method, "nearest_neighbors": self.nn,
                                  "best_nn": self.best_nn, "multi_fragment": self.mf}
        self.method = method
        self.solved = False
        assert method in self.available_methods, f"the {method} method is not available currently."

    def __call__(self, instance_, verbose=True, return_value=True):
        self.instance = instance_
        self.solved = False
        if verbose:
            print(f"###  solving with {self.method} ####")
        self.solution = self.available_methods[self.method](instance_)
        assert self.check_if_solution_is_valid(self.solution), "Error the solution is not valid"
        self.evaluate_solution()
        self._gap()
        if verbose:
            print(f"###  solution found with {self.gap} % gap ####")
        self._gap()
        if return_value:
            return self.solution

    def random_method(self, instance_):
        n = int(instance_.nPoints)
        solution = np.random.choice(np.arange(n), size=n, replace=False)
        self.solution = np.concatenate([solution, [solution[0]]])
        self.solved = True
        return self.solution

    def nn(self, instance_, starting_node=0):
        dist_matrix = np.copy(instance_.dist_matrix)
        n = int(instance_.nPoints)
        node = starting_node
        tour = [node]
        for _ in range(n - 1):
            for new_node in np.argsort(dist_matrix[node]):
                if new_node not in tour:
                    tour.append(new_node)
                    node = new_node
                    break
        tour.append(starting_node)
        self.solution = np.array(tour)
        self.solved = True
        return self.solution

    def best_nn(self, instance_):
        solutions, lens = [], []
        for start in range(self.instance.nPoints):
            new_solution = self.nn(instance_, starting_node=start)
            solutions.append(new_solution)
            assert self.check_if_solution_is_valid(new_solution), "error on best_nn method"
            lens.append(self.evaluate_solution(return_value=True))

        self.solution = solutions[np.argmin(lens)]
        self.solved = True
        return self.solution

    def mf(self, instance):
        mat = np.copy(instance.dist_matrix)
        mat = np.triu(mat)
        mat[mat == 0] = 100000
        solution = {str(i): [] for i in range(instance.nPoints)}
        start_list = [i for i in range(instance.nPoints)]
        inside = 0
        for el in np.argsort(mat.flatten()):
            node1, node2 = el // instance.nPoints, el % instance.nPoints
            possible_edge = [node1, node2]
            if multi_fragment.check_if_available(node1, node2, solution):
                if multi_fragment.check_if_not_close(possible_edge, solution):
                    # print("entrato", inside)
                    solution[str(node1)].append(node2)
                    solution[str(node2)].append(node1)
                    if len(solution[str(node1)]) == 2:
                        start_list.remove(node1)
                    if len(solution[str(node2)]) == 2:
                        start_list.remove(node2)
                    inside += 1
                    # print(node1, node2, inside)
                    if inside == instance.nPoints - 1:
                        # print(f"ricostruire la solutione da {start_list}",
                        #       f"vicini di questi due nodi {[solution[str(i)] for i in start_list]}")
                        solution = multi_fragment.create_solution(start_list, solution)
                        self.solution = solution
                        self.solved = True
                        return self.solution

    def plot_solution(self):
        assert self.solved, "You can't plot the solution, you need to solve it first!"
        plt.figure(figsize=(8, 8))
        self._gap()
        plt.title(f"{self.instance.name} solved with {self.method} solver, gap {self.gap}")
        ordered_points = self.instance.points[self.solution]
        plt.plot(ordered_points[:, 1], ordered_points[:, 2], 'b-')
        plt.show()

    def check_if_solution_is_valid(self, solution):
        rights_values = np.sum([self.check_validation(i, solution[:-1]) for i in np.arange(self.instance.nPoints)])
        if rights_values == self.instance.nPoints:
            return True
        else:
            return False

    def check_validation(self, node, solution):
        if np.sum(solution == node) == 1:
            return 1
        else:
            return 0

    def evaluate_solution(self, return_value=False):
        total_length = 0
        starting_node = self.solution[0]
        from_node = starting_node
        for node in self.solution[1:]:
            total_length += self.instance.dist_matrix[from_node, node]
            from_node = node

        self.found_length = total_length
        if return_value:
            return total_length

    def _gap(self):
        self.evaluate_solution(return_value=False)
        self.gap = np.round(((self.found_length - self.instance.best_sol) / self.instance.best_sol) * 100, 2)
