
import random
from copy import deepcopy
from datetime import datetime
from instance import Instance
from solution import Solution
from tabulist import TabuList
from utils import *

class TS_CSP:   
  def __init__(self, ternure_porcent, iterations, max_time, instance_file, improve='best', const_heuristic='random', probabilistic_ts=False, max_iter_no_improve=None, diversification=False, diversificate_in=0):
    self.instance = self.read_instance_file(instance_file)    
    self.rnd = random    
    self.ternure = round(ternure_porcent*self.instance.size)
    self.iterations = iterations
    self.max_time = max_time
    self.improve = improve
    self.const_heuristic = const_heuristic
    self.probabilistic_ts = probabilistic_ts
    self.max_iter_no_improve = max_iter_no_improve
    self.diversification = diversification
    self.diversificate_in = diversificate_in

    self._best_solution = None
    self._solution = None
    self._cost = None
    self._freq_list = None
    self._tabu_list = None

  def read_instance_file(self, file):   
    with open('./InstancesCSP/'+file, 'r') as f:     

      name = f.readline()
      size = int(f.readline())
      cover_size = int(f.readline())      
                 
      f.readline()      
      distances = []
      coverages = []

      for i in range(size):
        line = f.readline().split(' ')
        line.pop()
        distances.append(list(map(int, line)))

      f.readline()
        
      for i in range(size):
        line = f.readline().split(' ')    
        line.pop()
        coverages.append(list(map(int, line)))

    return Instance(name, size, cover_size, distances, coverages)

  def get_remove_cand_list(self):
    remove_cands = []
    visited_vertices = self._solution.visited_vertices  
    covered_vertices = self._solution.get_covered_vertices()    

    multi_covered_vertices = [vertice for n, vertice in enumerate(covered_vertices) if vertice in covered_vertices[:n]]  

    for cand in multi_covered_vertices: 
      if cand in visited_vertices:
        
        remove_cands.append(cand)
    return remove_cands

  def make_tabu_list(self):
    self._tabu_list = TabuList(self.ternure)     


  def evaluate_insertion_cost(self, ref_vertice, insert_vertice):
    cost = None
    dest_vertice = self._solution.edges[ref_vertice]
    removed_edge_cost = self.instance.distances[ref_vertice][dest_vertice]
    inserted_edges_cost = self.instance.distances[ref_vertice][insert_vertice] + self.instance.distances[insert_vertice][dest_vertice]
    cost = inserted_edges_cost - removed_edge_cost
    return cost

  def evaluate_removal_cost(self, element, accept_non_viable_solution = False):
    cost = None
    if(self.evaluate_removal_viability(element) or accept_non_viable_solution):      
      in_vertice = self._solution.edges.index(element)
      out_vertice = self._solution.edges[element]
      in_cost = self.instance.distances[in_vertice][element]
      out_cost = self.instance.distances[element][out_vertice]
      new_cost = self.instance.distances[in_vertice][out_vertice]
      cost = new_cost - (in_cost + out_cost)
    return cost

  def evaluate_swap_cost(self, element):       
    cost = 0
    best_vertice = None
    all_visited_minus_current = deepcopy(self._solution.visited_vertices)
    all_visited_minus_current.remove(self._solution.edges[element])
    all_visited_minus_current.remove(self._solution.edges.index(element))
    all_visited_minus_current.remove(element)
    
    for vertice in all_visited_minus_current:
      removal_cost = self.evaluate_removal_cost(vertice, True)
      insertion_cost = self.evaluate_insertion_cost(element, vertice)
      final_cost = insertion_cost + removal_cost
      
      if (final_cost < cost):
        best_vertice = vertice
        cost = final_cost
    
    return cost, best_vertice

  def evaluate_removal_viability(self, element):  
    element_cover = self.instance.coverages[element]
    solution_coverage = self._solution.get_covered_vertices()
    new_coverage = get_unique_values(diff_between_lists(solution_coverage, element_cover))   

    return (sorted(self._solution.covered_vertices) == sorted(new_coverage)) and (len(new_coverage) == self.instance.size)

  def evaluate_exchange_cost(self, removed_vertice, insert_vertice):
    cost = None
    if(self.evaluate_exchange_viability(removed_vertice, insert_vertice)):
      in_edge_removed = self._solution.edges.index(removed_vertice)
      out_edge_removed = self._solution.edges[removed_vertice]

      remove_cost = self.instance.distances[in_edge_removed][removed_vertice] + self.instance.distances[removed_vertice][out_edge_removed]
      add_cost = self.instance.distances[in_edge_removed][insert_vertice] + self.instance.distances[insert_vertice][out_edge_removed]

      cost = add_cost - remove_cost       
    return cost

  def evaluate_exchange_viability(self, removed_vertice, insert_vertice):
    solution_coverage = self._solution.get_covered_vertices()
    removed_vertice_cover = self.instance.coverages[removed_vertice]
    insert_vertice_cover = self.instance.coverages[insert_vertice]

    removed_coverage = diff_between_lists(solution_coverage, removed_vertice_cover)
    new_coverage = get_unique_values(sum_lists(removed_coverage, insert_vertice_cover))

    return (sorted(self._solution.covered_vertices) == sorted(new_coverage)) and (len(new_coverage) == self.instance.size)
    
  def make_freq_list(self):
    self._freq_list = []
    best_solution = self._best_solution
    
    for vertice in range(self.instance.size):
      if(vertice in best_solution.visited_vertices):
        self._freq_list.append(1)
      else:
        self._freq_list.append(0)      

  def update_freq_list(self):
    best_solution = self._best_solution
    
    for vertice in range(self.instance.size):
      if(vertice in best_solution.visited_vertices):
        self._freq_list[vertice] += 1   


  def reset_freq_list(self): 
    for vertice in range(self.instance.size):
      self._freq_list[vertice] = 0 

  def create_empty_solution(self):     
    size = self.instance.size      
    edges = [-1 for i in range(size)]      

    return Solution(self.instance, edges)

  def constructive_heuristic(self):
    self._solution = self.create_empty_solution()    
    i = 0
    
    while(not(self._solution.all_vertices_covered())):      
      self._solution.edges[i] = i+1
      self._solution.evaluate()
      i+=1  

    self._solution.edges[i-1] = 0
    self._solution.evaluate() 

  def random_constructive_heuristic(self):
    self._solution = self.create_empty_solution()     

    start_vertice = self.rnd.randrange(self.instance.size) 

    i = start_vertice

    while(not(self._solution.all_vertices_covered())): 
      random_vertice = self.rnd.randrange(self.instance.size)
      if random_vertice not in self._solution.covered_vertices and random_vertice != start_vertice:
        self._solution.edges[i] = random_vertice        
        i = random_vertice
        self._solution.evaluate()       
    
    self._solution.edges[i] = start_vertice
    self._solution.evaluate() 

  def get_best_neighbor(self, vertice):
    best_cost = float('inf')
    best_neighbor = None

    for i in range(self.instance.size):
      cost = self.instance.distances[vertice][i]
      cover = i in self._solution.covered_vertices

      if(cost < best_cost and cost > 0 and not cover and i != vertice):
        best_cost = cost
        best_neighbor = i   
    
    return best_cost, best_neighbor
   

  def greedy_constructive_heuristic(self):
    self._solution = self.create_empty_solution()
    start_vertice = self.rnd.randrange(self.instance.size)    
    vertice = start_vertice

    coverage = self.instance.coverages[start_vertice]    

    while (len(coverage) < self.instance.size):       
      best_cost, best_vertice = self.get_best_neighbor(vertice)      
      self._solution.edges[vertice] = best_vertice      
      vertice = best_vertice
      self._solution.evaluate()  
      coverage = get_unique_values(sum_lists(self._solution.get_uniques_covered_vertices(), self.instance.coverages[vertice]))         
  
    self._solution.edges[vertice] = start_vertice
    self._solution.evaluate() 
  
  def get_random_neighborhood(self, current_list):
    list = deepcopy(current_list)

    rand_size = self.rnd.randrange(1, len(list))
    random.shuffle(list)    
    
    return list[:rand_size]


  def neighborhood_move(self):
    
    best_removal_cost = float('inf')
    best_removal_cand = None

    best_swap_cost = float('inf')
    best_swap_cand = None
    best_swap_ref = None

    best_insert_cost = float('inf')
    best_insert_cand = None

    best_exchange_cost = float('inf')
    best_exchange_cand = None

    insert_ref = None
    exchange_remove_cand = None
    
    best_found = False

    unvisited_vertices = self._solution.get_unvisted_vertices()  
    visited_vertices = self._solution.visited_vertices

    if(self.probabilistic_ts == True):
      visited_vertices = self.get_random_neighborhood(visited_vertices)
      unvisited_vertices = self.get_random_neighborhood(unvisited_vertices)


    for visited_vertice in visited_vertices:
      removal_cost = self.evaluate_removal_cost(visited_vertice) 
      if removal_cost and removal_cost < best_removal_cost:
        best_removal_cost = removal_cost
        best_removal_cand = visited_vertice
        if(self.improve == 'first'):
          break        
        
      swap_cost, swap_vertice = self.evaluate_swap_cost(visited_vertice) 
      if swap_cost and swap_cost < best_swap_cost:
        best_swap_cost = swap_cost
        best_swap_cand = swap_vertice
        best_swap_ref = visited_vertice 
        if(self.improve == 'first'):
          break
        
      for unvisited_vertice in unvisited_vertices:             
        insert_cost = self.evaluate_insertion_cost(visited_vertice, unvisited_vertice)         
        if insert_cost and insert_cost < best_insert_cost:
          best_insert_cost = insert_cost
          best_insert_cand = unvisited_vertice
          insert_ref = visited_vertice
          if(self.improve == 'first'):
            best_found = True
            break   

        exchange_cost = self.evaluate_exchange_cost(visited_vertice, unvisited_vertice)    
        if exchange_cost and exchange_cost < best_exchange_cost:
          best_exchange_cost = exchange_cost
          best_exchange_cand = unvisited_vertice
          exchange_remove_cand = visited_vertice
          if(self.improve == 'first'):
            best_found = True
            break 

      if(self.improve == 'first' and best_found):
        break   

    if(best_removal_cand in self._tabu_list and not (self._solution.cost + best_removal_cost < self._best_solution.cost)):      
      best_removal_cand = None
      best_removal_cost = float('inf')

    if(best_swap_cand in self._tabu_list and not (self._solution.cost + best_swap_cost < self._best_solution.cost)):
      best_swap_cand = None
      best_swap_cost = float('inf')

    if(best_insert_cand in self._tabu_list and not (self._solution.cost + best_insert_cost < self._best_solution.cost)):
      best_insert_cand = None
      best_insert_cost = float('inf')

    if(best_exchange_cand in self._tabu_list and not (self._solution.cost + best_exchange_cost < self._best_solution.cost)):
      best_exchange_cand = None
      best_exchange_cost = float('inf')

    ops = {'remove': best_removal_cost, 'swap': best_swap_cost, 'insert': best_insert_cost, 'exchange': best_exchange_cost}
    min = self.get_minvalue_index(list(ops.values()))
    op = list(ops)[min]

    if(best_removal_cand != None and op == 'remove'):     
      self._solution.remove_vertice_from_solution(best_removal_cand)
      self._tabu_list.add(best_removal_cand)    
    
    elif(best_swap_cand != None and op == 'swap'):      
      self._solution.swap_vertice_from_solution(best_swap_cand, best_swap_ref)
      self._tabu_list.add(best_swap_cand)
      self._tabu_list.add(best_swap_ref) 

    elif(best_insert_cand != None and op == 'insert'):      
      self._solution.insert_vertice_in_solution(best_insert_cand, insert_ref)
      self._tabu_list.add(best_insert_cand)  

    elif(best_exchange_cand != None and op == 'exchange'):      
      self._solution.exchange_vertices_in_solution(best_exchange_cand, exchange_remove_cand)
      self._tabu_list.add(best_exchange_cand) 
      self._tabu_list.add(exchange_remove_cand) 

    else: 
      return False    

    self._solution.evaluate()
    return True

  def get_minvalue_index(self, inputlist):
    min_value = min(inputlist)
    min_index = inputlist.index(min_value)
    return min_index
  
  def diversificate(self): 
    new_solution = self.create_empty_solution()

    freq = deepcopy(self._freq_list) 
    start_min_index = self.get_minvalue_index(freq)         
    freq[start_min_index] = float('inf')

    vertice = start_min_index  
    coverage = self.instance.coverages[vertice] 

    while (len(coverage) < self.instance.size):  
      min_freq_vertice = self.get_minvalue_index(freq) 
      freq[min_freq_vertice] = float('inf')        
      new_solution.edges[vertice] = min_freq_vertice      
      vertice = min_freq_vertice
      new_solution.evaluate() 
      coverage = get_unique_values(sum_lists(new_solution.get_uniques_covered_vertices(), self.instance.coverages[vertice]))  

    new_solution.edges[vertice] = start_min_index
    new_solution.evaluate() 

    self._solution = deepcopy(new_solution)

    self.make_freq_list()
    self.make_tabu_list() 


  def solve(self, seed):       
    self.rnd.seed(seed) 

    start_time = datetime.now()  

    if (self.const_heuristic == 'greedy'):
      self.greedy_constructive_heuristic()
    else:
      self.random_constructive_heuristic()

    self._best_solution = deepcopy(self._solution)

    self.make_tabu_list() 

    if self.diversification:
      self.make_freq_list()

    iter_no_improve_best_solution = 0 
    iter_no_improve_cur_solution = 0

    for i in range(self.iterations):      
      improve_solution = self.neighborhood_move() 

      if (self._solution.cost < self._best_solution.cost):
        self._best_solution = deepcopy(self._solution)
        iter_no_improve_best_solution = 0
      else:
        iter_no_improve_best_solution+=1      

      elapsed_time = (datetime.now() - start_time).total_seconds()
      
      if self.max_iter_no_improve != None and iter_no_improve_best_solution > self.max_iter_no_improve:
        print("Interrupting: Max iteration without improvement reach")
        break  

      if(self.max_time-1 < int(elapsed_time)):
        print("Interrupting: Time Exceed")
        break

      if(not improve_solution):
        iter_no_improve_cur_solution+=1
      
      if self.diversification:
        self.update_freq_list()        
        if iter_no_improve_cur_solution == self.diversificate_in:  
          self.diversificate()
          iter_no_improve_cur_solution = 0 

    return self._best_solution, elapsed_time
      
