def jaccardSimilarity(setOne, setTwo):
  return len(setOne & setTwo) / len(setOne | setTwo)