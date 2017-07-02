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


def size(input):
    with openstream(input) as stream:
        _, width, height = probe(stream)
        return width, height


def probe(stream):
    w, h = None, None
    chunk = stream.read(26)

    if chunk.startswith(b'\x89PNG\r\n\x1a\n'):
        if chunk[12:16] == b'IHDR':
            w, h = struct.unpack(">LL", chunk[16:24])
        else:
            # todo: fried png's http://www.jongware.com/pngdefry.html
            w, h = struct.unpack(">LL", chunk[8:16])
        return 'png', w, h
    elif chunk.startswith(b'GIF89a') or chunk.startswith(b'GIF87a'):
        w, h = struct.unpack('<HH', chunk[6:10])
        return 'gif', w, h
    elif chunk.startswith(b'\xff\xd8'):
        start = 0
        data = chunk
        while True:
            chunk = stream.read(10)
            if not chunk:
                return None, None, None
            data += chunk
            next = data.find(b'\xff', start + 1)
            if next == -1:
                continue
            start = next
            data += stream.read(10)
            if data[start+1] in b'\xc0\xc2':
                h, w = struct.unpack('>HH', data[start+5:start+9])
                return 'jpg', w, h
    return None, None, None
