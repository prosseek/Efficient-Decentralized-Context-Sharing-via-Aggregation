import sys
sys.path.insert(0, "./src")
from networkgen import *

if __name__ == "__main__":
    dotPath = "/Users/smcho/Desktop/data/%s.dot"
    filePath = "/Users/smcho/Desktop/data/%s.txt"

    isTree = False
    name = "tree" if isTree else "mesh"
    for i in [200, 300, 400, 500]:
        numberOfNode = i
        c = NetworkGen(numberOfNode, tree = isTree, maxBranch = numberOfNode/10)
        text = filePath % (name + str(i))
        c.fileGen(text)
        dot = dotPath % (name + str(i))
        c.dotGen(dot)