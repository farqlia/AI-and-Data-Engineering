import re
from queue import PriorityQueue
from typing import Callable
from ai_data_eng.searching.a_star import Heuristic
from ai_data_eng.searching.globals import DATA_DIR
from ai_data_eng.searching.graph import *
from ai_data_eng.searching.searchning import a_star_p_print_info
from ai_data_eng.searching.utils import *


def changing_heuristic(start_stop: Stop, stop_to: Stop, stop_goal: Stop, N: int = 2):
    return distance_m(stop_to, stop_goal) / distance_m(start_stop, stop_goal) * N


def find_path(graph: Graph, start_stop: str, goal_stop: str, leave_hour: str):
    frontier = PriorityQueue()
    dep_time = time_to_normalized_sec(leave_hour)

    cost_so_far = {}
    # if commuting A -> B, then this will be came_from_conn[B] = A so we can recreate the path
    came_from_conn = {}
    goal_stop_coords = graph.compute_stop_coords(goal_stop)
    goal_stop = (goal_stop, goal_stop_coords['stop_lat'], goal_stop_coords['stop_lon'])
    start_stop_coords = graph.compute_stop_coords(start_stop)
    print(f'{start_stop} -> {goal_stop}')

    cost_so_far[('', start_stop)] = 1
    came_from_conn[('', start_stop)] = None
    frontier.put((cost_so_far[('', start_stop)], ('', start_stop)))

    start_stop = (start_stop, start_stop_coords['stop_lat'], start_stop_coords['stop_lon'])

    with open(DATA_DIR / ('a_star_runs/p_opt' + re.sub(r"\W+", "", start_stop[0]) + '-' + re.sub(r"\W+", "", goal_stop[0])),
              mode='w', encoding='utf-8') as f:

        i = 0
        while not frontier.empty():
            # get the stop with the lowest cost
            cost, (line, current) = frontier.get()

            # consider all possible end stops
            if current == goal_stop[0]:
                goal = (line, current)
                # theory - first found is the best
                break

            print(f'[{i}]')
            cost = cost_so_far[(line, current)]
            for next_conn in graph.get_neighbour_lines(current):
                # cost of commuting start --> current and current --> next
                next_stop_coords = graph.compute_stop_coords(next_conn.end_stop)
                next_stop = (next_conn.end_stop, next_stop_coords['stop_lat'], next_stop_coords['stop_lon'])
                new_cost = cost + (1 if line != '' and next_conn.line != line else 0)
                heuristic_cost = changing_heuristic(start_stop, next_stop, goal_stop)
                approx_goal_cost = new_cost + heuristic_cost
                if (next_conn.line, next_conn.end_stop) not in cost_so_far or new_cost < cost_so_far[(next_conn.line, next_conn.end_stop)]:
                    a_star_p_print_info(current, next_conn.end_stop, next_conn.line, new_cost, round(heuristic_cost, 2))
                    cost_so_far[(next_conn.line, next_conn.end_stop)] = new_cost
                    frontier.put((approx_goal_cost, (next_conn.line, next_conn.end_stop)))
                    came_from_conn[(next_conn.line, next_conn.end_stop)] = (line, current)
            i += 1

    return goal, came_from_conn, cost_so_far
