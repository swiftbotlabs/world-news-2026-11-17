"""Local gate check: run main.py twice and validate the copied image.

Checks: identical bytes across runs, same bytes as the repo's entry.png, PNG or JPEG by magic bytes,
every PNG chunk CRC, IHDR first and IEND last, image data present, <= 1 MiB, exactly 1024 x 1024.
"""
import hashlib
import os
import struct
import subprocess
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIMIT = 1048576
results = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{': ' + detail if detail else ''}")


def run(out: Path) -> bytes:
    out.mkdir(parents=True, exist_ok=True)
    target = out / "entry.png"
    if target.exists():
        target.unlink()
    env = {k: v for k, v in os.environ.items() if not k.startswith("MAKEFUN_")}
    env["OUTPUT_DIR"] = str(out)
    subprocess.run([sys.executable, str(ROOT / "main.py")], check=True, env=env, cwd=ROOT)
    return target.read_bytes()


def png_info(data: bytes):
    """Walk every chunk; return (width, height, problems)."""
    problems, pos, chunks, w = [], 8, [], None
    h = None
    while pos < len(data):
        if pos + 12 > len(data):
            problems.append(f"truncated chunk header at {pos}")
            break
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        if len(body) != length or pos + 12 + length > len(data):
            problems.append(f"truncated {ctype!r} chunk")
            break
        crc = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        if zlib.crc32(ctype + body) & 0xFFFFFFFF != crc:
            problems.append(f"bad CRC in {ctype!r}")
        if ctype == b"IHDR":
            w, h = struct.unpack(">II", body[:8])
        chunks.append(ctype)
        pos += 12 + length
        if ctype == b"IEND":
            break
    if not chunks or chunks[0] != b"IHDR":
        problems.append("IHDR is not first")
    if b"IDAT" not in chunks:
        problems.append("no IDAT")
    if not chunks or chunks[-1] != b"IEND":
        problems.append("IEND missing")
    if pos != len(data):
        problems.append(f"{len(data) - pos} trailing bytes after IEND")
    if not problems:  # image data decompresses to the size the header describes (8-bit RGB/RGBA)
        ihdr = data[16:29]
        depth, ctype_ = ihdr[8], ihdr[9]
        channels = {2: 3, 6: 4, 0: 1, 4: 2}.get(ctype_)
        if depth == 8 and channels:
            idat = b"".join(data[p + 8:p + 8 + struct.unpack(">I", data[p:p + 4])[0]]
                            for p in _chunk_positions(data, b"IDAT"))
            raw = zlib.decompress(idat)
            if len(raw) != h * (1 + w * channels):
                problems.append(f"image data {len(raw)} bytes, expected {h * (1 + w * channels)}")
    return w, h, problems


def _chunk_positions(data: bytes, want: bytes):
    pos = 8
    while pos < len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        if ctype == want:
            yield pos
        pos += 12 + length


def jpeg_info(data: bytes):
    problems, w, h = [], None, None
    if not data.endswith(b"\xff\xd9"):
        problems.append("no EOI marker at end")
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            problems.append(f"bad marker at {pos}")
            break
        marker = data[pos + 1]
        seglen = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[pos + 5:pos + 9])
        if marker == 0xDA:
            break
        pos += 2 + seglen
    return w, h, problems


def main() -> int:
    a = run(ROOT / "tmp" / "run1")
    b = run(ROOT / "tmp" / "run2")
    src = (ROOT / "entry.png").read_bytes()
    check("two runs write identical bytes", a == b)
    check("output equals repo entry.png", a == src)
    check("size <= 1048576 bytes", len(a) <= LIMIT, f"{len(a)} bytes")
    if a[:8] == b"\x89PNG\r\n\x1a\n":
        w, h, problems = png_info(a)
        check("PNG signature", True)
        check("PNG chunks, CRCs, IHDR/IDAT/IEND, data length", not problems, "; ".join(problems) or "all ok")
    elif a[:3] == b"\xff\xd8\xff":
        w, h, problems = jpeg_info(a)
        check("JPEG signature", True)
        check("JPEG segments and EOI", not problems, "; ".join(problems) or "all ok")
    else:
        check("PNG or JPEG signature", False, a[:8].hex())
        w = h = None
    check("exactly 1024 x 1024", (w, h) == (1024, 1024), f"{w} x {h}")
    print(f"sha256 {hashlib.sha256(a).hexdigest()}  {len(a)} bytes")
    print("ALL CHECKS PASSED" if all(results) else "SOME CHECKS FAILED")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
