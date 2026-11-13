---
name: cyber-nightmare
description: Make vertical (1080x1920) "Cyber Nightmare" Reels, a flat-vector motion-graphic survival story told in the second person ("ถ้าคืนนี้… คุณจะรอดไหม?"). Every scene is drawn in code (inline SVG + GSAP, no image generation). Moon (cat-eared host in a lab coat) narrates as a sticker in the bottom-left corner and changes pose per line. A red "อย่าเพิ่ง!" stop beat leads into the real way to survive. From one voice-over it delivers a long clip, a ≤30 s short clip, 2 covers and captions, and it writes the next episode's voice script. Use for Cyber Nightmare, คลิปเอาตัวรอดภัยไซเบอร์, คลิปอนิเมชันเล่าเรื่องมิจฉาชีพ, "คืนนี้คุณจะรอดไหม", or any scam/cyber survival story in this look.
---

# Cyber Nightmare (long clip + short clip + covers + captions)

Reply in the user's language (Thai). Users are not technical: run everything yourself and send the finished mp4s and covers.

The finished look is in `example-output/` (EP1 "แม่โทรมาร้องไห้ขอเงิน คุณจะรอดไหม?": covers and a frame grid). Build it with `python3 engine/new_episode.py <dir> --example`.

## The look
- **Drawing.** Flat vector with no outlines, soft gradients and a dark teal night palette: navy #0E2129, teal #1C4650, glow #7FE3D6, alert red #E5484D, yellow #FFD54A, cream #F4EEE4, skin #F2C9A5, hoodie #3E6E73.
  - Everything is SVG in `gen.py`: faces, hands, phones, bedrooms, app screens, waveforms, chips.
  - Nothing is generated, so it works without Flow or image credits.
- **The "you" character.** A gender-neutral young adult in a teal hoodie. The close-up face (`face()`) has blinking eyes, worried brows, an open mouth, tears and sweat.
- **UI chips.**
  - time chip (moon icon, "23:00");
  - red alert pill;
  - yellow series badge "CYBER NIGHTMARE · EPn" at the top.
- **Moon (narrator).** The usual lab-coat sticker, no frame, at the **bottom-left**: `#moon`, left -110, top 1190, 740 px.
  - One pose per spoken line (`POSES`), boiling frames at 8 fps, a pop on each change, and she waves at the end.
  - Keep scene art out of x<540, y>1240.
  - The user rejected a round frame in a corner: "ไม่ต้องมีกรอบ เอาเหมือนเดิม".
- **Subtitles.**
  - Box to the right of Moon: left 470, top 1490.
  - Kanit ExtraBold 58 px, white with a shadow. The key word goes in a red pill (`H()`, nowrap).
  - Split long lines with `<br>`. Subtitle 1 is on screen at frame 0.
- **Motion.**
  - Every scene has a slow camera push.
  - Phones fly up; thumbs slide to buttons; rings shake; counters count up; red vignette heartbeats on the tense beat.
  - The STOP scene (`s07`) is an overlay on top of the frozen previous scene.
- **Sound.**
  - `tools/mix.py` with `MUSIC=synth`: a synthesized bed plus synthesized SFX from `cues.json`, mastered to -13 LUFS.

## Story formula (12 lines, about 30-35 s after atempo 1.2)
1. Hook: "ถ้าคืนนี้ [the threat]… คุณจะรอดไหม?"
2. Time and place: "ห้าทุ่ม คุณ…", with the time chip.
3. The trigger arrives: a call, SMS or link.
4. The bait. Another character's line can be a separate voice file.
5. Pressure: emotion, urgency, money.
6. "ตอนนั้น สมองจะสั่งให้คุณ… [the wrong move]"
7. "อย่าเพิ่ง!" / "อย่ารอ!": the red-hand freeze, with 0.3 s silence before and 0.5 s after.
8. The reveal: what it really is (AI voice clone, a money-stealing app…).
9. How to survive, in concrete steps.
10. Relief: the safe outcome.
11. One rule to remember.
12. "คืนต่อไป… จะเป็นฝันร้ายเรื่องไหน กดติดตามมูนไว้นะคะ"

