"""Cyber Nightmare EP1 pilot: flat-vector motion-graphic story (second person, "would you survive tonight?").
Builds index.html (one root, scenes as timed <section class="clip">, inline SVG, one GSAP timeline) + cues.json for SFX.
Usage: python3 gen.py"""
import json, random

T = json.load(open("timing.json")); ST, DU, END = T["starts"], T["durs"], T["end"]
def ln(i): return ST[i - 1], ST[i - 1] + DU[i - 1]   # line i: (start, end)

# ---------------- palette ----------------
SKIN, SKIN2, HAIR, HOOD, HOOD2 = "#F2C9A5", "#E0AE88", "#1F2230", "#3E6E73", "#2F585D"
NAVY, TEAL, GLOW, RED, YEL, CREAM = "#0E2129", "#1C4650", "#7FE3D6", "#E5484D", "#FFD54A", "#F4EEE4"

# ---------------- scene windows (s, e) ----------------
b_ = lambda i, d=-.1: round(ST[i - 1] + d, 2)   # boundary just before line i
SC = {
    "s01": (0.0, b_(2)), "s02": (b_(2), b_(3)), "s03": (b_(3), b_(4, .6)), "s04": (b_(4, .6), b_(5)), "s05": (b_(5), b_(6)),
    "s06": (b_(6), b_(8, -.08)), "s07": (b_(7, -.05), b_(8, -.08)), "s08": (b_(8, -.08), b_(9)), "s09": (b_(9), b_(10)), "s10": (b_(10), b_(11)),
    "s11": (b_(11), b_(12)), "s12": (b_(12), END),
}

def bg(top, bot, gid):
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient></defs>'
            f'<rect width="1080" height="1920" fill="url(#{gid})"/>')

def glow(cx, cy, r, color, op, gid):
    return (f'<defs><radialGradient id="{gid}"><stop offset="0" stop-color="{color}" stop-opacity="{op}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/>')

def face(p, cx=540, cy=900, s=1.0, crying=False):
    """big close-up head of 'you' (ids prefixed p): eyes/brows/mouth/tear are animatable groups"""
    return f'''<g id="{p}-face" transform="translate({cx} {cy}) scale({s})">
  <path d="M -430 1020 C -390 600 -220 480 0 480 C 220 480 390 600 430 1020 Z" fill="{HOOD}"/>
  <path d="M -250 520 C -150 600 150 600 250 520 C 200 470 -200 470 -250 520 Z" fill="{HOOD2}"/>
  <rect x="-75" y="230" width="150" height="300" rx="40" fill="{SKIN2}"/>
  <ellipse cx="-268" cy="30" rx="48" ry="72" fill="{SKIN2}"/><ellipse cx="268" cy="30" rx="48" ry="72" fill="{SKIN2}"/>
  <ellipse cx="0" cy="0" rx="270" ry="330" fill="{SKIN}"/>
  <path d="M -278 20 C -300 -300 -120 -390 20 -385 C 200 -380 320 -280 282 20 C 262 -110 190 -190 90 -180 C 20 -250 -140 -200 -210 -110 C -250 -60 -268 -20 -278 20 Z" fill="{HAIR}"/>
  <path d="M -120 -215 C -60 -150 40 -150 120 -200 C 60 -260 -60 -260 -120 -215 Z" fill="{HAIR}"/>
  <ellipse cx="-150" cy="110" rx="46" ry="22" fill="#F0A6A0" opacity=".35"/><ellipse cx="150" cy="110" rx="46" ry="22" fill="#F0A6A0" opacity=".35"/>
  <g id="{p}-eyes">
    <g id="{p}-eL" transform="translate(-100 30)"><ellipse rx="44" ry="32" fill="#fff"/><circle id="{p}-pL" r="21" fill="#23252F"/><circle cx="7" cy="-8" r="7" fill="#fff"/></g>
    <g id="{p}-eR" transform="translate(100 30)"><ellipse rx="44" ry="32" fill="#fff"/><circle id="{p}-pR" r="21" fill="#23252F"/><circle cx="7" cy="-8" r="7" fill="#fff"/></g>
  </g>
  <path id="{p}-bL" d="M -150 -40 Q -100 -62 -50 -48" stroke="{HAIR}" stroke-width="13" fill="none" stroke-linecap="round"/>
  <path id="{p}-bR" d="M 50 -48 Q 100 -62 150 -40" stroke="{HAIR}" stroke-width="13" fill="none" stroke-linecap="round"/>
  <path d="M 0 60 Q -14 112 8 118" stroke="#C98D6C" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path id="{p}-mN" d="M -45 185 Q 0 172 45 185" stroke="#8A3B3B" stroke-width="10" fill="none" stroke-linecap="round"/>
  <ellipse id="{p}-mO" cx="0" cy="192" rx="30" ry="38" fill="#5A2328" opacity="0"/>
  <path id="{p}-tear" d="M -112 70 C -126 96 -128 112 -112 118 C -96 112 -98 96 -112 70 Z" fill="#9EDCF5" opacity="0"/>
  <path id="{p}-sweat" d="M 238 -120 C 222 -90 220 -70 238 -64 C 256 -70 254 -90 238 -120 Z" fill="#9EDCF5" opacity="0"/>
</g>'''

def phone(p, x, y, w, h, screen):
    return f'''<g id="{p}-ph" transform="translate({x} {y})">
  <rect width="{w}" height="{h}" rx="{w*0.12:.0f}" fill="#101418"/>
  <rect x="{w*0.04:.0f}" y="{w*0.04:.0f}" width="{w*0.92:.0f}" height="{h - w*0.08:.0f}" rx="{w*0.09:.0f}" fill="#0F1E26"/>
  <rect x="{w*0.38:.0f}" y="{w*0.07:.0f}" width="{w*0.24:.0f}" height="{w*0.05:.0f}" rx="{w*0.025:.0f}" fill="#000"/>
  {screen}
</g>'''

def hand(p, x, y, s=1.0, rot=0):
    """a hand coming up from the bottom, holding (fingers wrap the left edge)"""
    return f'''<g id="{p}-hand" transform="translate({x} {y}) rotate({rot}) scale({s})">
  <path d="M -60 520 C -80 380 -90 240 -40 120 C 0 40 120 30 170 90 C 210 140 220 300 200 520 Z" fill="{SKIN}"/>
  <path d="M -60 520 L 200 520 L 215 700 L -80 700 Z" fill="{HOOD}"/>
</g>'''

