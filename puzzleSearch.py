from tile import Position
from puzzleState import State


def aStarSearch(state):
    #in open list we put cells that we are going to look
    #in closed list we put tuple (x,y) coordinates of cells that we already looked
    openList = set()
    closedList = set()
    #current - start cell
    current = state #cell(self.mapSize-2,self.mapSize-2,None,self.getCell(heuristic,self.mapSize-2,self.mapSize-2))
    openList.add(current)
    
    while openList:
      temp = sorted(openList, key = lambda State:State.getG(), reverse=True)
      current = sorted(temp, key = lambda State:State.getF())[0]

      if current.getPosition() == '123456780':
        print "A* closed list:"+str(len(closedList))
        print len(openList)
        #self.aStarCheckedNodes = len(closedList)
        #self.aStarOpenNodes = len(openList)
        #self.printPath(current)
        return
      openList.remove(current)
      closedList.add(current)
      neighbors = current.getNeighborStates()
      for n in neighbors:
        if n() not in closedList:
          openList.add(n)
    print "Fail to find path"




f = file("db3x3.txt","r")

neki=f.readlines()
test = neki[0:19]
print test
result=[]
for line in test:
  result.append(line.strip('\n').split(','))

print result
print result[2][0]
print list(result[2][0])






