##create world with random bricks in it
##use printWorld to see it
def createBrickWorld(size):
  world = []
  for i in range(size*size):
    if i<size or i%size == 0 or i%size == size-1 or i/size==size-1:
      world.append(1)
    else:
      world.append(0)
      
  printWorld(world, size)

##prints given world
def printWorld(world, size):
  for i in range(size*size):
    if i%size == size-1:
      print world[i]
    else:
      print world[i],

createBrickWorld(10)
    