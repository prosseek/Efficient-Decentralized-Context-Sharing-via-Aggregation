import unittest
import sys
import os.path

#print os.path.abspath(".")
sys.path.append(os.path.abspath("../src"))
#print sys.path
from network import *
from networkAlgorithm import *

class TestNetwork(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_getDepth(self):
        a = Network("testFile/network1.txt")
        self.assertTrue(a.getDepth() == 6)
        
    def test_getMaxNeighbors(self):
        a = Network("testFile/network1.txt")
        self.assertEqual(a.getMinMaxNeighbors()[1], 3)
        
    def test_getItem(self):
        a = Network("testFile/network1.txt")
        # 6: 3 7
        res = a[6].getNeighbors()
        self.assertTrue(same(res, [3,7]))
        
    def test_getNumberOfNodes(self):
        a = Network("testFile/network1.txt")
        result = a.getNumberOfNodes()
        self.assertTrue(result == 8)
        
    def test_getNodes(self):
        a = Network("testFile/network1.txt")
        result = a.getNodes()
        self.assertTrue(same(result, [1,2,3,4,5,6,7,8]))
        
    def test_getEdges(self):
        a = Network("testFile/network1.txt")
        result = a.getEdges()
        #print result
        self.assertTrue(same(list(result), [(1, 2), (6, 7), (4, 5), (7, 8), (2, 3), (3, 6), (3, 4)]))
        
    def test_getNeighbors(self):
        a = Network("testFile/network1.txt")
        result = a.getNeighbors(2)
        self.assertTrue(same(result, [1,3]))
        
    ########################################
    # SIMULATION TEST
    ########################################
    def test_simulate(self):
        Network.printStep = range(0,0) # ,5)
        #a = Network("testFile/network_simple.txt")
        a = Network("testFile/network1.txt")
        a.simulate("testFile/sample.txt", 13)
        # TODO check the simulation results through analyzer
        analyzer = a.analyzer
        #print analyzer.getCommuncationCount()
        
    def test_buildHost(self):
        # import os
        # print sys.path
        #print os.path.abspath(".")
        a = Network("testFile/network1.txt")
        #a.buildHost()
        keys = a.hostDict.keys()
        self.assertTrue(set(keys), set([1,2,3,4,5,6,7,8]))
        
    def test_networkFileParsingError(self):
        # n.a is not available so Exception is expected to be raised
        self.assertRaises(Exception, Network, "testFile/n.a")
        
    def test_networkFileParsing(self):
        a = Network("testFile/network1.txt")
        expected = {1: [2], 3: [2, 4, 6], 2: [1, 3], 5: [4], 4: [3, 5], 7: [6, 8], 6: [3, 7], 8: [7]}
        res = a.networkFileParsing()
        self.assertEqual(expected, res)
        
    def test_dotGen(self):
        a = Network("testFile/network1.txt")
        #a = Network("testFile/network_simple.txt")
        res = a.dotGen() # "/Users/smcho/Desktop/simple.dot")
        #print res
        expected = """
graph graphname {
    1 -- 2
2 -- 3
3 -- 4
3 -- 6
4 -- 5
6 -- 7
7 -- 8

}
"""
        self.assertEqual(res, expected)
        
if __name__ == "__main__":
    import os
    unittest.main(verbosity=2)