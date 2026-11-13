"""Start a new Cyber Nightmare episode folder from the template.
Usage: python3 engine/new_episode.py <dir>             -> empty episode (copy of the EP1 engine; rewrite the scenes in gen.py)
       python3 engine/new_episode.py <dir> --example   -> EP1 "แม่โทรมาร้องไห้ขอเงิน" ready to build with a temp voice"""
import os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]
if os.path.exists(out) and os.listdir(out): raise SystemExit(f"{out} is not empty")
shutil.copytree(os.path.join(HERE, "template"), out, dirs_exist_ok=True)
open(os.path.join(out, "package.json"), "w").write('{"name": "cyber-nightmare-episode", "private": true}\n')
if "--example" in sys.argv:
    for f in os.listdir(os.path.join(HERE, "example-ep01")):
        shutil.copy(os.path.join(HERE, "example-ep01", f), os.path.join(out, f))
print("new episode ->", out)
