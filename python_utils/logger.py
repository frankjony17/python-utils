

def info_and_latency_only(record):
    """Helper function to filter out all levels except for INFO and LATENCY.
    This is used to control which messages are passed to the sink.
    """
    return record["level"].name in ["INFO", "LATENCY", "RESPONSE", "SUCCESS"]


def set_logger_configs(info_logs_file, error_logs_file) -> None:
    """Set custom logger configurations. Add sinks to record logs in specific files.
    Create levels for Response and Latency where each level has a name,
    a severity number (larger is more severe), and a color.
    """
    from loguru import logger
    try:
        logger.level("RESPONSE", no=15, color="<green><bold>")
        logger.level("LATENCY", no=15, color="<blue><bold>")
    except TypeError as e:
        logger.warning(f'Level already exists: {e}')

    logger.add(info_logs_file, filter=info_and_latency_only)
    logger.add(error_logs_file, level=30)  # WARNING, ERROR, and CRITICAL
