
import unittest

from python_utils import init_jaeger_tracer


class TestJaeger(unittest.TestCase):

    def setUp(self):
        pass

    def test_init_jaeger_tracer(self):
        config = init_jaeger_tracer()
        self.assertEqual(config.service_name, "python-utils")
