from ts_cps import TS_CPS

tabu_search = TS_CPS(ternure=10, iterations=100, max_time=30*60, instance_file='berlin52-7.csp2')
best_solution, total_time = tabu_search.solve()
print(best_solution, total_time)

