import sys
sys.path.insert(0, "./src")
from networkgen import *

if __name__ == "__main__":
    dotPath = "/Users/smcho/Desktop/data/%s.dot"
    filePath = "/Users/smcho/Desktop/data/%s.txt"

    isTree = False
    treeName = "tree" # if isTree else "mesh"
    meshName = "mesh"
    for i in [20,30,40,50,60,70,80,90,100]:
        numberOfNode = i
        width = 4
        depth = i

        c = NetworkGen()
        text = filePath % (treeName + str(i))
        tree = c.generate_tree_file(text, i, width=width, depth=depth)  # generate 10 nodes tree network
        dot = dotPath % (treeName + str(i))
        c.dotGen(dot, tree)

        text = filePath % (meshName + str(i))
        mesh = c.generate_mesh_file(text, tree, 0.3)
        dot = dotPath % (meshName + str(i))
        c.dotGen(dot, mesh)