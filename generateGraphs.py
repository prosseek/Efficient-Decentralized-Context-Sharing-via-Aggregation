import sys
sys.path.insert(0, "./src")

from networkgen import *
import configuration
import glob

def printOK(filePath):
    print "%s file is created" % filePath
    
def printError(filePath):
    print >> sys.err, "%s file is created" % filePath

def generateOneGraph(node, depth, width, count, density):
    tree_name = "tree" + str(node) + "_" + str(depth) + "_" + str(width) + "_" + str(count)
    mesh_name = "mesh" + str(node) + "_" + str(depth) + "_" + str(width) + "_" + str(density) + "_" + str(count)
    #print tree_name
    #print mesh_name
    dataDirectory = configuration.getDataDirectory()
    treeFilePath = os.path.join(dataDirectory, tree_name + ".txt")
    meshFilePath = os.path.join(dataDirectory, mesh_name + ".txt")
    treeDotFilePath = os.path.join(dataDirectory, tree_name + ".dot")
    meshDotFilePath = os.path.join(dataDirectory, mesh_name + ".dot")
    
    #print treeFilePath
    #print meshFilePath
    
    c = NetworkGen()
    try:
        tree = c.generate_tree_file(treeFilePath, node, depth=depth, width=width)
        #printOK(treeFilePath)
        c.dotGen(treeDotFilePath, tree)
        #printOK(treeDotFilePath)
        #print tree
    except NotGenerateGraphException as e:
        printError(treeFilePath)
        return False
        
    # Now, mesh file is generated
    try:
        mesh = c.generate_mesh_file(meshFilePath, tree, density)
        #printOK(meshFilePath)
        c.dotGen(meshDotFilePath, mesh)
        #printOK(meshDotFilePath)
    except NotGenerateGraphException as e:
        printError(meshFilePath)
        return False
        
    return True

def generateGraphs(totalSize, node, depth, width, density = 0.4):
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
    pattern = "tree" + str(node) + "_*.txt"
    directory = os.path.join(configuration.getTestDirectory(), "data")
    globintput = os.path.join(directory, pattern)
    res = glob.glob(globintput)
    newNumber = len(res)
    generatedFileCount = 0
    attemptCount = 0
    
    while generatedFileCount < totalSize:
        result = generateOneGraph(node, depth, width, newNumber + generatedFileCount, density)
        attemptCount += 1
        if result:
            generatedFileCount += 1
        else:
            print >> sys.stderr, "Couldn't generated with %d/%d/%d" % (node, depth, width)
            raise Exception("Not generated file")
    
def minimumCheckedWidth(min, value):
    return value if value > min else min
                
def generateVaryingGraphs(totalSize, node, density = 0.4):
    # very long graph
    generateGraphs(totalSize = totalSize/5, node = node, depth = node, width = 2, density = density)
    generateGraphs(totalSize = totalSize/5, node = node, depth = node, width = minimumCheckedWidth(3, int(0.25*node)), density = density)
    generateGraphs(totalSize = totalSize/5, node = node, depth = node, width = minimumCheckedWidth(3, int(node*0.5)), density = density)
    generateGraphs(totalSize = totalSize/5, node = node, depth = node, width = minimumCheckedWidth(3, int(node*0.75)), density = density)
    # very wide graph
    generateGraphs(totalSize = totalSize/5, node = node, depth = node/2, width = totalSize, density = density)

if __name__ == "__main__":
    generateVaryingGraphs(totalSize = 100, node = 100, density = 0.4)
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