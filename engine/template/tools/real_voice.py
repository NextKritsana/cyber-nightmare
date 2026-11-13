"""Line timings from the REAL voice-over.
1) Speed up + tighten pauses:  ffmpeg -i moon.mp3 -af atempo=1.2 -ar 44100 -ac 1 assets/audio/vo-raw.wav
                               python3 tools/tighten.py assets/audio/vo-raw.wav assets/audio/vo-tight.wav --gap 0.12 --long 0.24 > phrases.txt
   tighten prints the phrases (n, start - end). Listen / ASR them and decide which phrases make each script line.
2) Run:  python3 tools/real_voice.py assets/audio/vo-tight.wav "1-3,4-5,6,7,8-9,..." [--insert 3:voice/other.wav] [--pause 7:0.3:0.5]
   - groups: for every line in lines.txt, the tighten phrase numbers it spans (same order as lines.txt).
     A line spoken by ANOTHER voice (e.g. mom) is written as "x" in the group list and given with --insert AFTER_LINE:file.
   - --pause LINE:BEFORE:AFTER adds silence around one line (the "อย่าเพิ่ง!" beat).
Writes assets/audio/vo-final.wav, timing.json, cuts.json, transcript.json, tools/tight-map.json."""
import json, re, subprocess, sys

src, spec = sys.argv[1], sys.argv[2]
args = sys.argv[3:]
inserts = {int(a.split(":")[0]): a.split(":", 1)[1] for a in [args[i + 1] for i, x in enumerate(args) if x == "--insert"]}
pauses = {int(p.split(":")[0]): (float(p.split(":")[1]), float(p.split(":")[2])) for p in [args[i + 1] for i, x in enumerate(args) if x == "--pause"]}
out = open("phrases.txt", encoding="utf-8").read()   # tighten.py's printout for this file
PH = [(float(a), float(b)) for a, b in re.findall(r"^\s+\d+\s+([\d.]+)\s+-\s+([\d.]+)", out, re.M)]
if not PH: raise SystemExit("could not read phrases: save tighten.py output to phrases.txt (step 1)")
groups = spec.split(",")
def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
pieces, st, du, t = [], [], [], 0.0      # pieces: (file, a, b) or ("sil", d)
line = 0; cur_src_end = 0.0
for g in groups:
    line += 1
    if g == "x":                          # another voice, inserted whole
        f = inserts[line - 1] if (line - 1) in inserts else inserts[line]
        pieces.append(("sil", 0.25)); t += 0.25
        d = dur(f); pieces.append((f, 0, d)); st.append(round(t, 2)); du.append(round(d, 2)); t += d
        pieces.append(("sil", 0.3)); t += 0.3; continue
    a, b = (map(int, g.split("-")) if "-" in g else (int(g), int(g)))
    s, e = PH[a - 1][0], PH[b - 1][1]
    if line in pauses: pieces.append(("sil", pauses[line][0])); t += pauses[line][0]
    s0 = max(cur_src_end, s - 0.06); e0 = e + 0.06
    gap = s0 - cur_src_end if cur_src_end else 0
    if gap > 0: pieces.append((src, cur_src_end, s0)); t += gap
    pieces.append((src, s0, e0)); st.append(round(t + (s - s0), 2)); du.append(round(e - s, 2)); t += e0 - s0; cur_src_end = e0
    if line in pauses: pieces.append(("sil", pauses[line][1])); t += pauses[line][1]
inp, flt, lab = [], [], []
for i, p in enumerate(pieces):
    if p[0] == "sil": flt.append(f"anullsrc=r=44100:cl=mono,atrim=0:{p[1]}[p{i}]")
    else:
        inp += ["-i", p[0]]; k = len(inp) // 2 - 1
        flt.append(f"[{k}:a]aformat=sample_rates=44100:channel_layouts=mono,atrim={p[1]:.3f}:{p[2]:.3f},asetpts=N/SR/TB[p{i}]")
    lab.append(f"[p{i}]")
flt.append("".join(lab) + f"concat=n={len(pieces)}:v=0:a=1[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-c:a", "pcm_s16le", "assets/audio/vo-final.wav"], check=True)
end = round(dur("assets/audio/vo-final.wav") + 0.7, 2)
json.dump({"starts": st, "durs": du, "end": end}, open("timing.json", "w"))
json.dump({"cuts": [0, end]}, open("cuts.json", "w"))
json.dump({"phrases": [{"start": s, "end": s + d} for s, d in zip(st, du)]}, open("transcript.json", "w"))
json.dump({"audio": "assets/audio/vo-final.wav"}, open("tools/tight-map.json", "w"))
print(f"{len(st)} lines, {end} s -> timing.json (check every start against the audio before building)")
