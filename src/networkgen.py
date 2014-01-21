import random
import os
import sys

dotTemplate = """
graph graphname {
    %s
}
"""

class NetworkGen(object):
    def __init__(self, nodes, tree = False, maxBranch = 5):
        #print tree
        self.tree = tree
        self.maxBranch = maxBranch
        self.numberOfNodes = nodes
        self.topology = {}
        
        self.maxConnection = 5
        self.defaultMaxValue = 10
        
    def makeSymmetric(self, dictionary):
        """
        Make the input dictionary as symmetric
        1:[2,3], 2:[0,3] --> 1:[2,3], 2:[0,1,3], 3:[1,2]
        """
        res = {}
            
        for i, elements in dictionary.items():
            if i not in res: res[i] = set()
            for e in elements:
                if e not in res: res[e] = set()
                res[e].add(i)
                res[i].add(e)
                
        for i, elements in res.items():
            #print elements
            res[i] = list(elements)
        
        #print res
        return res
        
    def getNodes(self, numberOfNode, exclude = None):
        if exclude is None: exclude = []
        assert numberOfNode < self.numberOfNodes
        values = set()
        i = len(values)
        while (i < numberOfNode):
            r = random.randint(0, self.numberOfNodes-1)
            if r not in exclude:
                values.add(r)
            i = len(values)
        return list(values)
        
    def getValue(self, maxValue = None):
        if maxValue is None: 
            maxValue = self.defaultMaxValue
        assert maxValue >= 0
        r = random.randint(0, maxValue)
        return r
        
    def getRandomNetwork(self):
        result = {}
        for i in range(self.numberOfNodes):
            # Get the number of neighbor nodes which is bigger than 0
            n = self.getValue(self.maxConnection)
            while n == 0:
                n = self.getValue(self.maxConnection)
            
            # [i] excludes the self as an neighboring nodes
            nodes = self.getNodes(n, [i]) # , self.numberOfNodes)
            result[i] = nodes
            
        result = self.makeSymmetric(result)
        return result
        
    def treeGen(self, index, numberOfCreatedNodes, tree):
        """
        generates a tree network with numberOfNodes
        format -> dictionary
        {1:[2], 2:[3,4,5], ... }
        
        Then run makeSymmetric to get symmetric tree 
        
        input: numberOfCreatedNodes is the number of generated nodes so far
        """
        #print "INDEX", index 
        #print "numberOfCreatedNodes", numberOfCreatedNodes
        #print tree
        #print "\n"
        if numberOfCreatedNodes >= self.numberOfNodes:
            return
        else:
            maxNumberOfNodes = self.numberOfNodes - numberOfCreatedNodes
            maxBranch = min(self.maxBranch, maxNumberOfNodes)
            count = random.randint(1, maxBranch)
            #print "count", count
            origNumber = numberOfCreatedNodes
            numberOfCreatedNodes += count 
            for i in range(count):
                newIndex = origNumber + i
                #print "NI", newIndex
                tree[index].append(newIndex)
                tree[newIndex] = []
                
                # newIndex is the start of the node number
                self.treeGen(newIndex, numberOfCreatedNodes, tree)
                numberOfCreatedNodes += len(tree)
            
    def fileGen(self, filePath):
        #print self.tree
        if self.tree: # Tree structure
            tree = {0:[]}
            self.treeGen(0, 1, tree)
            self.topology = self.makeSymmetric(tree)
        else:
            if not self.topology:
                self.topology = self.getRandomNetwork()
                
        string = ""
        for key, value in sorted(self.topology.items()):
            string += "%d: " % key
            for i in value:
                string += "%d " % i
            string += "\n"
        
        with open(filePath, "w") as f:
            f.write(string)
            
    def dotGen(self, filePath = None):
        string = ""
        
        #print self.topology
        if not self.topology:
            print "ERROR: no self.topology run fileGen first"
            self.topology = self.getRandomNetwork()
            assert False
            
        cache = []
        for key, value in sorted(self.topology.items()):
            for i in value:
                if sorted((key,i)) not in cache:
                    string += "%d -- %d\n" % (key, i)
                    cache.append(sorted((key,i)))

        result = dotTemplate % string
        #print result
        if filePath:
            #print filePath
            with open(filePath, 'w') as f:
                f.write(result)
        return result
    
if __name__ == "__main__":
    os.chdir("../test")
    import unittest
    sys.path.append("../test")
    from testNetworkgen import *

    unittest.main(verbosity=2)