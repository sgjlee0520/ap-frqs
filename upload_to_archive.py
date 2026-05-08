#!/usr/bin/env python3
import argparse, json, os, re, sys, time
from pathlib import Path
from collections import defaultdict

try:
    from internetarchive import get_item, upload
except ImportError:
    print("Run: pipx install internetarchive")
    sys.exit(1)

FILES_DIR = Path("files")
MANIFEST  = Path("manifest.json")
LOG_FILE  = Path("upload_log.json")
IDENTIFIER_PREFIX = "ap-frq-"

def course_to_identifier(name):
    slug = name.lower()
    slug = re.sub(r'^ap\s+', '', slug)
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return f"{IDENTIFIER_PREFIX}{slug.strip('-')}"

def course_metadata(name):
    return {
        "title":      f"{name} Free Response Questions Archive",
        "mediatype":  "texts",
        "collection": "opensource",
        "subject":    ["AP exam", "free response", "College Board", name],
        "description": f"Complete archive of {name} AP exam Free Response Questions, Scoring Guidelines, and Sample Responses. Sourced from publicly available College Board documents. Organized by year.",
        "creator":    "College Board (original); archived by sgjlee0520",
        "language":   "eng",
    }

def load_log():
    return json.load(open(LOG_FILE)) if LOG_FILE.exists() else {}

def save_log(log):
    json.dump(log, open(LOG_FILE, "w"), indent=2)

def get_course_files(name):
    safe = name.replace("/", "-").replace(":", "-").strip()
    d = FILES_DIR / safe
    return sorted(d.rglob("*.pdf")) if d.exists() else []

def upload_course(name, dry_run, log):
    identifier = course_to_identifier(name)
    files = get_course_files(name)
    if not files:
        print(f"  [SKIP] No local files: {name}")
        return {"status": "skip"}

    already = log.get(identifier, {}).get("uploaded_files", [])
    pending = [f for f in files if str(f) not in already]

    print(f"\n{'='*60}")
    print(f"Course : {name}")
    print(f"Item   : {identifier}")
    print(f"Files  : {len(files)} total, {len(pending)} pending")

    if not pending:
        print("  [DONE] All files already uploaded.")
        return {"status": "complete"}

    if dry_run:
        for f in pending[:3]: print(f"  [DRY] {f}")
        return {"status": "dry_run"}

    safe = name.replace("/", "-").replace(":", "-").strip()
    course_dir = FILES_DIR / safe
    md = course_metadata(name)
    errors = []

    for f in pending:
        remote = str(f.relative_to(course_dir))
        try:
            r = upload(identifier, files={remote: str(f)}, metadata=md,
                       retries=5, retries_sleep=10, verbose=False, queue_derive=False)
            code = r[0].status_code if r else 0
            if code in (200, 201):
                already.append(str(f))
                print(f"  ✓ {remote}")
            else:
                errors.append(f"{remote}: HTTP {code}")
                print(f"  ✗ {remote}: HTTP {code}")
        except Exception as e:
            errors.append(f"{remote}: {e}")
            print(f"  ✗ {remote}: {e}")
        time.sleep(0.1)

    log[identifier] = {"course": name, "identifier": identifier,
                        "url": f"https://archive.org/details/{identifier}",
                        "uploaded_files": already, "errors": errors,
                        "status": "complete" if not errors else "partial"}
    save_log(log)
    return log[identifier]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", help="Single course name")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(MANIFEST) as f:
        entries = json.load(f)

    all_courses = sorted(set(e["course"] for e in entries))
    courses = [args.course] if args.course else all_courses

    log = load_log()
    for course in courses:
        upload_course(course, args.dry_run, log)

    print(f"\nDone. Log: {LOG_FILE}")
    print(f"View at: https://archive.org/search?query=creator%3A%22sgjlee0520%22")

if __name__ == "__main__":
    main()
