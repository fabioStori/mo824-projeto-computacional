from collections import Counter

def get_unique_values(l):
  return list(dict.fromkeys(l))

def diff_between_list(list1, list2): 
  return list((Counter(list1) - Counter(list2)).elements())