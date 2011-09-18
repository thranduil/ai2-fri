import random, hashlib
from Cell import cell
import time
import logging
from puzzleSearch import calculateNoise
from copy import copy

# Log everything, and send it to stderr.
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%H:%M:%S', level=logging.DEBUG)

Infinity = 1e10000

class brickWorld():
  world = None
  priceWorld = None
  mapSize = 0
  density = 0
  
  #hard-coded starting point and (offset for) finish point
  startPoint = (4,4)
  finishPoint = (-5,-5)
  
  aStarCheckedNodes = 0
  aStarOpenNodes = 0
  
  idaStarNodes = 0
  
  def __init__(self, size,density):
    self.world = []
    self.priceWorld = []
    self.mapSize = size
    self.finishPoint = (size + self.finishPoint[0], size + self.finishPoint[1])
    self.density = int((size-2)*(size-2)*float(density)/100)
    self.createBrickWorld()
    loopNotVisit = True
    #trying to make world until path from start to end exists
    while not self.pathExist():
      if loopNotVisit == True:
        logging.warning("Path in map does not exist - remaking map.")
        loopNotVisit = False
      self.createBrickWorld()
  
  
  ##create world with random bricks in it
  ##1 is block,0 is empty space, 2 is finish, 3 is start 
  def createBrickWorld(self):
    self.world = []
    self.priceWorld = []
    for i in range(self.mapSize*self.mapSize):
      #adds border
      if i<self.mapSize or i%self.mapSize == 0 or i%self.mapSize == self.mapSize-1 or i/self.mapSize==self.mapSize-1:
        self.world.append(1)
      else:
        self.world.append(0)
      #set all fields in price world to 0
      self.priceWorld.append('#')
      
    #add finish and starting cell
    self.setCell(self.world,self.startPoint[0],self.startPoint[1],2)
    self.setCell(self.world,self.finishPoint[0],self.finishPoint[1],3)
    ##finish point has heuristic 0
    self.setCell(self.priceWorld,self.finishPoint[0],self.finishPoint[1],0)
    
    #fill the map with random walls
    for i in range(self.density):
      x,y = random.randint(1,self.mapSize-2),random.randint(1,self.mapSize-2)
      #skip the finish and starting point
      if x == self.startPoint[0] and y == self.startPoint[1] or x == self.finishPoint[0] and y == self.finishPoint[1]:
        continue
      self.setCell(self.world,y,x,1)
    self.computePrices(self.finishPoint[0],self.finishPoint[1],self.priceWorld)
  
  
  ##recursively compute distance from finish point(x,y) for every cell
  def computePrices(self,x,y,priceWorld):
    if self.getCell(self.world,x,y) == 1:
      return
    if self.getCell(self.world,x-1,y) != 1:
      if self.getCell(priceWorld,x-1,y) == '#' or self.getCell(priceWorld,x-1,y) > self.getCell(priceWorld,x,y)+1:
        self.setCell(priceWorld,x-1,y,self.getCell(priceWorld,x,y)+1)
        self.computePrices(x-1,y,priceWorld)
    
    if self.getCell(self.world,x+1,y) != 1:
      if self.getCell(priceWorld,x+1,y) == '#' or self.getCell(priceWorld,x+1,y) > self.getCell(priceWorld,x,y)+1:
        self.setCell(priceWorld,x+1,y,self.getCell(priceWorld,x,y)+1)
        self.computePrices(x+1,y,priceWorld)
    
    if self.getCell(self.world,x,y-1) != 1:
      if self.getCell(priceWorld,x,y-1) == '#' or self.getCell(priceWorld,x,y-1) > self.getCell(priceWorld,x,y)+1:
        self.setCell(priceWorld,x,y-1,self.getCell(priceWorld,x,y)+1)
        self.computePrices(x,y-1,priceWorld)
    
    if self.getCell(self.world,x,y+1) != 1:
       if self.getCell(priceWorld,x,y+1) == '#' or self.getCell(priceWorld,x,y+1) > self.getCell(priceWorld,x,y)+1:
        self.setCell(priceWorld,x,y+1,self.getCell(priceWorld,x,y)+1)
        self.computePrices(x,y+1,priceWorld)
  
  
  ##prints world
  def printWorld(self):
    for i in range(self.mapSize*self.mapSize):
      if i%self.mapSize == self.mapSize-1:
        print self.world[i]
      else:
        print self.world[i],
  
  
  ##prints prices for world
  def printPriceWorld(self, prices):
    for i in range(self.mapSize*self.mapSize):
      if i%self.mapSize == self.mapSize-1:
        if prices[i] == '#':
          print prices[i]+'#'
        else:
          print '%02d'%int(prices[i])
      else:
        if prices[i] == '#':
          print prices[i]+'#',
        else:
          print '%02d'%int(prices[i]),
  
  
  ##checks if path for current world from start to finish point exists
  def pathExist(self):
    if self.getCell(self.priceWorld,self.startPoint[0],self.startPoint[1]) == '#':
      return False
    else:
      return True
  
 
  ##set value in the cell
  def setCell(self,world,row,column,value):
    world[row*self.mapSize+column] = value
  
  
  ##get value from the cell
  def getCell(self,world,row,column):
    return world[row*self.mapSize+column]
  
  
  ##perform A* search on given map from start to finish point
  def aStarSearch(self,heuristic):
    #in open list we put cells that we are going to look
    #in closed list we put tuple (x,y) coordinates of cells that we already looked
    openList = set()
    closedList = set()
    #closed list with F value, for reopening nodes in closed list
    closedListTemp = set()
    #current - start cell
    current = cell(self.startPoint[0],self.startPoint[1],None,self.getCell(heuristic,self.startPoint[0],self.startPoint[1]))
    openList.add(current)
    
    while openList:
      #temp = sorted(openList, key = lambda cell:cell.getG(), reverse=True)
      current = sorted(openList, key = lambda cell:cell.getF())[0]
      
      if current.getXY() == self.finishPoint:
        self.aStarCheckedNodes = len(closedList)
        self.aStarOpenNodes = len(openList)
        print "Path:",
        self.printAStarPath(current)
        print ""
        return self.getAStarPathLength(current)
        
      openList.remove(current)
      closedList.add(current.getXY())
      closedListTemp.add(current.getXYF())
      neighbors = self.getNeighborCell(current, heuristic)
      for n in neighbors:
        if n.getXY() in closedList:
          #go through closed list with F values and compare F of the same nodes
          for t in closedListTemp:
            if t[0] == n.getX() and t[1] == n.getY():
              #check if we can reopen node
              if n.getF() < t[2]:
                openList.add(n)
                closedList.remove(n.getXY())
                break
        else:
          openList.add(n)
    print "Fail to find path"
    return -1
  
  
  ##perform IDA* search on given map from start to finish point
  def idaStarSearch(self, heuristic):
    #start cell
    rootNode = cell(self.startPoint[0],self.startPoint[1],None,self.getCell(heuristic,self.startPoint[0],self.startPoint[1]))
    costLimit = rootNode.getH()
    self.idaStarNodes = 0
    it = 0
    while True:
      it+=1
      #logging.debug("Iteration:"+str(it))
      (solution, costLimit) = self.DFS(0, rootNode, costLimit, [rootNode],heuristic)
      if solution != None:
        return len(solution)
        #return (solution, costLimit)
      if costLimit == Infinity:
        logging.error("Path with IDA* was not found!")
        return None
  
  
  ##depth first search for IDA*
  def DFS(self, startCost, node, costLimit, currentPath, heuristic):
    self.idaStarNodes = self.idaStarNodes + 1
    minimumCost = startCost + node.getH()
    if minimumCost > costLimit:
      return (None, minimumCost)
    if node.getXY() == self.finishPoint:
      return (currentPath, costLimit)
      
    nextCostLimit = Infinity
    for succNode in self.getNeighborCell(node, heuristic):
      newStartCost = startCost + 1
      (solution, newCostLimit) = self.DFS(newStartCost, succNode, costLimit, currentPath + [succNode],heuristic)
      if solution != None:
        return (solution, newCostLimit)
      nextCostLimit = min(nextCostLimit, newCostLimit)
    return (None,nextCostLimit)
  
  
  ##returns list of empty neighbor cells
  def getNeighborCell(self,current, heuristic):
    cells = []
    if current.getX()-1 >= 0 and self.getCell(self.world,current.getX()-1,current.getY()) != 1:
      cells.append(cell(current.getX()-1, current.getY(), current, self.getCell(heuristic,current.getX()-1,current.getY())))
    if current.getX()+1 <= self.mapSize-1 and self.getCell(self.world,current.getX()+1,current.getY()) != 1:
      cells.append(cell(current.getX()+1, current.getY(), current, self.getCell(heuristic,current.getX()+1,current.getY())))
    if current.getY()-1 >= 0 and self.getCell(self.world,current.getX(),current.getY()-1) != 1:
      cells.append(cell(current.getX(), current.getY()-1, current, self.getCell(heuristic,current.getX(),current.getY()-1)))
    if current.getY()+1 <= self.mapSize-1 and self.getCell(self.world,current.getX(),current.getY()+1) != 1:
      cells.append(cell(current.getX(), current.getY()+1, current, self.getCell(heuristic,current.getX(),current.getY()+1)))
    return cells
  
  
  ##recursively print path from finish to start point for A* algorithm
  def printAStarPath(self,currentCell):
    while currentCell != None:
      print currentCell,
      currentCell = currentCell.parent
  
  
  ##returns lengt of solution (path) for A* algorithm
  def getAStarPathLength(self,currentCell):
    l = 0
    while currentCell != None:
      l+=1
      currentCell = currentCell.parent
    return l
  
  
  ##returns length of ideal path from start to end
  def getIdealPathLength(self):
    return self.getCell(self.priceWorld,self.startPoint[0], self.startPoint[1])
  
  
  ##returns distorted heuristic
  ##possible noise types: gauss, optimistic_gauss, pessimistic_gauss
  ##possible part types: start, center, end  
  def distortHeuristic(self, better_part, noise_type, noise_magnitude, better_noise):
    new_h = copy(self.priceWorld)
    solution_length = self.getCell(self.priceWorld,self.startPoint[0],self.startPoint[1])
    
    for i in range(0, self.mapSize-1):
      for j in range(0, self.mapSize-1):
        curr_h = self.getCell(new_h, i, j)
        
        if curr_h == '#':
          continue
        
        #heuristic in start point is number of steps to finish point and not the other way around
        #so conditions for start, middle and end are little different than in puzzleSearch
        elif better_part == 'start':
          if curr_h < round(2*solution_length/3):
            self.setCell(new_h, i, j, calculateNoise(curr_h, noise_type, noise_magnitude))
          elif better_noise > 0:
            self.setCell(new_h, i, j, calculateNoise(curr_h, noise_type, better_noise))
        
        if better_part == 'end':
          if curr_h >= round(solution_length/3):
            self.setCell(new_h, i, j, calculateNoise(curr_h, noise_type, noise_magnitude))
          elif better_noise > 0:
            self.setCell(new_h, i, j, calculateNoise(curr_h, noise_type, better_noise))
      
        elif better_part == 'middle':
          if curr_h < round(solution_length/3) or curr_h > round(2*solution_length/3):
            self.setCell(new_h, i, j, calculateNoise(curr_h, noise_type, noise_magnitude))
          elif better_noise > 0:
            self.setCell(new_h, i, j, calculateNoise(curr_h, noise_type, better_noise))
      

    
    return new_h
  
  
  ##prints map with heuristic on places where is different from real values    
  def compareHeuristics(self, newHeuristic):
    for i in range(self.mapSize*self.mapSize):
      if i%self.mapSize == self.mapSize-1:
        if self.priceWorld[i] == '#':
          print self.priceWorld[i]+'#'
        else:
          if self.priceWorld[i]-newHeuristic[i] == 0:
            print "  "
          else:
            print '%02d'%i(self.priceWorld[i]-newHeuristic[i])
      else:
        if self.priceWorld[i] == '#':
          print self.priceWorld[i]+'#,',
        else:
          if self.priceWorld[i]-newHeuristic[i] == 0:
            print "  ,",
          else:
            print '%02d,'%(self.priceWorld[i]-newHeuristic[i]),
  
  
  #Helper function that checks if heuristic is only positive 
  def heuristicTestNegative(self,h):
      for i in range(len(h)):
          if h[i]!='#':
              if h[i]<0:
                  logging.error("Field in heuristic is negative!")
                  break
  
