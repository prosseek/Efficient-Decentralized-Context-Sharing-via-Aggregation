import sys
sys.path.insert(0, "./src")
from networkgen import *

if __name__ == "__main__":
    dotPath = "/Users/smcho/Desktop/data/%s.dot"
    filePath = "/Users/smcho/Desktop/data/%s.txt"

    isTree = False
    name = "tree" if isTree else "mesh"
    for i in [20,30,40,50,60,70,80,90,100]:
        numberOfNode = i
        c = NetworkGen()
        text = filePath % (name + str(i))
        width = 4
        depth = i
        tree = c.generate_tree_file(text, i, width=width, depth=depth) # generate 10 nodes tree network

        dot = dotPath % (name + str(i))
        c.dotGen(dot, tree)