def thumb(p, x, y, rot=0):
    return f'''<g id="{p}-th" transform="translate({x} {y}) rotate({rot})">
  <path d="M -38 0 C -46 -60 -30 -120 0 -130 C 32 -122 44 -60 38 0 L 30 260 L -40 260 Z" fill="{SKIN}"/>
  <path d="M -22 -100 C -16 -122 16 -122 22 -100 C 16 -88 -16 -88 -22 -100 Z" fill="#F7DCC6"/>
</g>'''

def chip_time(t, icon="moon"):
    ic = ('<svg width="34" height="34" viewBox="0 0 34 34"><path d="M24 4 A14 14 0 1 0 30 24 A11 11 0 0 1 24 4 Z" fill="#FFD54A"/></svg>' if icon == "moon"
          else '<svg width="34" height="34" viewBox="0 0 34 34"><rect x="6" y="2" width="22" height="30" rx="5" fill="#7FE3D6"/></svg>')
    return f'<div class="tchip">{ic}<span>{t}</span></div>'

# ---------------- scenes ----------------
S = {}
S["s01"] = bg("#0F2A33", "#081419", "g1") + glow(540, 980, 620, GLOW, .28, "gl1") + face("f1", 540, 930, 1.05)
S["s02"] = bg("#13323C", "#0A1A20", "g2") + f'''
  <g id="s02-win" transform="translate(-490 50)"><rect x="610" y="250" width="320" height="420" rx="8" fill="#0A1820" stroke="#2B4A55" stroke-width="16"/>
   <circle cx="830" cy="360" r="62" fill="#F4EEC8"/><circle cx="808" cy="345" r="58" fill="#0A1820"/>
   {''.join(f'<rect x="618" y="{262 + i*44}" width="304" height="14" fill="#1C3540" opacity=".85"/>' for i in range(9))}</g>
  <polygon points="120,720 440,720 680,1300 0,1300" fill="#7FE3D6" opacity=".05"/>
  <rect x="0" y="1460" width="1080" height="460" fill="#0A161B"/>
  <rect x="90" y="930" width="760" height="300" rx="30" fill="#2B4A55"/>
  <rect x="60" y="1180" width="860" height="300" rx="40" fill="#3C6670"/>
  <ellipse cx="300" cy="1150" rx="190" ry="70" fill="#E8E2D6"/>
  <g id="s02-kid">
    <path d="M 210 1300 C 220 1180 300 1130 380 1130 C 470 1130 540 1190 560 1300 Z" fill="{HOOD}"/>
    <circle cx="380" cy="1050" r="92" fill="{SKIN}"/>
    <path d="M 286 1050 C 280 950 340 940 390 945 C 450 950 486 990 474 1050 C 460 1010 430 990 400 994 C 360 980 310 1000 286 1050 Z" fill="{HAIR}"/>
    <ellipse id="s02-eL" cx="352" cy="1062" rx="9" ry="11" fill="#23252F"/><ellipse id="s02-eR" cx="412" cy="1062" rx="9" ry="11" fill="#23252F"/>
    <path d="M 365 1104 Q 382 1110 399 1104" stroke="#8A3B3B" stroke-width="5" fill="none" stroke-linecap="round"/>
    <rect id="s02-ph" x="430" y="1150" width="70" height="120" rx="12" fill="#CFF7F0" transform="rotate(-18 465 1210)"/>
    <polygon id="s02-beam" points="440,1160 500,1150 420,1040 330,1060" fill="#CFF7F0" opacity=".22"/>
  </g>
  <path d="M 60 1290 C 260 1250 600 1260 920 1300 L 920 1440 L 60 1440 Z" fill="#4FA3A0"/>
  <path d="M 60 1290 C 260 1250 600 1260 920 1300" stroke="#6CC2BD" stroke-width="10" fill="none"/>
  <rect x="900" y="1150" width="150" height="330" rx="10" fill="#22404A"/><rect x="930" y="1080" width="90" height="70" rx="8" fill="#365A63"/>'''
S["s03"] = bg("#0D2730", "#061016", "g3") + glow(540, 900, 600, GLOW, .22, "gl3") + hand("s03", 300, 1180, 1.25, -4) + phone("s03", 270, 360, 540, 1080, f'''
   <circle id="s03-ring" cx="270" cy="360" r="150" fill="none" stroke="#7FE3D6" stroke-width="6" opacity=".6"/>
   <circle cx="270" cy="360" r="120" fill="#F2C9A5"/><path d="M 170 330 C 170 220 370 220 370 330 C 340 280 200 280 170 330 Z" fill="#6B6F7A"/><circle cx="270" cy="255" r="40" fill="#6B6F7A"/>
   <ellipse cx="232" cy="370" rx="9" ry="11" fill="#23252F"/><ellipse cx="308" cy="370" rx="9" ry="11" fill="#23252F"/><path d="M 245 420 Q 270 432 295 420" stroke="#8A3B3B" stroke-width="6" fill="none" stroke-linecap="round"/>
   <text x="270" y="580" text-anchor="middle" class="ui" font-size="78" fill="#fff">แม่</text>
   <text x="270" y="640" text-anchor="middle" class="uir" font-size="36" fill="#9FB8BF">สายเรียกเข้า…</text>
   <g id="s03-no"><circle cx="130" cy="880" r="62" fill="#E5484D"/><rect x="100" y="872" width="60" height="16" rx="8" fill="#fff"/></g>
   <g id="s03-yes"><circle cx="410" cy="880" r="62" fill="#2ECC71"/><path d="M 385 860 C 380 900 420 920 440 905 L 432 890 C 420 896 404 884 404 870 Z" fill="#fff"/></g>''') + thumb("s03", 760, 1500, -14)
