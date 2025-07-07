#!/usr/bin/env python3
"""Looping runner for spicy self check."""

import subprocess
import time
from pathlib import Path


def main() -> None:
    """Continuously rerun test when files in src/spicy or docs change."""
    watch_dirs = ["src/spicy", "docs"]
    self_check_files = Path(".self_check_files")
    while True:
        files = [
            str(path)
            for d in watch_dirs
            for path in Path(d).rglob("*")
            if "__pycache__" not in str(path) and path.is_file()
        ]
        self_check_files.write_text("\n".join(files))
        try:
            subprocess.run(
                [
                    "entr",
                    "-d",
                    "bash",
                    "-c",
                    "clear && uv run spicy --check-refs docs",
                ],
                input="\n".join(files),
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError:
            pass
        finally:
            if self_check_files.is_file():
                self_check_files.unlink()
        time.sleep(4)


if __name__ == "__main__":
    main()
