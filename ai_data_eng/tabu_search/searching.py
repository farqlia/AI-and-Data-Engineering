from functools import partial
from typing import List

from ai_data_eng.searching.a_star_p.a_star_changes_opt import find_path_a_star_p, path_to_list_p
from ai_data_eng.searching.a_star_t.a_star_time_opt import find_path_a_star_t
from ai_data_eng.searching.graph import Graph
from ai_data_eng.searching.heuristics import WeightedAverageTimeHeuristic, ChangeHeuristic
from ai_data_eng.searching.searchning import OptimizationType, idxs_to_nodes
from ai_data_eng.searching.utils import sec_to_time


def get_a_star(g: Graph):
    def get_a_star_for_graph(criterion: OptimizationType):
        if criterion == OptimizationType.TIME:
            return partial(find_path_a_star_t, graph=g, heuristic=WeightedAverageTimeHeuristic(),
                           cost_func=g.time_cost_between_conns,
                           neighbours_gen=g.get_earliest_from_with_and_without_change)
        elif criterion == OptimizationType.CHANGES:
            return partial(find_path_a_star_p, graph=g, heuristic=ChangeHeuristic(),
                           cost_func=g.change_cost_between_conns, neighbours_gen=g.get_lines_from)

    return get_a_star_for_graph


def get_connection_path(g: Graph, criterion: OptimizationType):
    if criterion == OptimizationType.TIME:
        def recreate(goal_index, came_from):
            return idxs_to_nodes(g, goal_index, came_from)

        return recreate
    elif criterion == OptimizationType.CHANGES:
        def recreate(goal, came_from):
            came_from_conn, stop_conn = came_from
            conns = path_to_list_p(goal, came_from_conn, stop_conn)
            connections = [g.conn_at_index(idx) for idx in conns]
            return connections

        return recreate


def naive_solution(g: Graph):

    def naive_solution_for_graph(criterion: OptimizationType, start_stop: str, visiting_stops: List[str],
                                 leave_hour: str):
        a_star = get_a_star(g)(criterion)
        conn_path = get_connection_path(g, criterion)

        prev_stop = start_stop
        solution = []
        for stop in visiting_stops:
            goal, came_from, costs = a_star(start_stop=prev_stop, goal_stop=stop, leave_hour=leave_hour,
                                            prev_conn_idx=solution[-1].name if solution else None)
            subsol = conn_path(goal, came_from)
            solution += subsol
            prev_stop = stop
            # add change time
            leave_hour = sec_to_time(subsol[-1]['arrival_sec'])
            g.reset()
        goal, came_from, costs = a_star(start_stop=prev_stop, goal_stop=start_stop, leave_hour=leave_hour,
                                        prev_conn_idx=solution[-1].name)
        solution += conn_path(goal, came_from)
        g.reset()
        return solution

    return naive_solution_for_graph