S["s04"] = bg("#12303A", "#081419", "g4") + glow(540, 1050, 560, GLOW, .2, "gl4") + f'''
  <g id="s04-kid" transform="translate(540 1300)">
    <path d="M -330 800 C -300 430 -170 330 0 330 C 170 330 300 430 330 800 Z" fill="{HOOD}"/>
    <rect x="-55" y="160" width="110" height="200" rx="30" fill="{SKIN2}"/>
    <ellipse cx="0" cy="0" rx="190" ry="232" fill="{SKIN}"/>
    <path d="M -196 20 C -212 -210 -86 -272 14 -270 C 140 -266 226 -196 198 20 C 184 -76 134 -130 64 -124 C 14 -174 -98 -140 -148 -76 C -176 -40 -188 -10 -196 20 Z" fill="{HAIR}"/>
    <g id="s04-eyes"><ellipse cx="-70" cy="20" rx="30" ry="22" fill="#fff"/><circle cx="-70" cy="22" r="14" fill="#23252F"/><ellipse cx="70" cy="20" rx="30" ry="22" fill="#fff"/><circle cx="70" cy="22" r="14" fill="#23252F"/></g>
    <path d="M -110 -34 Q -70 -54 -30 -40" stroke="{HAIR}" stroke-width="10" fill="none" stroke-linecap="round" transform="rotate(10 -70 -44)"/>
    <path d="M 30 -40 Q 70 -54 110 -34" stroke="{HAIR}" stroke-width="10" fill="none" stroke-linecap="round" transform="rotate(-10 70 -44)"/>
    <ellipse id="s04-mo" cx="0" cy="130" rx="22" ry="28" fill="#5A2328"/>
    <g transform="translate(150 -40) rotate(14)"><rect x="0" y="-20" width="80" height="190" rx="16" fill="#101418"/><path d="M 20 170 C 0 260 30 330 90 340 L 130 200 C 110 170 60 160 20 170 Z" fill="{SKIN}"/></g>
  </g>
  <g id="s04-bub" transform="translate(540 690)"><rect x="-430" y="-150" width="860" height="300" rx="60" fill="#fff"/><path d="M 120 140 L 220 250 L 40 150 Z" fill="#fff"/>
    <g id="s04-wave">{''.join(f'<rect class="wv" x="{-360 + i*30}" y="-40" width="16" height="80" rx="8" fill="#E5484D"/>' for i in range(25))}</g></g>
  <g id="s04-alert" transform="translate(540 930)"><rect x="-370" y="-55" width="740" height="110" rx="55" fill="#E5484D"/>
    <circle cx="-310" cy="0" r="30" fill="#fff"/><rect x="-314" y="-18" width="8" height="22" rx="4" fill="#E5484D"/><circle cx="-310" cy="14" r="5" fill="#E5484D"/>
    <text x="35" y="18" text-anchor="middle" class="ui" font-size="50" fill="#fff">ด่วน! ค่ารักษา 30,000 บาท</text></g>'''
S["s05"] = bg("#10232B", "#060E12", "g5") + glow(540, 900, 650, "#E5484D", .12, "gl5") + face("f5", 540, 960, 1.0, True) + f'''
  <g id="s05-wave" transform="translate(540 350)">{''.join(f'<rect class="wv" x="{-330 + i*30}" y="-35" width="16" height="70" rx="8" fill="#7FE3D6" opacity=".8"/>' for i in range(23))}</g>'''
S["s06"] = bg("#0D2730", "#061016", "g6") + f'''<defs><radialGradient id="vig6" r=".75"><stop offset=".55" stop-color="#E5484D" stop-opacity="0"/><stop offset="1" stop-color="#E5484D" stop-opacity=".55"/></radialGradient></defs>''' + hand("s06", 300, 1180, 1.25, -4) + phone("s06", 270, 360, 540, 1080, f'''
   <text x="270" y="130" text-anchor="middle" class="ui" font-size="44" fill="#fff">โอนเงิน</text>
   <rect x="40" y="190" width="460" height="150" rx="24" fill="#18303A"/>
   <text x="70" y="250" class="uir" font-size="30" fill="#9FB8BF">ไปที่บัญชี</text><text x="70" y="305" class="ui" font-size="38" fill="#fff">นาย ส. (ไม่รู้จัก)</text>
   <text x="270" y="470" text-anchor="middle" class="uir" font-size="32" fill="#9FB8BF">จำนวนเงิน</text>
   <text id="s06-amt" x="270" y="580" text-anchor="middle" class="ui" font-size="96" fill="#fff">฿0</text>
   <g id="s06-btn"><rect x="60" y="820" width="420" height="120" rx="60" fill="#2ECC71"/><text x="270" y="898" text-anchor="middle" class="ui" font-size="46" fill="#fff">ยืนยันโอน</text></g>''') + thumb("s06", 790, 1560, -16) + '<rect id="s06-vig" width="1080" height="1920" fill="url(#vig6)" opacity="0"/>'
S["s07"] = '''<rect width="1080" height="1920" fill="#000" opacity=".55"/>
  <g id="s07-stop" transform="translate(540 820)"><circle r="230" fill="#E5484D" opacity=".18"/><circle r="200" fill="none" stroke="#E5484D" stroke-width="26"/>
   <path d="M -70 120 L -95 -10 C -100 -40 -60 -48 -54 -18 L -45 30 L -50 -120 C -52 -150 -12 -152 -10 -122 L -6 10 L -2 -150 C 0 -180 40 -180 40 -150 L 38 10 L 50 -120 C 54 -150 92 -146 88 -116 L 78 40 L 104 -10 C 118 -36 152 -20 140 8 L 96 120 C 80 160 -50 170 -70 120 Z" fill="#FFD9C2"/></g>'''
