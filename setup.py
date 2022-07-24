# -*- encoding: utf-8 -*-
# Source: https://packaging.python.org/guides/distributing-packages-using-setuptools/

import io
import typing

from setuptools import find_packages, setup

dev_requirements = [
    'bandit',
    'flake8',
    'isort',
    'pytest',
]
unit_test_requirements = [
    'pytest-cov',
]
integration_test_requirements = unit_test_requirements
run_requirements = [
    'loguru==0.5.3',
    'pydantic==1.8.2',
    'jaeger-client==4.5.0',
    'starlette==0.14.2',
    'starlette_exporter==0.7.0',
    'numpy>=1.18.4',
    'opencv-python==4.5.2.52',
    'wget==3.2',
]

about: typing.Dict[str, str] = {}
with open('python_utils/__about__.py') as fp:
    exec(fp.read(), about)

with io.open('README.md', encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name="python_utils",
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    package_data={'': ['images/fake/*.jpg', 'images/real/*.jpg']},
    url=about['__url__'],
    license="COPYRIGHT",
    description=about['__description__'],
    long_description=long_description,
    zip_safe=False,
    install_requires=run_requirements,
    extras_require={
         'dev': dev_requirements,
         'unit': unit_test_requirements,
         'integration': integration_test_requirements,
    },
    python_requires='>=3.8',
    classifiers=[
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['fksolutions', 'utils']
)
