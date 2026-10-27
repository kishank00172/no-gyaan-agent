#!/usr/bin/env bash
# yt_audio.sh — YouTube URL(s) → best-quality audio, no babysitting.
# Works on Termux (Android) and Linux. Output: .opus (zero re-encode), .mp3, ALL_combined.mp3
#
#   bash yt_audio.sh "https://youtu.be/ID1" "https://youtu.be/ID2"
#   YT_AUDIO_OUT=/sdcard/Download/mynight bash yt_audio.sh URL1 URL2
#   bash yt_audio.sh --check
#
set -u

if [ "${1:-}" = "--check" ]; then
  echo "yt-dlp : $(command -v yt-dlp || echo missing)"
  echo "ffmpeg : $(command -v ffmpeg || echo missing)"
  echo "python : $(command -v python3 || echo missing)"
  echo "net    : $(curl -sS -m 8 -o /dev/null -w '%{http_code}' https://www.youtube.com/ 2>/dev/null || echo no-net)"
  exit 0
fi

[ "$#" -ge 1 ] || { echo "Usage: bash tools/yt_audio.sh URL [URL...]"; exit 1; }

# ---- output dir (Termux: /sdcard/Download — no setup-storage needed if already visible)
OUT="${YT_AUDIO_OUT:-}"
if [ -z "$OUT" ]; then
  if [ -d /sdcard/Download ] && [ -w /sdcard/Download ]; then OUT=/sdcard/Download/yt-audio
  else OUT="$HOME/yt-audio"; fi
fi
mkdir -p "$OUT/tmp" || { echo "cannot create $OUT"; exit 1; }

# ---- tool auto-install (reversible, no sudo)
ensure_ytdlp() {
  command -v yt-dlp >/dev/null 2>&1 && return 0
  python3 -m pip install --user -q yt-dlp 2>/dev/null || python3 -m pip install -q yt-dlp 2>/dev/null
  export PATH="$HOME/.local/bin:$PATH"
  command -v yt-dlp >/dev/null 2>&1
}
ensure_ffmpeg() {
  FFMPEG=$(command -v ffmpeg 2>/dev/null || true)
  [ -n "$FFMPEG" ] && return 0
  if command -v pkg >/dev/null 2>&1; then pkg install -y ffmpeg >/dev/null 2>&1; FFMPEG=$(command -v ffmpeg 2>/dev/null || true); fi
  [ -n "$FFMPEG" ] && return 0
  python3 -m pip install --user -q imageio-ffmpeg 2>/dev/null || python3 -m pip install -q imageio-ffmpeg 2>/dev/null
  FFMPEG=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())" 2>/dev/null || true)
  [ -n "$FFMPEG" ]
}
ensure_ytdlp || { echo "ERROR: yt-dlp install nahi hua"; exit 1; }
ensure_ffmpeg || { echo "ERROR: ffmpeg nahi mila"; exit 1; }
echo "tools OK: $(command -v yt-dlp) | $FFMPEG"
echo "output  : $OUT"

rm -f "$OUT/tmp/list.txt" "$OUT/tmp/concat.txt"
i=0; ok=0
for URL in "$@"; do
  i=$((i+1))
  echo "--- [$i] $URL"
  TITLE=$(yt-dlp --skip-download --no-warnings --print "%(title)s" "$URL" 2>/dev/null | head -1)
  if [ -z "$TITLE" ]; then echo "    SKIP: video unavailable / galat ID"; continue; fi
  yt-dlp -f "251/250/140/249/139/bestaudio" --no-part --no-warnings \
         -o "$OUT/tmp/raw_$i.%(ext)s" "$URL" || { echo "    download FAILED"; continue; }
  SRC=$(ls -1 "$OUT/tmp/raw_$i".* 2>/dev/null | head -1)
  [ -n "$SRC" ] || { echo "    source file missing"; continue; }
  SAFE=$(printf '%s' "$TITLE" | tr -c 'A-Za-z0-9 _-' '_' | cut -c1-60)
  BASE=$(printf '%02d_%s' "$i" "$SAFE")
  # .opus = original stream, no re-encode (best quality)
  "$FFMPEG" -hide_banner -loglevel error -y -i "$SRC" -c:a copy "$OUT/$BASE.opus" \
    || echo "    opus remux FAILED"
  # .mp3 = universal compatibility
  "$FFMPEG" -hide_banner -loglevel error -y -i "$SRC" -vn -c:a libmp3lame -q:a 2 \
    "$OUT/$BASE.mp3" || echo "    mp3 FAILED"
  echo "$OUT/$BASE.mp3" >> "$OUT/tmp/list.txt"
  ok=$((ok+1))
  echo "    OK -> $BASE.opus / .mp3"
done

# ---- one continuous file (2s gap between tracks) — for sleep/headphones
if [ "$ok" -ge 2 ] && [ -f "$OUT/tmp/list.txt" ]; then
  "$FFMPEG" -hide_banner -loglevel error -y -f lavfi -i "anullsrc=r=48000:cl=stereo:d=2" \
    -c:a libmp3lame -b:a 128k "$OUT/tmp/gap.mp3"
  first=1
  while IFS= read -r f; do
    [ "$first" -eq 1 ] || echo "file '$OUT/tmp/gap.mp3'" >> "$OUT/tmp/concat.txt"
    echo "file '$f'" >> "$OUT/tmp/concat.txt"
    first=0
  done < "$OUT/tmp/list.txt"
  "$FFMPEG" -hide_banner -loglevel error -y -f concat -safe 0 -i "$OUT/tmp/concat.txt" \
    -c copy "$OUT/ALL_combined.mp3" && echo "combined -> $OUT/ALL_combined.mp3"
fi

rm -rf "$OUT/tmp"
echo "DONE: $ok file(s) in $OUT"