S["s08"] = bg("#0B1D24", "#050C10", "g8") + f'''
  <g id="s08-card" transform="translate(460 560)"><rect x="-260" y="-240" width="520" height="480" rx="36" fill="#1B2E36"/>
   <rect x="-230" y="-210" width="460" height="300" rx="20" fill="#2B4A55"/><circle cx="0" cy="-70" r="80" fill="#F2C9A5"/><path d="M -80 -90 C -80 -170 80 -170 80 -90 C 60 -130 -60 -130 -80 -90 Z" fill="#6B6F7A"/><circle cx="0" cy="-160" r="30" fill="#6B6F7A"/>
   <circle cx="0" cy="-60" r="44" fill="#000" opacity=".35"/><path d="M -12 -82 L 22 -60 L -12 -38 Z" fill="#fff"/>
   <rect x="120" y="50" width="90" height="34" rx="10" fill="#000" opacity=".6"/><text x="165" y="77" text-anchor="middle" class="uir" font-size="24" fill="#fff">0:05</text>
   <text x="-230" y="150" class="ui" font-size="34" fill="#fff">คลิปแม่ในโซเชียล</text><text x="-230" y="200" class="uir" font-size="28" fill="#9FB8BF">ใครก็โหลดได้</text></g>
  <path id="s08-a1" d="M 540 820 L 540 900" stroke="#7FE3D6" stroke-width="10" stroke-linecap="round"/><path d="M 515 880 L 540 910 L 565 880" stroke="#7FE3D6" stroke-width="10" fill="none" stroke-linecap="round" id="s08-a1h"/>
  <g id="s08-chip" transform="translate(540 1040)"><rect x="-120" y="-100" width="240" height="200" rx="36" fill="#7FE3D6"/>
   {''.join(f'<rect x="{-100 + i*50}" y="-128" width="14" height="28" rx="4" fill="#7FE3D6"/><rect x="{-100 + i*50}" y="100" width="14" height="28" rx="4" fill="#7FE3D6"/>' for i in range(5))}
   <text x="0" y="28" text-anchor="middle" class="ui" font-size="92" fill="#0B1D24">AI</text></g>
  <path id="s08-a2" d="M 600 1170 L 680 1230" stroke="#7FE3D6" stroke-width="10" stroke-linecap="round"/>
  <g id="s08-wave" transform="translate(730 1300)">{''.join(f'<rect class="wv" x="{-270 + i*30}" y="-45" width="16" height="90" rx="8" fill="#E5484D"/>' for i in range(19))}</g>
  <g id="s08-tag" transform="translate(730 1420)"><rect x="-200" y="-40" width="400" height="80" rx="40" fill="#E5484D"/><text y="16" text-anchor="middle" class="ui" font-size="40" fill="#fff">เสียงแม่ (ปลอม)</text></g>'''
S["s09"] = bg("#0D2730", "#061016", "g9") + glow(540, 900, 600, GLOW, .18, "gl9") + hand("s09", 300, 1180, 1.25, -4) + phone("s09", 270, 360, 540, 1080, f'''
   <g id="s09-end"><text x="270" y="300" text-anchor="middle" class="ui" font-size="60" fill="#fff">แม่</text><text x="270" y="360" text-anchor="middle" class="uir" font-size="34" fill="#9FB8BF">00:42</text>
    <circle id="s09-red" cx="270" cy="860" r="72" fill="#E5484D"/><rect x="236" y="851" width="68" height="18" rx="9" fill="#fff"/></g>
   <g id="s09-list" opacity="0"><text x="50" y="140" class="ui" font-size="48" fill="#fff">รายชื่อ</text>
    {''.join(f'<rect x="40" y="{190 + i*130}" width="460" height="110" rx="20" fill="#18303A"/><circle cx="100" cy="{245 + i*130}" r="34" fill="#2B4A55"/><rect x="155" y="{230 + i*130}" width="{200 - i*30}" height="26" rx="13" fill="#2B4A55"/>' for i in range(5))}
    <g id="s09-mom"><rect x="30" y="440" width="480" height="130" rx="24" fill="#2ECC71" opacity=".18" stroke="#2ECC71" stroke-width="5"/><circle cx="100" cy="505" r="38" fill="#F2C9A5"/>
     <text x="160" y="500" class="ui" font-size="44" fill="#fff">แม่</text><text x="160" y="545" class="uir" font-size="26" fill="#9FEBC0">เบอร์ที่บันทึกเอง</text>
     <circle id="s09-call" cx="440" cy="505" r="40" fill="#2ECC71"/><path d="M 422 488 C 418 520 446 535 462 524 L 456 512 C 446 517 434 508 434 497 Z" fill="#fff"/></g></g>''') + thumb("s09", 560, 1500, -6)
S["s10"] = bg("#1A2F3A", "#0C171C", "g10") + f'''
  <rect x="120" y="300" width="300" height="380" rx="8" fill="#0A1820" stroke="#2B4A55" stroke-width="14"/><circle cx="200" cy="410" r="50" fill="#F4EEC8"/>
  <rect x="0" y="1460" width="1080" height="460" fill="#0A161B"/>
  <rect x="80" y="960" width="720" height="280" rx="30" fill="#3B3550"/><rect x="50" y="1200" width="820" height="280" rx="40" fill="#5A5274"/>
  <ellipse cx="320" cy="1170" rx="190" ry="70" fill="#E8E2D6"/>
  <g id="s10-mom"><circle cx="340" cy="1120" r="88" fill="{SKIN}"/>
   <path d="M 252 1110 C 250 1010 320 1000 350 1004 C 420 1008 440 1060 430 1110 C 410 1070 380 1056 350 1060 C 310 1054 270 1076 252 1110 Z" fill="#9AA0AA"/><circle cx="350" cy="1018" r="40" fill="#9AA0AA"/>
   <path id="s10-eL" d="M 300 1128 Q 315 1138 330 1128" stroke="#23252F" stroke-width="6" fill="none" stroke-linecap="round"/><path id="s10-eR" d="M 356 1128 Q 371 1138 386 1128" stroke="#23252F" stroke-width="6" fill="none" stroke-linecap="round"/>
   <path d="M 330 1170 Q 343 1176 356 1170" stroke="#8A3B3B" stroke-width="5" fill="none" stroke-linecap="round"/>
   <g id="s10-ph"><rect x="430" y="1110" width="60" height="110" rx="12" fill="#CFF7F0"/></g></g>
  <path d="M 50 1290 C 250 1250 600 1260 870 1300 L 870 1460 L 50 1460 Z" fill="#8C7FB0"/>
  <rect x="890" y="1150" width="150" height="330" rx="10" fill="#2B2640"/>
  <g id="s10-z" class="ui" fill="#CFC4F0"><text id="s10-z1" x="470" y="1000" font-size="54">Z</text><text id="s10-z2" x="520" y="940" font-size="70">Z</text></g>
  <g id="s10-ok" transform="translate(540 600)"><rect x="-260" y="-60" width="520" height="120" rx="60" fill="#2ECC71"/>
   <path d="M -200 0 L -175 25 L -135 -25" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/><text x="30" y="18" text-anchor="middle" class="ui" font-size="52" fill="#fff">แม่ปลอดภัยดี</text></g>'''
