import base64
import binascii
import ssl
from pathlib import Path

import cv2
import numpy as np
import wget
from loguru import logger

from python_utils.decorator import run_for_each


def b64_to_numpy(
        encoded: str, color: bool = True, rgb: bool = True) -> np.ndarray:
    """Convert base64 encoded string to NumPy array.
    If color, converts to RGB format, else, converts to grayscale format.

    Parameters:
        - encoded: Base64 encoded string to decode.
        - color: Flag indicating if the result should be in cv2.IMREAD_COLOR.
        - rgb: Flag indicating if the result should be in cv2.COLOR_BGR2RGB.
        - gray: Flag indicating if the result should be in cv2.IMREAD_GRAYSCALE.

    Returns:
        - img_np: An n-dimentional array of the input image.

    Raises:
        - `ValueError`
    """
    try:
        image = np.frombuffer(base64.b64decode(encoded), np.uint8)

        if color:
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            if rgb:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
    except (binascii.Error, cv2.error) as e:
        logger.opt(exception=True).error(f'[-] ValueError: {e}')
        raise ValueError
    return image


def download_model(model_file, model_name) -> None:
    """Downloads the machine learning model, unless the model file already exists.

    Parameters:
    ----------
    str: model_file
        Path to medel file.
    str: model_dir
        Path to model dir.
    str: model_name
        Name of model.
    Returns:
    -------
    None

    Raises:
    ------
    ModelError

    """
    from python_utils import ATF_MODELS_URL
    if not model_file.exists():
        logger.info(f'[*] {model_file} not found! Downloading...')
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            wget.download(ATF_MODELS_URL + model_name, out=str(model_file))
            logger.success(f'[+] {model_name} successfully downloaded')
        except Exception as e:
            logger.opt(exception=True).error(f'Unable to download model: {e}')
            raise


def get_base_64_for_test(image, name):
    """Get base64 encode from an image.
    Python contains 10 images (5 spoofing and 5 reais).

    Parameters:
    ----------
    image: str
        'real' or 'fake'.
    name: str
        Name of available images - '1', '2', '3', '4', '5'.
    Returns:
    -------
    str:
        Base64 (images decode).
    Raises:
    ------
    FileNotFoundError
        If it doesn't find the image it throws an exception
    """
    path = Path(__file__).parent.joinpath("images")

    if image == "real":
        path = path.joinpath("real")
    else:
        path = path.joinpath("fake")
    path = path.joinpath(f"{name}.jpg")

    try:
        with open(str(path), "rb") as image:
            image_string = base64.b64encode(image.read())
        return image_string.decode('utf-8')
    except FileNotFoundError as e:
        logger.opt(exception=True).error(f'[-] File not found exception: {e}')


def warm_up_starter(spoofing_func, models):
    """Start model inference to prompt the application. (first calls are slower). Made 3 calls.

        Parameters:
        ----------
        spoofing_func: function
            Spoofing function that starts the inference process, usually the endpoint.
        """
    from python_utils import RequestBase64
    request = RequestBase64(base_64=get_base_64_for_test("real", 5))
    logger.info('[***] Start model inference to prompt the application. 3 times...')

    @run_for_each(5)
    def _exc_function():
        _ = spoofing_func(request, models)

    return _exc_function()
