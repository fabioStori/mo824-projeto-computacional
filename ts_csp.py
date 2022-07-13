
from random import random
from copy import deepcopy
from datetime import datetime
from instance import Instance
from solution import Solution
from utils import *

class TS_CPS:   
  def __init__(self, ternure, iterations, max_time, instance_file):
    self.instance = self.read_instance_file(instance_file)
    # self.all_cand_list = self.make_cand_list()
    self.rnd = random()
    self.ternure = ternure
    self.iterations = iterations
    self.max_time = max_time

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
        # line.pop()
        distances.append(list(map(int, line)))

      f.readline()
        
      for i in range(size):
        line = f.readline().split(' ')    
        # line.pop()    
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
    pass 

  def evaluate_insertion_cost(element, solution):
    pass

  def evaluate_removal_cost(self, element):       
    cost = None
    if(self.evaluate_removal_viability(element)):    
      in_vertice = self._solution.edges.index(element)
      out_vertice = self._solution.edges[element]
      in_cost = self.instance.distances[in_vertice][element]  
      out_cost = self.instance.distances[element][out_vertice]
      new_cost = self.instance.distances[in_vertice][out_vertice]
      cost = new_cost - (in_cost + out_cost)
    return cost

  def evaluate_removal_viability(self, element):  
    element_cover = self.instance.coverages[element]
    solution_coverage = self._solution.get_covered_vertices()

    new_coverage = get_unique_values(diff_between_list(solution_coverage, element_cover))    

    return (sorted(self._solution.covered_vertices) == sorted(new_coverage)) and (len(new_coverage) == self.instance.size)

  def evaluate_exchange_cost(element, solution):
    pass

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


  def neighborhood_move(self):
    unvisited_vertices = self._solution.get_unvisted_vertices()  

    best_removal_cost = 0
    best_removal_cand = None

    for visited_vertice in self._solution.visited_vertices:        
        removal_cost = self.evaluate_removal_cost(visited_vertice) 
        if removal_cost and removal_cost < best_removal_cost:
          best_removal_cost = removal_cost
          best_removal_cand = visited_vertice
        
        # for unvisited_vertice in unvisited_vertices:          
        #   insert_cost = self.evaluate_insertion_cost(unvisited_vertices) 
        #   evaluate_exchange_cost = self.evaluate_insertion_cost(visited_vertice)    
    
    # remove_cands = self.get_remove_cand_list() 
    
    # best_removal_cost = 0
    # best_removal_cand = None
    # for cand in remove_cands:
    #   removal_cost = self.evaluate_removal_cost(cand)    
    #   if removal_cost < best_removal_cost:
    #     best_removal_cost = removal_cost
    #     best_removal_cand = cand

    print(best_removal_cost, best_removal_cand)
    
    self.remove_vertice_from_solution(best_removal_cand)
    self._solution.evaluate()      

  def remove_vertice_from_solution(self, vertice):    
    in_vertice = self._solution.edges.index(vertice)
    out_vertice = self._solution.edges[vertice]

    self._solution.edges[vertice] = -1
    self._solution.edges[in_vertice] = out_vertice 


  def solve(self):    
    start_time = datetime.now()    

    self.constructive_heuristic()

    self._best_solution = deepcopy(self._solution)

    print(self._solution)

    self.make_tabu_list() 

    for i in range(self.iterations):      
      self.neighborhood_move()     

      if (self._solution.cost < self._best_solution.cost):
        self._best_solution = deepcopy(self._solution)
        print(self._best_solution)
      
      elapsed_time = datetime.now() - start_time

      # if(elapsed_time > self.max_time):
      #   print("Interrupting: Time Exceed")

    return self._best_solution, elapsed_time
      
