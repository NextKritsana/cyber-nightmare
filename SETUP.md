# Setup (for the AI to run)

The user opened this folder in Claude Code and typed something like "อ่าน SETUP.md แล้วติดตั้งให้หน่อย". Do the whole setup for them, one step at a time, in their language, without jargon. Before each step, check whether it already works and skip it if so.

1. **Package manager.** Homebrew on Mac; winget on Windows.
2. **Tools.** Run `brew install node git ffmpeg python` (Windows: winget Node.js, Git, FFmpeg, Python).
3. **HyperFrames.** Run:
   - `claude plugin marketplace add https://github.com/heygen-com/hyperframes.git`
   - `claude plugin install hyperframes@hyperframes`
   - `npx hyperframes doctor`
   - `npx hyperframes browser ensure`
4. **Python environment.** Run `python3 -m venv ~/.venvs/ai-lab && ~/.venvs/ai-lab/bin/pip install numpy pillow scipy sherpa-onnx`. From now on, `PY=~/.venvs/ai-lab/bin/python`.
5. **Thai word timing.** Download `sherpa-onnx-zipformer-thai-2024-06-20.tar.bz2` from https://github.com/k2-fsa/sherpa-onnx/releases (tag `asr-models`) and unpack it into `~/asr/`.
6. **Previews and covers.** Run `npm i -g playwright && npx playwright install chromium`.
7. **Install the skill** so every new Claude Code session knows this look:
   - Mac: `mkdir -p ~/.claude/skills && cp -R <this folder> ~/.claude/skills/cyber-nightmare`
   - Windows: copy the folder to `%USERPROFILE%\.claude\skills\cyber-nightmare`.
8. **Self-test** (below). Then tell the user in 4 short lines how clips in this look are made, where the test clip is, and what to type next time: "ทำคลิป Cyber Nightmare จากเสียงนี้", with a voice-over attached.

## Self-test
1. `python3 engine/new_episode.py ~/cyber-nightmare-test --example && cd ~/cyber-nightmare-test`
2. `python3 tools/temp_voice.py --pause 6:0.55,7:0.45` (Mac: Thai system voice; elsewhere a silent placeholder)
3. `python3 gen.py && cp cues.json tools/cues.json && MUSIC=synth ~/.venvs/ai-lab/bin/python tools/mix.py`
4. `node tools/frames.js test.jpg 1 9 20 30` and look at the grid, then `npx hyperframes render . -o renders/test.mp4`
