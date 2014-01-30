"""
The simulation data
-------------------

The simulation data is stored in ``~/temp/simulation/data``, and they are generated
with `generateGraphs.py`.

The file format is ::

    [mesh|tree]NODESIZE_MAXWIDTH_MAXDEPTH_COUNT.txt

As long as NODESIZE is the same, they are in the same group of tests.

"""
import glob

import sys
import os.path

sys.path.insert(0, "./src")
from network import *
from tupleProcessor import TupleProcessor
from configuration import *

def getFilePath(inputFile, resultDirectory, ext, name):
    fileName = os.path.split(inputFile)[1]
    fileWithoutExt = fileName.split('.')[0]
    return os.path.join(resultDirectory, fileWithoutExt + "_" + name + "." + ext)

def runOneSimulate(inputFile, singleOnly):
    """
    It executes simulation on the inputFile (graph), and returns the result in
    one class object

    @singleOnly:
        When singleOnly is True, it runs without aggregation
    """

    result = {}
    sampleFile = "./test/testFile/sample.txt"
    Network.s = singleOnly
    #assert os.path.exists(inputFile)

    n = Network(inputFile)

    Network.printStep = range(0,0)
    n.simulate(sampleFile, endCount=100)
    a = n.analyzer

    result["packetCount"] = a.getFinalPacketNumber()
    # 'accuracy': (4.0, 4.0, 0.0, 0.0)
    # 1. 4.0 -> Total number of recognition
    # 2. 4.0 -> Total number of single context recognition
    # 3. 0.0 -> Total number of aggregated context count
    # 4. 0.0 -> Total number of cohorts
    # When you divide 3/4, you'll get the average number of elements in a cohort
    result["accuracy"] = a.getFinalAccuracy()
    result["speed"] = a.getFinalSpeed()

    return result

def get_average(input):
    a = TupleProcessor()
    s = 0.0
    c = TupleProcessor()
    for file in input:
        # get the average of packet number
        r = input[file]
        #print r
        a += r['accuracy']
        s += r['speed']
        c += r['packetCount']
    # get the average of accuracy
    size = len(input)
    return a/size, s/size, c/size

def runMassiveSimulation(pattern, singleOnly=True):
    files = glob.glob(pattern)
    #print len(files)
    result = {}
    for f in files:
        result[f] = runOneSimulate(f, singleOnly)

    if len(files) > 0:
        return get_average(result)
    else:
        print >>sys.stderr, "No files in this pattern %s" % pattern
        return None

if __name__ == "__main__":
    testSampleDirectory = getDataDirectory()
    # mesh
    #inputFile = os.path.join(testSampleDirectory,"mesh20_3_10_0.txt")
    #res = runOneSimulate(inputFile, singleOnly=False)
    #print res

    pattern = os.path.join(testSampleDirectory, "_mesh*.txt")
    a,s,c = runMassiveSimulation(pattern, singleOnly=True)
    print a
    print s
    print c
