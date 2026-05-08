#!/usr/bin/env python3
"""
AP FRQ Bulk Downloader (Python version — works on Windows/Mac/Linux)
Downloads all PDFs from manifest.json, organized by course/year.
Resume-safe: skips already-downloaded files.

Usage:
    python3 download.py
    python3 download.py --workers 4   # parallel downloads
"""

import json
import os
import sys
import time
import argparse
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

OUTPUT_DIR = Path("files")
MANIFEST = Path("manifest.json")
DELAY = 0.03  # seconds between requests per thread

def sanitize(name: str) -> str:
    return name.replace("/", "-").replace(":", "-").strip()

def download_file(entry: dict) -> tuple[str, str]:
    course = sanitize(entry["course"])
    year = str(entry["year"])
    name = entry["name"]
    url = entry["url"]

    dest = OUTPUT_DIR / course / year / name
    if dest.exists():
        return "skip", f"{entry['course']}/{year}/{name}"

    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            dest.write_bytes(r.read())
        time.sleep(DELAY)
        return "ok", f"{entry['course']}/{year}/{name}"
    except Exception as e:
        dest.unlink(missing_ok=True)
        return "err", f"{entry['course']}/{year}/{name}: {e}"

def main():
    parser = argparse.ArgumentParser(description="AP FRQ Bulk Downloader")
    parser.add_argument("--workers", type=int, default=1,
                        help="Number of parallel download workers (default: 1)")
    args = parser.parse_args()

    if not MANIFEST.exists():
        print("Error: manifest.json not found. Run from repo root.")
        sys.exit(1)

    with open(MANIFEST) as f:
        entries = json.load(f)

    total = len(entries)
    print(f"Total files in manifest: {total}")
    print(f"Output directory: {OUTPUT_DIR.resolve()}")
    print(f"Workers: {args.workers}\n")

    downloaded = skipped = errors = 0
    done = 0

    if args.workers == 1:
        for entry in entries:
            status, msg = download_file(entry)
            done += 1
            if status == "ok":
                downloaded += 1
                print(f"[{done}/{total}] ✓ {msg}")
            elif status == "skip":
                skipped += 1
            else:
                errors += 1
                print(f"[{done}/{total}] ✗ {msg}")
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {ex.submit(download_file, e): e for e in entries}
            for future in as_completed(futures):
                status, msg = future.result()
                done += 1
                if status == "ok":
                    downloaded += 1
                    print(f"[{done}/{total}] ✓ {msg}")
                elif status == "skip":
                    skipped += 1
                else:
                    errors += 1
                    print(f"[{done}/{total}] ✗ {msg}")

    print(f"\n{'='*60}")
    print(f"Done.")
    print(f"  Downloaded : {downloaded}")
    print(f"  Skipped    : {skipped}")
    print(f"  Errors     : {errors}")
    print(f"  Total      : {total}")

if __name__ == "__main__":
    main()
