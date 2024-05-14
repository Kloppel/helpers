from state_transition_manager import StateTransitionManager
from config import Config

# import the logging config will set up the root logger from which
# module-level loggers automatically inherit from
import logging_config

from parser import Parser



def parse_file(filepath):
    """
    Takes a prm file path as str and parses its content.
    Returns a parser object containing prm section objects that contain
    the parsed data as pandas DataFrames.
    """
    
    # instantiate parsing config
    config=Config()
    
    # instantiate parser with required args
    p = Parser(filepath=filepath, 
               config=config,
               StateTransitionManager=StateTransitionManager)
    
    # inject configuration class to allow module-wise logging downstream
    p.add_module_logger(logging_config.ModuleLogging)
               
    # start parsing process           
    p.start()

    return p


# state this module is a script
if __name__ == "__main__":
    filepath = "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/par_bv.prm"
    p = parse_file(filepath)
    
# assign section dataframes to variables
atoms, angles, bonds, dihedrals, improper, nonbonded = (
                            p.nodes[i][0].section_dataframe for i in p.nodes)