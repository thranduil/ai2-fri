import random
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
    #self.printPriceWorld(self.priceWorld)
    
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
    
    for i in range(self.density):
      x,y = random.randint(1,self.mapSize-2),random.randint(1,self.mapSize-2)
      if x == 1 and y == 1 or x == self.mapSize-2 and y == self.mapSize-2:
        continue
      self.setCell(self.world,y,x,1)
    self.computePrices(1,1,self.priceWorld)
    return self
  
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

def testingHeuristic(noOfExamples):
  maps = []
  
  i=0
  while i<noOfExamples:
    temp1=brickWorld(20,70).createBrickWorld()
    temp2=brickWorld(20,70).createBrickWorld()
    maps.append(temp1)
    maps.append(temp2)
    i+=2
    #print i
    #temp = brickWorld(20,70)
    #temp.createBrickWorld()
    #if temp.pathExist() == True:
      #temp.printPriceWorld(temp.priceWorld)
      #print ""
      #maps.append(temp)
      #i+=1
    #else:
      #temp.printPriceWorld(temp.priceWorld)
    #del(temp)
    maps[-1].printPriceWorld(maps[-1].priceWorld)
    maps[-2].printPriceWorld(maps[-1].priceWorld)
    print ""
    
  
  realData = []
  startH = []
  centerH = []
  endH = []
  
  for m in maps:
    m.aStarSearch(m.priceWorld)
    print "a"
    m.idaStarSearch(m.priceWorld)
    print "ida"
    realData.append((m.aStarCheckedNodes, m.idaStarNodes))
    
    #start = m.changeHeuristic('optimistic_gauss','start',10)
    #center = m.changeHeuristic('optimistic_gauss','center',10)
    #end = m.changeHeuristic('optimistic_gauss','end',10)
    
    #m.aStarSearch(start)
    #m.idaStarSearch(start)
    #startH.append((m.aStarCheckedNodes, m.idaStarNodes))
    
    #m.aStarSearch(center)
    #m.idaStarSearch(center)
    #centerH.append((m.aStarCheckedNodes, m.idaStarNodes))
    
    #m.aStarSearch(end)
    #m.idaStarSearch(end)
    #endH.append((m.aStarCheckedNodes, m.idaStarNodes))
    
  for a  in realData:
    print a

#random.seed(int(time.time()))  
#testingHeuristic(5)

#for i in range(1):
#  brickWorld(25,70)
#  print ""
#  brickWorld(30,70)
#  print ""
#  brickWorld(20,70)
#  print"\n----\n"
  
for i in range(20):
  a = brickWorld(20,70)
  #a.createBrickWorld()
  
  if a.pathExist()==True:
    a.aStarSearch(a.priceWorld)
    a.idaStarSearch(a.priceWorld)
    print "a*:"+str(a.aStarCheckedNodes)
    print "ida*:"+str(a.idaStarNodes)
    print ""
    
    start = a.changeHeuristic('optimistic_gauss','start',10)
    center = a.changeHeuristic('optimistic_gauss','center',10)
    end = a.changeHeuristic('optimistic_gauss','end',10)
        
    a.aStarSearch(start)
    a.idaStarSearch(start)
    print "start a*:"+str(a.aStarCheckedNodes)
    print "start ida*:"+str(a.idaStarNodes)
    print ""   
    
    a.aStarSearch(center)
    a.idaStarSearch(center)
    print "center a*:"+str(a.aStarCheckedNodes)
    print "center ida*:"+str(a.idaStarNodes)
    print ""
          
    a.aStarSearch(end)
    a.idaStarSearch(end)
    print "end a*:"+str(a.aStarCheckedNodes)
    print "end ida*:"+str(a.idaStarNodes)
    print ""
    
  else:
    print "Path doesnt exist. Try again."


