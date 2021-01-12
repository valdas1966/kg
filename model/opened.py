from f_utils import u_set


class Opened:
    """
    ===========================================================================
     Description: Opened Priority Queue for A*.
    ===========================================================================
     Methods:
    ---------------------------------------------------------------------------
        1. is_empty() -> bool [Return True if the Opened is empty].
            
        2. contains(node) -> bool [Return True if Opened contains the node].
            
        3. get_best(node) -> Node [Return the Best Node from Opened].
        
        4. get(node) -> Node [Return Node if exist, Node otherwise].
        
        5. get_nodes() -> set of Node (Set of Nodes in Opened).
        
        6. remove(node) -> [Remove the Node from the Opened].
        
        7. push(node) -> [Push the Node into Opened].
        
        8. pop() -> Node [Return the Best Node and Remove it from the Opened].
        
        9. load(set) -> [Load set of Nodes].
    ===========================================================================
    """

    def __init__(self):
        """
        =======================================================================
         Description: Constructor. Init the Attributes.
        =======================================================================
        """
        self._opened = set()

    def is_empty(self):
        """
        =======================================================================
         Description: Return True if the Opened is empty.
        =======================================================================
         Return: bool.
        =======================================================================
        """
        return len(self._opened) == 0

    def contains(self,node):
        """
        =======================================================================
         Description: Return True if Opened Set contains the Node
        =======================================================================
         Arguments: node : Node.
        =======================================================================
        """
        return node in self._opened

    def get_best(self):
        """
        =======================================================================
         Description: Return the Best Node in Opened.
        =======================================================================
         Return: Node (Best Node in Opened), None on Opened is Empty.
        =======================================================================
        """
        if self.is_empty():
            return None
        return min(self._opened)

    def get(self, node):
        """
        =======================================================================
         Description: Return the Node if exists (None otherwise).
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. node : Node
        =======================================================================
         Return: Node if exists (None otherwise).
        =======================================================================
        """
        return u_set.get(self._opened, node)

    def get_nodes(self):
        """
        =======================================================================
         Description: Return Set of Nodes in Opened.
        =======================================================================
         Return: Set of Nodes in Opened.
        =======================================================================
        """
        return self._opened

    def remove(self, node):
        """
        =======================================================================
         Description: Remove specified Node from the Opened.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. node : Node.
        =======================================================================
        """
        try:
            self._opened.remove(node)
        except:
            pass

    def push(self, node):        
        """
        =======================================================================
         Description: Push Node into the Opened.
        =======================================================================
         Complexity: O(1).
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. node : Node.
        =======================================================================
        """
        self._opened.add(node)        

    def pop(self):
        """
        =======================================================================
         Description: Pop Node from the Opened.
        =======================================================================
         Return: Node.
        =======================================================================
        """
        best = self.get_best()
        self.remove(best)
        return best
    
    
    def load(self, opened):
        """
        =======================================================================
         Description: Load Opened with Set of Nodes.
        =======================================================================
        """
        self._opened = opened.copy()
    
    
    def __str__(self):
        """
        =======================================================================
         Description: Return String Representation of Opened.
        =======================================================================
         Return: str
        =======================================================================
        """
        if self.is_empty(): return 'Empty Opened'
        
        best = self.get_best()
        temp = 'Opened:\n' + '='*10 + '\n{0}\n'.format(best)
        for node in self._opened:
            if (node != best):
                temp += '{0}\n'.format(node)
        return temp
    
    
"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
    
    import sys
    sys.path.append('D:\\MyPy\\f_utils')
    import u_tester       
    

    def tester_is_empty():
        
        opened = Opened()
        p0 = opened.is_empty()
        
        opened.push(1)
        p1 = not opened.is_empty()
        
        u_tester.run([p0,p1])
        
    
    def tester_contains():
        
        opened = Opened()
        opened.push(1)
        p0 = opened.contains(1)
        p1 = not opened.contains(2)
        
        u_tester.run([p0,p1])
        
    
    def tester_get_best():
        
        opened = Opened()
        opened.push(3)
        opened.push(1)
        opened.push(2)
        p0 = opened.get_best() == 1
        
        u_tester.run([p0])
        
        
    def tester_get():
        
        from c_node import Node
        
        opened = Opened()
        node = Node(1)
        node.g = 1
        opened.push(node)
        opened.push(Node(2))
        node.g = 2
        node_test = opened.get(node)
        p0 = node_test.g == 2
        
        u_tester.run([p0])
        
    
    def tester_get_nodes():

        nodes_true = {1,2,3}
        opened = Opened()   
        for node in nodes_true:
            opened.push(node)
        nodes_test = opened.get_nodes()
        p0 = nodes_test == nodes_true
        
        u_tester.run([p0])
        
        
    def tester_remove():
        
        opened = Opened()
        opened.push(1)
        opened.remove(1)
        p0 = not opened.contains(1)
        
        u_tester.run([p0])
        
        
    def tester_push():
    
        opened = Opened()
        opened.push(1)
        best = opened.get_best()
        p0 = best == 1
        
        u_tester.run([p0])
        
        
    def tester_pop():
        
        opened = Opened()
        opened.push(3)
        opened.push(1)
        opened.push(2)
        best = opened.pop()
        p0 = best == 1
        
        u_tester.run([p0])
        
    
    def tester_load():

        nodes_true = {1,2,3}
        opened = Opened()
        opened.load(nodes_true)
        nodes_test = opened.get_nodes()
        p0 = nodes_test == nodes_true

        u_tester.run([p0])
 
       
    def tester_str():
        
        opened = Opened()
        opened.push(2)
        opened.push(1)
        str_test = str(opened)
        p0 = str_test == 'Opened:\n{0}\n{1}\n{2}\n'.format('='*10,1,2)
        
        u_tester.run([p0])
        
    
    u_tester.print_start(__file__)
    tester_is_empty()
    tester_contains()
    tester_remove()
    tester_get_best()
    tester_get()
    tester_get_nodes()
    tester_push()
    tester_pop()
    tester_load()
    tester_str()
    u_tester.print_finish(__file__)        
    
    
if __name__ == '__main__':
    tester()
 