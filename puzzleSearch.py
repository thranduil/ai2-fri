from tile import Position
from puzzleState import State
import random
import time


##perform A* search on given 8-puzzle problem; implemented noise distortion
def aStarSearch(start_state, heuristic, exact_part, noise_type, noise_magnitude):
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
        print solutionPath(current)
        return
      openList.remove(current)
      closedList.add(current)
      neighbors = getNeighborStates(current,heuristic, start_state.getH(), exact_part, noise_type, noise_magnitude)
      for n in neighbors:
        if n not in closedList:
          openList.add(n)
    print "Fail to find path"


Infinity = float("inf")
##preform IDA* search on given 8-puzzle problem
def idaStarSearch(start_state, heuristic, exact_part, noise_type, noise_magnitude):
  rootNode = start_state
  costLimit = rootNode.getH()
  c=0
  while True:
    (solution, costLimit,c) = DFS(0, rootNode, costLimit, [rootNode], heuristic, exact_part, noise_type, noise_magnitude,c)
    if solution != None:
      print 'count:',c
      return (solution, costLimit)
    if costLimit == Infinity:
      return None

##depth first search for IDA*
def DFS(startCost, node, costLimit, currentPath, heuristic, exact_part, noise_type, noise_magnitude,c):
  c+=1
  minimumCost = startCost + node.getH()
  if minimumCost > costLimit:
    return (None, minimumCost,c)
  if node.position == '123456780':
    return (currentPath, costLimit,c)
    
  
  nextCostLimit = Infinity
  neighbors = getNeighborStates(node, heuristic, heuristic[currentPath[0].getPosition()], exact_part, noise_type, noise_magnitude)
  for succNode in neighbors:
    newStartCost = startCost + 1
    (solution, newCostLimit,c) = DFS(newStartCost, succNode, costLimit, currentPath + [succNode], heuristic, exact_part, noise_type, noise_magnitude,c)
    if solution != None:
      return (solution, newCostLimit,c)
    nextCostLimit = min(nextCostLimit, newCostLimit)
  return (None,nextCostLimit,c)


def getNeighborStates(start_position, heuristic, solution_length, exact_part, noise_type, noise_magnitude):
  neighbors=[]
  nexts = start_position.getNeighborPositions()
  for next in nexts:
    noisy_h = distortHeuristic(heuristic[next], solution_length, exact_part, noise_type, noise_magnitude)
    neighbors.append(State(next,start_position,noisy_h))
  return neighbors


def distortHeuristic(h, solution_length, exact_part, noise_type, noise_magnitude):
  new_h = h
  
  if exact_part == 'start':
    if h > round(solution_length/3):
      new_h = calculateNoise(h, noise_type, noise_magnitude)
      
  elif exact_part == 'middle':
    if h < round(solution_length/3) or h > round(2*solution_length/3):
      new_h = calculateNoise(h, noise_type, noise_magnitude)
      
  elif exact_part == 'end':
    if h < round(2*solution_length/3):
      new_h = calculateNoise(h, noise_type, noise_magnitude)
      
  return new_h


def calculateNoise(h, noise_type, noise_magnitude):
  x = h
  
  if noise_type == 'gauss':
    x = int(round(random.gauss(h,float(h)*noise_magnitude)))
    
  elif noise_type == 'optimistic_gauss':
    x=h+1
    while x > h:
      x = int(round(random.gauss(h,float(h)*noise_magnitude)))
  
  return x


def exactHeuristic():
  f = file("db3x3.txt","r")
  lines=f.readlines()
  heuristic = {'123456780':0}
  for line in lines:
    temp = line.strip('\n').split(',')
    if int(temp[1]) != -100:
      heuristic[temp[0]]=int(temp[1])
    
  return heuristic


def solutionsDistribution(heuristics):
  distribution = []
  for i in range(32):
    distribution.append([i,0])
  
  for k,v in heuristics.iteritems():
    distribution[v][1]+=1
  
  return distribution


def solutionPath(ending_position):
  path = ['',['123456780']]
  node = ending_position
  while node.parent != None:
    row = list(node.position).index('0')/3
    col = list(node.position).index('0')%3
    rowp = list(node.parent.position).index('0')/3
    colp = list(node.parent.position).index('0')%3
    if rowp < row: path[0] = 'D'+path[0]
    elif rowp > row: path[0] = 'U'+path[0]
    elif colp < col: path[0] = 'R'+path[0]
    elif colp > col: path[0] = 'L'+path[0]
    path[1].insert(0,node.parent.position)
    node = node.parent
  
  return path


def findPosition(solution_length,db):
  for k,v in db.iteritems():
    if v == solution_length: return k
  return None



start = time.clock()
h = exactHeuristic()
print 'nalaganje hevristike:', time.clock()-start
print '---'
start = time.clock()
aStarSearch(State('012345678',None,22), h, 'start', 'no_noise', 0.20)
print 'A* alg:', time.clock()-start

print solutionsDistribution(h)

p = findPosition(24,h)
path,limit = idaStarSearch(State(p,None,24), h, 'end', 'gauss', 0.50)
print limit
print len(path)
