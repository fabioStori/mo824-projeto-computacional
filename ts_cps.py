
from random import random
from datetime import datetime
from instance import Instance
from solution import Solution

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
        line.pop()
        distances.append(list(map(int, line)))

      f.readline()
        
      for i in range(size):
        line = f.readline().split(' ')        
        coverages.append(list(map(int, line)))

    return Instance(name, size, cover_size, distances, coverages)

  def make_cand_list(self):
    pass

  def make_tabu_list(self):
    pass

  def evaluate(solution):
    pass

  def evaluate_insertion_cost(element, solution):
    pass

  def evaluate_removal_cost(element, solution):
    pass

  def evaluate_exchange_cost(element, solution):
    pass

  def update_cand_list():
    pass

  def create_empty_solution(self):     
    size = self.instance.size      
    edges = [[0  for i in range(size)] for j in range(size)] 
    return Solution(self.instance, edges)

  def constructive_heuristic(self):
    pass

  def neighborhood_move(self):
    pass

  def solve(self):    
    start_time = datetime.now()

    self._best_solution = self.create_empty_solution()
    # self.constructive_heuristic()
    self._tabu_list = self.make_tabu_list()    

    for i in range(self.iterations):      
      self.neighborhood_move()
      
      # if (self._solution.cost < self._best_solution.cost):
      #   self._best_solution = self._solution
      #   print(self._best_solution)
      
      elapsed_time = datetime.now() - start_time

      # if(elapsed_time > self.max_time):
      #   print("Interrupting: Time Exceed")

    return self._best_solution, elapsed_time
      