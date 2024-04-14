from ai_data_eng.searching.a_star_p.a_star_changes_opt import a_star_changes_opt_light
from ai_data_eng.searching.heuristics import TimeAndChangeHeuristic

results = []

for (a, b) in [(0.1, 0.5), (0.01, 0.5), (0.05, 0.5), (0.1, 1), (0.01, 1), (0.05, 1)]:
    for test_case in [['Palacha', 'Jutrosińska', '16:24:00'], ['Mokra', 'Syrokomli', '14:41:00']]:
        _, cost, elapsed_time = a_star_changes_opt_light(*test_case, heuristic=TimeAndChangeHeuristic(a, b))
        results.append([*test_case, cost, elapsed_time])

