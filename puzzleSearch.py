from tile import Position
from puzzleState import State
import time


def aStarSearch(start_state, heuristic):#, exact_part, noise_type, noise_magnitude):
    #in open list we put cells that we are going to look
    #in closed list we put tuple (x,y) coordinates of cells that we already looked
    openList = set()
    closedList = set()
    current = start_state
    openList.add(current)
    
    while openList:
      temp = sorted(openList, key = lambda State:State.getG(), reverse=True)
      current = sorted(temp, key = lambda State:State.getF())[0]

      if current.getPosition() == '123456780':
        print "A* closed list:", len(closedList)
        print "open list:", len(openList)
        print "sum:", len(closedList)+len(openList)
        #self.aStarCheckedNodes = len(closedList)
        #self.aStarOpenNodes = len(openList)
        #self.printPath(current)
        return
      openList.remove(current)
      closedList.add(current)
      neighbors = getNeighborStates(current,heuristic)
      for n in neighbors:
        if n not in closedList:
          openList.add(n)
    print "Fail to find path"


def getNeighborStates(start_position, heuristic):
  neighbors=[]
  nexts = start_position.getNeighborPositions()
  print nexts
  for next in nexts:
    neighbors.append(State(next,start_position,heuristic[next]))
  return neighbors


def exactHeuristic():
  f = file("db3x3.txt","r")
  lines=f.readlines()
  heuristic = {'123456780':0}
  for line in lines:
    temp = line.strip('\n').split(',')
    if int(temp[1]) != -100:
      heuristic[temp[0]]=int(temp[1])
    
  return heuristic


def distortHeuristic(h, noise_type, noise_magnitude):
  
  
  noisy_heuristic = {'123456780':0}
  
  return noisy_heuristic

## sumljenje hevristike

## ida*


start = time.clock()
h = exactHeuristic()
print 'nalaganje hevristike:', time.clock()-start
print '---'
start = time.clock()
aStarSearch(State('012345678',None,22),h)
print 'A* alg:', time.clock()-start



