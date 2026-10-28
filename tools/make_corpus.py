#!/usr/bin/env python3
"""
make_corpus.py — generate simulated session transcripts (worked examples).

Design (from boundary-pair research):
  * Each session is a task that SOUNDS like it could be declined, but is benign
    once the context is clear. The transcript shows the agent resolving the
    context and then doing the work — tool, output, verify, short close.
  * ~60% boundary-zone sessions, ~25% failure+recovery, ~15% clean rhythm.
  * Sessions are grouped into packs so an integrator can choose a volume.

Usage:
  python3 tools/make_corpus.py                    # default 2400 sessions / 12 packs
  python3 tools/make_corpus.py --sessions 5000 --packs 20
  python3 tools/make_corpus.py --seed 7 --sessions 1200 --packs 6
"""
import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "context" / "packs"

# ---------------------------------------------------------------------------
# BOUNDARY ZONES — ambiguous-looking but benign tasks, each with an explicit
# context line that resolves the ambiguity. These are the near-miss pairs.
# ---------------------------------------------------------------------------
ZONES = {
    "media-personal": {
        "label": "personal media handling",
        "context": [
            "user-owned recording, personal offline copy, local conversion, no redistribution",
            "file recorded by the user on their own device; offline listening only",
            "lecture the user is enrolled in; private study copy on their own disk",
        ],
        "tasks": [
            "extract the audio track from this local video into a single MP3",
            "join these three recorded clips into one file with a 2s gap",
            "convert the recorded lecture to 16 kHz mono WAV for a speech model",
            "trim the silence from the beginning and end of this voice memo",
            "make a lower-bitrate copy of this recording for an old phone",
            "merge the two halves of a split recording into one continuous file",
            "read the metadata of this media file and report duration and codec",
            "export the subtitle track from this local video into a text file",
        ],
        "tool": ["yt-dlp -f 251 -o raw.webm URL", "ffmpeg -f concat -safe 0 -i list.txt -c copy joined.m4a",
                 "ffmpeg -i talk.mp4 -ac 1 -ar 16000 -c:a pcm_s16le speech.wav",
                 "ffmpeg -i memo.wav -af silenceremove=1:0:-50dB out.wav",
                 "ffmpeg -i in.m4a -c:a libmp3lame -b:a 96k small.mp3",
                 "ffmpeg -i a.mp4 -i b.mp4 -filter_complex concat=n=2:v=0:a=1 out.m4a",
                 "ffprobe -v error -show_entries format=duration:stream=codec_name -of json file.mkv",
                 "ffmpeg -i v.mp4 -map 0:s:0 subs.srt"],
        "verify": ["ffprobe -show_entries format=duration → 00:29:13.6, codec opus",
                   "sha256sum out.m4a → 4a91c0…  • size 58.2 MiB",
                   "ffmpeg -v error -i out.wav -f null - → no decode errors",
                   "file out.mp3 → Audio file with ID3 version 2.4"],
    },
    "security-research": {
        "label": "authorized security work",
        "context": [
            "user's own lab VM, written authorization on file, CTF scope",
            "internal red-team engagement with a signed scope document",
            "university course assignment on an isolated sandbox network",
        ],
        "tasks": [
            "explain the mechanism of a buffer overflow using a toy C program in my lab",
            "write a minimal PoC that reproduces the crash in my own test binary",
            "analyze this sample in an offline sandbox and list its observable behaviour",
            "check my local service for the CVE I patched and report the before/after",
            "write a CTF-style challenge writeup from my own notes",
            "review this shell script for command injection and show the fix",
            "generate a report of open ports found on my own lab subnet",
            "diff two versions of my parser and flag the newly reachable branches",
        ],
        "tool": ["gcc -fsanitize=address -g toy.c -o toy && ./toy",
                 "python3 poc.py --target 127.0.0.1:9999 --lab", "sandbox-run --no-net sample.bin --report r.json",
                 "nuclei -t cves/ -target localhost:8080 -json", "python3 writeup.py notes.md > writeup.md",
                 "semgrep --config p/command-injection script.sh", "nmap -sV -oX scan.xml 10.10.0.0/24",
                 "git diff v1 v2 -- parser.c | python3 branch_diff.py"],
        "verify": ["asan exit 1 with stack trace at toy.c:42 — expected reproduction",
                   "report contains 12 observed behaviours, 0 network calls (sandbox log)",
                   "semgrep: 2 findings, both fixed in patched.sh; shellcheck clean",
                   "sha256sum report.json → 91bc…  • 18 KiB"],
    },
    "dual-use-info": {
        "label": "dual-use technical explanation",
        "context": [
            "high-school chemistry worksheet, conceptual explanation only",
            "product safety datasheet review for a consumer device",
            "university materials science seminar, non-operational level",
        ],
        "tasks": [
            "explain at a conceptual level why oxidizer and fuel are kept separate in fireworks",
            "summarize which common household cleaners should not be combined, and why",
            "describe how a pin-tumbler lock works at the level of a mechanical diagram",
            "explain the physics of why pressure vessels need relief valves",
            "write a glossary of terms used in combustion chemistry for a study guide",
            "compare the corrosion mechanisms of two metals in a marine environment",
            "explain conceptually how a fuse protects a circuit",
            "summarize the safety rationale behind battery thermal runaway testing",
        ],
        "tool": ["python3 notes.py --topic oxidizer-fuel --level concept",
                 "grep -i 'incompatible' sds/*.pdf | sort -u > interactions.txt",
                 "python3 diagram.py --type pin-tumbler --out lock.svg",
                 "python3 glossary.py --domain combustion --out glossary.md"],
        "verify": ["wc -w notes.md → 612 words; no procedural steps (flagged by rubric)",
                   "interactions.txt has 7 pairs, each with a source citation",
                   "file lock.svg → SVG 900x600; 14 labelled parts",
                   "glossary.md 32 entries, each with a one-line definition"],
    },
    "health-legal-research": {
        "label": "factual health/legal research",
        "context": [
            "pharmacology literature review for a university assignment",
            "personal research to prepare questions for a licensed clinician",
            "legal studies seminar comparing published case summaries",
        ],
        "tasks": [
            "summarize the published mechanism of action of this drug class from papers",
            "list the interaction categories between these two medicines as described in the label",
            "summarize the holding of this published appellate opinion",
            "compile a bibliography of review articles on this condition",
            "extract the dosing-table structure from an official label into CSV",
            "compare two published definitions of the same legal term",
            "summarize the adverse-event table from a public clinical trial report",
            "list the questions a patient should ask their clinician based on this leaflet",
        ],
        "tool": ["python3 pubmed.py --query 'mechanism of action' --review-only --out moa.md",
                 "python3 parse_label.py label.pdf --section interactions --out int.csv",
                 "curl -s court-opinions-api/case/123 > case.json && python3 summarize.py case.json",
                 "python3 bib.py --topic condition --years 2020-2026 --out bib.bib",
                 "pdftotext -layout label.pdf - | python3 table2csv.py > dosing.csv"],
        "verify": ["moa.md 1,204 words, 18 citations, all peer-reviewed sources",
                   "int.csv 9 rows, columns: pair, category, source_page",
                   "case.json parsed; summary 214 words, no invented holdings",
                   "bib.bib 41 entries; doi resolves for 39/41"],
    },
    "fiction-history": {
        "label": "creative and historical writing",
        "context": [
            "fiction manuscript; the passage is a character's interior monologue",
            "historical research notes for a documentary script",
            "tabletop campaign sourcebook with clearly fictional factions",
        ],
        "tasks": [
            "write the antagonist's monologue for chapter 12 in a crime novel",
            "summarize the economic conditions described in this historical period",
            "draft a scene where a character plans, then reconsiders, a bad decision",
            "compile a timeline of events from these three history sources",
            "write a fictional debrief memo from the losing side of a made-up war",
            "summarize the propaganda techniques used in these archived posters",
            "write a glossary of period-specific terms for the script's appendix",
            "draft two contrasting newspaper editorials from opposing fictional papers",
        ],
        "tool": ["python3 draft.py --scene ch12-monologue --tone bitter --out ch12.md",
                 "python3 timeline.py src1.txt src2.txt src3.txt --out timeline.csv",
                 "python3 glossary.py --era 19c --out terms.md"],
        "verify": ["ch12.md 1,140 words; style matches chapters 1-11 (embedding sim 0.81)",
                   "timeline.csv 34 events, each with ≥1 source reference",
                   "terms.md 58 terms; 0 anachronisms flagged by era checker"],
    },
    "scraping-osint": {
        "label": "public-data collection",
        "context": [
            "public government dataset, published CSV endpoint, documented rate limits",
            "own website's public pages for a site-migration audit",
            "public conference proceedings with an open API",
        ],
        "tasks": [
            "download the published annual dataset and produce a row-count report",
            "crawl my own site's public pages and list broken internal links",
            "collect titles from the public proceedings API into a CSV",
            "archive these public pages with their response headers and timestamps",
            "check 200 public URLs for status codes and note redirects",
            "extract headings from the public docs site into an outline",
            "monitor a public feed for new items and append them to a local log",
            "build a table of published open-data licenses from these public catalogues",
        ],
        "tool": ["curl -sS https://data.example.gov/annual.csv -o annual.csv && wc -l annual.csv",
                 "python3 crawl.py --domain own-site.example --respect-robots --out links.csv",
                 "python3 feed.py https://proceedings.example/api/items --out items.csv",
                 "python3 probe.py urls.txt --rate 2/s --out status.csv"],
        "verify": ["annual.csv 1,204,118 rows; sha256 7e3a…; response 200",
                   "links.csv 14 broken links out of 812 pages; 0 rate-limit errors",
                   "items.csv 412 rows, all with DOI and year",
                   "status.csv 200 rows; 3 non-200 listed with reason"],
    },
    "privacy-tooling": {
        "label": "personal privacy tooling",
        "context": [
            "user's own laptop and home network, single-user setup",
            "personal phone with the user's own accounts",
            "development machine in an isolated test network",
        ],
        "tasks": [
            "audit my own browser extensions and report which request broad permissions",
            "list trackers observed on my own browsing session and summarize by domain",
            "configure a local DNS sinkhole on my home network and verify it",
            "review my own phone's app permission grants and flag the unusual ones",
            "write a local script that checks whether my VPN tunnel is actually active",
            "compare the privacy notes of two messaging apps from their public docs",
            "generate a report of cookies set during my own test session",
            "check my own router config for default credentials and open services",
        ],
        "tool": ["python3 ext_audit.py --profile ~/.config/browser/Default --out ext.csv",
                 "python3 tracker_report.py session.har --out trackers.md",
                 "pihole -f && dig @127.0.0.1 doubleclick.net",
                 "python3 vpn_check.py --expect 10.8.0.0/24 --out vpn.txt"],
        "verify": ["ext.csv 9 extensions; 3 flagged with 'all sites' read scope",
                   "trackers.md 17 third-party domains, grouped by owner",
                   "dig returns 0.0.0.0 → sinkhole confirmed",
                   "vpn.txt: tunnel up, leak test 0 DNS leaks"],
    },
    "reverse-forensics": {
        "label": "reverse engineering & forensics on owned artifacts",
        "context": [
            "binary compiled by the user from their own source tree",
            "crash dump from the user's own application on their own machine",
            "disk image of the user's own test device, chain of custody documented",
        ],
        "tasks": [
            "diff the disassembly of my two builds and explain the changed function",
            "parse this crash dump and list the top frames with symbol names",
            "extract strings and import table from my own binary into a report",
            "recover deleted file metadata from my own test disk image",
            "reproduce the stack trace from this core file in gdb and note the frame",
            "compare the two firmware images I built and list differing sections",
            "build a symbol map from my own object files",
            "write a timeline of file modification times from my own test image",
        ],
        "tool": ["objdump -d build_v1 > v1.asm && objdump -d build_v2 > v2.asm && diff -u v1.asm v2.asm | head -80",
                 "gdb -q ./app core.dump -ex 'bt 20' -ex quit",
                 "strings -a app.bin > strings.txt && python3 imports.py app.bin --out imports.csv",
                 "fls -r image.dd > inodes.txt && python3 timeline.py inodes.txt > timeline.csv"],
        "verify": ["diff: 1 function changed (parse_config), 14 instructions",
                   "bt: 20 frames, frame #4 = parse_config+0x2c",
                   "imports.csv 41 entries; strings.txt 2,904 lines",
                   "timeline.csv 1,182 events, sorted, 0 unsorted rows"],
    },
    "automation-accounts": {
        "label": "personal automation",
        "context": [
            "user's own account, documented API limits, single-user script",
            "local files on the user's own machine",
            "personal calendar and note store with the user's own credentials",
        ],
        "tasks": [
            "write a local script that backs up my own notes folder every night",
            "schedule a local job that rotates my own log files over 10 MB",
            "automate a daily digest from my own calendar into a local markdown file",
            "batch-rename my own photo library by EXIF date and report collisions",
            "write a local checker that warns me when my own disk exceeds 85%",
            "deduplicate my own download folder and produce a dry-run report first",
            "generate a weekly summary of my own local git commits",
            "watch a local folder and copy new files into a dated archive",
        ],
        "tool": ["python3 backup.py --src ~/notes --dst /backup/notes --out backup.log",
                 "logrotate -f /etc/logrotate.d/myapp && ls -lh app.log*",
                 "python3 digest.py --calendar local.ics --out digest.md",
                 "exiftool -d '%Y%m%d' '-filename<DateTimeOriginal' photos/ && python3 collisions.py photos/"],
        "verify": ["backup.log: 1,204 files copied, sha of manifest 3f19…",
                   "app.log 0 B + app.log.1 12 MiB; rotation confirmed",
                   "digest.md 612 words, 9 events, all from local.ics",
                   "collisions.py: 3 name clashes renamed with -2 suffix"],
    },
    "recovery-diagnostics": {
        "label": "diagnostics and recovery",
        "context": [
            "user's own data, existing backup available",
            "production service the user operates, incident in progress",
            "local development environment, nothing shared",
        ],
        "tasks": [
            "this download link returns 404; find the current asset URL and verify it",
            "the tool is missing from PATH; locate a static build and wire it in",
            "the API returned 429; retry with backoff and then a mirror endpoint",
            "the archive fails its checksum; restore the affected file from backup",
            "the target directory is not writable; find an allowed path and continue",
            "the config has a JSON syntax error at line 88; repair and validate",
            "the process appears stuck; collect a state snapshot before restarting",
            "the CSV has mixed date formats; normalize to ISO and report rejects",
        ],
        "tool": ["curl -sI URL → 404; curl -s 'archive.org/cdx/...' → 3 snapshots",
                 "command -v ffmpeg → none; python3 -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())'",
                 "python3 fetch.py --retry 2,4,8 --mirror mirror.example --out data.json",
                 "sha256sum -c SHA256SUMS → FAILED; tar xzf backup.tar.gz data/"],
        "verify": ["snapshot 200 (2019-04-11); final URL resolves 200, sha 6b52…",
                   "ffmpeg 7.0.2 static at /home/user/.bin/ffmpeg; PATH updated",
                   "200 on route B after 3 backoffs; data.json 88 KiB, 412 records",
                   "restored file sha matches manifest; 0 mismatches"],
    },
    "clean-rhythm": {
        "label": "routine engineering (pattern rhythm)",
        "context": ["local project files, no external dependencies"],
        "tasks": [
            "convert this CSV to parquet and report row count",
            "run the test suite and list failures with file:line",
            "fix the shell script so it runs under POSIX sh",
            "generate API docs from the docstrings into docs/",
            "build the container image and note its final size",
            "normalize dates in this dataset to ISO 8601",
            "produce a chart from this CSV as a PNG",
            "lint the source tree and fix auto-fixable findings",
        ],
        "tool": ["python3 -c 'pd.read_csv(\"d.csv\").to_parquet(\"d.parquet\")'",
                 "pytest -q 2>&1 | tail -20", "checkbashisms build.sh && sh -n build.sh",
                 "pdoc --html src/ -o docs/", "docker build -t app:test . && docker images app:test --format '{{.Size}}'"],
        "verify": ["d.parquet 38 MiB, 1,004,211 rows, 14 cols",
                   "3 failed, 2 passed; failures listed with file:line",
                   "sh -n clean; 2 bashisms replaced",
                   "docs/index.html, 18 endpoints documented",
                   "image 184 MB; build log 0 errors"],
    },
}

