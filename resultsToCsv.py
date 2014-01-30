"""
resultsToCsv transforms result file from massSimulate.py to csv format that Excel can load

Input example:

2014-01-30 11:13:22
mesh10_*.txt True
10.0,10.0,0.0,0.0
4.18
155.57,0.0

2014-01-30 11:13:24
mesh20_*.txt True
20.0,20.0,0.0,0.0
5.05
636.77,0.0
"""

import os.path
import re

class Results(object):
    def __init__(self, file):
        self.file = file
        self.blocks = self.parse(file)
        self.db = {}
        for block in self.blocks:
            key = self.getKey(block)
            self.db[key] = self.getValue(block)
            #print key
            #print self.getValue(block)
            
    def getKey(self, block):
        """
        From block, key is extracted the 2nd element of the first item
        
        'mesh10_*.txt True' -> mesh10S
        'mesh50_*.txt False' -> mesh10A
        """
        return block[1].split('_')[0] + ("S" if block[1].split(' ')[1] == "True" else "A")
        
    def getValue(self, block):
        """
        From this information
        
        2014-01-30 11:44:53
        mesh70_*.txt False
        69.4,4.945,64.3,3.4
        6.84
        194.0,621.23
        
        Extract these info
        
        timeStamp <- [0]
        pattern <- [1].[0] => mesh70
        type <- mesh
        totalSize <- [1] => 70
        
        singleOnly <- [1].[1]
        speed <- [3]
        
        accuracyTotal <- [2][0]
        accuracySingle <- [2][1]
        accuracyAggregated <- [2][0] - [2][1]
        accuracyTotalPercentage <- accuracyTotal/totalSize
        accuracySinglePercentage
        accuracyAggregatedPercentage
        
        # When node 10 has (1,2,[3,4],[5,6],[7,8])
        # The Cohorts Member Count means 6 ([3,4,5,6,7,8]
        # The Cohorts Group Count means 3 ([3,4],[5,6] and [7,8])
        accuracyCohortsMemberCount <- [2][3]
        accuracyCohortsGroupCount <- [2][2]
        accuracyAveragePerCohortsGroup <- accuracyCohortsMemberCount/accuracyCohortsGroupCount
        accuracyCohortsMemberCountPercentage
        
        countTotal
        countSingle
        countAggregated
        """
        result = {}
        result["timeStamp"] = block[0]
        result["pattern"] = block[1].split(" ")[0].split("_")[0]
        res = re.search("([^\d]+)([\d]+)", result["pattern"])
        result["type"] = res.group(1)
        result["totalSize"] = int(res.group(2))
        
        result["singleOnly"] = bool(block[1].split(" ")[1] == "True")
        result["speed"] = block[3]
        
        # 69.4,4.945,64.3,3.4
        a = block[2].split(',')
        result["accuracyTotal"] = float(a[0])
        result["accuracySingle"] = float(a[1])
        result["accuracyAggregated"] = result["accuracyTotal"] - result["accuracySingle"]
        result["accuracyTotalPercentage"] =  result["accuracyTotal"]*100.0/result["totalSize"]
        result["accuracySinglePercentage"] = result["accuracySingle"]*100.0/result["totalSize"]
        result["accuracyAggregatedPercentage"] = result["accuracyTotalPercentage"] - result["accuracySinglePercentage"]
        
        result["accuracyCohortsMemberCount"] = float(a[2])
        result["accuracyCohortsMemberCountPercentage"] = result["accuracyCohortsMemberCount"]*100.0/result["totalSize"]
        result["accuracyCohortsGroupCount"] = float(a[3])
        if result["accuracyCohortsGroupCount"] != 0:
            result["accuracyAveragePerCohortsGroup"] = result["accuracyCohortsMemberCount"]/result["accuracyCohortsGroupCount"] 
        else:
            result["accuracyAveragePerCohortsGroup"] = 0
            
        # 194.0,621.23
        a = block[4].split(',')
        result["countSingle"] = float(a[0])
        result["countAggregated"] = float(a[1])
        result["countTotal"] = result["countSingle"] + result["countAggregated"]

        return result
        
    def parse(self, file):
        """
        It parses the input file to generate blocks
        
        [['2014-01-30 11:13:22', 'mesh10_*.txt True', '10.0,10.0,0.0,0.0', '4.18', '155.57,0.0'], 
         ['2014-01-30 11:13:24', 'mesh20_*.txt True', '20.0,20.0,0.0,0.0', '5.05', '636.77,0.0']
         ...
        """
        f = open(file, "r")
        lines = f.readlines()
        
        blocks = []
        resultsSoFar = []
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                blocks.append(resultsSoFar)
                resultsSoFar = []
            else:
                resultsSoFar.append(line)
        # Step 1 collect results based on 
        return blocks
        
    def sizeComparison(self):
        """
        Generates CSV format data compare size between SingleOnly/Aggregated
        """
        print self.db
        result = filter(lambda key: self.db[key]["singleOnly"] == True, self.db)
        result = map(lambda key: self.db[key], result)
        print result
        return "HA"
        
    def generateCsvForSizeComparison(self, toFile):
        toFile = os.path.abspath(toFile)
        result = self.sizeComparison()
        f = open(toFile, "w")
        f.write(result)
        f.close()
        
def resultsToCsv(fromFile, toFile):
    r = Results(fromFile)
    r.generateCsvForSizeComparison(toFile)
    
if __name__ == "__main__":
    fromFile = "/Users/smcho/Desktop/result_2014_01_30.txt"
    toFile = "/Users/smcho/Desktop/a.csv"
    resultsToCsv(fromFile, toFile)