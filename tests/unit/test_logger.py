
import unittest
from unittest import mock

from python_utils import set_logger_configs
from python_utils.logger import info_and_latency_only


class TestLogger(unittest.TestCase):

    def setUp(self):
        pass

    @mock.patch("loguru.logger.add", return_value=None)
    def test_set_logger_configs(self, _logger):
        for _ in range(2):
            self.assertIsNone(set_logger_configs("", ""))

    def test_info_and_latency_only(self):
        level = mock.Mock()
        level.name = "INFO"
        self.assertTrue(info_and_latency_only({"level": level}))
