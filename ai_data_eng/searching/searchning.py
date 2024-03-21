import pandas as pd

from ai_data_eng.searching.graph import Graph, add_constant_change_time
from ai_data_eng.searching.utils import sec_to_time, diff

pd.options.mode.chained_assignment = None
from pathlib import Path
from timeit import default_timer as timer

DATA_DIR = Path('../data')

def print_info(conn, file=None):
    print(f"{conn['line']} goes from {conn['start_stop']} to {conn['end_stop']} and leaves at {conn['departure_time']}, arrives at {conn['arrival_time']}", 
          file=file)
    
def path_to_list(node: str, connections: dict):
    path = [node]
    while node:
        node = connections[node]
        path.append(node)
    path.reverse()
    return path[1:]

def idxs_to_nodes(graph: Graph, goal_idx: int, conn_idxs: dict):
    idx_path = path_to_list(goal_idx, conn_idxs)
    return [graph.conn_at_index(idx) for idx in idx_path[1:]]

def print_path(connections: dict):
    for conn in connections:
        print(f'{conn["start_stop"]} [{sec_to_time(conn["departure_sec"])}] --- {conn["line"]} ---> {conn["end_stop"]} [{sec_to_time(conn["arrival_sec"])}]')


def assert_connection_path(dept_time, connections):
    if connections[0]['departure_sec'] < dept_time:
        return False 
    for i in range(len(connections) - 1):
        if diff(connections[i + 1]['departure_sec'], connections[i + 1]['arrival_sec']) < 0:
            return False 
    return True 

def run_solution(find_path_function, start_stop: str, goal_stop: str, leave_hour: str, change_time=0):
    start = timer()
    connection_graph = pd.read_csv(DATA_DIR / 'connection_graph.csv', 
                               usecols=['line', 'departure_time', 'arrival_time', 'start_stop',
       'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat', 'end_stop_lon'])
    graph = Graph(connection_graph, add_constant_change_time)
    goal_index, came_from, costs = find_path_function(graph, start_stop, goal_stop, leave_hour)
    end = timer()
    elapsed_time = (end - start)
    solution_cost = costs[graph.stop_as_tuple(graph.rename_stop(graph.conn_at_index(goal_index)))]
    return graph, goal_index, came_from, solution_cost, elapsed_time 