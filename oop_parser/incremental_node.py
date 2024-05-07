#!!! not used in current version 24-05-06, J.S.

class IncrementalNode:
    """
    Placeholder class for Node type that might be required in future.
    
    This node here needs to be used multiple times by StateTransitionManager.
    
    Every time it is used again, association to former instances is required.
        => parent and childen attrs
    """
    
    def __init__(self, tag_name, parent=None):
        self.parent = parent 
        self.tag_name = tag_name 
        self.children = [] 


    def process(self, remaining_lines, parser):
        NotImplementedError()