S["s11"] = bg("#13323C", "#081419", "g11") + glow(540, 860, 560, YEL, .14, "gl11") + f'''
  <g id="s11-card" transform="translate(540 820)"><rect x="-340" y="-300" width="680" height="600" rx="48" fill="{CREAM}"/>
   <g transform="translate(0 -150)"><rect x="-70" y="-30" width="140" height="120" rx="20" fill="#E5A93B"/><path d="M -45 -30 L -45 -70 C -45 -130 45 -130 45 -70 L 45 -30" stroke="#E5A93B" stroke-width="22" fill="none"/><circle cx="0" cy="25" r="16" fill="#7A4E10"/></g>
   <text y="40" text-anchor="middle" class="ui" font-size="64" fill="#1E2533">คำลับครอบครัว</text>
   <g id="s11-dots">{''.join(f'<circle cx="{-150 + i*100}" cy="150" r="26" fill="#1E2533"/>' for i in range(4))}</g></g>
  <g id="s11-fam" transform="translate(540 1270)">{''.join(f'<g transform="translate({x} 0)"><circle cy="-40" r="44" fill="{c}"/><path d="M -70 90 C -60 10 60 10 70 90 Z" fill="{c}"/></g>' for x, c in [(-180, "#7FE3D6"), (0, YEL), (180, "#F2A7B3")])}</g>'''
S["s12"] = bg("#0E2430", "#03080B", "g12") + f'''
  {''.join(f'<circle class="star" cx="{random.Random(i).randint(40, 1040)}" cy="{random.Random(i + 99).randint(120, 1300)}" r="{random.Random(i + 7).choice([3, 4, 5])}" fill="#fff" opacity=".7"/>' for i in range(40))}
  <g id="s12-moon"><circle cx="540" cy="370" r="150" fill="#F4EEC8"/><circle cx="490" cy="335" r="142" fill="#0E2430"/></g>
  <g id="s12-title"><text x="540" y="660" text-anchor="middle" class="ui" font-size="120" fill="#fff" letter-spacing="6">CYBER</text>
   <text x="540" y="790" text-anchor="middle" class="ui" font-size="120" fill="{RED}" letter-spacing="6">NIGHTMARE</text></g>'''

# ---------------- subtitles: (start, end, html) ----------------
def H(t): return f'<b class="hl">{t}</b>'
SUB = []
def sub(i, parts):  # split line i into parts by char weight
    a, b = ln(i); a = 0.0 if i == 1 else a; tot = sum(len(p.replace("<br>", "")) for p in parts); t = a
    for k, p in enumerate(parts):
        d = (b - a) * len(p.replace("<br>", "")) / tot; SUB.append((t, (b if k == len(parts) - 1 else t + d), p)); t += d
sub(1, ["ถ้าคืนนี้ แม่โทรมา<br>ร้องไห้ขอเงิน", "คุณจะ" + H("รอดไหม?")])
sub(2, [H("ห้าทุ่ม") + " คุณนอนเล่น<br>มือถือคนเดียว"])
sub(3, ["แล้วสายจาก" + H("แม่") + "<br>ก็เข้ามา…"])
sub(4, ["“ลูก… แม่โดนรถชน", "ต้องจ่าย<br>" + H("ค่ารักษาด่วน") + "”"])
sub(5, ["เสียงแม่" + H("จริงๆ") + "<br>ร้องไห้ สั่นเครือ…"])
sub(6, ["ตอนนั้น สมอง<br>จะสั่งให้คุณ…", H("โอนเลย")])
sub(7, [H("อย่าเพิ่ง!")])
sub(8, ["นั่นอาจไม่ใช่แม่", "แต่เป็น<br>" + H("AI เลียนเสียง"), "จากคลิปเสียง<br>ไม่กี่วินาที"])
sub(9, [H("วางสาย") + "<br>แล้วโทรกลับ", "เบอร์แม่ที่คุณ<br>" + H("บันทึกไว้เอง")])
sub(10, ["แม่รับสายงัวเงีย…", "แม่หลับอยู่ที่บ้าน<br>" + H("ปลอดภัยดี")])
sub(11, ["ตั้ง" + H("คำลับ") + "<br>ไว้กับครอบครัว", "ตั้งแต่วันนี้"])
sub(12, ["คืนต่อไป… จะเป็น<br>" + H("ฝันร้าย") + "เรื่องไหน?"])

# ---------------- corner Moon (narrator) ----------------
POSES = [(1, '07-worried'), (2, '13-shush'), (3, '05-surprised'), (4, '14-listening'), (5, '18-panic'), (6, '06-pointing'), (7, '22-cross-x'), (8, '20-magnifier'), (9, '03-explaining'), (10, '08-thumbsup'), (11, '11-clipboard'), (12, '12-waving')]
PN = sorted(set(p for _, p in POSES))
MOON_END = END
moon = '<div class="clip" id="moon" data-start="0" data-duration="%.2f" data-track-index="5"><div id="moon-in"><div class="ring">' % MOON_END + "".join(
    f'<div class="pose" id="mp-{p}">' + "".join(f'<img id="mp-{p}-{f}" src="assets/host/{p}/f{f}.png" alt="">' for f in range(3)) + '</div>' for p in PN) + '</div></div></div>'
def pose_at(t):
    cur = POSES[0][1]
    for i, p in POSES:
        if t >= max(0, ST[i - 1] - 0.15): cur = p
    return cur
# ---------------- HTML ----------------
secs = []
for k, (a, b) in SC.items():
    over = ' style="z-index:5"' if k == "s07" else ""
    s_ = a; d = b - a
    if k == "s07": pass
    secs.append(f'<section id="{k}" class="clip scene" data-start="{s_:.2f}" data-duration="{d:.2f}" data-track-index="{2 if k == "s07" else 1}"{over}><div class="cam" id="{k}-cam"><svg viewBox="0 0 1080 1920" width="1080" height="1920">{S[k]}</svg></div>'
                + (chip_time("23:00") if k == "s02" else chip_time("23:06 · บ้านแม่") if k == "s10" else "")
                + ('<div class="cta" id="s12-cta"><span>กดติดตาม</span></div>' if k == "s12" else "") + '</section>')
subs = "".join(f'<div class="clip sub" id="sub{n:02d}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="3"><span>{t}</span></div>' for n, (a, b, t) in enumerate(SUB))

# ---------------- timeline JS ----------------
js = []
J = js.append
cues = []
def cue(t, n, g=1.0): cues.append([round(t, 3), n, g])
for k, (a, b) in SC.items():
    if k != "s07": J(f'tl.fromTo("#{k}-cam", {{scale:1.0}}, {{scale:1.07, duration:{b - a:.2f}, ease:"none", immediateRender:false}}, {a:.2f});')
