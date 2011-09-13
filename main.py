import bricksWorld
import logging


# Log everything, and send it to stderr.
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%H:%M:%S', level=logging.DEBUG)

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
    ##parameters for running tests
    mapSize=[15,20,25]
    mapBricksAmount=[20,40,60,80]
    heuristic_type=['optimistic_gauss', 'gauss']
    noise_amount=[10,20,40,60]
    iterationNo = 10
    
    test_brickWorld(mapSize, mapBricksAmount, heuristic_type, noise_amount, iterationNo)

##
##preform search on brickWorld with given parameters   
##    
def test_brickWorld(mapSize, mapBricksAmount, heuristic_type, noise_amount, iterationNo):
    testMap = None
    for size in mapSize:
        for brickPercentage in mapBricksAmount:
            for heuristic in heuristic_type:
                for noise in noise_amount:
                    result_a_i,result_a_s,result_a_c,result_a_e = 0,0,0,0
                    result_ida_i,result_ida_s,result_ida_c,result_ida_e = 0,0,0,0
                    for iteration in range(iterationNo):
    
                        #size in one demension and density in %
                        testMap = bricksWorld.brickWorld(size,brickPercentage)

                        start = testMap.changeHeuristic(heuristic,'start',noise)
                        center = testMap.changeHeuristic(heuristic,'center',noise)
                        end = testMap.changeHeuristic(heuristic,'end',noise)

                        logging.debug("Preforming A*")
                        testMap.aStarSearch(testMap.priceWorld)
                        result_a_i = result_a_i + testMap.aStarCheckedNodes
                        testMap.aStarSearch(start)
                        result_a_s = result_a_s + testMap.aStarCheckedNodes
                        testMap.aStarSearch(center)
                        result_a_c = result_a_c + testMap.aStarCheckedNodes
                        testMap.aStarSearch(end)
                        result_a_e = result_a_e + testMap.aStarCheckedNodes
                        
                        logging.debug("Preforming IDA*")
                        testMap.idaStarSearch(testMap.priceWorld)
                        result_ida_i = result_ida_i + testMap.getIdaStarNodes()
                        testMap.idaStarSearch(start)
                        result_ida_s = result_ida_s + testMap.getIdaStarNodes()
                        testMap.idaStarSearch(center)
                        result_ida_c = result_ida_c + testMap.getIdaStarNodes()
                        testMap.idaStarSearch(end)
                        result_ida_e = result_ida_e + testMap.getIdaStarNodes()
                    
                    f = file("results/brick_size%s_%sproc_%s_%sproc.txt"%(size,brickPercentage,heuristic,noise),"w")
                    f.write("ideal A*:"+str(float(result_a_i)/iterationNo)+"\t\tideal IDA*:"+str(float(result_ida_i)/iterationNo)+"\n")
                    f.write("start A*:"+str(float(result_a_s)/iterationNo)+"\t\tstart IDA*:"+str(float(result_ida_s)/iterationNo)+"\n")
                    f.write("center A*:"+str(float(result_a_c)/iterationNo)+"\t\tcenter IDA*:"+str(float(result_ida_c)/iterationNo)+"\n")
                    f.write("end A*:"+str(float(result_a_e)/iterationNo)+"\t\tend IDA*:"+str(float(result_ida_e)/iterationNo)+"\n")
                    f.close()
                    logging.info("Write completed: brick_size%s_%sproc_%s_%sproc.txt"%(size,brickPercentage,heuristic,noise))

if __name__ == "__main__":test()