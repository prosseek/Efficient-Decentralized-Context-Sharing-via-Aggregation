import random
import sys

class TreeGen:
    def __init__(self): 
        pass
        
    def get_depth(self, tree):
        last_element = tree[len(tree)-1]
        #print last_element
        parent = last_element[1]
        depth = 1

        while parent is not None:
            index = tree.index(filter(lambda x: x[0] == parent, tree)[0])
            #print index
            parent = tree[index][1]
            depth += 1
        return depth
        
    def _generate(self, node_size, max_width, max_depth):
        self.node_size = node_size
        self.max_width = max_width
        self.max_depth = max_depth
        
        # depth is in (1 .. max_depth - 1)
        # When users give max_depth 3, users expect the range from 1 to 3 (not 0 to 2)
        # Instead of depth = random.randrange(1, self.max_depth+1)
        depth = random.randrange(self.max_depth) + 1
        tree = []
        index = 0
        tree.append((0, None))
        count = 1  # There is 1 node
        current_depth = 1
        parent = 0
        
        while (count < node_size and current_depth <= depth):
            width = random.randrange(self.max_width)
            
            if width > 0:
                if count + width > node_size:
                    width = node_size - count
                
                for j in range(width):  
                    tree.append((count, parent))
                    count += 1
                
            index += 1
            current_depth = self.get_depth(tree)
                        
            if index < len(tree):
                parent = tree[index][0]
            else:
                raise Exception("not enough node generated")
                
        return tree, depth
        
    def generate(self, node_size, max_width, max_depth, max_attempt = 100):
        assert max_depth != 1
        assert max_width != 1
        max_node_size = (max_width**max_depth - 1)/(max_width - 1)
        if max_node_size < node_size:
            print >>sys.stderr, "Increase the width or depth"
            sys.exit(0)
        
        #print max_width
        tree = []
        count = 0
        while count < max_attempt:
            try:
                tree, depth = self._generate(node_size, max_width, max_depth)
                generated_tree_size = len(tree)
                if generated_tree_size == node_size:
                    return tree, depth
            except Exception, e:
                count += 1
        return [], 0
            
if __name__ == "__main__":
    import unittest
    sys.path.append("../test")
    from testTreeGen import *

    unittest.main(verbosity=2)