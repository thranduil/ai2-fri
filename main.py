import bricksWorld
import logging

# Log everything, and send it to stderr.
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%H:%M:%S', level=logging.DEBUG)

def test():
    ##parameters for running tests
    mapSize=[20]
    mapBricksAmount=[20]
    heuristic_type=['optimistic_gauss']
    noise_amount=[0.2]
    iterationNo = 100
    
    test_brickWorld(mapSize, mapBricksAmount, heuristic_type, noise_amount, iterationNo)

##
##perform search on brickWorld with given parameters   
##    
def test_brickWorld(mapSize, mapBricksAmount, heuristic_type, noise_amount, iterationNo):
    testMap = None
    better_noise = 0
    
    for heuristic in heuristic_type:
        for size in mapSize:
            for brickPercentage in mapBricksAmount:
                for noise in noise_amount:
                    result_a_i,result_a_s,result_a_c,result_a_e = 0,0,0,0
                    result_ida_i,result_ida_s,result_ida_c,result_ida_e = 0,0,0,0
                    delta_optimal_a_s, delta_optimal_a_c, delta_optimal_a_e = 0,0,0
                    delta_optimal_ida_s, delta_optimal_ida_c, delta_optimal_ida_e = 0,0,0
                    
                    f = file("results_grid/brick_size%s_%sproc_%s_%sproc.txt"%(size,brickPercentage,heuristic,noise),"w")
                    
                    for iteration in range(iterationNo):
                        
                        logging.debug("iteration:"+str(iteration))
                        
                        #size in one dimension and density in %
                        testMap = bricksWorld.brickWorld(size,brickPercentage)
                        
                        idealPathLength = testMap.getIdealPathLength() + 1
                        start = testMap.distortHeuristic('start', heuristic, noise, 0)
                        center = testMap.distortHeuristic('middle', heuristic, noise, 0)
                        end = testMap.distortHeuristic('end', heuristic, noise, 0)
                              
                        logging.debug("Performing A*")
                        testMap.aStarSearch(testMap.priceWorld)
                        #result used for average
                        result_a_i = result_a_i + testMap.aStarCheckedNodes
                        #result used for writing in file (for specific map)
                        temp_a_i = testMap.aStarCheckedNodes
                        
                        pl1 = testMap.aStarSearch(start)
                        result_a_s = result_a_s + testMap.aStarCheckedNodes
                        temp_a_s = testMap.aStarCheckedNodes
                        delta_optimal_a_s = delta_optimal_a_s + (pl1 - idealPathLength)
                        if (pl1 - idealPathLength) > 0:
                          testMap.compareHeuristics(start)
                        
                        pl2 = testMap.aStarSearch(center)
                        result_a_c = result_a_c + testMap.aStarCheckedNodes
                        temp_a_c = testMap.aStarCheckedNodes
                        delta_optimal_a_c = delta_optimal_a_c + (pl2 - idealPathLength)
                        if (pl2 - idealPathLength) > 0:
                          testMap.compareHeuristics(center)
                        
                        pl3 = testMap.aStarSearch(end)
                        result_a_e = result_a_e + testMap.aStarCheckedNodes
                        temp_a_e = testMap.aStarCheckedNodes
                        delta_optimal_a_e = delta_optimal_a_e + (pl3 - idealPathLength)
                        if (pl3 - idealPathLength) > 0:
                          testMap.compareHeuristics(end)
                        
                        logging.debug("Performing IDA*")
                        testMap.idaStarSearch(testMap.priceWorld)
                        result_ida_i = result_ida_i + testMap.idaStarNodes
                        temp_ida_i = testMap.idaStarNodes
                        
                        #logging.debug("Performing IDA* (start)")
                        pl4 = testMap.idaStarSearch(start)
                        result_ida_s = result_ida_s + testMap.idaStarNodes
                        temp_ida_s = testMap.idaStarNodes
                        delta_optimal_ida_s = delta_optimal_ida_s + (pl4 - idealPathLength)
                        
                        #logging.debug("Performing IDA* (center)")
                        pl5 = testMap.idaStarSearch(center)
                        result_ida_c = result_ida_c + testMap.idaStarNodes
                        temp_ida_c = testMap.idaStarNodes
                        delta_optimal_ida_c = delta_optimal_ida_c + (pl5 - idealPathLength)
                        
                        #logging.debug("Performing IDA* (end)")
                        pl6 = testMap.idaStarSearch(end)
                        result_ida_e = result_ida_e + testMap.idaStarNodes
                        temp_ida_e = testMap.idaStarNodes
                        delta_optimal_ida_e = delta_optimal_ida_e + (pl6 - idealPathLength)
                        
                        f.write("\t\t-------------"+str(iteration+1)+"-------------\n")
                        f.write("ideal A*:"+str(temp_a_i)+"\t\tideal IDA*:"+str(temp_ida_i)+"\n")
                        f.write("start A*:"+str(temp_a_s)+"/"+str(pl1 - idealPathLength)+"\t\tstart IDA*:"+str(temp_ida_s)+"/"+str(pl4 - idealPathLength)+"\n")
                        f.write("center A*:"+str(temp_a_c)+"/"+str(pl2 - idealPathLength)+"\t\tcenter IDA*:"+str(temp_ida_c)+"/"+str(pl5 - idealPathLength)+"\n")
                        f.write("end A*:"+str(temp_a_e)+"/"+str(pl3 - idealPathLength)+"\t\tend IDA*:"+str(temp_ida_e)+"/"+str(pl6 - idealPathLength)+"\n")
                        
                    f.write("\n---------------------------Average result---------------------------\n")
                    f.write("ideal A*:"+str(float(result_a_i)/iterationNo)+"\t\tideal IDA*:"+str(float(result_ida_i)/iterationNo)+"\n")
                    f.write("start A*:"+str(float(result_a_s)/iterationNo)+"/"+str(float(delta_optimal_a_s)/iterationNo)+"\t\tstart IDA*:"+str(float(result_ida_s)/iterationNo)+"/"+str(float(delta_optimal_ida_s)/iterationNo)+"\n")
                    f.write("center A*:"+str(float(result_a_c)/iterationNo)+"/"+str(float(delta_optimal_a_c)/iterationNo)+"\t\tcenter IDA*:"+str(float(result_ida_c)/iterationNo)+"/"+str(float(delta_optimal_ida_c)/iterationNo)+"\n")
                    f.write("end A*:"+str(float(result_a_e)/iterationNo)+"/"+str(float(delta_optimal_a_e)/iterationNo)+"\t\tend IDA*:"+str(float(result_ida_e)/iterationNo)+"/"+str(float(delta_optimal_ida_e)/iterationNo)+"\n")
                    f.close()
                    logging.info("Write completed: brick_size%s_%sproc_%s_%sproc.txt"%(size,brickPercentage,heuristic,noise))

if __name__ == "__main__":test()