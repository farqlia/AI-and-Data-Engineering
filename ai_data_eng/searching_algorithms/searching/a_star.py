from ai_data_eng.searching.a_star_t.a_star_time_opt import a_star_t_solution
from ai_data_eng.searching.a_star_p.a_star_changes_opt import a_star_p_solution
from ai_data_eng.searching.heuristics import WeightedAverageTimeHeuristic, ChangeHeuristic


def a_star_solution(start_stop, goal_stop, leave_hour, criterion):
    if criterion == 't':
        return a_star_t_solution(start_stop, goal_stop, leave_hour)
    elif criterion == 'p':
        return a_star_p_solution(start_stop, goal_stop, leave_hour)