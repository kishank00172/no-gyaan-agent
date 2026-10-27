#!/usr/bin/env python3
"""
find_broken_id.py — jab YouTube link "Video unavailable" bole.

Do tricks:
  --brute      : 1-character typo variants (substitution/insert/delete/swap) ko
                 thumbnail CDN par parallel check karo (~1400 IDs, ~2 sec).
  --channel    : channel ki saari videos enumerate karo, aur har ID ka
                 Levenshtein edit-distance dead ID se nikaalo. Phir oembed se
                 top candidates verify karo. Yahi trick se C9MAl9NGLsk →
                 C9mAI9NGLsk mila tha.

Usage:
  python3 find_broken_id.py --dead-id C9MAl9NGLsk --brute
  python3 find_broken_id.py --dead-id C9MAl9NGLsk \
      --channel "https://www.youtube.com/@MaheshArya/videos" --verify
  python3 find_broken_id.py --dead-id C9MAl9NGLsk --list-file channel.txt --top 5

Dependencies: python3 stdlib + yt-dlp (sirf --channel ke liye).
"""
import argparse
import concurrent.futures as cf
import json
import subprocess
import sys
import urllib.parse
import urllib.request

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"


def levenshtein(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def variants(vid):
    out = set()
    for i in range(len(vid)):
        for c in CHARSET:
            if c != vid[i]:
                out.add(vid[:i] + c + vid[i + 1:])          # substitution
            out.add(vid[:i] + c + vid[i:])                    # insertion
        out.add(vid[:i] + vid[i + 1:])                        # deletion
        if i < len(vid) - 1:
            out.add(vid[:i] + vid[i + 1] + vid[i] + vid[i + 2:])  # swap
    out.discard(vid)
    return sorted(out)


def oembed(vid):
    url = ("https://www.youtube.com/oembed?url="
           + urllib.parse.quote("https://www.youtube.com/watch?v=" + vid, safe="")
           + "&format=json")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            d = json.load(r)
            return d.get("title"), d.get("author_name")
    except Exception:
        return None


def thumb_exists(vid):
    try:
        req = urllib.request.Request(
            "https://img.youtube.com/vi/" + vid + "/default.jpg",
            method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return vid if r.status == 200 else None
    except Exception:
        return None


def channel_videos(channel):
    cmd = ["yt-dlp", "--no-warnings", "--flat-playlist", "--print",
           "%(id)s|%(title)s", channel]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    rows = []
    for line in p.stdout.splitlines():
        if "|" in line:
            vid, title = line.split("|", 1)
            vid = vid.strip()
            if len(vid) == 11:
                rows.append((vid, title.strip()))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dead-id", required=True, help="11-char ID jo kaam nahi kar raha")
    ap.add_argument("--brute", action="store_true", help="1-char typo variants check karo")
    ap.add_argument("--channel", help="channel /videos URL (yt-dlp flat playlist)")
    ap.add_argument("--list-file", help="offline file: har line 'id|title'")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--verify", action="store_true", help="top candidates oembed se validate karo")
    a = ap.parse_args()

    dead = a.dead_id.strip()
    print(f"dead ID      : {dead}  (len={len(dead)})")
    print(f"direct check : {oembed(dead) or 'UNAVAILABLE (oembed 404)'}")

    if a.brute:
        cands = variants(dead)
        print(f"\n[brute] {len(cands)} variants check kar raha hoon...")
        hits = []
        with cf.ThreadPoolExecutor(max_workers=40) as ex:
            for r in ex.map(thumb_exists, cands):
                if r:
                    hits.append(r)
        print("[brute] hits:", hits or "koi nahi — galati 1 character se zyada ki hai")

    rows = []
    if a.list_file:
        with open(a.list_file, encoding="utf-8", errors="replace") as f:
            for line in f:
                if "|" in line:
                    vid, title = line.split("|", 1)
                    if len(vid.strip()) == 11:
                        rows.append((vid.strip(), title.strip()))
    elif a.channel:
        print(f"\n[channel] enumerating {a.channel} ...")
        rows = channel_videos(a.channel)
    if rows:
        print(f"[channel] {len(rows)} videos mile\n")
        ranked = sorted(((levenshtein(dead, v), v, t) for v, t in rows))[:a.top]
        print(f"{'dist':>4}  {'id':<12} title")
        for d, v, t in ranked:
            extra = ""
            if a.verify:
                info = oembed(v)
                extra = f"   [oembed: {info[0]}]" if info else "   [oembed: FAIL]"
            print(f"{d:>4}  {v:<12} {t[:80]}{extra}")
        best = ranked[0][1]
        print(f"\nBEST GUESS: https://youtu.be/{best}")
        print(f"oembed      : {oembed(best) or 'nope'}")


if __name__ == "__main__":
    sys.exit(main())