def blink(p, t): J(f'tl.to("#{p}-eL, #{p}-eR", {{scaleY:.08, duration:.07, yoyo:true, repeat:1, transformOrigin:"50% 50%"}}, {t:.2f});')
def wave(sel, a, b, seed, amp=1.0):
    r = random.Random(seed); t = a
    while t < b:
        J(f'tl.to("{sel} .wv", {{scaleY:(i)=>{{const v=[{",".join(f"{r.uniform(.25, 1.9) * amp:.2f}" for _ in range(25))}];return v[i%25];}}, duration:.12, ease:"sine.inOut", transformOrigin:"50% 50%"}}, {t:.2f});'); t += 0.13
    J(f'tl.to("{sel} .wv", {{scaleY:.3, duration:.2}}, {b:.2f});')
# s01 hook: face looks down at phone light, worry builds
a, b = SC["s01"]; blink("f1", 1.2); blink("f1", 3.6)
J('tl.from("#f1-face", {y:"+=40", duration:.6, ease:"power2.out"}, 0);')
J('tl.to("#f1-pL, #f1-pR", {y:8, x:-6, duration:.5, ease:"power2.inOut"}, 1.6);')
J('tl.to("#f1-bL", {rotation:-14, y:-8, transformOrigin:"0% 50%", duration:.35, ease:"back.out(2)"}, 3.0); tl.to("#f1-bR", {rotation:14, y:-8, transformOrigin:"100% 50%", duration:.35, ease:"back.out(2)"}, 3.05);')
J('tl.to("#f1-mN", {opacity:0, duration:.1}, 3.3); tl.to("#f1-mO", {opacity:1, scale:1.1, transformOrigin:"50% 50%", duration:.25, ease:"back.out(3)"}, 3.3);')
cue(0.05, "thunder", .4); cue(3.3, "wrong", .5)
# s02 bedroom
a, b = SC["s02"]; J(f'tl.from("#s02 .tchip", {{y:-60, opacity:0, duration:.4, ease:"back.out(2)"}}, {a + .15:.2f});'); cue(a + .15, "tick", .6)
J(f'tl.to("#s02-beam", {{opacity:.34, duration:.5, yoyo:true, repeat:5, ease:"sine.inOut"}}, {a:.2f});')
J(f'tl.to("#s02-eL, #s02-eR", {{scaleY:.1, duration:.07, yoyo:true, repeat:1, transformOrigin:"50% 50%"}}, {a + 1.8:.2f});')
J(f'tl.fromTo("#s02-cam", {{x:40}}, {{x:-20, duration:{b - a:.2f}, ease:"none", immediateRender:false}}, {a:.2f});')
# s03 incoming call: ring + shake, thumb slides to answer
a, b = SC["s03"]
J(f'tl.from("#s03-ph", {{y:"+=900", duration:.45, ease:"power3.out"}}, {a:.2f});')
for i in range(8): J(f'tl.to("#s03-ph", {{rotation:{(-1.6 if i % 2 else 1.6)}, transformOrigin:"50% 50%", duration:.06}}, {a + .5 + i * .07:.2f});')
J(f'tl.to("#s03-ph", {{rotation:0, duration:.06}}, {a + 1.08:.2f});')
J(f'tl.fromTo("#s03-ring", {{scale:.8, opacity:.8, transformOrigin:"50% 50%"}}, {{scale:1.35, opacity:0, duration:.7, repeat:2, ease:"power1.out", immediateRender:false}}, {a + .4:.2f});')
cue(a + .45, "whoosh", .5); [cue(a + .5 + i * .35, "beep", .5) for i in range(4)]
J(f'tl.to("#s03-th", {{x:"-=60", y:"-=560", duration:.55, ease:"power2.inOut", immediateRender:false}}, {a + .85:.2f});')
J(f'tl.to("#s03-yes", {{scale:1.25, transformOrigin:"50% 50%", duration:.15, yoyo:true, repeat:1}}, {a + 1.38:.2f});'); cue(a + 1.38, "click", .8)
# s04 the call: bubble, waveform, alert
a, b = SC["s04"]; s4, e4 = ln(4)
J(f'tl.from("#s04-bub", {{scale:.3, opacity:0, transformOrigin:"50% 100%", duration:.35, ease:"back.out(2)"}}, {a + .05:.2f});'); cue(a + .05, "pop", .7)
wave("#s04-wave", a, e4, 4)
J(f'tl.from("#s04-alert", {{y:"+=60", opacity:0, duration:.35, ease:"back.out(2.5)"}}, {s4 + 2.6:.2f});'); cue(s4 + 2.6, "alarm", .6)
J(f'tl.to("#s04-alert", {{scale:1.06, transformOrigin:"50% 50%", duration:.25, yoyo:true, repeat:5}}, {s4 + 3.0:.2f});')
J(f'tl.fromTo("#s04-mo", {{scaleY:.4}}, {{scaleY:1.2, transformOrigin:"50% 50%", duration:.3, ease:"back.out(3)", immediateRender:false}}, {s4 + 1.4:.2f});'); cue(s4 + 1.4, "slap", .5)
J(f'tl.from("#s04-kid", {{y:"+=60", duration:.5, ease:"power2.out"}}, {a:.2f});')
# s05 close-up: crying, sweat, mom's voice wave
a, b = SC["s05"]; s5, e5 = ln(5)
J('tl.set("#f5-bL", {rotation:-16, y:-10, transformOrigin:"0% 50%"}, 0); tl.set("#f5-bR", {rotation:16, y:-10, transformOrigin:"100% 50%"}, 0);')
wave("#s05-wave", s5, e5, 5, .8)
J(f'tl.to("#f5-tear", {{opacity:1, duration:.2}}, {a + .6:.2f}); tl.to("#f5-tear", {{y:120, duration:1.4, ease:"power1.in"}}, {a + .8:.2f});')
J(f'tl.to("#f5-sweat", {{opacity:1, duration:.2}}, {a + 1.2:.2f}); tl.to("#f5-sweat", {{y:60, duration:1.2, ease:"power1.in"}}, {a + 1.3:.2f});')
blink("f5", a + 2.2); cue(a + .3, "rise", .5)
# s06 bank app: amount counts up, thumb hovers, red pulse heartbeat
a, b = SC["s06"]
J(f'tl.from("#s06-ph", {{y:"+=900", duration:.45, ease:"power3.out"}}, {a:.2f});'); cue(a, "whoosh", .5)
J(f'(function(){{const o={{v:0}};tl.to(o,{{v:30000,duration:1.0,ease:"power2.out",onUpdate:()=>{{document.querySelector("#s06-amt").textContent="฿"+Math.round(o.v).toLocaleString("en-US");}}}},{a + .5:.2f});}})();')
J(f'tl.set("#s06-amt", {{textContent:"฿0"}}, {a:.2f});')
[cue(a + .3 + i * .1, "tick", .4) for i in range(9)]
J(f'tl.to("#s06-th", {{x:"-=180", y:"-=520", duration:1.1, ease:"power2.inOut", immediateRender:false}}, {a + .9:.2f});')
for i in range(4):
    t = a + .8 + i * .5; J(f'tl.to("#s06-vig", {{opacity:.9, duration:.12, yoyo:true, repeat:1}}, {t:.2f});'); cue(t, "thud", .55)
