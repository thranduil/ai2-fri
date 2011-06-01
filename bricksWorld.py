import random

class brickWorld():
  world = []
  priceWorld=[]
  mapSize = 0
  density = 0
  
  def __init__(self, size,density):
    self.mapSize = size
    self.density = density
    
  ##create world with random bricks in it
  def createBrickWorld(self):
    for i in range(self.mapSize*self.mapSize):
      #adds border
      if i<self.mapSize or i%self.mapSize == 0 or i%self.mapSize == self.mapSize-1 or i/self.mapSize==self.mapSize-1:
        self.world.append(1)
      else:
        self.world.append(0)
      #set all fields in price world to -1
      self.priceWorld.append(-1)
      
    #add finish and starting point
    self.setCell(self.world,1,1,2)
    self.setCell(self.world,self.mapSize-2,self.mapSize-2,3)
    self.setCell(self.priceWorld,1,1,0)
    
    
    #fill the map with walls
    random.seed()
    for i in range(self.density):
      x,y = random.randint(1,self.mapSize-2),random.randint(1,self.mapSize-2)
      if x == 1 and y == 1 or x == self.mapSize-2 and y == self.mapSize-2:
        continue
      self.setCell(self.world,y,x,1)
  
  ##prints world
  def printWorld(self):
    for i in range(self.mapSize*self.mapSize):
      if i%self.mapSize == self.mapSize-1:
        print self.world[i]
      else:
        print self.world[i],
  
  ##prints prices for world
  def printPriceWorld(self):
    for i in range(self.mapSize*self.mapSize):
      if i%self.mapSize == self.mapSize-1:
        print self.priceWorld[i]
      else:
        print self.priceWorld[i],
  
  ##set value in the cell
  def setCell(self,world,row,column,value):
    world[row*self.mapSize+column] = value
  
  ##get value from the cell
  def getCell(self,world,row,column):
    return world[row*self.mapSize+column]
  
##testing on one object
w = brickWorld(10,5)
w.createBrickWorld()
w.printWorld()
w.printPriceWorld()