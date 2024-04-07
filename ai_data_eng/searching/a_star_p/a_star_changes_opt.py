from functools import partial
from queue import PriorityQueue
from typing import Callable

from ai_data_eng.searching.a_star_p.initialization import initialize_queue_with_prev_conn, initialize_queue
from ai_data_eng.searching.globals import A_STAR_RUNS_P
from ai_data_eng.searching.graph import *
from ai_data_eng.searching.heuristics import Heuristic
from ai_data_eng.searching.searchning import PrioritizedItem, run_solution, \
    print_path, write_solution_to_file
from ai_data_eng.searching.utils import *


def find_path_a_star_p(graph: Graph, heuristic: Heuristic, cost_func: Callable,
                       neighbours_gen: Callable, start_stop: str, goal_stop: str, leave_hour: str, prev_conn_idx=None):
    dep_time = time_to_normalized_sec(leave_hour)
    # print_info = a_star_print_info(lambda x: round(x, 2))
    cost_so_far = {}
    # if commuting A -> B, then this will be came_from_conn[B] = A so we can recreate the path
    came_from_conn = {}
    stop_conn = {}
    goal_stop_coords = graph.compute_stop_coords(goal_stop)
    goal_stop = (goal_stop, goal_stop_coords['stop_lat'], goal_stop_coords['stop_lon'])
    start_stop_coords = graph.compute_stop_coords(start_stop)
    # print(f'{start_stop} -> {goal_stop}')
    if prev_conn_idx is not None:
        frontier = initialize_queue_with_prev_conn(prev_conn_idx, graph=graph, cost_so_far=cost_so_far,
                                                   came_from_conn=came_from_conn, stop_conn=stop_conn,
                                                   start_stop=start_stop, dep_time=dep_time)
    else:
        frontier = initialize_queue(graph=graph, cost_so_far=cost_so_far,
                                    came_from_conn=came_from_conn, stop_conn=stop_conn,
                                    start_stop=start_stop, dep_time=dep_time)

    start_stop = (start_stop, start_stop_coords['stop_lat'], start_stop_coords['stop_lon'])
    graph.add_conn(dep_time, start_stop, -1)

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
        # print(f'[{i}]')
        for next_conn in neighbours_gen(conn).itertuples():
            # cost of commuting start --> current and current --> next
            new_cost = cost_so_far[(line, current)] + cost_func(prev_conn=conn, next_conn=next_conn)
            heuristic_cost = heuristic.compute(start_stop, goal_stop, conn, next_conn, new_cost)
            approx_goal_cost = new_cost + heuristic_cost
            if (next_conn.line, next_conn.end_stop) not in cost_so_far or new_cost < cost_so_far[
                (next_conn.line, next_conn.end_stop)]:
                # print_info(next_conn, new_cost, heuristic_cost)
                cost_so_far[(next_conn.line, next_conn.end_stop)] = new_cost
                item = PrioritizedItem(approx_goal_cost, (next_conn.line, next_conn.end_stop))
                frontier.put(item)
                came_from_conn[(next_conn.line, next_conn.end_stop)] = (line, current)
                stop_conn[(next_conn.line, next_conn.end_stop)] = next_conn.Index
        # i += 1
        graph.exclude_stop_and_line(current, line)

    graph.reset()
    return goal, (came_from_conn, stop_conn), cost_so_far


def path_to_list_p(goal, came_from_conn, stop_conn):
    came_from = goal
    conns = []
    while came_from:
        line, current = came_from
        index = stop_conn[(line, current)]
        conns.append(index)
        came_from = came_from_conn[(line, current)]

    conns.reverse()
    return conns[1:]


def a_star_changes_opt(start_stop: str, goal_stop: str, leave_hour: str,
                       heuristic: Heuristic, change_time=0, run_dir=A_STAR_RUNS_P):
    with open(run_dir / f'run-change_time-{change_time}', mode='a', encoding='utf-8') as f:
        print(f'Testcase: {start_stop} -> {goal_stop}\nStart time: {leave_hour}\nRoute', file=f)
        graph, goal, came_from, costs, elapsed_time = run_solution(
            partial(find_path_a_star_p, heuristic=heuristic),
            start_stop, goal_stop, leave_hour, change_time, criterion=heuristic.criterion)
        came_from_conn, stop_conn = came_from
        conns = path_to_list_p(goal, came_from_conn, stop_conn)
        connections = [graph.conn_at_index(idx) for idx in conns]
        # assert assert_connection_path(time_to_normalized_sec(leave_hour), connections)
        print_path(connections, f)
        # write_solution_to_file(A_STAR_RUNS_P / f'{start_stop}-{goal_stop}')
        print(f'Total number of changes is {costs[goal]}', file=f)
        print(f'Algorithm took {elapsed_time:.2f}s to execute\n', file=f)
        write_solution_to_file(run_dir / 'summary', connections, leave_hour, elapsed_time, costs[goal], change_time)
    return graph, connections


def a_star_changes_opt_light(start_stop: str, goal_stop: str, leave_hour: str,
                             heuristic: Heuristic, change_time=0):
    graph, goal, came_from, costs, elapsed_time = run_solution(
        partial(find_path_a_star_p, heuristic=heuristic),
        start_stop, goal_stop, leave_hour, change_time, criterion=heuristic.criterion)
    came_from_conn, stop_conn = came_from
    conns = path_to_list_p(goal, came_from_conn, stop_conn)
    connections = [graph.conn_at_index(idx) for idx in conns]
    return graph, connections
