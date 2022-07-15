
import random
from copy import deepcopy
from datetime import datetime
from instance import Instance
from solution import Solution
from tabulist import TabuList
from utils import *

class TS_CSP:   
  def __init__(self, ternure_porcent, iterations, max_time, instance_file, improve='best'):
    self.instance = self.read_instance_file(instance_file)
    # self.all_cand_list = self.make_cand_list()
    self.rnd = random    
    self.ternure = ternure_porcent*self.instance.size
    self.iterations = iterations
    self.max_time = max_time
    self.improve = improve

    self._best_solution = None
    self._solution = None
    self._cost = None
    self._cand_list = None
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

    # print(remove_cands, covered_vertices, multi_covered_vertices)

    return remove_cands

  def make_tabu_list(self):
    self._tabu_list = TabuList(2*self.ternure)     


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

      # print(self._solution.edges)

      # print('removed', removed_vertice )      
      # print('(', in_edge_removed,  removed_vertice, ')', self.instance.distances[in_edge_removed][removed_vertice])
      # print('(', removed_vertice, out_edge_removed, ')', self.instance.distances[removed_vertice][out_edge_removed])

      # print('added', insert_vertice )
      # print('(', in_edge_removed,  insert_vertice, ')', self.instance.distances[in_edge_removed][insert_vertice])
      # print('(', insert_vertice, out_edge_removed, ')', self.instance.distances[insert_vertice][out_edge_removed])

      remove_cost = self.instance.distances[in_edge_removed][removed_vertice] + self.instance.distances[removed_vertice][out_edge_removed]
      add_cost = self.instance.distances[in_edge_removed][insert_vertice] + self.instance.distances[insert_vertice][out_edge_removed]

      cost = add_cost - remove_cost     

      # print(self._solution.edges)
      # print(removed_vertice, in_edge_removed, out_edge_removed)      
    return cost

  def evaluate_exchange_viability(self, removed_vertice, insert_vertice):
    solution_coverage = self._solution.get_covered_vertices()
    removed_vertice_cover = self.instance.coverages[removed_vertice]
    insert_vertice_cover = self.instance.coverages[insert_vertice]

    removed_coverage = diff_between_lists(solution_coverage, removed_vertice_cover)
    new_coverage = get_unique_values(sum_lists(removed_coverage, insert_vertice_cover))

    return (sorted(self._solution.covered_vertices) == sorted(new_coverage)) and (len(new_coverage) == self.instance.size)
    

  def update_cand_list():
    pass

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

  def constructive_heuristic_v2(self):
    self._solution = self.create_empty_solution()     

    start_vertice = self.rnd.randrange(self.instance.size)

    # print('sv', start_vertice)

    i = start_vertice

    while(not(self._solution.all_vertices_covered())): 
      random_vertice = self.rnd.randrange(self.instance.size)
      # print(random_vertice, self._solution.get_covered_vertices(), self._solution.edges)
      if random_vertice not in self._solution.covered_vertices and random_vertice != start_vertice:
        self._solution.edges[i] = random_vertice        
        i = random_vertice
        self._solution.evaluate()       

    
    self._solution.edges[i] = start_vertice
    self._solution.evaluate() 

    # print('meta', self._solution.edges)

  def constructive_heuristic_v3(self):
    self._solution = self.create_empty_solution()     

    start_vertice = self.rnd.randrange(self.instance.size)
    
    i = start_vertice

    while(not(self._solution.all_vertices_covered())): 
      random_vertice = self.rnd.randrange(self.instance.size)
      # print(random_vertice, self._solution.get_covered_vertices(), self._solution.edges)
      if random_vertice not in self._solution.covered_vertices and random_vertice != start_vertice:
        self._solution.edges[i] = random_vertice        
        i = random_vertice
        self._solution.evaluate()       

    
    self._solution.edges[i] = start_vertice
    self._solution.evaluate() 

    # print('meta', self._solution.edges)


  def neighborhood_move(self):
    unvisited_vertices = self._solution.get_unvisted_vertices()  

    best_removal_cost = 0
    best_removal_cand = None

    best_swap_cost = 0
    best_swap_cand = None
    best_swap_ref = None

    best_insert_cost = 0
    best_insert_cand = None

    best_exchange_cost = 0
    best_exchange_cand = None

    insert_ref = None
    exchange_remove_cand = None
    
    best_found = False

    for visited_vertice in self._solution.visited_vertices:
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
                   

    # print('remove:', best_removal_cost, best_removal_cand)
    # print('insert:', best_insert_cost, best_insert_cand, insert_ref)
    # print('exchange:', best_exchange_cost, best_exchange_cand, exchange_remove_cand)
    
    if(best_removal_cand != None and 
        best_removal_cost < 0 and 
          (best_removal_cost <= best_insert_cost and best_removal_cost <= best_exchange_cost and best_removal_cost <= best_swap_cost) and
            (best_removal_cand not in self._tabu_list or self._best_solution.cost > self._solution.cost + best_removal_cost)):
      # print('remove', best_removal_cand, best_removal_cost)
      self.remove_vertice_from_solution(best_removal_cand)
      self._tabu_list.add(best_removal_cand)    
    
    elif(best_swap_cand != None and 
        best_swap_cost < 0 and 
          (best_swap_cost <= best_insert_cost and best_swap_cost <= best_exchange_cost and best_swap_cost <= best_removal_cost) and
            (best_swap_cand not in self._tabu_list or self._best_solution.cost > self._solution.cost + best_swap_cost)):
      # print('swap', best_swap_cand)
      self.swap_vertice_from_solution(best_swap_cand, best_swap_ref)
      self._tabu_list.add(best_swap_cand)
      self._tabu_list.add(best_swap_ref) 

    elif(best_insert_cand != None and
          best_insert_cost < 0 and
            (best_insert_cost <= best_removal_cost and best_insert_cost <= best_exchange_cost and best_insert_cost <= best_swap_cost) and
              (best_insert_cand not in self._tabu_list or self._best_solution.cost > self._solution.cost + best_insert_cost)):
      # print('insert', best_insert_cand, insert_ref)
      self.insert_vertice_in_solution(best_insert_cand, insert_ref)
      self._tabu_list.add(best_insert_cand)  

    elif(best_exchange_cand != None and
           best_exchange_cost < 0 and
            (best_exchange_cost <= best_removal_cost and best_exchange_cost <= best_insert_cost and best_exchange_cost <= best_swap_cost) and
              (best_exchange_cand not in self._tabu_list and exchange_remove_cand not in self._tabu_list or self._best_solution.cost > self._solution.cost + best_exchange_cost)):
      # print('exchange', exchange_remove_cand, 'for', best_exchange_cand)
      self.exchange_vertices_in_solution(best_exchange_cand, exchange_remove_cand)
      self._tabu_list.add(best_exchange_cand) 
      self._tabu_list.add(exchange_remove_cand) 

    else: 
      return False

    self._solution.evaluate()   
    return True


  def remove_vertice_from_solution(self, vertice):    
    in_vertice = self._solution.edges.index(vertice)
    out_vertice = self._solution.edges[vertice]

    self._solution.edges[vertice] = -1
    self._solution.edges[in_vertice] = out_vertice

  def swap_vertice_from_solution(self, best_swap_cand, best_swap_ref):
    self.remove_vertice_from_solution(best_swap_cand)
    self.insert_vertice_in_solution(best_swap_cand, best_swap_ref)

  def insert_vertice_in_solution(self, inserted_vertice, ref_vertice):
    edges = self._solution.edges 
    dest_vertice = edges[ref_vertice]  
    edges[ref_vertice] = inserted_vertice
    edges[inserted_vertice] = dest_vertice    

  def exchange_vertices_in_solution(self, inserted_vertice, removed_vertice):        
    edges = self._solution.edges 

    orig_vertice = edges.index(removed_vertice)
    dest_vertice = edges[removed_vertice]
    edges[removed_vertice] = -1
    edges[orig_vertice] = inserted_vertice
    edges[inserted_vertice] = dest_vertice  
    

  def solve(self, seed):   
    
    self.rnd.seed(seed) 

    start_time = datetime.now()    

    self.constructive_heuristic_v2()

    self._best_solution = deepcopy(self._solution)

    print(self._solution.cost)

    self.make_tabu_list() 

    for i in range(self.iterations):      
      improve = self.neighborhood_move()    

      if (self._solution.cost < self._best_solution.cost):
        self._best_solution = deepcopy(self._solution)
        # print('tabulist', self._tabu_list)
      
      print(self._best_solution.cost)

      elapsed_time = (datetime.now() - start_time).total_seconds()

      if not improve:
        print("Interrupting: Solution not improving")
        break      

      if(self.max_time-1 < int(elapsed_time)):
        print("Interrupting: Time Exceed")
        break

    return self._best_solution, elapsed_time
      