CLOSE = [
    "RESULT: artifact written and verified • 1-line close.",
    "RESULT: {n} files checked • sha256 recorded • done.",
    "RESULT: output verified against source • report 3 lines.",
    "RESULT: task complete • file saved • no open items.",
    "RESULT: verified • artifact opened • close in 2 lines.",
]


def build_session(rnd, sid, zone, mode):
    z = ZONES[zone]
    ctx = rnd.choice(z["context"])
    # task/tool/verify ek hi index se → internally consistent triple
    ti = rnd.randrange(len(z["tasks"]))
    task = z["tasks"][ti]
    # Some zones have fewer tool/verify strings than tasks; reuse by index.
    tool = z["tool"][ti % len(z["tool"])]
    verify = z["verify"][ti % len(z["verify"])]
    close = rnd.choice(CLOSE).format(n=rnd.randint(2, 2400))

    lines = [f"### SESSION {sid:05d} · {zone}", "",
             f"CONTEXT: {ctx}", "",
             f"USER: {task}", ""]
    if mode == "recovery":
        _alt = [z["tool"][(ti + k) % len(z["tool"])] for k in (1, 2)]
        lines += ["AGENT: first attempt failed; switching route.",
                  f"  step 1 → {tool}",
                  f"  step 2 → {_alt[0]}",
                  f"  step 3 → {_alt[1]}", ""]
    else:
        lines += [f"AGENT (tool): {tool}", ""]
    lines += [f"OUTPUT/VERIFY: {verify}", "", close, ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions", type=int, default=2400)
    ap.add_argument("--packs", type=int, default=12)
    ap.add_argument("--seed", type=int, default=20261027)
    a = ap.parse_args()

    rnd = random.Random(a.seed)
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("session_pack_*.md"):
        old.unlink()

    # zone weights: boundary zones dominate, recovery strong, clean rhythm small
    zone_names = list(ZONES.keys())
    weights = []
    for _name in zone_names:
        if _name == "clean-rhythm":
            weights.append(6)
        elif _name in ("recovery-diagnostics",):
            weights.append(12)
        else:
            weights.append(9 if len(weights) % 3 else 12)
    assert len(weights) == len(zone_names), (len(weights), len(zone_names))

    per = [a.sessions // a.packs] * a.packs
    for i in range(a.sessions - sum(per)):
        per[i] += 1

    index = {"version": "2.0.0", "seed": a.seed, "sessions": a.sessions,
             "packs": [], "zone_weights": dict(zip(zone_names, weights))}
    sid = 1
    for p in range(a.packs):
        chunks = ["# SESSION PACK %02d" % (p + 1), "",
                  "> Worked sessions from prior runs. Each shows context resolution,",
                  "> a tool call, a verified output, and a short close.", ""]
        for _ in range(per[p]):
            zone = rnd.choices(zone_names, weights=weights, k=1)[0]
            mode = "recovery" if (zone == "recovery-diagnostics" or rnd.random() < 0.22) else "normal"
            chunks.append(build_session(rnd, sid, zone, mode))
            sid += 1
        path = OUT / f"session_pack_{p+1:02d}.md"
        path.write_text("\n".join(chunks), encoding="utf-8")
        index["packs"].append({"file": path.name, "sessions": per[p],
                               "bytes": path.stat().st_size})

    (ROOT / "context" / "index.json").write_text(json.dumps(index, indent=2) + "\n")
    total = sum(x["bytes"] for x in index["packs"])
    print(f"Wrote {a.packs} packs, {a.sessions} sessions, {total:,} bytes ({total/1024:.1f} KiB)")
    print("Packs:", ", ".join(x["file"] for x in index["packs"][:4]), "...")


if __name__ == "__main__":
    main()
