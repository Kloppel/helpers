import logging
debug_mode = False

class StateTransitionManager:
    """
            ...::: State Manager class of OOD 'State Pattern' :::...
    
    Is called by a parser object and sets the required parser state and active
    node by detection of state-specific specifiers in the input line, therefore
    managing creation of states.
    
    Returns the remaining lines.
    
    
    State AND Strategy agnostic Manager class!:
        - initializes file-specific state classes (node classes) from a config
        
        As long as the underlying objects fulfill a few interface requirements,
        a diverse set of file types and corresponding state classes can be used
        with this STM.
 
    """
        
    def process(self, parser, remaining_lines): 
        """
        If start specifier is detected:
            do not prune this line
                => some files might have data in same line as start specifier
                => this strategy-specific handling is done in node classes
                
        NO stripping of remaining_lines:
            - whitespace and other characters eventually required for formatting
              within node classes
        
        """
        # set node classes for strategy
        node_classes = parser.config.get_node_classes()
        
        # access file end specifier for strategy/filetype
        file_end_specifier = parser.config.get_file_end_specifier()
        
    
        
        # initialize a node container once
        if not parser.nodes:
            if debug_mode: 
                print(f"initiate node container")

            # container for nodes; instantiated with key:val pairs like
            # "node_class_name: []"
            parser.nodes = {k:j for k, j in zip(
                                    # node class names
                                    list(node_classes), 
                                    # list of empty lists
                                    [[] for i in range(len(node_classes))]
                                              )
                                              }
        
        # loop over node_classes of strategy
        for node_name in node_classes:
            # select node class
            NodeClass = node_classes[node_name]
            

            if debug_mode: 
                print(f"looping over node {NodeClass}")
            
            if debug_mode: 
                print(remaining_lines[0])

            # instantiate node if specifier is detected
            if NodeClass.START_SPECIFIER in remaining_lines[0]:
                # if debug_mode: print(f"{NodeClass.START_SPECIFIER} is current start specifier: bonds detected")

                node = NodeClass()
                # if debug_mode: print(f"starting to process Node {node.START_SPECIFIER}")
                # append node object to container
                parser.nodes[node_name].append(node)
                # switch parser state to that node object
                parser.state = node
                # update current node
                parser.current_node = node

                return remaining_lines

            
            
            # add last node to container
            if file_end_specifier in remaining_lines[0]:
                
                # parser.nodes[node_name].append(node)
                # empty list signalizes parser to stop processing
                return []
            
        # use current node to process if no specifier was found
        if parser.current_node:
            parser.state = parser.current_node
            return remaining_lines
                
            
            
        # discard line if no specifier was detected nor node is active
            # => e.g. line of introductory paragraph, preamble
        return remaining_lines[1:]
    