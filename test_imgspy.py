import os
import re
import glob
import textwrap
import urllib.request

import imgspy


BASEDIR = os.path.dirname(os.path.abspath(__file__))
FORMAT = r'sample(?P<width>\d+)x(?P<height>\d+)(?P<comment>[^.]*).(?P<format>\w+)'


def test_samples():
    for filepath in glob.glob(os.path.join(BASEDIR, 'fixtures/sample*')):
        filename = os.path.basename(filepath)
        match = re.match(FORMAT, filename)
        expected = {
            'type': match.group('format'),
            'width': int(match.group('width')),
            'height': int(match.group('height'))}

        actual = imgspy.info(open(filepath, 'rb'))
        assert isinstance(actual, dict), filename

        actual_subset = {k: v for k, v in actual.items() if k in expected}
        assert actual_subset == expected, filename


def test_datastr():
    data = textwrap.dedent('''data:image/png;base64,
        iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
        KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''')
    assert imgspy.info(data) == {'type': 'png', 'width': 2, 'height': 1}


def test_url():
    domain = 'http://via.placeholder.com'
    urls = {
        domain + '/500x500.png': {'type': 'png', 'width': 500, 'height': 500},
        domain + '/500x500.jpg': {'type': 'jpg', 'width': 500, 'height': 500},}
    for url, expected in urls.items():
        assert imgspy.info(urllib.request.urlopen(url)) == expected
