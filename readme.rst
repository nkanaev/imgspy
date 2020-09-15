imgspy
======

imgspy finds the metadata (type, size) of an image given its url by fetching as little as needed. This is a python implementation of `fastimage`_. Supports image types BMP, CUR, GIF, ICO, JPEG, PNG, PSD, TIFF, WEBP.

.. _fastimage: https://github.com/sdsykes/fastimage

usage
-----

::

    >>> imgspy.info('http://via.placeholder.com/1920x1080')
    {'type': 'png', 'width': 1920, 'height': 1080}
    >>> with requests.get('http://via.placeholder.com/1920x1080', stream=True) as res:
    ...     imgspy.info(res.raw)
    {'type': 'png', 'width': 1920, 'height': 1080}
    >>> imgspy.info('/path/to/image.jpg')
    {'type': 'jpg', 'width': 420, 'height': 240}
    >>> with open('/path/to/image.jpg') as f:
    ...     imgspy.info(f)
    {'type': 'jpg', 'width': 420, 'height': 240}

.. image:: https://github.com/nkanaev/imgspy/workflows/test/badge.svg
    :target: https://github.com/nkanaev/imgspy/actions
