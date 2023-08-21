import sys
from src.util.exception_and_logging.process_logs import berdi_logger


class ExceptionHandler:
    """
        captures specified exception 
    """
    def __init__(self, message):
        self.message = message
        self.logger = berdi_logger
    
    def __enter__(self):
        return self
    
    # this function is executed after completion of the 'with' block
    # if the with block ends normally, exc_val parameter would be None
    # thereby, the execution flow of the code continues as normal
    # if the with block ends because of an exception
    # then, exc_val parameter would contain a string representing an exception
    # thereby, the execution flow of the code halts and we terminate the program 
    # after logging relevant messages
    def __exit__(self, exc_type, exc_val, _):
        if exc_val:
            self.logger.log_exception(f"\nType:- {exc_type}\nValue:- {exc_val}\nMessage:- {self.message}\n")
            sys.exit()
