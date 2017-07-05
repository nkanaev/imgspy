import io
import os
import sys
import base64
import struct
import contextlib


PY2 = sys.version_info[0] == 2

if PY2:
    from urllib import urlopen
    binary_type = str
else:
    from urllib.request import urlopen
    binary_type = bytes


@contextlib.contextmanager
def openstream(input):
    if hasattr(input, 'read'):
        input.seek(0)
        yield input
    elif os.path.isfile(input):
        with open(input, 'rb') as f:
            yield f
    elif input.startswith('http'):
        with contextlib.closing(urlopen(input)) as f:
            yield f
    elif isinstance(input, str) and input.startswith('data:'):
        parts = input.split(';', 2)
        if len(parts) == 2 and parts[1].startswith('base64,'):
            yield io.BytesIO(base64.b64decode(parts[1][7:]))


def info(input):
    with openstream(input) as stream:
        return probe(stream)


def probe(stream):
    w, h = None, None
    chunk = stream.read(26)

    if chunk.startswith(b'\x89PNG\r\n\x1a\n'):
        if chunk[12:16] == b'IHDR':
            w, h = struct.unpack(">LL", chunk[16:24])
        else:
            # todo: fried png's http://www.jongware.com/pngdefry.html
            w, h = struct.unpack(">LL", chunk[8:16])
        return {'type': 'png', 'width': w, 'height': h}
    elif chunk.startswith(b'GIF89a') or chunk.startswith(b'GIF87a'):
        w, h = struct.unpack('<HH', chunk[6:10])
        return {'type': 'gif', 'width': w, 'height': h}
    elif chunk.startswith(b'\xff\xd8'):
        start = 0
        data = chunk
        while True:
            chunk = stream.read(10)
            if not chunk:
                return None
            data += chunk
            next = data.find(b'\xff', start + 1)
            if next == -1:
                continue
            start = next
            data += stream.read(10)
            if data[start+1] in b'\xc0\xc2':
                h, w = struct.unpack('>HH', data[start+5:start+9])
                return {'type': 'jpg', 'width': w, 'height': h}
    elif chunk.startswith(b'\x00\x00\x01\x00') or chunk.startswith(b'\x00\x00\x02\x00'):
        img_type = 'ico' if chunk[2] == 1 else 'cur'
        num_images = struct.unpack('<H', chunk[4:6])[0]
        w, h = struct.unpack('BB', chunk[6:8])
        w = 256 if w == 0 else w
        h = 256 if h == 0 else h
        return {'type': img_type, 'width': w, 'height': h, 'num_images': num_images}
