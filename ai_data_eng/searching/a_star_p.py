import re
from queue import PriorityQueue

from ai_data_eng.searching.a_star import Heuristic
from ai_data_eng.searching.globals import A_STAR_RUNS
from ai_data_eng.searching.graph import *
from ai_data_eng.searching.searchning import a_star_print_info
from ai_data_eng.searching.utils import *

from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def changing_heuristic(start_stop: Stop, stop_to: Stop, stop_goal: Stop, N: int = 2):
    return distance_m(stop_to, stop_goal) / distance_m(start_stop, stop_goal) * N


def find_path(graph: Graph, heuristic: Heuristic, start_stop: str, goal_stop: str, leave_hour: str):
    frontier = PriorityQueue()
    dep_time = time_to_normalized_sec(leave_hour)
    print_info = a_star_print_info(lambda x: round(x, 2))

    cost_so_far = {}
    # if commuting A -> B, then this will be came_from_conn[B] = A so we can recreate the path
    came_from_conn = {}
    stop_conn = {}
    goal_stop_coords = graph.compute_stop_coords(goal_stop)
    goal_stop = (goal_stop, goal_stop_coords['stop_lat'], goal_stop_coords['stop_lon'])
    start_stop_coords = graph.compute_stop_coords(start_stop)
    print(f'{start_stop} -> {goal_stop}')

    cost_so_far[('', start_stop)] = 0
    stop_conn[('', start_stop)] = -1
    came_from_conn[('', start_stop)] = None
    item = PrioritizedItem(cost_so_far[('', start_stop)], ('', start_stop))
    frontier.put(item)

    start_stop = (start_stop, start_stop_coords['stop_lat'], start_stop_coords['stop_lon'])

    graph.add_conn(dep_time, start_stop, -1)

    with open(str(A_STAR_RUNS) + ('p_opt' + re.sub(r"\W+", "", start_stop[0]) + '-' + re.sub(r"\W+", "", goal_stop[0])),
              mode='w', encoding='utf-8') as f:

        i = 0
        while not frontier.empty():
            # get the stop with the lowest cost
            item = frontier.get()
            (line, current) = item.item

            conn = graph.conn_at_index(stop_conn[(line, current)])
            # consider all possible end stops
            if current == goal_stop[0]:
                goal = (line, current)
                # theory - first found is the best
                break

            #print(f'[{i}]')

            current_stop = graph.stop_as_tuple(graph.rename_stop(conn))
            for next_conn in graph.get_lines_from(conn['arrival_sec'], current_stop, conn['line']).itertuples():
                # cost of commuting start --> current and current --> next
                next_stop_coords = graph.compute_stop_coords(next_conn.end_stop)
                next_stop = (next_conn.end_stop, next_stop_coords.stop_lat, next_stop_coords.stop_lon)
                new_cost = cost_so_far[(line, current)] + graph.change_cost_between_conns(conn, next_conn)
                heuristic_cost = heuristic.compute(start_stop, current_stop, next_stop, goal_stop,
                                                   conn, next_conn, new_cost)
                approx_goal_cost = new_cost + heuristic_cost
                if (next_conn.line, next_conn.end_stop) not in cost_so_far or new_cost < cost_so_far[(next_conn.line, next_conn.end_stop)]:
                    #print_info(next_conn, new_cost, heuristic_cost)
                    cost_so_far[(next_conn.line, next_conn.end_stop)] = new_cost
                    item = PrioritizedItem(approx_goal_cost, (next_conn.line, next_conn.end_stop))
                    frontier.put(item)
                    came_from_conn[(next_conn.line, next_conn.end_stop)] = (line, current)
                    stop_conn[(next_conn.line, next_conn.end_stop)] = next_conn.Index
            i += 1

    return goal, came_from_conn, stop_conn, cost_so_far
