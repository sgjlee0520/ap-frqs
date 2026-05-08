import json, re, sys
from pathlib import Path
from urllib.parse import quote

MANIFEST = Path("manifest.json")
LOG_FILE = Path("upload_log.json")
IA_BASE  = "https://archive.org/download"

def course_to_identifier(name):
    slug = name.lower()
    slug = re.sub(r'^ap\s+', '', slug)
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return f"ap-frq-{slug.strip('-')}"

def build_ia_url(course, year, filename):
    identifier = course_to_identifier(course)
    return f"{IA_BASE}/{identifier}/{quote(str(year))}/{quote(filename)}"

with open(MANIFEST) as f:
    entries = json.load(f)

Path("manifest.original.json").write_text(json.dumps(entries, indent=2))

new_entries = []
for e in entries:
    new = dict(e)
    new["source"] = e["url"]
    new["url"] = build_ia_url(e["course"], e["year"], e["name"])
    new_entries.append(new)

MANIFEST.write_text(json.dumps(new_entries, indent=2))
print(f"Done. {len(new_entries)} URLs updated to archive.org.")
print("Original saved to manifest.original.json")
