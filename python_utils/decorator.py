import functools
import time

from loguru import logger


def latency_router(func):
    """
    Calculate endpoint latency.
        Print latency and response logs:
            logger.log('RESPONSE') - logger.log('LATENCY')
    """
    @functools.wraps(func)
    def wrap_func(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        logger.log('RESPONSE', f'[*] {result}')
        logger.log('LATENCY', f'[*] {round(time.time() - start_time, 10)} s')
        return result
    return wrap_func


def latency_function(func):
    """
    Calculate endpoint latency.
        Print latency logs [logger.log('LATENCY')].
    """
    @functools.wraps(func)
    def wrap_func(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        logger.log('LATENCY', f'[*] {round(time.time() - start_time, 10)} s')
        return result
    return wrap_func


def run_for_each(each=10):
    """
    Execute a certain function x times.

    Parameters:
    ----------
    str: each
        Number of times to be executed the function.

    Returns:
    -------
    None
    """
    def for_each(func):
        @functools.wraps(func)
        def wrap_func(*args, **kwargs):
            for i in range(each):
                _ = func(*args, **kwargs)
                logger.info(f"Run {i + 1} for {func.__name__}")
        return wrap_func
    return for_each
