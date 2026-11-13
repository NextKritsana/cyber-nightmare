"""Two covers for Cyber Nightmare EP1, drawn from the same scene SVGs as the clip. -> renders/cover/cover-v1.jpg, cover-v2.jpg
v1 = bank-app phone with the red STOP hand over it, title on top, Moon bottom-left crossing her arms.
v2 = the crying close-up face with the red "ด่วน! 30,000" alert, title "เสียงแม่… หรือ AI?", Moon bottom-left with the magnifier."""
import re, subprocess, os
ns = {}; exec(open("gen.py").read(), ns)          # rebuilds index.html too; gives S, palette
S = ns["S"]; css = re.search(r"<style>(.*?)</style>", open("index.html").read(), re.S).group(1)
EXTRA = """
.ct { position:absolute; left:0; right:0; top:120px; text-align:center; z-index:9; font-family:KanitX; }
.ct .k { display:inline-block; background:#FFD54A; color:#1E2533; font-size:42px; padding:6px 30px 10px; border-radius:40px; margin-bottom:22px; }
.ct .t1 { color:#fff; font-size:104px; line-height:1.12; text-shadow:0 6px 0 rgba(0,0,0,.5); }
.ct .t2 { display:inline-block; background:#E5484D; color:#fff; font-size:112px; line-height:1.1; padding:4px 34px 18px; border-radius:26px; margin-top:12px; }
.mh { position:absolute; left:-90px; top:1150px; width:780px; height:780px; z-index:8; }
.mh img { width:100%; filter:drop-shadow(0 14px 18px rgba(0,0,0,.45)); }
.dark { position:absolute; inset:0; background:linear-gradient(#081419 0%, rgba(8,20,25,.0) 30%); z-index:2; }
"""
def page(svg, cam_tf, title, pose, extra=""):
    svg = re.sub(r'<rect width="1080" height="1920" fill="url\(#g\d+\)"/>', "", svg, count=1)
    return f"""<!DOCTYPE html><html lang="th"><head><meta charset="UTF-8"><style>{css}{EXTRA}</style></head><body><div id="root" style="background:linear-gradient(#10262F,#060E12)">
<div class="scene"><div class="cam" style="transform:{cam_tf}"><svg viewBox="0 0 1080 1920" width="1080" height="1920">{svg}</svg></div></div>
<div class="dark"></div>{extra}<div class="ct">{title}</div>
<div class="mh"><img src="assets/host/{pose}/f0.png" alt=""></div></div></body></html>"""
stop = S["s07"].replace('<rect width="1080" height="1920" fill="#000" opacity=".55"/>', '')
v1 = page(S["s06"].replace('<rect id="s06-vig" width="1080" height="1920" fill="url(#vig6)" opacity="0"/>', "").replace('id="s06-amt" x="270" y="580" text-anchor="middle" class="ui" font-size="96" fill="#fff">฿0', 'id="s06-amt" x="270" y="580" text-anchor="middle" class="ui" font-size="96" fill="#fff">฿30,000') + stop,
          "translate(70px, 330px) scale(.8)",
          '<div class="k">CYBER NIGHTMARE · EP1</div><div class="t1">แม่โทรมาร้องไห้ขอเงิน</div><div class="t2">คุณจะรอดไหม?</div>', "22-cross-x")
f5 = S["s05"].replace('id="f5-tear" d="M -112 70 C -126 96 -128 112 -112 118 C -96 112 -98 96 -112 70 Z" fill="#9EDCF5" opacity="0"', 'id="f5-tear" d="M -112 70 C -126 96 -128 112 -112 118 C -96 112 -98 96 -112 70 Z" fill="#9EDCF5" opacity="1" transform="translate(0 40)"').replace('fill="#9EDCF5" opacity="0"/>', 'fill="#9EDCF5" opacity="1"/>')
f5 = f5.replace('<path id="f5-bL" d="M -150 -40 Q -100 -62 -50 -48"', '<path id="f5-bL" transform="rotate(-16 -150 -40) translate(0 -10)" d="M -150 -40 Q -100 -62 -50 -48"').replace('<path id="f5-bR" d="M 50 -48 Q 100 -62 150 -40"', '<path id="f5-bR" transform="rotate(16 150 -40) translate(0 -10)" d="M 50 -48 Q 100 -62 150 -40"')
v2 = page(f5, "translate(130px, 260px) scale(.86)",
          '<div class="k">คืนนี้ 23:00</div><div class="t1">เสียงแม่จริงๆ…</div><div class="t2">หรือ AI?</div>', "20-magnifier",
          '<div style="position:absolute;left:470px;top:1520px;z-index:9;transform:rotate(-5deg)"><span style="display:inline-block;background:#E5484D;color:#fff;font-family:KanitX;font-size:64px;padding:8px 34px 16px;border-radius:24px;border:6px solid #fff">ด่วน! โอน 30,000</span></div>')
os.makedirs("renders/cover", exist_ok=True)
for n, h in (("v1", v1), ("v2", v2)): open(f"cover-{n}.html", "w").write(h)
js = """const path=require('path'),{execFileSync}=require('child_process');let pw;try{pw=require('playwright')}catch(e){pw=require(path.join(execFileSync('npm',['root','-g']).toString().trim(),'playwright'))}
(async()=>{const b=await pw.chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});for(const n of ['v1','v2']){await p.goto('file://'+path.resolve('cover-'+n+'.html'));await p.waitForTimeout(700);await p.screenshot({path:'renders/cover/cover-'+n+'.jpg',type:'jpeg',quality:92});}await b.close();})();"""
open("/tmp/cn_cover.js", "w").write(js)
subprocess.run(["node", "/tmp/cn_cover.js"], check=True); print("covers done")
