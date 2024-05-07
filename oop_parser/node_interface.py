#!!! not used in current version 24-05-06, J.S.

class NodeInterface:
    """
    Interface class:
        Defines interface for all node base classes regardless of strategy.
    
    Arguments required for __init__:
        parser: <class Parser>
        
        
    """
        
    def process(self, parser, remaining_lines):
        """
        docstring describing method
        """
        
    def invoke_node_finalization(self):
        """
        Invoke method of node object that calls methods of self to do final 
        processing.

        Returns
        -------
        None.

        """