#!/usr/bin/env python3
"""news-image-20261124 entrypoint.

Copies the pre-rendered front page (assets/entry.png, 1024x1024 PNG) to
/output/entry.png. No network, fully deterministic: both runs write the
same bytes. Standard library only.

The image is validated before it is copied: PNG signature, every chunk's
CRC, declared width/height, and the expected sha256 of the shipped file.
"""
import hashlib
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "entry.png")
EXPECTED_SHA256 = "949bf7c9c9a527b01df56e413f4216d49512b15c25121acdb5504a76bc857b48"
EXPECTED_SIZE = 146429
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1048576  # competition limit: at most 1 MiB


def fail(msg):
    sys.stderr.write("main.py: " + msg + "\n")
    sys.exit(1)


def check_png(data):
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("not a PNG file")
    pos = 8
    width = height = None
    seen_iend = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            fail("truncated PNG chunk %r" % ctype)
        body = data[pos + 8:pos + 8 + length]
        crc_stored = struct.unpack(">I", data[pos + 8 + length:end])[0]
        crc_real = zlib.crc32(ctype + body) & 0xFFFFFFFF
        if crc_real != crc_stored:
            fail("bad CRC in chunk %r" % ctype)
        if ctype == b"IHDR":
            width, height = struct.unpack(">II", body[:8])
        if ctype == b"IEND":
            seen_iend = True
            if end != len(data):
                fail("trailing bytes after IEND")
        pos = end
    if not seen_iend:
        fail("missing IEND chunk")
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail("unexpected dimensions %sx%s" % (width, height))
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        with open(SRC, "rb") as f:
            data = f.read()
    except OSError as exc:
        fail("cannot read %s: %s" % (SRC, exc))
    if len(data) != EXPECTED_SIZE:
        fail("unexpected size %d (expected %d)" % (len(data), EXPECTED_SIZE))
    if len(data) > MAX_BYTES:
        fail("image over the 1 MiB limit: %d bytes" % len(data))
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        fail("sha256 mismatch: %s" % digest)
    check_png(data)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as f:
        f.write(data)
    with open(dest, "rb") as f:
        copied = f.read()
    if hashlib.sha256(copied).hexdigest() != EXPECTED_SHA256:
        fail("copied file failed verification")
    print("wrote %s (%d bytes, sha256 %s)" % (dest, len(copied), EXPECTED_SHA256))


if __name__ == "__main__":
    main()
