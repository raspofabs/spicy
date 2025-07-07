#!/usr/bin/env python3
"""Looping runner for spec check on test data."""

import subprocess
import time
from pathlib import Path


def main() -> None:
    """Continuously rerun test when files in src/spicy or test spec change."""
    test_spec = "tests/test_data/simple_test_spec"
    watch_dirs = ["src/spicy", test_spec]
    spec_check_files = Path(".spec_check_files")
    while True:
        files = [
            str(path)
            for d in watch_dirs
            for path in Path(d).rglob("*")
            if "__pycache__" not in str(path) and path.is_file()
        ]
        spec_check_files.write_text("\n".join(files))
        try:
            subprocess.run(
                [
                    "entr",
                    "-d",
                    "bash",
                    "-c",
                    f"clear && uv run spicy --check-refs {test_spec}",
                ],
                input="\n".join(files),
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError:
            pass
        finally:
            if spec_check_files.is_file():
                spec_check_files.unlink()
        time.sleep(4)


if __name__ == "__main__":
    main()
