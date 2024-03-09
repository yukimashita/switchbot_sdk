from setuptools import setup, find_packages

from switchbot import __version__


setup(
    name='switchbot_sdk',
    version=__version__,
    description='SwitchBot API client',
    author='hiroya@spir.co.jp',
    packages=find_packages(),
    license='BSD',
    install_requires=[
        'requests'
    ]
)
