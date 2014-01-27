import sys
sys.path.insert(0, "./src")

from networkgen import *
import configuration
import glob

def generateOneGraph(node, depth, width, count, density):
    tree_name = "tree" + str(node) + "_" + str(depth) + "_" + str(width) + "_" + str(count) + ".txt"
    mesh_name = "mesh" + str(node) + "_" + str(depth) + "_" + str(width) + "_" + str(density) + "_" + str(count) + ".txt"
    #print tree_name
    #print mesh_name
    dataDirectory = configuration.getDataDirectory()
    treeFilePath = os.path.join(dataDirectory, tree_name)
    meshFilePath = os.path.join(dataDirectory, mesh_name)
    
    #print treeFilePath
    #print meshFilePath
    
    c = NetworkGen()
    try:
        tree = c.generate_tree_file(treeFilePath, node, width=width, depth=depth)
        print tree
    except TestAggregationExceptions as e:
        pass
    
    # text = filePath % tree_name
    # tree = c.generate_tree_file(text, i, width=width, depth=depth)  # generate 10 nodes tree network
    # dot = dotPath % tree_name
    # c.dotGen(dot, tree)
    # 
    # text = filePath % (mesh_name)
    # mesh = c.generate_mesh_file(text, tree, 0.4)
    # dot = dotPath % (mesh_name)
    # c.dotGen(dot, mesh)


def generateGraphs(totalSize, node, depth, width, type = "tree", density = 0.4):
    """
    It looks into the directory to count the number of files already generated.
    It **tries** to generate totalSize of circuits from them
   
    @totalSize: number of graphs generated 

    @node: total number of nodes
    @depth: maximum depth
    @width: maximum width
    @type: "tree" or "mesh" (default is tree)
    @density: when "mesh" graph, the generated number of edges. If it's 0.4, the generated number
              will be the number of exisiting edges * 0.4
    """
    
    ## Get the number of exisiting graphs
    pattern = type + str(node) + "*.txt"
    directory = os.path.join(configuration.getTestDirectory(), "data")
    globintput = os.path.join(directory, pattern)
    res = glob.glob(globintput)
    newNumber = len(res)
    generatedFileCount = 0
    attemptCount = 0
    
    while generatedFileCount <= totalSize:
        result = generateOneGraph(node, depth, width, newNumber + generatedFileCount, density)
        attemptCount += 1
        if result:
            generatedFileCount += 1
        else:
            print >> sys.stderr, "Couldn't generated with %d/%d/%d" % (node, depth, width)
            raise Exception("Not generated file")

if __name__ == "__main__":
    generateGraphs(totalSize = 10, node = 10, depth = 10, width = 3)
"""    
    # narrow one check
    iteration = 30
    for i in [10]: #[10,20]: # ,30,40,50,60,70,80,90,100]:
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
"""