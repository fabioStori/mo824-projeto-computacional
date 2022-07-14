from utils import *

class Solution():
  def __init__(self, instance, edges):
    self.instance = instance
    self.edges = edges
    self.cost = float('inf')
    self.visited_vertices = []
    self.covered_vertices = []

  def __str__(self):
    return f"Solution: cost = {self.cost}, visted vertices = {self.visited_vertices}, covered vertices = {sorted(self.covered_vertices)}\n"

  def get_visited_vertices(self):
    size = len(self.edges)
    visited_vertices = []   

    for vertice in range(size):
      if self.edges[vertice] != -1: 
        visited_vertices.append(vertice)     

    return visited_vertices

  def get_covered_vertices(self):       
    covered_vertices = []   

    for vertice in self.visited_vertices:
      for cover in self.instance.coverages[vertice]:
        covered_vertices.append(cover)   

    return covered_vertices

  def get_uniques_covered_vertices(self):
    return get_unique_values(self.get_covered_vertices())

  def evaluate_solution_cost(self):      
    sum = 0
    for vertice in self.visited_vertices:       
      sum = sum + self.instance.distances[vertice][self.edges[vertice]]     
    return sum

  def evaluate(self):
    
    self.visited_vertices = self.get_visited_vertices()
    self.covered_vertices = self.get_uniques_covered_vertices()
    self.cost = self.evaluate_solution_cost()

    # print('evaluate', self.visited_vertices, self.covered_vertices, self.cost)

  def all_vertices_covered(self):
    return len(self.covered_vertices) == self.instance.size

  def get_unvisted_vertices(self):
    all_vertices = list(range(self.instance.size))    
    return diff_between_lists(all_vertices, self.visited_vertices)


    