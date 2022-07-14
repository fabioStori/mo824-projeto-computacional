from collections import deque

class TabuList(deque):
  def __init__(self, size):
    self._size = size

  def add(self, element):
    if len(self) == self._size:
      self.popleft()
      self.append(element)

    else:
      self.append(element)
  