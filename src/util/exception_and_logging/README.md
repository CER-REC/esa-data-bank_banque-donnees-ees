Handling Exception
-------------------
use the following code snippet for handling exception. Enclose every code block
using a 'with' block with ExceptionHandler context class to handle exception and
automatic logging.

from src.util.exception_and_logging.handle_exception import ExceptionHandler

with ExceptionHandler("a general message describing the context"):
    raise ValueError("specific error message")


Logging manually
-------------------

If you want to log manually, use the following code snippet:


from src.util.exception_and_logging.process_logs import Logger

logger = Logger()
logger.log_exception("relevant message")

The above mentioned way, the logs would be done on the file and the console. 
However, we need to use a slightly different approach for logging into the
Prefect orchestration tool.

use the following code snippet to log into the Prefect orchestration tool:

from src.util.exception_and_logging.process_logs import Logger, get_prefect_logger

logger = Logger(get_prefect_logger())
logger.log_exception("relevant message")

The function get_prefect_logger() only works inside a function tagged as @task
or @flow. Prefect logger object is only accessible inside these two tags.

For more information, visit the following link:
https://discourse.prefect.io/t/can-i-define-the-logger-globally/114