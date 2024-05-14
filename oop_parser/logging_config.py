
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





# # create logger
# logger = logging.getLogger("basic_logger")
# logger.setLevel(logging.DEBUG)

# # create handler
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)

# # create formatter
# formatter = logging.Formatter(
#                         '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# # set formatter
# console_handler.setFormatter(formatter)

# # add handler to logger
# logger.addHandler(console_handler)

