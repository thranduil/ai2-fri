from tile import Position
from puzzleState import State
from copy import copy
import random
import time


##perform A* search on given 8-puzzle problem; implemented noise distortion
def aStarSearch(start_state, heuristic):
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
        count = len(closedList)+1
        path = solutionPath(current)[1]
        return path, count
      openList.remove(current)
      closedList.add(current)
      neighbors = getNeighborStates(current,heuristic)
      for n in neighbors:
        if n not in closedList:
          openList.add(n)
    print "Fail to find path"



##preform IDA* search on given 8-puzzle problem
def idaStarSearch(start_state, heuristic):
  Infinity = float("inf")
  rootNode = start_state
  costLimit = rootNode.getH()
  c=0
  while True:
    (solution, costLimit,c) = DFS(0, rootNode, costLimit, [rootNode], heuristic,c)
    if solution != None:
      return (solution, costLimit, c)
    if costLimit == Infinity:
      print 'IDA* fail!!'
      return None

##depth first search for IDA*
def DFS(startCost, node, costLimit, currentPath, heuristic,c):
  Infinity = float("inf")
  c+=1
  minimumCost = startCost + node.getH()
  if minimumCost > costLimit:
    return (None, minimumCost,c)
  if node.position == '123456780':
    return (currentPath, costLimit,c)
    
  
  nextCostLimit = Infinity
  neighbors = getNeighborStates(node, heuristic)
  for succNode in neighbors:
    newStartCost = startCost + 1
    (solution, newCostLimit,c) = DFS(newStartCost, succNode, costLimit, currentPath+[succNode], heuristic, c)
    if solution != None:
      return (solution, newCostLimit,c)
    nextCostLimit = min(nextCostLimit, newCostLimit)
  return (None,nextCostLimit,c)


def getNeighborStates(start_position, heuristic):
  neighbors=[]
  nexts = start_position.getNeighborPositions()
  for next in nexts:
    neighbors.append(State(next,start_position,heuristic[next]))
  return neighbors


def distortHeuristic(h, solution_length, better_part, noise_type, noise_magnitude, better_noise):
  new_h = copy(h)
  
  for k,v in new_h.iteritems():
    if better_part == 'start':
      if v > round(solution_length/3):
        new_h[k] = calculateNoise(v, noise_type, noise_magnitude)
      elif better_noise > 0:
        new_h[k] = calculateNoise(v, noise_type, better_noise)
        
    elif better_part == 'middle':
      if v < round(solution_length/3) or v > round(2*solution_length/3):
        new_h[k] = calculateNoise(v, noise_type, noise_magnitude)
      elif better_noise > 0:
        new_h[k] = calculateNoise(v, noise_type, better_noise)
        
    elif better_part == 'end':
      if v < round(2*solution_length/3):
        new_h[k] = calculateNoise(v, noise_type, noise_magnitude)
      elif better_noise > 0:
        new_h[k] = calculateNoise(v, noise_type, better_noise)
      
  return new_h


def calculateNoise(h, noise_type, noise_magnitude):
  x = h
  
  if noise_type == 'gauss':
    x = int(round(random.gauss(h,float(h)*noise_magnitude)))
    if x<0 : x=0
    
  elif noise_type == 'optimistic_gauss':
    x = int(round(random.gauss(h,float(h)*noise_magnitude)))
    if x > h:
      x = h-(x-h)
    if x<0 : x=0
      
  elif noise_type == 'pessimistic_gauss':
    x = int(round(random.gauss(h,float(h)*noise_magnitude)))
    if x < h:
      x = h+(h-x)
  
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


def findPositions(solution_length,db):
  results = []
  for k,v in db.iteritems():
    if v == solution_length: results.append(k)
  return results


def testing(sol_lens, noise_types, noise_mags, repeats):
  #sol_lens = list of solution lengths
  #noise_types = list of noise types
  #noise_mags = list of 2 el lists with noise magnitudes; 2nd el for noise of better part
  #repeats = number of iterations for each test
  
  eH = exactHeuristic()
  test_counter = 0
  for sl in sol_lens:
    positions = findPositions(sl,eH)
    random.shuffle(positions)
    # calculate ideal
    for nt in noise_types:
      for nm in noise_mags:
        test_counter+=1
        print 'testing...',test_counter
        f = file("results_puzzle/sol_len%i_%s_noise%i_%iproc.txt"%(sl,nt,int(nm[0]*100),int(nm[1])*100),"w")
        for part in ['start', 'middle', 'end']:
          a_nodes = []
          a_diff = []
          ida_nodes = []
          ida_diff = []
          f.write('\n------'+part+':------\n')
          for r in range(repeats):
            distorted = distortHeuristic(eH, sl, part, nt, nm[0], nm[1])
            #print 'A* test'
            path,count = aStarSearch(State(positions[r],None,sl), distorted)
            a_nodes.append(count)
            a_diff.append(len(path)-sl)
            #print 'IDA* test'
            path,limit,count = idaStarSearch(State(positions[r],None,sl), distorted)
            ida_nodes.append(count)
            ida_diff.append(len(path)-sl)
            
          f.write('A*\n explored_nodes: ')
          for n in a_nodes:
            f.write(str(n)+', ')
          f.write('\n suboptimal_solution: ')
          for n in a_diff:
            f.write(str(n)+', ')
          f.write('IDA*\n explored_nodes: ')
          for n in ida_nodes:
            f.write(str(n)+', ')
          f.write('\n suboptimal_solution: ')
          for n in ida_diff:
            f.write(str(n)+', ')
          f.write('\n')
        f.close()



#test 3 sizes (15,20,25) - solution length
#test 3 types of noises: optimistic, pessimistic and normal gauss
# --- with pessimistic and normal gauss calculate and compare also difference to optimal solution
#test 3 noises: 10%,20%,30% with 1 part ideal
#test 3 noises: 20%,30%,40% with 1 part 10% noise
#100 iterations for each test
solution_lengths = [15,20,25]
noise_types = ['optimistic_gauss','pessimistic_gauss','gauss']
noise_magnitudes = [[0.1,0],[0.2,0],[0.3,0],[0.2,0.1],[0.3,0.1],[0.4,0.1]]
iterations = 1
testing(solution_lengths, noise_types, noise_magnitudes, iterations)

#start = time.clock()
#h = exactHeuristic()
#print 'nalaganje hevristike:', time.clock()-start

#start = time.clock()
#aStarSearch(State('012345678',None,22), h)
#print 'A* alg:', time.clock()-start

#print solutionsDistribution(h)

#start = time.clock()
#distorted = distortHeuristic(h, 24, 'middle', 'gauss', 0.2, 0.0)
#print 'distortion time:', time.clock()-start

#p = findPositions(24,h)
#path,limit = idaStarSearch(State(p[0],None,24), distorted)
#print limit
#print len(path)
