class Instance: 
  def __init__(self, name, size, cover_size, distances, coverages):      
    self.name = name
    self.size = size
    self.cover_size = cover_size
    self.distances = distances
    self.coverages = coverages

  def __str__(self):
    return f"Instance {self.name} size = {self.size}, cover_size = {self.cover_size}\n distances = {self.distances} \n coverages = {self.coverages}"
