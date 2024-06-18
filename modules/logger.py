import logging
import os

def setup_logging(timestamp, log_dir='data/log', log_filename=None):
    """
    Sets up the logging configuration.

    Args:
        timestamp (str): The timestamp to be included in the log filename.
        log_dir (str): The directory where the log file will be saved.
        log_filename (str): The name of the log file.

    Returns:
        None
    """
    if log_filename is None:
        log_filename = f'log_{timestamp}.txt'

    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Set up logging
    logging.basicConfig(
        filename=os.path.join(log_dir, log_filename),
        filemode='w',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
