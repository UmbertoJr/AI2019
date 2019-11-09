class multi_fragment:

    @staticmethod
    def check_if_available(n1, n2, sol):
        if len(sol[str(n1)]) < 2 and len(sol[str(n2)]) < 2:
            return True
        else:
            return False

    @staticmethod
    def check_if_not_close(edge_to_append, sol):
        n1, n2 = edge_to_append
        from_city = n2
        if len(sol[str(from_city)]) == 0:
            return True
        partial_tour = [from_city]
        end = False
        iterazione = 0
        while not end:
            if len(sol[str(from_city)]) == 1:
                if from_city == n1:
                    return_value = False
                    end = True
                elif iterazione > 1:
                    # print(f"iterazione {iterazione}, elementi dentro partial {len(partial_tour)}",
                    #       f"from city {from_city}")
                    return_value = True
                    end = True
                else:
                    from_city = sol[str(from_city)][0]
                    partial_tour.append(from_city)
                    iterazione += 1
            else:
                # print(from_city, partial_tour, sol[str(from_city)])
                for node_connected in sol[str(from_city)]:
                    # print(node_connected)
                    if node_connected not in partial_tour:
                        from_city = node_connected
                        partial_tour.append(node_connected)
                        # print(node_connected, sol[str(from_city)])
                        iterazione += 1
        return return_value

    @staticmethod
    def create_solution(start_sol, sol):
        assert len(start_sol) == 2, "too many cities with just one link"
        end = False
        n1, n2 = start_sol
        from_city = n2
        sol_list = [n1, n2]
        iterazione = 0
        while not end:
            for node_connected in sol[str(from_city)]:
                iterazione += 1
                if node_connected not in sol_list:
                    from_city = node_connected
                    sol_list.append(node_connected)
                    # print(f"prossimo {node_connected}",
                    #       f"possibili {sol[str(from_city)]}",
                    #       f"ultim tour {sol_list[-5:]}")
                if iterazione > 300:
                    end = True
        sol_list.append(n1)
        return sol_list
