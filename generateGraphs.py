import sys
sys.path.insert(0, "./src")
from networkgen import *

if __name__ == "__main__":
    dotPath = "/Users/smcho/temp/simulation/data/%s.dot"
    filePath = "/Users/smcho/temp/simulation/data/%s.txt"

    # narrow one check
    iteration = 3
    for i in [4, 5, 6]: #[10,20]: # ,30,40,50,60,70,80,90,100]:
        numberOfNode = i
        width = 3
        depth = i

        for j in range(iteration):
            tree_name = "tree" + str(i) + "_" + str(width) + "_" + str(depth) + "_" + str(j)
            mesh_name = "mesh" + str(i) + "_" + str(width) + "_" + str(depth) + "_" + str(j)
            c = NetworkGen()
            text = filePath % tree_name
            tree = c.generate_tree_file(text, i, width=width, depth=depth)  # generate 10 nodes tree network
            dot = dotPath % tree_name
            c.dotGen(dot, tree)

            text = filePath % (mesh_name)
            mesh = c.generate_mesh_file(text, tree, 0.4)
            dot = dotPath % (mesh_name)
            c.dotGen(dot, mesh)