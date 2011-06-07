import random
from Cell import cell

Infinity = 1e10000

class brickWorld():
  world = []
  priceWorld=[]
  mapSize = 0
  density = 0
  
  aStarCheckedNodes = 0
  aStarOpenNodes = 0
  
  idaStarNodes = 0
  
  def __init__(self, size,density):
    self.mapSize = size
    self.density = density
    
  ##create world with random bricks in it
  ##1 is block,0 is empty space, 2 is finish, 3 is start 
  def createBrickWorld(self):
    for i in range(self.mapSize*self.mapSize):
      #adds border
      if i<self.mapSize or i%self.mapSize == 0 or i%self.mapSize == self.mapSize-1 or i/self.mapSize==self.mapSize-1:
        self.world.append(1)
      else:
        self.world.append(0)
      #set all fields in price world to 0
      self.priceWorld.append('#')
      
    #add finish and starting cell
    self.setCell(self.world,1,1,2)
    self.setCell(self.world,self.mapSize-2,self.mapSize-2,3)
    self.setCell(self.priceWorld,1,1,0)
    
    #fill the map with random walls
    random.seed()
    for i in range(self.density):
      x,y = random.randint(1,self.mapSize-2),random.randint(1,self.mapSize-2)
      if x == 1 and y == 1 or x == self.mapSize-2 and y == self.mapSize-2:
        continue
      self.setCell(self.world,y,x,1)
    self.computePrices(1,1,self.priceWorld)
  
  ##recursively compute distance from finish for every cell
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
        print "Path found"
        print "A* closed list:"+str(len(closedList))
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

  ##preform RBFS search on given map from start to finish point
  def rbfsSearch(self):
    print "test"


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
  def changeHeuristic(self, part, percentage):
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
        
        if part == "start":
          if curr_h < (float(path_length*2)/3):
            self.setCell(newHeuristic, i, j, int(round(random.gauss(curr_h,float(curr_h)*percentage))))
        
        if part == "center":
          if curr_h > (float(path_length*2)/3) or curr_h < (float(path_length)/3):
            self.setCell(newHeuristic, i, j, int(round(random.gauss(curr_h,float(curr_h)*percentage))))
        
        if part == "end":
          if curr_h > (float(path_length)/3):
            self.setCell(newHeuristic, i, j, int(round(random.gauss(curr_h,float(curr_h)*percentage))))
    
    return newHeuristic
      
    
##testing on one object
w = brickWorld(20,70)
w.createBrickWorld()
w.printWorld()

print w.pathExist()

w.printPriceWorld(w.priceWorld)
#w.printPriceWorld(a)

w.aStarSearch(w.priceWorld)
w.idaStarSearch(w.priceWorld)
print "IDA* nodes:" +str(w.idaStarNodes)

a = w.changeHeuristic('center',10)

w.aStarSearch(a)
w.idaStarSearch(a)
print "IDA* nodes:" +str(w.idaStarNodes)

