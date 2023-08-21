# pylint: disable=invalid-name
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from enum import Enum
from dotenv import load_dotenv
from prefect import get_run_logger, context

load_dotenv(".env", override=True)

# format used for logging
log_formatter = logging.Formatter('%(asctime)-15s %(levelname)-2s %(message)s')

# log file location
log_file_directory = os.getenv("LOG_FILE_DIRECTORY")
log_filepath = Path(log_file_directory).joinpath(f"log_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.log")


class LoggerType(Enum):
    """ Enum for python loggers """
    CONSOLE_LOGGER = "console_logger"
    FILE_LOGGER = "file_logger"
    PREFECT_LOGGER = "prefect_logger"


def get_file_logger():
    """
        logging to file configurations
    """
    file_handler = logging.FileHandler(filename=log_filepath, mode="a", encoding="utf-8")
    file_handler.setFormatter(log_formatter)
    file_logger = logging.getLogger(LoggerType.FILE_LOGGER.value)
    file_logger.addHandler(file_handler)
    file_logger.setLevel(logging.INFO)
    
    return file_logger


def get_console_logger():
    """
        console logging configurations
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_logger = logging.getLogger(LoggerType.CONSOLE_LOGGER.value)
    console_logger.addHandler(console_handler)
    console_logger.setLevel(logging.DEBUG)

    return console_logger


class Logger:
    """
        a class object that handles all logging related tasks
    """
    def __init__(self):
        self.console_logger = get_console_logger()
        self.file_logger = get_file_logger()

    def _has_active_prefect_runs(self):
        task_context = context.TaskRunContext.get()
        flow_context = context.FlowRunContext.get()
        if task_context or flow_context:
            return True
        return False

    def log_exception(self, message):
        """
            This function logs exceptions during BERDI data processing 

            Parameters
            ----------------
            message (str): exception message
            Output
            --------------
            None
        """
        self.console_logger.exception(message, stack_info=True, exc_info=True)
        self.file_logger.exception(message, stack_info=True, exc_info=True)
        if self._has_active_prefect_runs():
            get_run_logger().exception(message, stack_info=True, exc_info=True)

    def log_info(self, message):
        """
            This function logs general information during BERDI data processing 

            Parameters
            ----------------
            message (str): exception message
            Output
            --------------
            None
        """
        self.console_logger.info(message)
        self.file_logger.info(message)
        if self._has_active_prefect_runs():
            get_run_logger().info(message)

    def log_warning(self, message):
        """
            This function logs warning messages during BERDI data processing 

            Parameters
            ----------------
            message (str): exception message

            Output
            --------------
            None
        """
        self.console_logger.warning(message)
        self.file_logger.warning(message)
        if self._has_active_prefect_runs():
            get_run_logger().warning(message)

    def log_debug(self, message):
        """
            This function logs warning messages during BERDI data processing 

            Parameters
            ----------------
            message (str): exception message

            Output
            --------------
            None
        """
        self.console_logger.debug(message, stack_info=True)
        self.file_logger.debug(message, stack_info=True)
        if self._has_active_prefect_runs():
            get_run_logger().debug(message, stack_info=True)


berdi_logger = Logger()
