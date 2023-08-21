import inspect
from functools import wraps
from src.util.exception_and_logging.process_logs import berdi_logger


def log_execution_info(func):
    """
    decorator to be used for functions that we want to log the start and the end of the execution and along with the
    function name and the input argument keys and values
    """
    @wraps(func)
    def inner(*args, **kwargs):
        berdi_logger.log_info(f"Executing {func.__name__} with "
                                              f"{inspect.signature(func).bind(*args, **kwargs).arguments}")
        func(*args, **kwargs)
        berdi_logger.log_info(f"Finished executing {func.__name__}")
    return inner
