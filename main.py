"""Copy the repository's entry.png to the output folder, byte for byte, after checking it.

Checks: the file starts with the PNG or JPEG signature and is at most 1048576 bytes.
The output folder is /output unless OUTPUT_DIR is set (for local tests).
Standard library only, no network.
"""
import os
import sys
from pathlib import Path

LIMIT = 1048576
PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPEG_SIG = b"\xff\xd8\xff"


def main() -> int:
    src = Path(__file__).resolve().parent / "entry.png"
    data = src.read_bytes()
    if not (data.startswith(PNG_SIG) or data.startswith(JPEG_SIG)):
        print(f"error: {src} is neither PNG nor JPEG", file=sys.stderr)
        return 1
    if len(data) > LIMIT:
        print(f"error: {src} is {len(data)} bytes, over {LIMIT}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.png").write_bytes(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
