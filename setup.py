# coding: utf-8
"""
imgspy
======

imgspy finds the metadata (type, size) of an image given its url by fetching
as little as needed. This is a python implementation of `fastimage`_. Supports
image types BMP, CUR, GIF, ICO, JPEG, PNG, PSD, TIFF, WEBP.

.. _fastimage: https://github.com/sdsykes/fastimage

usage
-----

::

    >>> imgspy.info('http://via.placeholder.com/1920x1080')
    {'type': 'png', 'width': 1920, 'height': 1080}
    >>> imgspy.info('/path/to/image.jpg')
    {'type': 'jpg', 'width': 420, 'height': 240}
"""
from setuptools import setup


setup(
    name='imgspy',
    version='0.2.0',
    description='Find the size or type of the image without '
                'fetching the whole content.',
    long_description=__doc__,
    url='https://github.com/nkanaev/imgspy',
    license='MIT',
    keywords='fastimage image size',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    author='Nazar Kanaev',
    author_email='nkanaev@live.com',
    py_modules=['imgspy'],
    test_suite='tests'
)
