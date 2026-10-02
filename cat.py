```python
#!/usr/bin/env python3
"""
A memory‑efficient implementation of the Unix `cat` utility.

The original version read an entire file into memory with
`file.read()`, which caused O(n) memory usage and caused the
GitHub Actions test to OOM when fed a long /dev/urandom stream.

This version reads the input in fixed‑size blocks (default 64 KiB)
and writes each block directly to stdout, guaranteeing O(1) memory.
"""

import sys
from typing import BinaryIO

# Size of each chunk we read/write. 64 KiB is a good trade‑off
# between I/O overhead and memory footprint.
CHUNK_SIZE = 64 * 1024


def cat(file_obj: BinaryIO) -> None:
    """Copy all data from *file_obj* to stdout using a constant‑size buffer."""
    # `sys.stdout.buffer` is a binary stream; we write raw bytes.
    out = sys.stdout.buffer

    while True:
        chunk = file_obj.read(CHUNK_SIZE)
        if not chunk:               # EOF
            break
        out.write(chunk)


def main(argv: list[str] | None = None) -> int:
    """Entry point for the script.

    - If file names are supplied, each file is opened in binary mode
      and streamed.
    - If no file name is given, data is read from stdin.
    Returns an exit code (0 on success, non‑zero on error).
    """
    if argv is None:
        argv = sys.argv

    try:
        if len(argv) > 1:
            # Process each file name provided on the command line.
            for filename in argv[1:]:
                with open(filename, "rb") as f:
                    cat(f)
        else:
            # No arguments → read from standard input.
            cat(sys.stdin.buffer)
        return 0
    except Exception as exc:
        # Print a short error message to stderr and return a non‑zero code.
        sys.stderr.write(f"cat.py: error: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```
