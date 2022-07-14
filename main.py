from ts_csp import TS_CSP

tabu_search = TS_CSP(ternure=2, iterations=6, max_time=30*60, instance_file='simple_tests.csp2')
best_solution, total_time = tabu_search.solve()
print(best_solution, total_time)

print('edges', best_solution.edges)