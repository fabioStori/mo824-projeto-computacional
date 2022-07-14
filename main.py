from ts_csp import TS_CSP

tabu_search = TS_CSP(ternure=5, iterations=10, max_time=30*60, instance_file='eil51-7.csp2')
best_solution, total_time = tabu_search.solve(2)
print(best_solution, total_time)

print('edges', best_solution.edges)