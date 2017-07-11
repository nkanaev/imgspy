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
                return
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
        img_type = 'ico' if chunk[2:3] == b'\x01' else 'cur'
        num_images = struct.unpack('<H', chunk[4:6])[0]
        w, h = struct.unpack('BB', chunk[6:8])
        w = 256 if w == 0 else w
        h = 256 if h == 0 else h
        return {'type': img_type, 'width': w, 'height': h, 'num_images': num_images}
    elif chunk.startswith(b'BM'):
        headersize = struct.unpack("<I", chunk[14:18])[0]
        if headersize == 12:
            w, h = struct.unpack("<HH", chunk[18:22])
        elif headersize >= 40:
            w, h = struct.unpack("<ii", chunk[18:26])
        else:
            return
        return {'type': 'bmp', 'width': w, 'height': h}
    elif chunk.startswith(b'MM\x00\x2a') or chunk.startswith(b'II\x2a\x00'):
        w, h, orientation = None, None, None

        endian = '>' if chunk[0:2] == b'MM' else '<'
        offset = struct.unpack(endian + 'I', chunk[4:8])[0]
        chunk += stream.read(offset - len(chunk) + 2)

        tag_count = struct.unpack(endian + 'H', chunk[offset:offset+2])[0]
        offset += 2
        for i in range(tag_count):
            if len(chunk) - offset < 12:
                chunk += stream.read(12)
            type = struct.unpack(endian + 'H', chunk[offset:offset+2])[0]
            data = struct.unpack(endian + 'H', chunk[offset+8:offset+10])[0]
            offset += 12
            if type == 0x100:
                w = data
            elif type == 0x101:
                h = data
            elif type == 0x112:
                orientation = data
            if all([w, h, orientation]):
                break

        if orientation >= 5:
            w, h = h, w
        return {'type': 'tiff', 'width': w, 'height': h, 'orientation': orientation}

