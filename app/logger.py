import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='[%(levelname)s] %(asctime)s %(module)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log = logging.getLogger(__name__)