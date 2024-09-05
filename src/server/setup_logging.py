import logging
import os

def setup_logging():
    logFile = get_log_path()

    logging.basicConfig(
        filename=logFile,
        filemode='a',
        format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
        level=logging.DEBUG
    )

    return logFile

def get_log_path():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, use the AppData directory
        log_dir = os.path.join(os.path.expanduser("~"), 'AppData', 'Roaming', 'Ace Centre', 'AACSpeakHelper')
    else:
        # If run from a Python environment, use the current directory
        log_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'app.log')
    return log_file