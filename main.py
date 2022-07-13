from ts_csp import TS_CPS

tabu_search = TS_CPS(ternure=10, iterations=1, max_time=30*60, instance_file='simple_tests.csp2')
best_solution, total_time = tabu_search.solve()
# print(best_solution, total_time)