J(f'tl.to("#s06-btn", {{scale:1.06, transformOrigin:"50% 50%", duration:.3, yoyo:true, repeat:3}}, {a + 1.5:.2f});')
# s07 STOP (overlay freeze)
a, b = SC["s07"]
J(f'tl.from("#s07-stop", {{scale:2.2, opacity:0, transformOrigin:"50% 50%", duration:.28, ease:"back.out(2.5)"}}, {a + .02:.2f});'); cue(a, "stamp", 1.0); cue(a + .02, "slap", .8)
J(f'tl.to("#s07-stop", {{x:"+=10", duration:.05, yoyo:true, repeat:5}}, {a + .3:.2f});')
# s08 AI voice clone: card -> AI chip -> fake waveform
a, b = SC["s08"]
J(f'tl.from("#s08-card", {{y:"-=200", opacity:0, duration:.45, ease:"back.out(2)"}}, {a + .1:.2f});'); cue(a + .1, "whoosh", .5)
J(f'tl.from("#s08-a1, #s08-a1h", {{opacity:0, y:-30, duration:.3}}, {a + 1.2:.2f});')
J(f'tl.from("#s08-chip", {{scale:0, rotation:-30, transformOrigin:"50% 50%", duration:.45, ease:"back.out(2.5)"}}, {a + 1.5:.2f});'); cue(a + 1.5, "ping", .8)
J(f'tl.to("#s08-chip", {{scale:1.08, transformOrigin:"50% 50%", duration:.3, yoyo:true, repeat:5}}, {a + 2.0:.2f});')
J(f'tl.from("#s08-a2", {{opacity:0, duration:.3}}, {a + 2.6:.2f}); tl.from("#s08-wave", {{opacity:0, duration:.3}}, {a + 2.8:.2f});')
wave("#s08-wave", a + 2.8, b - .3, 8); cue(a + 2.8, "static", .6)
J(f'tl.from("#s08-tag", {{scale:.4, opacity:0, transformOrigin:"50% 50%", duration:.35, ease:"back.out(3)"}}, {a + 3.6:.2f});'); cue(a + 3.6, "wrong", .6)
for i in range(3): J(f'tl.to("#s08-wave", {{x:"{("+=14" if i % 2 else "-=14")}", duration:.05, yoyo:true, repeat:1}}, {a + 4.2 + i * .6:.2f});')
# s09 hang up -> contacts -> call saved number
a, b = SC["s09"]; s9, e9 = ln(9)
J(f'tl.from("#s09-ph", {{y:"+=900", duration:.45, ease:"power3.out"}}, {a:.2f});')
J(f'tl.to("#s09-th", {{x:"-=210", y:"-=260", duration:.35, ease:"power2.inOut", immediateRender:false}}, {a + .2:.2f});')
J(f'tl.to("#s09-red", {{scale:.85, transformOrigin:"50% 50%", duration:.1, yoyo:true, repeat:1}}, {a + .55:.2f});'); cue(a + .55, "click", .8); cue(a + .6, "tapestop", .5)
J(f'tl.to("#s09-end", {{opacity:0, duration:.2}}, {a + .75:.2f}); tl.to("#s09-list", {{opacity:1, duration:.25}}, {a + .8:.2f});'); cue(a + .8, "flipcard", .6)
J(f'tl.to("#s09-th", {{x:"+=120", y:"-=640", duration:.5, ease:"power2.inOut"}}, {a + 1.1:.2f});')
J(f'tl.fromTo("#s09-mom", {{scale:1}}, {{scale:1.05, transformOrigin:"50% 50%", duration:.25, yoyo:true, repeat:3, immediateRender:false}}, {a + 2.6:.2f});'); cue(a + 2.9, "ding", .7)
J(f'tl.to("#s09-call", {{scale:1.3, transformOrigin:"50% 50%", duration:.3, yoyo:true, repeat:3}}, {a + 1.7:.2f});')
# s10 mom asleep, answers, safe
a, b = SC["s10"]
J(f'tl.from("#s10 .tchip", {{y:-60, opacity:0, duration:.4, ease:"back.out(2)"}}, {a + .1:.2f});')
J(f'tl.to("#s10-ph rect", {{fill:"#7FE3D6", duration:.15, yoyo:true, repeat:5}}, {a + .2:.2f});'); [cue(a + .2 + i * .35, "beep", .4) for i in range(3)]
J(f'tl.to("#s10-z1", {{y:-40, opacity:0, duration:1.6, ease:"sine.out"}}, {a + .3:.2f}); tl.to("#s10-z2", {{y:-50, opacity:0, duration:1.8, ease:"sine.out"}}, {a + .6:.2f});')
J(f'tl.to("#s10-ph", {{y:-60, x:-40, rotation:-10, transformOrigin:"50% 50%", duration:.5, ease:"power2.inOut"}}, {a + .9:.2f});')
J(f'tl.from("#s10-ok", {{scale:.3, opacity:0, transformOrigin:"50% 50%", duration:.4, ease:"back.out(2.5)"}}, {a + 1.7:.2f});'); cue(a + 1.7, "ding", .8)
# s11 family code word
a, b = SC["s11"]
J(f'tl.from("#s11-card", {{y:"+=300", opacity:0, rotation:-6, transformOrigin:"50% 50%", duration:.5, ease:"back.out(2)"}}, {a + .05:.2f});'); cue(a + .05, "whoosh", .5)
J(f'tl.from("#s11-dots circle", {{scale:0, transformOrigin:"50% 50%", duration:.25, stagger:.15, ease:"back.out(3)"}}, {a + .7:.2f});'); [cue(a + .7 + i * .15, "pop", .5) for i in range(4)]
J(f'tl.from("#s11-fam g", {{y:80, opacity:0, duration:.35, stagger:.12, ease:"back.out(2)"}}, {a + 1.4:.2f});')
# s12 title + CTA
a, b = SC["s12"]
J(f'tl.from("#s12-moon", {{y:120, opacity:0, duration:.8, ease:"power2.out"}}, {a:.2f});')
J(f'tl.from("#s12-title text", {{y:60, opacity:0, duration:.45, stagger:.2, ease:"back.out(2)"}}, {a + .5:.2f});'); cue(a + .5, "thunder", .4)
J(f'tl.to(".star", {{opacity:.2, duration:.6, stagger:{{each:.05, repeat:3, yoyo:true}}}}, {a:.2f});')
s12, e12 = ln(12)
J(f'tl.from("#s12-cta", {{scale:.4, opacity:0, duration:.4, ease:"back.out(2.5)"}}, {s12 + 2.2:.2f}); tl.to("#s12-cta", {{scale:1.1, duration:.2, yoyo:true, repeat:5}}, {s12 + 2.7:.2f});'); cue(s12 + 2.2, "ding", .8)
J(f'tl.to("#s12-cam, #s12-cta", {{opacity:0, duration:.4}}, {END - .45:.2f});')
# subtitles pop in
for n, (sa, sb, t) in enumerate(SUB):
    if n == 0: continue
    J(f'tl.from("#sub{n:02d} span", {{y:24, opacity:0, scale:.94, duration:.18, ease:"back.out(2)"}}, {sa:.2f});')
