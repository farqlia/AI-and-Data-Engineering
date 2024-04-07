from queue import PriorityQueue

from ai_data_eng.searching.graph import Graph
from ai_data_eng.searching.searchning import PrioritizedItem


def initialize_queue(graph: Graph, cost_so_far, came_from_conn, stop_conn,
                     start_stop: str, dep_time: int):
    frontier = PriorityQueue()

    cost_so_far[('', start_stop)] = 0
    stop_conn[('', start_stop)] = -1
    came_from_conn[('', start_stop)] = None
    item = PrioritizedItem(cost_so_far[('', start_stop)], ('', start_stop))
    frontier.put(item)

    return frontier


def initialize_queue_with_prev_conn(prev_conn_idx: int, graph: Graph, cost_so_far, came_from_conn, stop_conn,
                                    start_stop: str, dep_time: int):
    prev_conn = graph.conn_at_index(prev_conn_idx)

    frontier = PriorityQueue()

    cost_so_far[(prev_conn.line, prev_conn.end_stop)] = 0
    stop_conn[(prev_conn.line, prev_conn.end_stop)] = prev_conn_idx
    came_from_conn[(prev_conn.line, prev_conn.end_stop)] = None
    item = PrioritizedItem(cost_so_far[(prev_conn.line, prev_conn.end_stop)], (prev_conn.line, prev_conn.end_stop))
    frontier.put(item)
    return frontier
