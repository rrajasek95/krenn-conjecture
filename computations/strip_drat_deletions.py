#!/usr/bin/env python3
"""Remove optional DRAT deletion records, yielding a deletion-free trace."""

from __future__ import annotations

import argparse
from pathlib import Path


def strip(source, target):
    kept = 0
    deleted = 0
    with Path(source).open(encoding="ascii") as input_stream:
        with Path(target).open("w", encoding="ascii") as output_stream:
            for line in input_stream:
                if line.startswith("d "):
                    deleted += 1
                else:
                    output_stream.write(line)
                    kept += 1
    print(f"kept additions={kept}; removed deletions={deleted}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("target")
    args = parser.parse_args()
    strip(args.source, args.target)


if __name__ == "__main__":
    main()
