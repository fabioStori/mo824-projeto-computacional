import os
from ts_csp import TS_CSP

max_time = 60*60

files = os.listdir('InstancesCSP')

for file in files:
  tabu_search = TS_CSP(ternure_porcent=0.2, iterations=10000, max_time=max_time, instance_file=file, improve='first', const_heuristic='greedy')
  best_solution, total_time = tabu_search.solve(seed=2)
  f = open('all_instances_ts_random_fi.out', 'a')
  f.write(f"{file}  {best_solution.cost}  {total_time} \n")
  f.close()

# tabu_search = TS_CSP(ternure_porcent=0.3, iterations=1000, max_time=max_time, instance_file='berlin52-9.csp2', improve='best', const_heuristic='greedy')
# tabu_search = TS_CSP(ternure_porcent=1, iterations=10, max_time=30*60, instance_file='simple_tests.csp2')
# best_solution, total_time = tabu_search.solve(seed=2)

# print(best_solution, total_time)