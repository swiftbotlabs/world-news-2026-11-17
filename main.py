"""Copy the repository's entry.png to the output folder, byte for byte.

The output folder is /output unless MAKEFUN_OUTPUT_DIR (or OUTPUT_DIR) is set, for local tests.
Standard library only, no network.
"""
import os
import shutil
from pathlib import Path


def main() -> None:
    src = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