**Facts and wording:**
- Keep facts generic and verified (cite official sources in the caption). Say in the caption that the story is fictional. Use no statistics unless checked.
- Avoid jargon on screen. Use icons, not emoji, inside the video.

## Workflow
`PY=~/.venvs/ai-lab/bin/python` (the venv from SETUP.md).

1. **New episode.** Run `python3 engine/new_episode.py <dir>`. Write `lines.txt` (12 lines) and `voice-script.md` (the ElevenLabs v4 script with tags, for Moon's voice), and give the script to the user in chat.
2. **Temp voice** (optional, to build before the real voice arrives): `python3 tools/temp_voice.py --pause 6:0.55,7:0.45`.
3. **Real voice.**
   - `ffmpeg -i moon.mp3 -af atempo=1.2 -ar 44100 -ac 1 assets/audio/vo-raw.wav`
   - `$PY tools/tighten.py assets/audio/vo-raw.wav assets/audio/vo-tight.wav --gap 0.12 --long 0.24 > phrases.txt`
   - Map phrases to lines, using ASR or by ear, then run `python3 tools/real_voice.py assets/audio/vo-tight.wav "1-3,4-5,6,x,7,…" --insert 3:voice/other.wav --pause 7:0.3:0.5`.
   - Lines spoken by another voice are `x` and are inserted after the given line. With no file, use `say -v Kanya` with a phone-band filter: `highpass=f=380,lowpass=f=3200,acompressor`.
4. **Scenes.**
   - Edit the `S["sNN"]` SVG strings and the per-scene JS in `gen.py`.
   - Scene windows come from the line starts in `timing.json` (`SC`). Animation times are offsets from the scene start `a`. Keep them inside short scenes.
   - Then run `python3 gen.py`.
5. **Preview.** `node tools/frames.js out.jpg t1 t2 …`: check overlaps (Moon zone, the subtitle box, the badge).
6. **Sound.** `cp cues.json tools/cues.json && MUSIC=synth $PY tools/mix.py`
7. **Render.** `npx hyperframes render . -o "renders/Cyber Nightmare EPn <title>.mp4"` (run it in the background), then pull frames and check them.
8. **Short clip (≤30 s, a complete story).**
   - Write `cuts.json` with every scene start (s06 runs until s07 starts).
   - Run `$PY tools/short_cut.py <mp4> 1,3-11 <out>`. Usually drop the set-up scene and the end card.
9. **Covers.** Run `python3 cover_gen.py` (v1 = the stop moment plus a 2-line title, v2 = the emotional close-up plus an alert pill). Moon is bottom-left on both.
10. **Captions.** Write the long caption, the short caption, the sources, the hashtags and "เรื่องในคลิปเป็นเหตุการณ์สมมติ".

## GSAP gotcha (SVG)
SVG groups placed with a `transform` attribute must be tweened with **relative** values (`y:"+=900"`, `x:"-=60"`) and `transformOrigin:"50% 50%"`. An absolute x/y wipes the group's translate, and the drawing jumps to the top-left.

## Files
- `engine/template/`: `gen.py` (all scenes, subtitles, Moon, timeline and cues), `cover_gen.py`, and `tools/`:
  - `temp_voice.py`, `real_voice.py`, `tighten.py`
  - `mix.py`, `frames.js`, `short_cut.py`
- `engine/template/assets/host/`: Moon's 24 lab poses (`f0..f2.png` boiling frames).
- `engine/example-ep01/`: EP1 timings, lines and script (no audio).
- `references/ep02-voice-script.md`: the next episode, "มือถือจอดำ เงินหายเอง" (an SMS parcel link leads to a money-stealing app; airplane mode; hotline 1441).

**No voice files are published.** Moon's voice is a private voice clone. Keep mp3/wav out of the repo (see `.gitignore`).