# corner Moon: boiling frames 8 fps, pop on each pose change
prev = None; k = 0
while k / 8 < MOON_END:
    t = k / 8; p = pose_at(t)
    J(f'tl.set("#moon .pose img", {{opacity:0}}, {t:.3f}); tl.set("#mp-{p}-{k % 3}", {{opacity:1}}, {t:.3f});')
    if p != prev and k > 0: J(f'tl.fromTo("#moon-in", {{scale:.86, rotation:-4}}, {{scale:1, rotation:0, duration:.3, ease:"back.out(3)", immediateRender:false}}, {t:.3f});')
    prev = p; k += 1
J('tl.from("#moon-in", {y:500, duration:.45, ease:"back.out(1.6)"}, 0.1);'); cue(0.15, "pop", .5)
J(f'tl.to("#moon-in", {{opacity:0, duration:.4}}, {END - .45:.2f});')
a, b = SC["s12"]
J(f'tl.to("#moon-in", {{rotation:3, duration:.35, yoyo:true, repeat:5, ease:"sine.inOut", transformOrigin:"50% 100%"}}, {a + .6:.2f});')
# scene cut whoosh
for k, (a, b) in SC.items():
    if a > 0 and k not in ("s07",): cue(a, "flick", .35)

HTML = f'''<!DOCTYPE html>
<html lang="th"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/lib/gsap.min.js"></script>
<style>
@font-face {{ font-family: KanitX; src: url(assets/fonts/Kanit-ExtraBold.ttf); }}
@font-face {{ font-family: KanitS; src: url(assets/fonts/Kanit-SemiBold.ttf); }}
html, body {{ margin:0; width:1080px; height:1920px; background:#000; overflow:hidden; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:#0E2129; font-family:KanitX, sans-serif; }}
.scene {{ position:absolute; inset:0; overflow:hidden; }}
.cam {{ position:absolute; inset:0; transform-origin:50% 45%; }}
.cam svg {{ display:block; }}
.ui {{ font-family:KanitX; }} .uir {{ font-family:KanitS; }}
.sub {{ position:absolute; left:470px; right:24px; top:1490px; text-align:center; z-index:9; }}
.sub span {{ display:inline-block; color:#fff; font-size:58px; line-height:1.32; word-break:keep-all; text-shadow:0 4px 0 rgba(0,0,0,.55), 0 0 22px rgba(0,0,0,.6); }}
.hl {{ white-space:nowrap; display:inline-block; background:{RED}; color:#fff; padding:0 16px 6px; border-radius:14px; text-shadow:none; }}
.badge {{ position:absolute; left:0; right:0; top:90px; text-align:center; z-index:8; }}
.badge span {{ display:inline-block; background:{YEL}; color:#1E2533; font-size:36px; padding:6px 30px 10px; border-radius:40px; box-shadow:0 6px 0 rgba(0,0,0,.25); }}
.tchip {{ position:absolute; left:60px; top:190px; display:flex; gap:12px; align-items:center; background:rgba(10,24,32,.85); color:#fff; font-family:KanitS; font-size:40px; padding:10px 26px; border-radius:20px; border:3px solid #2B4A55; }}
#moon {{ position:absolute; left:-110px; top:1190px; width:740px; height:740px; z-index:7; }}
#moon-in {{ position:absolute; inset:0; }}
.ring {{ position:absolute; inset:0; }}
.pose {{ position:absolute; inset:0; }}
.pose img {{ position:absolute; width:100%; left:0; top:0; opacity:0; filter:drop-shadow(0 14px 18px rgba(0,0,0,.45)); }}
#s12-moonhost {{ position:absolute; left:250px; top:960px; width:580px; height:580px; }}
#s12-moonhost img {{ width:100%; }}
.cta {{ position:absolute; left:0; right:0; top:860px; text-align:center; }}
.cta span {{ display:inline-block; background:#2ECC71; color:#fff; font-size:72px; padding:8px 60px 16px; border-radius:24px; border:6px solid #fff; }}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
{"".join(secs)}
<div class="clip badge" id="badge" data-start="0" data-duration="{SC['s12'][0]:.2f}" data-track-index="4"><span>CYBER NIGHTMARE · EP1</span></div>
{subs}
{moon}
<audio id="soundtrack" src="assets/audio/derived/soundtrack.wav" data-start="0" data-duration="{END}" data-track-index="9" data-volume="1"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
tl.set({{}}, {{}}, {END});
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>'''
open("index.html", "w").write(HTML)
json.dump(sorted(cues), open("cues.json", "w"))
print("scenes", len(SC), "subs", len(SUB), "cues", len(cues), "dur", END)
