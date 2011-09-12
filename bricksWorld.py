import random, hashlib
from Cell import cell
import time

Infinity = 1e10000

class brickWorld():
  world = None
  priceWorld = None
  mapSize = 0
  density = 0
  
  aStarCheckedNodes = 0
  aStarOpenNodes = 0
  
  idaStarNodes = 0
  
  def __init__(self, size,density):
    self.world = []
    self.priceWorld = []
    self.mapSize = size
    self.density = density
    self.createBrickWorld()
    while not self.pathExist():
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
    self.setCell(self.world,4,4,2)
    self.setCell(self.world,self.mapSize-6,self.mapSize-6,3)
    self.setCell(self.priceWorld,4,4,0)
    
    #fill the map with random walls
    for i in range(self.density):
      x,y = random.randint(1,self.mapSize-2),random.randint(1,self.mapSize-2)
      #skip the finish and starting point
      if x == 4 and y == 4 or x == self.mapSize-6 and y == self.mapSize-6:
        continue
      self.setCell(self.world,y,x,1)
    self.computePrices(4,4,self.priceWorld)
  
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
    if self.getCell(self.priceWorld,self.mapSize-2,self.mapSize-2) == '#':
      return False
    else:
      return True
  
  ##set value in the cell
  def setCell(self,world,row,column,value):
    world[row*self.mapSize+column] = value
  
  ##get value from the cell
  def getCell(self,world,row,column):
    return world[row*self.mapSize+column]
  
  ##preform A* search on given map from start to finish point
  def aStarSearch(self,heuristic):
    #in open list we put cells that we are going to look
    #in closed list we put tuple (x,y) coordinates of cells that we already looked
    openList = set()
    closedList = set()
    #current - start cell
    current = cell(self.mapSize-2,self.mapSize-2,None,self.getCell(heuristic,self.mapSize-2,self.mapSize-2))
    openList.add(current)
    
    while openList:
      temp = sorted(openList, key = lambda cell:cell.getG(), reverse=True)
      current = sorted(temp, key = lambda cell:cell.getF())[0]

      if current.getXY() == (1,1):
        #print "A* closed list:"+str(len(closedList))
        #print len(openList)
        self.aStarCheckedNodes = len(closedList)
        self.aStarOpenNodes = len(openList)
        #self.printPath(current)
        return
      openList.remove(current)
      closedList.add(current.getXY())
      neighbors = self.getNeighborCell(current, heuristic)
      for n in neighbors:
        if n.getXY() not in closedList:
          openList.add(n)
    print "Fail to find path"
      

  ##preform IDA* search on given map from start to finish point
  def idaStarSearch(self, heuristic):
    #start cell
    rootNode = cell(self.mapSize-2,self.mapSize-2,None,self.getCell(heuristic,self.mapSize-2,self.mapSize-2))
    costLimit = rootNode.getH()
    self.idaStarNodes = 0
    while True:
      (solution, costLimit) = self.DFS(0, rootNode, costLimit, [rootNode],heuristic)
      if solution != None:
        return (solution, costLimit)
      if costLimit == Infinity:
        return None
 
  ##depth first search for IDA*
  def DFS(self, startCost, node, costLimit, currentPath, heuristic):
    minimumCost = startCost + node.getH()
    if minimumCost > costLimit:
      return (None, minimumCost)
    if node.getXY() == (1,1):
      return (currentPath, costLimit)
 
    nextCostLimit = Infinity
    for succNode in self.getNeighborCell(node, heuristic):
      self.idaStarNodes += 1
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

  ##recursively print path from finish to start point
  def printPath(self,currentCell):
    while currentCell != None:
      print currentCell
      currentCell = currentCell.parent
  
  ##returns changed heuristic, part is place where heuristic are real values
  ##possible noise types: gauss, optimistic_gauss
  ##possible part types: start, center, end
  def changeHeuristic(self, noise, part, percentage):
    newHeuristic = []
    percentage = float(percentage)/100
    for i in self.priceWorld:
      newHeuristic.append(i)
    
    path_length = self.getCell(self.priceWorld,self.mapSize-2,self.mapSize-2)
    
    for i in range(0, self.mapSize-1):
      for j in range(0, self.mapSize-1):
        curr_h = self.getCell(newHeuristic, i, j)
        if curr_h == '#':
          continue
        
        if noise == "gauss":
          if part == "start":
            if curr_h < (float(path_length*2)/3):
              self.setCell(newHeuristic, i, j, int(round(random.gauss(curr_h,float(curr_h)*percentage))))
          
          if part == "center":
            if curr_h > (float(path_length*2)/3) or curr_h < (float(path_length)/3):
              self.setCell(newHeuristic, i, j, int(round(random.gauss(curr_h,float(curr_h)*percentage))))
          
          if part == "end":
            if curr_h > (float(path_length)/3):
              self.setCell(newHeuristic, i, j, int(round(random.gauss(curr_h,float(curr_h)*percentage))))
              
        elif noise == "optimistic_gauss":
          if part == "start":
            if curr_h < (float(path_length*2)/3):
              new_h = int(round(random.gauss(curr_h,float(curr_h)*percentage)))
              while new_h > curr_h:
                new_h = int(round(random.gauss(curr_h,float(curr_h)*percentage)))
              self.setCell(newHeuristic, i, j, new_h)
          
          if part == "center":
            if curr_h > (float(path_length*2)/3) or curr_h < (float(path_length)/3):
              new_h = int(round(random.gauss(curr_h,float(curr_h)*percentage)))
              while new_h > curr_h:
                new_h = int(round(random.gauss(curr_h,float(curr_h)*percentage)))
              self.setCell(newHeuristic, i, j, new_h)
          
          if part == "end":
            if curr_h > (float(path_length)/3):
              new_h = int(round(random.gauss(curr_h,float(curr_h)*percentage)))
              while new_h > curr_h:
                new_h = int(round(random.gauss(curr_h,float(curr_h)*percentage)))
              self.setCell(newHeuristic, i, j, new_h)
    
    return newHeuristic
