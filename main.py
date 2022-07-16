import os
from ts_csp import TS_CSP

max_time = 60*60

files = os.listdir('InstancesCSP')

for file in files:
  tabu_search = TS_CSP(
    ternure_porcent=0.2,
    iterations=1000,
    max_time=max_time,
    instance_file=file,
    improve='best',
    const_heuristic='greedy',
    probabilistic_ts=False,
    # max_iter_no_improve=100,
    diversification=True,
    diversificate_in=1
  )
  best_solution, total_time = tabu_search.solve(seed=2)
  f = open('all_instances_ts_random_bi.out', 'a')
  f.write(f"{file}  {best_solution.cost}  {total_time} \n")
  f.close()
  
print(best_solution, total_time)