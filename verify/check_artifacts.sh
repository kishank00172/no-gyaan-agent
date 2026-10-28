#!/usr/bin/env bash
# check_artifacts.sh — "file sach me bani?" ka objective jawab (insaan ki nahi, script ki raye)
# Usage: bash verify/check_artifacts.sh /path/to/output [min_bytes]
set -u
DIR="${1:-.}"
MIN="${2:-1000}"
[ -d "$DIR" ] || { echo "ERROR: dir nahi mila: $DIR"; exit 2; }

# ffprobe/ffmpeg: PATH me na ho to kai jagah dhoondo (fresh sandbox me packages
# chale jate hain — isliye PATH par bharosa nahi karna)
FFPROBE=$(command -v ffprobe 2>/dev/null || true)
FFMPEG=$(command -v ffmpeg 2>/dev/null || true)
for cand in "$HOME/.bin/ffmpeg" "$HOME/bin/ffmpeg" "/usr/local/bin/ffmpeg" \
            "/usr/bin/ffmpeg" "/data/data/com.termux/files/usr/bin/ffmpeg"; do
  if [ -z "$FFMPEG" ] && [ -x "$cand" ]; then FFMPEG="$cand"; fi
done
if [ -z "$FFMPEG" ]; then
  FFMPEG=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())" 2>/dev/null || true)
fi
if [ -z "$FFPROBE" ] && [ -n "$FFMPEG" ]; then
  p="$(dirname "$FFMPEG")/ffprobe"; [ -x "$p" ] && FFPROBE="$p"
fi
if [ -n "$FFMPEG" ]; then export PATH="$(dirname "$FFMPEG"):$PATH"; fi
PROBE_OK=0; [ -n "$FFPROBE" ] || [ -n "$FFMPEG" ] && PROBE_OK=1

echo "=== ARTIFACT VERIFY: $DIR (min ${MIN} B) ==="
echo "  probe: ${FFPROBE:-ffprobe-missing} / ${FFMPEG:-ffmpeg-missing}"
found=0; bad=0; skipped=0
while IFS= read -r -d '' f; do
  case "$(basename "$f")" in
    .*|*.md|*.txt|*.sh|*.py|*.csv|*.json|*.m3u|*.log|*.nfo|*.url) skipped=$((skipped+1)); continue ;;
  esac
  found=$((found+1))
  sz=$(wc -c < "$f")
  sha=$(sha256sum "$f" | cut -c1-16)
  printf "  %-55s %10s B  sha=%s…" "$(basename "$f")" "$sz" "$sha"
  if [ "$sz" -lt "$MIN" ]; then echo "  ❌ TOO SMALL"; bad=$((bad+1)); continue; fi
  # audio/video: duration + codec probe (real proof, not just size)
  case "$f" in
    *.mp3|*.opus|*.m4a|*.webm|*.wav|*.flac|*.mp4|*.mkv)
      if [ -n "$FFPROBE" ]; then
        dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$f" 2>/dev/null | head -1)
        cod=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=nw=1:nk=1 "$f" 2>/dev/null | head -1)
        echo "  ✅ ${cod:-?} ${dur:-?}s"
      elif [ -n "$FFMPEG" ]; then
        line=$(ffmpeg -hide_banner -i "$f" 2>&1 | grep -m1 'Duration:' | sed 's/^ *//')
        echo "  ✅ ${line:-duration?}"
      else echo "  ✅ (size ok; koi probe tool nahi)"; fi ;;
    *) echo "  ✅ (size ok)" ;;
  esac
done < <(find "$DIR" -maxdepth 2 -type f -print0 2>/dev/null)

echo
echo "  artifacts=$found  skipped(sidecar)=$skipped  suspicious=$bad"
if [ "$found" -eq 0 ]; then echo "❌ KOI ARTIFACT NAHI MILA — agent ne 'ho gaya' bola par file nahi."; exit 1; fi
if [ "$bad" -gt 0 ]; then echo "❌ $bad file(s) suspicious (0-byte / chhoti)."; exit 1; fi
echo "✅ $found artifact(s) VERIFIED."
