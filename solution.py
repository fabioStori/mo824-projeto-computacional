class Solution():
  def __init__(self, instance, edges):
    self.instance = instance
    self.edges = edges
    self.cost = float('inf')
    self.visited_vertices = []
    self.covered_vertices = []

  def __str__(self):
    return f"Solution: cost = {self.cost}, visted vertices = {self.visited_vertices}, covered vertices = {self.covered_vertices}\n"

  def getVisitedVertices(self):
    size = len(self.edges)
    visited_vertices = []   

    for vertice in range(size):
      if 1 in self.edges[vertice]: 
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

  def evaluateSolutionCost(self):  
    sum = 0
    for row in range(self.instance.size):
      for col in range(self.instance.size):
        sum = sum + self.edges[row][col] * self.instance.distances[row][col] 

    return sum

  def evaluate(self):
    self.cost = self.evaluateSolutionCost()
    self.visited_vertices = self.getVisitedVertices()
    self.covered_vertices = self.get_uniques_covered_vertices()

  def all_vertices_covered(self):
    return len(self.covered_vertices) == self.instance.size

# Utils
def get_unique_values(l):
  return list(dict.fromkeys(l))
    