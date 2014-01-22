import unittest
import sys

sys.path.append("../src")

from networkgen import *
from util import *

class TestNetworkgen(unittest.TestCase):
    def setUp(self):
        numberOfNode = 100
        self.ng = NetworkGen(numberOfNode)
        
    def test_treeGen(self):
        # create tree with 10 nodes with maximum branch of 3
        ng = NetworkGen(10, True, 3)
        
        # initialize
        tree = {0:[]}
        # 10 nodes with maximum width 4 and depth 3
        tree = ng.generate_tree_network(10, 4, 3)
        #print "\nRESULT"
        #print tree
        self.assertTrue(len(tree) == 10)
        s = sorted(tree.values(), key=len, reverse=True)[0]
        #print len(s)
        self.assertTrue(len(s) <= 3) 
        
    def test_makeSymmetric(self):
        input = {0:[1,2,3]}
        expcted = {0:[1,2,3], 1:[0], 2:[0], 3:[0]}
        res = self.ng.makeSymmetric(input)
        self.assertTrue(sameDictionary(res, expcted))
        
        input = {0:[1,2,3], 1:[2,3]}
        expcted = {0:[1,2,3], 1:[0,2,3], 2:[0,1], 3:[0,1]}
        res = self.ng.makeSymmetric(input)
        self.assertTrue(sameDictionary(res, expcted))
        
    def test_getRandomNetwork(self):
        #print self.ng.getRandomNetwork()
        pass
        
    def test_getValue(self):
        # default maxValue is 10
        for i in range(100):
            n = self.ng.getValue(200)
            res = self.ng.getValue(n)
            self.assertTrue(res <= n)
            #print res
    def test_getNodes(self):
        for i in range(100):
            n = self.ng.getValue(30)
            res = self.ng.getNodes(n)
            self.assertTrue(len(res) == n)
        
    def test_dotGen(self):
        filePath = "/Users/smcho/Desktop/abc.dot"
        fileTxtPath = "/Users/smcho/Desktop/abc.txt"
        numberOfNode = 100
        c = NetworkGen(numberOfNode)
        #c.dotGen(filePath)
        c.fileGen(fileTxtPath)

if __name__ == "__main__":
    unittest.main(verbosity=2)