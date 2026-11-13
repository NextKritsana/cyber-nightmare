"""Cut a complete short clip (<= 30 s) out of the rendered full clip by picking whole scenes, so the story ends instead of
stopping on a cliffhanger: hook -> proof -> bigger proof -> the reveal, skipping the scenes in between.

  python3 tools/short_cut.py "renders/EP<n> <title>.mp4" 1-3,5-7 ["renders/EP<n> สตอรี่ hook <title>.mp4"]

- Scenes are numbered as in cuts.json (scene n runs from cuts[n-1] to cuts[n]); give runs like 1-3,5-7.
- Each run keeps whole phrases: the sound starts 0.05 s before the run's first cut and stops 0.08 s after the last phrase
  inside the run. The picture skips the transitions (it starts 0.17 s after the first cut, freezing that frame for the
  first moment, and stops 0.2 s before the run's last cut), so no half-transition shows at a join.
- Joins are hard cuts with a 40 ms sound crossfade; the last frame holds for HOLD seconds while the sound fades out.
- Also writes the "-small" copy at 3 Mbps. Prints the length; aim for 25-30 s.
"""
import json, os, subprocess, sys

HOLD = 1.0
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, spec = sys.argv[1], sys.argv[2]
out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(src), os.path.basename(src).replace(" ", " สตอรี่ hook ", 1))
ph = json.load(open(os.path.join(R, "transcript.json"), encoding="utf-8"))["phrases"]
C = json.load(open(os.path.join(R, "cuts.json")))["cuts"]
runs = [tuple(map(int, r.split("-"))) if "-" in r else (int(r), int(r)) for r in spec.split(",")]

f, vl, al, total = "", [], [], 0.0
for i, (a, b) in enumerate(runs):
    s, e = C[a - 1], C[b]
    last = max(p["end"] for p in ph if s - 0.05 <= p["start"] < e - 0.05)
    a0, a1 = max(0.0, s - 0.05), last + 0.08
    v0, v1 = (0.0 if a == 1 else s + 0.17), min(e - 0.2, a1)
    lead = v0 - a0
    tail = (a1 - a0) - lead - (v1 - v0) + (HOLD if i == len(runs) - 1 else 0)
    f += (f"[0:v]trim={v0:.3f}:{v1:.3f},setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration={lead:.3f}"
          f":stop_mode=clone:stop_duration={max(tail, 0):.3f}[v{i}];")
    dur = (a1 - a0) + (HOLD if i == len(runs) - 1 else 0)
    f += f"[0:a]atrim={a0:.3f}:{a1:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={a1 - a0 - 0.06:.3f}:d=0.06,apad=whole_dur={dur:.3f}[a{i}];"
    vl.append(f"[v{i}]"); al.append(f"[a{i}]"); total += dur
n = len(runs)
f += "".join(v + a for v, a in zip(vl, al)) + f"concat=n={n}:v=1:a=1[v][a]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", f, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", out], check=True)
small = out[:-4] + "-small.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-c:v", "libx264", "-b:v", "3M", "-c:a", "copy", small], check=True)
print(f"{out}  {total:.1f} s  (scenes {spec})")
print(small)
