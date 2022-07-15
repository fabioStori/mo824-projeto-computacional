import os
from ts_csp import TS_CSP

max_time = 60*60

files = os.listdir('InstancesCSP')

for file in files:
  tabu_search = TS_CSP(ternure_porcent=0.2, iterations=10000, max_time=max_time, instance_file=file)
  best_solution, total_time = tabu_search.solve(seed=2)
  f = open('all_instances_ts_simples_bi.out', 'a')
  f.write(f"{file}  {best_solution.cost}  {total_time} \n")
  f.close()

# tabu_search = TS_CSP(ternure_porcent=0.3, iterations=1000, max_time=max_time, instance_file='kroE100-7.csp2')
# # tabu_search = TS_CSP(ternure=1, iterations=10, max_time=30*60, instance_file='simple_tests.csp2')
# best_solution, total_time = tabu_search.solve(seed=1)

print(best_solution, total_time)