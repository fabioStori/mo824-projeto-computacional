from ts_csp import TS_CSP

tabu_search = TS_CSP(ternure=5, iterations=10, max_time=30*60, instance_file='eil51-7.csp2')
# tabu_search = TS_CSP(ternure=1, iterations=10, max_time=30*60, instance_file='simple_tests.csp2')
diva = float('inf')
for i in range(1):
    best_solution, total_time = tabu_search.solve(i)
    if best_solution.cost < diva:
        diva = best_solution.cost
print(diva, total_time)

print('edges', best_solution.edges)