import sys
from context import *
from groupContext import *
from contextUtil import *

class Analyzer(object):
    def __init__(self, networkObject):
        self.network = networkObject
        self.communications = {}
        self.dbs = {}
    
    def getNodeSize(self):
        return len(self.getNodes())
        
    def getNodes(self):
        return self.network.hostDict.keys()
        
    def add(self, count, fromNode, toNode, content):
        result = [fromNode, toNode, content]
        #print result
        if count in self.communications:
            self.communications[count].append(result)
        else:
            self.communications[count] = [result]
        #print self.communications
        
    def addDb(self, count, node, db):
        if count not in self.dbs:
            self.dbs[count] = {}
            
        self.dbs[count][node] = db
        
    def getDb(self, count, node):
        return self.dbs[count][node]
        
    def getCommuncationCount(self):
        count = 0
        for n, coms in self.communications.items():
            #print n
            #print coms
            count += len(coms)
            
        return count
        
    def getSize(self):
        totalSum = 0
        result = ""
        for n, contents in self.communications.items():
            total = 0
            groupCount = 0
            singleCount = 0
            for c in contents:
                #print c # c == [7, 6, [<context.Context object at 0x10b252750>]]
                        #      [1, 2, [<groupContext.GroupContext object at 0x10b252910>]]
                total += len(c[2])
                for i in c[2]:
                    if type(i) is Context:
                        singleCount += 1
                    elif type(i) is GroupContext:
                        groupCount += 1
            result = result + ("%d:%d(%d) -> (g(%d):c(%d))\n" % (n, total, totalSum + total, groupCount, singleCount))
            totalSum += total
        return result, totalSum
            #print contents
    
    def getProgress(self, node):
        result = ""
        for count, dictionary in self.dbs.items():
            result += str(dictionary[node])
        return result
            
    def getAccuracy(self):
        """
        Accuracy is defined in terms of single + prime, which needs no estimation
        """
        node = self.getNodes()
        #nodeSize = self.getNodeSize()
        result = {}
        resultSingle = {}
        resultTotal = {}
        resultCohorts = {}

        # iterate over each time count
        for time_count, dictionary in self.dbs.items():
            # n is the node number, contents is the results from the node
            accuracyTotalDict = {}
            accuracyDict = {}
            accuracy_single_dict = {}
            accuracy_cohorts_dict = {}

            #print dictionary
            for i in node:
                #if i != 1: continue
                db = dictionary[i]
                sc = len(db.singleContexts)
                
                #print db.singleContexts
                pcCount = 0
                number_of_cohorts = 0
                #accuracy_cohorts[i] = db.primeContexts
                for pc in db.primeContexts:
                    pcCount += len(pc.getElements())
                    number_of_cohorts += 1

                #print db.nonPrimeContexts
                npc = db.nonPrimeContexts
                npcCount = len(maxCover(npc))
                
                accuracyDict[i] = (sc + pcCount)
                accuracyTotalDict[i] = (sc + pcCount + npcCount)
                accuracy_single_dict[i] = sc
                accuracy_cohorts_dict[i] = [number_of_cohorts, pcCount]


            result[time_count] = accuracyDict
            resultSingle[time_count] = accuracy_single_dict
            resultTotal[time_count] = accuracyTotalDict
            resultCohorts[time_count] = accuracy_cohorts_dict

        #print result, resultSingle
        return resultTotal, result, resultSingle, resultCohorts
        
    def getAccuracyHistoryForNode(self, target, node):
        size = self.getNodeSize()

        res = []    
        for count, dictionary in target.items():
            if node < 0:
                result = avg(dictionary.values())
            else:
                result = dictionary[node]
            res.append(result/(size*1.0))
        return res
            
    def get(self):
        self.getSize()
        self.getAccuracy()
        
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testAnalyzer import *

    unittest.main(verbosity=2)