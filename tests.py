import re
import os
import imgspy
import unittest
import textwrap


BASEDIR = os.path.dirname(os.path.abspath(__file__))
FORMAT = 'sample(?P<width>\d+)x(?P<height>\d+)(?P<comment>[^.]*).(?P<format>\w+)'


class TestAll(unittest.TestCase):
    def test_files(self):
        for filename in os.listdir(os.path.join(BASEDIR, 'fixtures')):
            match = re.match(FORMAT, filename)
            if not match:
                continue
            filepath = os.path.join(BASEDIR, 'fixtures', filename)
            size_expected = int(match.group('width')), int(match.group('height'))
            size_actual = imgspy.size(filepath)
            self.assertEqual(size_expected, size_actual, msg=filename)
            with open(filepath, 'rb') as f:
                self.assertEqual(size_expected, imgspy.size(f), msg=filename)

    def test_datastr(self):
        data = textwrap.dedent('''data:image/png;base64,
            iVBORw0KGgoAAAANSUhEUgAAAAIAAAABCAYAAAD0In+
            KAAAAD0lEQVR42mNk+M9QzwAEAAmGAYCF+yOnAAAAAElFTkSuQmCC''')
        self.assertEqual((2, 1), imgspy.size(data))

    def test_url(self):
        urls = [
            'http://via.placeholder.com/500x500',
            'http://via.placeholder.com/500x500.png',
            'http://via.placeholder.com/500x500.jpg',
        ]
        for url in urls:
            self.assertEqual((500, 500), imgspy.size(url))


if __name__ == '__main__':
    unittest.main()
