class Solution():
  def __init__(self, instance, edges):
    self.instance = instance
    self.edges = edges
    self.cost = float('inf')
    self.visited_vertices = []
    self.covered_vertices = []

  def __str__(self):
    return f"Solution: cost = {self.cost}, visted vertices = {self.visited_vertices}, covered vertices = {self.visited_vertices}\n"

  def getVisitedVertices(self):
    size = len(self.edges)
    visited_vertices = []   

    for vertice in range(size):
      if 1 in self.edges[vertice]: 
        visited_vertices.append(vertice)  

    return visited_vertices

  def getCoveredVertices(self):       
    covered_vertices = []   

    for vertice in self.visited_vertices:
      for cover in self.instance.coverages[vertice]:
        covered_vertices.append(cover)    
    
    return getUniqueValues(covered_vertices)

  def evaluateSolutionCost(self):     
    #TODO
    return 0

  def evaluate(self):
    self.cost = self.evaluateSolutionCost()
    self.visited_vertices = self.getVisitedVertices()
    self.covered_vertices = self.getCoveredVertices()

# Utils
def getUniqueValues(l):
  return list(dict.fromkeys(l))
    