# AP FRQ Archive

A complete archive of AP exam Free Response Questions, scoring guidelines, sample responses, and related materials — organized by course and year.

**7,483 files | 40 courses | 1998–2025**

> Source: [apfrqs.com](https://apfrqs.com) — publicly available College Board materials.  
> This repository is not affiliated with College Board or apfrqs.com.

---

## Courses Included

| Category | Courses |
|---|---|
| Math | Calculus AB, Calculus BC, Statistics, Precalculus |
| Science | Biology, Chemistry, Physics 1, Physics 2, Physics C Mechanics, Physics C E&M, Environmental Science |
| History | US History, World History Modern, European History, African American Studies |
| English | English Language & Composition, English Literature & Composition |
| Social Studies | Psychology, US Gov & Politics, Comparative Gov & Politics, Human Geography, Macroeconomics, Microeconomics |
| Languages | Spanish, Chinese, French, German, Italian, Japanese, Latin |
| Arts | 2-D Art & Design, 3-D Art & Design, Drawing, Music Theory, Art History |
| CS | Computer Science A, Computer Science Principles |
| Capstone | Seminar, Research |

---

## File Structure

```
files/
  AP Calculus BC/
    2025/
      Free-Response Questions.pdf
      Scoring Guidelines.pdf
      Sample Responses Q1.pdf
      ...
    2024/
      ...
  AP Biology/
    ...
```

---

## How to Download All Files

### Option 1 — Python (Mac/Windows/Linux)

```bash
git clone https://github.com/YOUR_USERNAME/ap-frqs.git
cd ap-frqs
python3 download.py
```

For faster parallel downloads:
```bash
python3 download.py --workers 4
```

### Option 2 — Bash (Mac/Linux)

```bash
git clone https://github.com/YOUR_USERNAME/ap-frqs.git
cd ap-frqs
bash download.sh
```

Both scripts are **resume-safe** — if interrupted, just re-run and they skip already-downloaded files.

---

## Auto-Sync via GitHub Actions

The included workflow (`.github/workflows/sync.yml`) runs automatically on the 1st of each month to catch newly released exam materials. You can also trigger it manually from the Actions tab.

To enable it:
1. Go to your repo → Settings → Actions → General
2. Set "Workflow permissions" to **Read and write**

---

## manifest.json

`manifest.json` contains the complete list of all 7,483 files with their source URLs. You can use it to build your own tooling, filter by course/year, or verify downloads.

```json
[
  {
    "course": "AP Calculus BC",
    "year": "2025",
    "name": "Free-Response Questions.pdf",
    "url": "https://..."
  },
  ...
]
```
