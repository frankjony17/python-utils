
import unittest
from unittest import mock

import numpy as np

from python_utils import (b64_to_numpy, download_model,
                          get_base_64_for_test, warm_up_starter)


def _exists():
    return False


def _exists_true():
    return True


class TestOthers(unittest.TestCase):

    def setUp(self):
        self.base_64 = get_base_64_for_test("real", 5)

    @mock.patch("python_utils.others.wget.download", return_value=None)
    def test_download_model(self, wget):
        model_file = mock.Mock(exists=_exists)
        model_name = "file.teste"
        self.assertEqual(download_model(model_file, model_name), None)

    @mock.patch("python_utils.others.wget.download")
    def test_download_model_exc(self, wget):
        model_file = mock.Mock(exists=_exists)
        model_name = "file.teste"
        wget.side_effect = Exception(mock.Mock(return_value={'status': 500}), 'error')
        with self.assertRaises(Exception):
            download_model(model_file, model_name)

    def test_download_model_exists(self):
        model_file = mock.Mock(exists=_exists_true)
        model_name = "file.teste"
        self.assertIsNone(download_model(model_file, model_name))

    def test_b64_to_numpy_rgb(self):
        np_img_rgb = b64_to_numpy(self.base_64)
        self.assertIsInstance(np_img_rgb, np.ndarray)
        self.assertEqual(np_img_rgb.ndim, 3)

    def test_b64_to_numpy_grayscale(self):
        np_img_color = b64_to_numpy(self.base_64, rgb=False)
        np_img_rgb = b64_to_numpy(self.base_64)
        np_img_grayscale = b64_to_numpy(self.base_64, color=False)

        self.assertIsInstance(np_img_color, np.ndarray)
        self.assertEqual(np_img_color.ndim, 3)
        self.assertIsInstance(np_img_rgb, np.ndarray)
        self.assertEqual(np_img_rgb.ndim, 3)
        self.assertIsInstance(np_img_grayscale, np.ndarray)
        self.assertEqual(np_img_grayscale.ndim, 2)

    def test_b64_to_numpy_exception(self):
        with self.assertRaises(ValueError):
            b64_to_numpy("100", color=False)

    def test_opencv_b64_for_text(self):  # TODO
        pass

    def test_get_base_64_for_test_exception(self):
        image = get_base_64_for_test("fake", 6)
        self.assertIsNone(image)

    def test_warm_up_starter(self):
        self.assertIsNone(warm_up_starter(get_base_64_for_test, 6))
