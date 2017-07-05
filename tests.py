import re
import os
import imgspy
import unittest
import textwrap


BASEDIR = os.path.dirname(os.path.abspath(__file__))
FORMAT = 'sample(?P<width>\d+)x(?P<height>\d+)(?P<comment>[^.]*).(?P<format>\w+)'


class TestAll(unittest.TestCase):
    def assert_dict_contains(self, result, subset, msg=None):
        # todo: diff message
        self.assertTrue(set(subset.items()).issubset(set(result.items())), msg=msg)

    def test_files(self):
        for filename in os.listdir(os.path.join(BASEDIR, 'fixtures')):
            match = re.match(FORMAT, filename)
            if not match:
                continue
            filepath = os.path.join(BASEDIR, 'fixtures', filename)
            result_actual = imgspy.info(filepath)
            result_expected = {
                'type': match.group('format'),
                'width': int(match.group('width')),
                'height': int(match.group('height')),
            }
            self.assert_dict_contains(result_actual, result_expected, msg=filename)
            with open(filepath, 'rb') as f:
                self.assert_dict_contains(imgspy.info(f), result_expected, msg=filename)

    def test_datastr(self):
        data = textwrap.dedent('''data:image/png;base64,
            iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
            KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''')
        self.assertEqual({'type': 'png', 'width': 2, 'height': 1}, imgspy.info(data))

    def test_url(self):
        domain = 'http://via.placeholder.com'
        urls = {
            domain + '/500x500': {'type': 'png', 'width': 500, 'height': 500},
            domain + '/500x500.png': {'type': 'png', 'width': 500, 'height': 500},
            domain + '/500x500.jpg': {'type': 'jpg', 'width': 500, 'height': 500},
        }
        for url, result_expected in urls.items():
            self.assertEqual(result_expected, imgspy.info(url))


if __name__ == '__main__':
    unittest.main()
