from ai_data_eng.searching.graph import Graph
from ai_data_eng.searching.searchning import OptimizationType
from ai_data_eng.tabu_search.searching import get_a_star, get_connection_path


def conn_start_from_end_to(g: Graph, criterion: OptimizationType):
    a_star = get_a_star(g)(criterion)
    conn_path = get_connection_path(g, criterion)

    def find_conn(conn_from, conn_to, prev_conn_idx=None):
        goal_index, came_from, _ = a_star(start_stop=conn_from.start_stop, goal_stop=conn_to.end_stop,
                                          leave_hour=conn_from.departure_time,
                                          prev_conn_idx=prev_conn_idx)
        g.reset()
        return conn_path(goal_index, came_from)

    return find_conn


def conn_end_from_end_to(g: Graph, criterion: OptimizationType):
    a_star = get_a_star(g)(criterion)
    conn_path = get_connection_path(g, criterion)

    def find_conn(from_conn, to_conn):
        goal_index, came_from, _ = a_star(start_stop=from_conn.end_stop, goal_stop=to_conn.end_stop,
                                          leave_hour=from_conn.arrival_time,
                                          prev_conn_idx=from_conn.name)
        g.reset()
        return conn_path(goal_index, came_from)

    return find_conn


def is_not_loop(conn_from, conn_to):
    return (conn_from.end_stop != conn_to.end_stop) and (conn_from.start_stop != conn_to.end_stop)


def insert_conn_between(g: Graph, criterion: OptimizationType):
    def insert_for_conn(connections, m, k, i, j):
        conn_s_f_e_t = conn_start_from_end_to(g, criterion)
        conn_e_f_e_t = conn_end_from_end_to(g, criterion)
        solution = connections[:m] + (
            conn_s_f_e_t(connections[m], connections[i], prev_conn_idx=connections[m - 1].name if m > 0 else None)
            if is_not_loop(connections[m], connections[i]) else [])
        solution += conn_e_f_e_t(solution[-1], connections[k]) if is_not_loop(solution[-1], connections[k]) else []
        solution += conn_e_f_e_t(solution[-1], connections[j]) if is_not_loop(solution[-1], connections[j]) else []
        # Make sure that stops are continued
        if connections[j + 1:] and solution[-1].end_stop != connections[j + 1].start_stop:
            solution += conn_e_f_e_t(solution[-1], connections[j])
        prev_conn = solution[-1]
        for conn in connections[j + 1:]:
            assert prev_conn.end_stop == conn.start_stop, f"{prev_conn} does not connect with {conn}"
            # prefer line continuation if it exists
            new_conn = g.get_earliest_from_to(prev_conn, conn).iloc[0]
            solution.append(new_conn)
            prev_conn = new_conn
        return solution

    return insert_for_conn
