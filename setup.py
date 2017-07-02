# coding: utf-8
from setuptools import setup


with open('readme.rst') as f:
    readme = f.read()


setup(
    name='imgspy',
    version='0.1.0',
    description='Find the size or type of the image without '
                'fetching the whole content.',
    long_description=readme,
    license='MIT',
    author='Nazar Kanaev',
    author_email='nkanaev@live.com',
    py_modules=['imgspy'],
    test_suite='tests')
