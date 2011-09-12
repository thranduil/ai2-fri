
## Description of a state of 8-puzzle (locations of tiles)
## for the use in A* and IDA* search
class State():
  position = '123456780'
  parent = None
  #f(x) = g(x) + h(x)
  h = None
  g = None
  
  def __init__(self,pos,parent,heuristic):
    self.position = pos
    self.parent = parent
    self.h = heuristic
    if self.parent == None:
      self.g = 0
    else:
      self.g = parent.getG() + 1
  
  
  ##get current path g(x)
  def getG(self):
    return self.g
  
  ##get heuristic score for cell
  def getH(self):
    return self.h
  
  ##get f(x) for cell
  def getF(self):
    return self.h + self.g
  
  ##get position
  def getPosition(self):
    return self.position

  def printPosition(self):
    print self.position[:3]
    print self.position[3:6]
    print self.position[6:]
    
  ## possible moves
  def getNeighborStates(self):
    pos = list(self.position)
    empty = pos.index('0')
    neighbours = []
    temp = pos
    if empty==0:
      pos[0]=pos[1]; pos[1]='0'; neighbours.append("".join(pos));
      pos = temp; pos[0]=pos[3]; pos[3]='0'; neighbours.append("".join(pos));
    elif empty==1:
      pos[1]=pos[0]; pos[0]='0'; neighbours.append("".join(pos));
      pos = temp; pos[1]=pos[4]; pos[4]='0'; neighbours.append("".join(pos));
      pos = temp; pos[1]=pos[2]; pos[2]='0'; neighbours.append("".join(pos));
    elif empty==2:
      pos[2]=pos[1]; pos[1]='0'; neighbours.append("".join(pos));
      pos = temp; pos[2]=pos[5]; pos[5]='0'; neighbours.append("".join(pos));
    elif empty==3:
      pos[3]=pos[0]; pos[0]='0'; neighbours.append("".join(pos));
      pos = temp; pos[3]=pos[4]; pos[4]='0'; neighbours.append("".join(pos));
      pos = temp; pos[3]=pos[6]; pos[6]='0'; neighbours.append("".join(pos));
    elif empty==4:
      pos[4]=pos[3]; pos[3]='0'; neighbours.append("".join(pos));
      pos = temp; pos[4]=pos[1]; pos[1]='0'; neighbours.append("".join(pos));
      pos = temp; pos[4]=pos[5]; pos[5]='0'; neighbours.append("".join(pos));
      pos = temp; pos[4]=pos[7]; pos[5]='0'; neighbours.append("".join(pos));
    elif empty==5:
      pos[5]=pos[2]; pos[2]='0'; neighbours.append("".join(pos));
      pos = temp; pos[5]=pos[4]; pos[4]='0'; neighbours.append("".join(pos));
      pos = temp; pos[5]=pos[8]; pos[8]='0'; neighbours.append("".join(pos));
    elif empty==6:
      pos[6]=pos[3]; pos[3]='0'; neighbours.append("".join(pos));
      pos = temp; pos[6]=pos[7]; pos[7]='0'; neighbours.append("".join(pos));
    elif empty==7:
      pos[7]=pos[4]; pos[4]='0'; neighbours.append("".join(pos));
      pos = temp; pos[7]=pos[6]; pos[6]='0'; neighbours.append("".join(pos));
      pos = temp; pos[7]=pos[8]; pos[8]='0'; neighbours.append("".join(pos));
    elif empty==8:
      pos[8]=pos[5]; pos[5]='0'; neighbours.append("".join(pos));
      pos = temp; pos[8]=pos[7]; pos[7]='0'; neighbours.append("".join(pos));
    else:
      print 'FAIL! - Incorrect empty index at getNeighbourStates.'
    
  
  
  ##redefine hash and compare
  def __hash__(self):
    tiles = list(self.position)
    hash = 0
    for tile in tiles:
      hash = hash*10+int(tile)
    return hash
  
  def __eq__(self, other):
    if self.__hash__() == other.__hash__():
      return True
    return False
  
  
  
    



