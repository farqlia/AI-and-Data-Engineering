import re
from pathlib import Path
from queue import PriorityQueue

import pandas as pd

from ai_data_eng.searching.graph import Graph
from ai_data_eng.searching.searchning import print_info, run_solution, assert_connection_path, idxs_to_nodes, print_path
from ai_data_eng.searching.utils import time_to_normalized_sec, sec_to_time

pd.options.mode.chained_assignment = None

DATA_DIR = Path('../data')

def find_path(graph: Graph, start_stop: str, goal_stop: str, leave_hour: str):
    
    frontier = PriorityQueue()
    dep_time = time_to_normalized_sec(leave_hour)
    
    print(f'STOP {start_stop} --> TO {goal_stop}')

    cost_so_far = {}
    # if commuting A -> B, then this will be came_from[B] = A so we can recreate the path
    came_from = {}

    # given only stop name consider all possible start stops??  
    j = -1
    for _, candidate_start_stop in graph.get_possible_stops(start_stop).iterrows():
        candidate_stop_id = graph.stop_as_tuple(candidate_start_stop)
        cost_so_far[candidate_stop_id] = 0
        graph.add_conn(dep_time, candidate_start_stop, j)
        came_from[j] = None
        frontier.put((cost_so_far[candidate_stop_id], j))
        j -= 1

    with open(DATA_DIR / ('dijkstra_runs/' + re.sub(r"\W+", "", start_stop) + '-' + re.sub(r"\W+", "", goal_stop)), mode='w', encoding='utf-8') as f:

        i = 0
        while not frontier.empty():
            # get the stop with the lowest cost 
            cost, index = frontier.get()

            conn = graph.conn_at_index(index)
            current = graph.stop_as_tuple(graph.rename_stop(conn))

            # consider all possible end stops 
            if current[0] == goal_stop:
                goal_stop_index = index
                # theory - first found is the best
                break 

            print(f'[{i}]', file=f)
            for next_conn in graph.get_earliest_from(start_stop=conn):
                print_info(next_conn, file=f)
                # cost of commuting start --> current and current --> next 
                new_cost = cost + graph.cost_getting_to(next_conn.name, conn.name)
                next_stop_id = graph.stop_as_tuple(graph.rename_stop(next_conn))
                if next_stop_id not in cost_so_far or new_cost < cost_so_far[next_stop_id]:
                    print(f'We arrive from {start_stop} to {next_stop_id} at {sec_to_time(dep_time + new_cost)}', file=f)
                    cost_so_far[next_stop_id] = new_cost
                    frontier.put((new_cost, next_conn.name))
                    came_from[next_conn.name] = index
            i+=1

    return goal_stop_index, came_from, cost_so_far


def dijkstra(start_stop: str, goal_stop: str, leave_hour: str, change_time=0):
    print(f'Commute from {start_stop} to {goal_stop} at {leave_hour}')
    graph, goal_index, came_from, solution_cost, elapsed_time = run_solution(find_path, start_stop, goal_stop, leave_hour, change_time)
    
    connections = idxs_to_nodes(graph, goal_index, came_from)
    assert assert_connection_path(time_to_normalized_sec(leave_hour), connections)
    print_path(connections)
    print(f'Total trip time is {sec_to_time(solution_cost)}')
    print(f'Algorithm took {elapsed_time:.2f}s to execute')
