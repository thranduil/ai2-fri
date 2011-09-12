import bricksWorld
import logging


# Log everything, and send it to stderr.
logging.basicConfig(level=logging.DEBUG)

def main():
    idealA = []
    idealIDA = []
    startA = []
    startIDA = []
    centerA = []
    centerIDA = []
    endA = []
    endIDA = []
 
    for i in range(250):
      a = bricksWorld.brickWorld(20,140)
      if a.pathExist()==True:
        a.aStarSearch(a.priceWorld)
        a.idaStarSearch(a.priceWorld)
        idealA.append(a.aStarCheckedNodes)
        idealIDA.append(a.idaStarNodes)
        #print "a*:"+str(a.aStarCheckedNodes)
        #print "ida*:"+str(a.idaStarNodes)
        #print ""
    
        start = a.changeHeuristic('optimistic_gauss','start',10)
        center = a.changeHeuristic('optimistic_gauss','center',10)
        end = a.changeHeuristic('optimistic_gauss','end',10)
        
        a.aStarSearch(start)
        a.idaStarSearch(start)
        startA.append(a.aStarCheckedNodes)
        startIDA.append(a.idaStarNodes)
        #print "start a*:"+str(a.aStarCheckedNodes)
        #print "start ida*:"+str(a.idaStarNodes)
        #print ""   
    
        a.aStarSearch(center)
        a.idaStarSearch(center)
        centerA.append(a.aStarCheckedNodes)
        centerIDA.append(a.idaStarNodes)
        #print "center a*:"+str(a.aStarCheckedNodes)
        #print "center ida*:"+str(a.idaStarNodes)
        #print ""
          
        a.aStarSearch(end)
        a.idaStarSearch(end)
        endA.append(a.aStarCheckedNodes)
        endIDA.append(a.idaStarNodes)
        #print "end a*:"+str(a.aStarCheckedNodes)
        #print "end ida*:"+str(a.idaStarNodes)
        #print ""
    
      else:
        print "Path doesnt exist. Try again."
        
    f = file("test.txt","w")
    for i in range(len(idealA)):
      f.write(str(idealA[i])+","+str(idealIDA[i])+","+str(startA[i])+","+str(startIDA[i])+","+str(centerA[i])+","+str(centerIDA[i])+","+str(endA[i])+","+str(endIDA[i])+"\n")
  
    f.close()
    print "idealA"
    print idealA
    print "idealIDa"
    print idealIDA
    print "startA"
    print startA
    print "startIDA"
    print startIDA
    print "centerA"
    print centerA
    print "centerIDA"
    print centerIDA
    print "endA"
    print endA
    print "endIDA"
    print endIDA


def test():
    testMap = None
    testMap = bricksWorld.brickWorld(20,100)
    testMap.printWorld()
    testMap.printPriceWorld(testMap.priceWorld)
    
    logging.debug("making heuristics")
    start = testMap.changeHeuristic('optimistic_gauss','start',10)
    center = testMap.changeHeuristic('optimistic_gauss','center',10)
    end = testMap.changeHeuristic('optimistic_gauss','end',10)
    
    logging.debug("preforming A*")
    testMap.aStarSearch(start)
    logging.debug("preforming ida*")
    testMap.idaStarSearch(start)
    
    print testMap.aStarCheckedNodes
    print testMap.idaStarNodes
    

if __name__ == "__main__":test()