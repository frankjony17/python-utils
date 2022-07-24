
import pytest
from _pytest.logging import LogCaptureFixture
from loguru import logger

from python_utils import latency_function, latency_router


@latency_router
def func_test_1():
    return 1


@latency_function
def func_test_2():
    return 2


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    handler_id = logger.add(caplog.handler, format="{message}")
    yield caplog
    logger.remove(handler_id)


@pytest.fixture
def set_up():
    try:
        logger.level("RESPONSE", no=15, color="<green><bold>")
        logger.level("LATENCY", no=15, color="<blue><bold>")
    except TypeError:
        pass


def test_latency_router(caplog, set_up):
    value = func_test_1()
    assert value == 1
    assert len(caplog.records) == 2  # Two logs
    assert "15" in caplog.text  # Level 15


def test_latency_function(caplog, set_up):
    value = func_test_2()
    assert value == 2
    assert len(caplog.records) == 1  # Two logs
    assert "15" in caplog.text  # Level 15
