class cell():
  x = None
  y = None
  parent = None
  #f(x) = g(x) + h(x)
  h = None
  g = None
  
  def __init__(self,x,y,parent,heuristic):
    self.x = x
    self.y = y
    self.parent = parent
    #heuristic can be # if this cell cant reach finish
    heu = str(heuristic)
    if heu != heuristic:
      self.h = heuristic
    else:
      self.h = 0
    #
    if self.parent == None:
      self.g = 0
    else:
      self.g = parent.getG() + 1
  
  def __str__(self):
    return "[" + str(self.x) + "," + str(self.y)+"]"

  def __repr__(self):
    return "[" + str(self.x) + "," + str(self.y)+"]"
  
  ##get current path g(x)
  def getG(self):
    return self.g
  
  ##get heuristic score for cell
  def getH(self):
    return self.h
  
  ##get f(x) for cell
  def getF(self):
    return self.h + self.g
  
  ##get current row
  def getX(self):
    return self.x
  
  ##get current column  
  def getY(self):
    return self.y
  
  ##get coordinate tuple
  def getXY(self):
    return (self.x,self.y)
  
  
    