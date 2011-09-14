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
    mapSize=[20,25]
    mapBricksAmount=[20,40,60,80]
    heuristic_type=['optimistic_gauss', 'gauss']
    noise_amount=[20,40,60]
    iterationNo = 10
    
    test_brickWorld(mapSize, mapBricksAmount, heuristic_type, noise_amount, iterationNo)

##
##preform search on brickWorld with given parameters   
##    
def test_brickWorld(mapSize, mapBricksAmount, heuristic_type, noise_amount, iterationNo):
    testMap = None
    for heuristic in heuristic_type:
        for size in mapSize:
            for brickPercentage in mapBricksAmount:
                for noise in noise_amount:
                    result_a_i,result_a_s,result_a_c,result_a_e = 0,0,0,0
                    result_ida_i,result_ida_s,result_ida_c,result_ida_e = 0,0,0,0
                    result_ida_ie,result_ida_se,result_ida_ce,result_ida_ee = 0,0,0,0
                    
                    f = file("results/brick_size%s_%sproc_%s_%sproc.txt"%(size,brickPercentage,heuristic,noise),"w")
                    
                    for iteration in range(iterationNo):
    
                        #size in one demension and density in %
                        testMap = bricksWorld.brickWorld(size,brickPercentage)

                        start = testMap.changeHeuristic(heuristic,'start',noise)
                        center = testMap.changeHeuristic(heuristic,'center',noise)
                        end = testMap.changeHeuristic(heuristic,'end',noise)
                        
                        testMap.heuristicTestNegative(start)
                        testMap.heuristicTestNegative(center)
                        testMap.heuristicTestNegative(end)
                        
                        logging.debug("Preforming A*")
                        testMap.aStarSearch(testMap.priceWorld)
                        #result used for average
                        result_a_i = result_a_i + testMap.aStarCheckedNodes
                        #result used for writting in file (for specific map)
                        temp_a_i = testMap.aStarCheckedNodes
                        testMap.aStarSearch(start)
                        result_a_s = result_a_s + testMap.aStarCheckedNodes
                        temp_a_s = testMap.aStarCheckedNodes
                        testMap.aStarSearch(center)
                        result_a_c = result_a_c + testMap.aStarCheckedNodes
                        temp_a_c = testMap.aStarCheckedNodes
                        testMap.aStarSearch(end)
                        result_a_e = result_a_e + testMap.aStarCheckedNodes
                        temp_a_e = testMap.aStarCheckedNodes
                        
                        logging.debug("Preforming IDA*")
                        testMap.idaStarSearch(testMap.priceWorld)
                        result_ida_i = result_ida_i + testMap.idaStarNodes
                        result_ida_ie = result_ida_ie + testMap.getIdaStarNodes()
                        temp_ida_i = testMap.idaStarNodes
                        temp_ida_ie = testMap.getIdaStarNodes()
                        testMap.idaStarSearch(start)
                        result_ida_s = result_ida_s + testMap.idaStarNodes
                        result_ida_se = result_ida_se + testMap.getIdaStarNodes()
                        temp_ida_s = testMap.idaStarNodes
                        temp_ida_se = testMap.getIdaStarNodes()
                        testMap.idaStarSearch(center)
                        result_ida_c = result_ida_c + testMap.idaStarNodes
                        result_ida_ce = result_ida_ce + testMap.getIdaStarNodes()
                        temp_ida_c = testMap.idaStarNodes
                        temp_ida_ce = testMap.getIdaStarNodes()
                        testMap.idaStarSearch(end)
                        result_ida_e = result_ida_e + testMap.idaStarNodes
                        result_ida_ee = result_ida_ee + testMap.getIdaStarNodes()
                        temp_ida_e = testMap.idaStarNodes
                        temp_ida_ee = testMap.getIdaStarNodes()
                        
                        f.write("\t\t-------------"+str(iteration+1)+"-------------\n")
                        f.write("ideal A*:"+str(temp_a_i)+"\t\tideal IDA*:"+str(temp_ida_i)+"\t\t(expand)ideal IDA*:"+str(temp_ida_ie)+"\n")
                        f.write("start A*:"+str(temp_a_s)+"\t\tstart IDA*:"+str(temp_ida_s)+"\t\t(expand)start IDA*:"+str(temp_ida_se)+"\n")
                        f.write("center A*:"+str(temp_a_c)+"\t\tcenter IDA*:"+str(temp_ida_c)+"\t\t(expand)center IDA*:"+str(temp_ida_ce)+"\n")
                        f.write("end A*:"+str(temp_a_e)+"\t\tend IDA*:"+str(temp_ida_e)+"\t\t(expand)end IDA*:"+str(temp_ida_ee)+"\n")
                        
                    f.write("\n---------------------------Average result---------------------------\n")
                    f.write("ideal A*:"+str(float(result_a_i)/iterationNo)+"\t\tideal IDA*:"+str(float(result_ida_i)/iterationNo)+"\t\t(expand)ideal IDA*:"+str(float(result_ida_ie)/iterationNo)+"\n")
                    f.write("start A*:"+str(float(result_a_s)/iterationNo)+"\t\tstart IDA*:"+str(float(result_ida_s)/iterationNo)+"\t\t(expand)start IDA*:"+str(float(result_ida_se)/iterationNo)+"\n")
                    f.write("center A*:"+str(float(result_a_c)/iterationNo)+"\t\tcenter IDA*:"+str(float(result_ida_c)/iterationNo)+"\t\t(expand)center IDA*:"+str(float(result_ida_ce)/iterationNo)+"\n")
                    f.write("end A*:"+str(float(result_a_e)/iterationNo)+"\t\tend IDA*:"+str(float(result_ida_e)/iterationNo)+"\t\t(expand)end IDA*:"+str(float(result_ida_ee)/iterationNo)+"\n")
                    f.close()
                    logging.info("Write completed: brick_size%s_%sproc_%s_%sproc.txt"%(size,brickPercentage,heuristic,noise))

if __name__ == "__main__":test()