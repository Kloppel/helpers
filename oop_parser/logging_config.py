
# %%% Goals

"""
Goal:
    Be able to debug efficiently via logging library.
    
Subgoal:
    Know which object of software causes problem and which objects work
    as expected.
    
Subsubgoal: 
    detailed info required for source of error
        - which module contains implementation?
        - what class instance?
        - method/function?
        - input args?
        - output?
    
Tasks:
    
    1) use Nereu's logging utils and adjust + simplify if required
    
    2) Substitute print statements in source code with logging events to
       achieve goals above.
    
"""




# %%% Documentation

"""
1) use Nereu's logging utils and adjust + simplify if required
    
Simplification:
    simplify ModuleLogging by reducing inspect usage to just add 
    a class/module-specific log file:
    
        
        event (logger.debug() call) has default arg 'stacklevel=1'. that means,
        it automatically passes the calling function name to the LogRecord object.
        
        the LogRecord object contains the function name via its attr 'funcName'.
        
        By that, the logger object, which holds all LogRecords, can directly access
        a records calling function.
        
        This is reflected by the updated formatter:
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

"""


# %%% Logging Config


import logging
import inspect


# !!! ADJUST LEVEL HERE
# Set the logging level for the root logger
LOG_LEVEL = logging.DEBUG  

# Configure console handler
console_handler = logging.StreamHandler()

console_formatter = logging.Formatter(
                        '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_formatter)

# set log level
logging.getLogger().setLevel(LOG_LEVEL)

# add handlers to logger
logging.getLogger().addHandler(console_handler)



# %%% Wrap Logging Utilities into a Class

class ModuleLogging:
    """
    Utility Class:
        provides methods to dynamically create a logger name 
        based on the class and function names where it is used.
    
    get_function_logger now must be called only once in Base Class 
    Abstract Method in order to log specific names of multiple child classes 
    and their methods.
    
    # How to use:
        - pass ModuleLogging class instance to Base Class via 
          implicit dependency injection
        - call ModuleLogging.get_function_logger(), assign to self.logger
        - use self.logger to make event calls in all methods
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
        
        logger = ModuleLogging.set_module_log_file(logger)
        
        return logger
    
        
    
    
    def set_module_log_file(logger):
        """
        Extract caller class name and add FileHandler to logger to log events
        class-wise.        
        """
        
        # access logger name
        name = logger.name
        
        # split name into: module_name, class name, method name
        split_name = name.split(".")

        for i in split_name:
            # class name is CamelCase: only name fulfilling condition
            if i[0].isupper():
                # assign class name
                caller_class_name = i
                # instantiate log file using class name
                module_log_file_handler = logging.FileHandler(
                    f"{caller_class_name}.log")
                # use general formatter
                module_log_file_handler.setFormatter(console_formatter)
    
                # add FileHander to logger
                logger.addHandler(module_log_file_handler)
        
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

    ##!!! integrate in future
    # def setup_logger(logger_name:str, log_file:str, 
    #                   mode: str = 'w',
    #                   level:int = logging.DEBUG, filter = None,
    #                   format:str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    #     """
    #     Set up logging for the charmm_manager class.
    
    #     Args:
    #     logger_name (str):                          Logger name.
    #     log_file    (str):                          Log file name.
    #     mode        (str, optional):                Mode to open the log file. Default is 'w'.
    #     level       (int, optional):                Logging level. Default is logging.DEBUG.
    #     filter      (str or str list, optional):    Filter to apply to the logger. Default is None.
    #     format      (str, optional):                Format of the log message. Default is '%(asctime)s - %(name)s - %(levelname)s - %(message)s'.
    
    #     """
    #     debug_handler = logging.FileHandler(log_file, mode=mode)
    #     debug_handler.setLevel(level)  # Set the handler's level to DEBUG
    
    #     # Create a formatter for the handler
    #     formatter = logging.Formatter(format)
    #     debug_handler.setFormatter(formatter)
    
    #     if filter is not None:
    #         if isinstance(filter, list):
    #             for f in filter:
    #                 debug_handler.addFilter(logging.Filter(f))
    #         else:
    #             debug_handler.addFilter(logging.Filter(filter))
    
    #     # Add the handler to the logger
    #     logger=logging.getLogger(logger_name)
    #     logger.addHandler(debug_handler)
    #     logger.setLevel(level)  