import re

debug_mode = False


class Parser:
    """
    Parses data of a file for which specifications exist in the parser config.
    Parsed data is assigned to node objects as specified in the given
    StateTransitionManager and/or node classes.    
    
    """
    
    def __init__(self, 
                 filepath: str, 
                 config,
                 StateTransitionManager):
        """
        Initialize and set variables required for starting the parsing process.
        """
        
        if debug_mode: 
            print("parser initiated")

        self.filepath = filepath
        
        # read lines from file
        self.lines = self.read_file(filepath)
        
        
        # set required config for filetype
        self.config = self.select_config_strategy(config)
        
        
        # instantiate state transition manager with nodes for specific strategy
        self.state_transition_manager = StateTransitionManager()
        
        # no node selected upon instantiation
        self.current_node = None
        
        # nodes container that will be filled by state transition manager
        self.nodes = {}
        
        # initial state is StateTransitionManager
        self.state = self.state_transition_manager
        
        
        
    def select_config_strategy(self, config):
        """
        Extracts file type, initializes config setting and returns set config.
        
        Tightly coupled to the config, which specifies allowed file types.
        """
        
        if debug_mode: 
            print("selecting config") 

        # extract file suffix from filepath
        file_suffix = re.search(r"\.(\w+)$", self.filepath).groups()[0]

        # set filetype and thus strategy
        config.select_strategy_by_filetype(file_suffix)
        
        return config
    
    
    def read_file(self, filepath):
        """
        Read file and return file contents as a list of line strings.
        """
        
        with open(filepath, "r") as file:
            lines = file.readlines()
        
            if debug_mode: 
                print("reading file content into list") 
            
            return lines
    


    def process(self, lines): 
        """
        Calls process method of the current state to process the remaining
        file lines.
        
        Resembles the object-oriented design pattern "State Pattern".
        """
        
        if debug_mode: 
            print(f"Parser calls process of STATE {self.state} for line {lines[0]}") 

        if debug_mode: 
            print(f"Contents of Nodes container 1: {self.nodes}")        

        # call monkey patched "process" method of state
        remaining_lines = self.state.process(self, lines)
        
        
        if debug_mode: 
            print(f"Parser is in state {self.state}")
        
        if debug_mode: 
            print(f"Contents of Nodes container 2: {self.nodes}")  
        
        
        if remaining_lines: 
            self.process(remaining_lines) 
    
    
    def start(self): 
        """
        Starts parsing of the file.
        """
        
        if debug_mode: 
            print("start processing") 

        # start parsing
        self.process(self.lines) 





