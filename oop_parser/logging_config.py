
# %%% Goals / Documentation
"""
Goal:
    Be able to debug efficiently via logging library.
    
Subgoal:
    Know which object of software causes problem and which objects work
    as expected.
    
Subsubgoal: detailed info required for source of error
    - which module contains implementation?
    - what class instance?
    - method/function?
    - input args?
    - output?
    
Task:
    Substitute print statements in source code with logging utilities to
    achieve goals above.
    
# usage requirements
Have logging code statements in source code permanently without (un)commenting
logging statements.

"""

# %%% Logging Config


import logging
import inspect


# Set the logging level for the root logger
LOG_LEVEL = logging.DEBUG  # Adjust as needed

# Configure console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter(
                        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_formatter)

# configure file handler
file_handler = logging.FileHandler("central_log.log")
file_handler.setFormatter(console_formatter)

# set log level
logging.getLogger().setLevel(LOG_LEVEL)

# add handlers to logger
logging.getLogger().addHandler(console_handler)

logging.getLogger().addHandler(file_handler)


# %%% 
class ModuleLogging:
    """
    Utility Class:
        provides methods to dynamically create a logger name 
        based on the class and function names where it is used.
    
    Allows single implementation in a Base Class Abstract Method in order to 
    log specific names of multiple child classes and methods.
    
    # How to use:
        - pass ModuleLogging to Base Class via implicit dependency injection
        - call ModuleLogging.get_function_logger()
    """
    

    @staticmethod
    def get_function_logger():
        """
        Dynamically creates a logger name based on the class and function names.

        Returns:
            logging.Logger: A logger object.
        """
        # access method via class name
        logger_name = ModuleLogging.get_caller_function_name(get_class_name=True, depth=2)
        logger_name = f"{logger_name}"
        logger = logging.getLogger(logger_name)
        
        return logger
    
    
    def get_caller_function_name(get_class_name:bool = False,
                                  depth:int = 1):
        """
        Get the name of the function that called the current function. 
        Also, get the class name if the caller is a class method.
    
        Args:
        get_class_name (bool, optional):       If True, return the class name as well. Default is False.
        depth           (int, optional):       The depth of the caller. Default is 1.
    
        """
    
        # Get the frame of the caller
        frame = inspect.currentframe()
        for _ in range(depth):
            frame = frame.f_back
        # Get the caller's function name
        package_name = frame.f_globals.get('__name__', None)
        caller_function_name = frame.f_code.co_name
        if get_class_name:
            # Get the caller's class name
            caller_class_name = frame.f_locals.get('self', None)
            if caller_class_name is not None:
                caller_class_name = caller_class_name.__class__.__name__
                caller_function_name = caller_class_name + '.' + caller_function_name
    
        return package_name+"."+caller_function_name

