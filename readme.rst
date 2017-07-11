imgspy
======

imgspy finds the metadata (type, size) of an image given its url by fetching as little as needed. This is a python implementation of `fastimage`_. Supports image types BMP, CUR, GIF, ICO, JPEG, PNG, PSD, TIFF, WEBP.

.. _fastimage: https://github.com/sdsykes/fastimage

usage
-----

::

    >>> imgspy.info('http://via.placeholder.com/1920x1080')
    {'type': 'png', 'width': 1920, 'height': 1080}
    >>> imgspy.info('/path/to/image.jpg')
    {'type': 'jpg', 'width': 420, 'height': 240}

tests
-----

.. image:: https://travis-ci.org/nkanaev/imgspy.svg?branch=master
    :target: https://travis-ci.org/nkanaev/imgspy
