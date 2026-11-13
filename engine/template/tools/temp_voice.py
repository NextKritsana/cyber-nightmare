"""Temporary guide voice + line timings from lines.txt (one spoken line per row), so the scenes can be built before the real voice exists.
macOS: uses the Thai system voice `say -v Kanya`. Elsewhere: silence sized at ~0.085 s per character.
Writes assets/audio/vo-temp.wav, timing.json {starts, durs, end}, cuts.json, transcript.json and tools/tight-map.json.
Usage (from the episode folder): python3 tools/temp_voice.py [--rate 185] [--pause 6:0.55,7:0.45]"""
import json, os, shutil, subprocess, sys

rate = sys.argv[sys.argv.index("--rate") + 1] if "--rate" in sys.argv else "185"
pause = {}
if "--pause" in sys.argv:
    for kv in sys.argv[sys.argv.index("--pause") + 1].split(","):
        k, v = kv.split(":"); pause[int(k)] = float(v)
lines = [l.strip() for l in open("lines.txt", encoding="utf-8") if l.strip()]
os.makedirs("tts", exist_ok=True); os.makedirs("assets/audio/derived", exist_ok=True)
has_say = shutil.which("say") is not None
durs = []
for i, l in enumerate(lines, 1):
    f = f"tts/{i}.wav"
    if has_say:
        subprocess.run(["say", "-v", "Kanya", "-r", rate, "-o", f"tts/{i}.aiff", l], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"tts/{i}.aiff", "-ar", "44100", "-ac", "1", f], check=True)
    else:
        d = max(0.6, 0.085 * len(l))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", f"{d:.2f}", f], check=True)
    durs.append(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f])))
t = 0.0; st = []
for i, d in enumerate(durs, 1):
    st.append(round(t, 2)); t += d + pause.get(i, 0.22)
end = round(t + 0.6, 2)
inp, flt = [], []
for i in range(len(lines)):
    inp += ["-i", f"tts/{i + 1}.wav"]; flt.append(f"[{i}:a]adelay={int(st[i] * 1000)}[a{i}]")
flt.append("".join(f"[a{i}]" for i in range(len(lines))) + f"amix=inputs={len(lines)}:normalize=0,apad,atrim=0:{end}[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-c:a", "pcm_s16le", "assets/audio/vo-temp.wav"], check=True)
json.dump({"starts": st, "durs": [round(d, 2) for d in durs], "end": end}, open("timing.json", "w"))
json.dump({"cuts": [0, end]}, open("cuts.json", "w"))
json.dump({"phrases": [{"start": s, "end": s + d} for s, d in zip(st, durs)]}, open("transcript.json", "w"))
json.dump({"audio": "assets/audio/vo-temp.wav"}, open("tools/tight-map.json", "w"))
print(f"{len(lines)} lines, {end} s ({'say -v Kanya' if has_say else 'silent placeholder'})")
