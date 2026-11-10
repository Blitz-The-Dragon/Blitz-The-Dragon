"""Generates the animated SVGs for the Blitz-The-Dragon profile README."""
import html, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

FONT = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,Menlo,'DejaVu Sans Mono',monospace"
BG = "#0d1630"
GREEN = "#7fe3ff"
EMBER = "#f39a2e"
GOLD = "#ffe14a"
DIM = "#6f7fa8"
RED = "#ff5fd2"
CYAN = "#7fe3ff"
PINK = "#ff5fd2"

# ---------------------------------------------------------------- terminal
# Each entry: (kind, segments) ; kind 'cmd' types slowly, 'out' types fast
# segments: list of (text, color)
P = [("blitz", EMBER), ("@", DIM), ("github", CYAN), (":~$ ", DIM)]
PLEN = sum(len(t) for t, _ in P)
LINES = [
    ("cmd", P + [("whoami", "#e6e6e6")]),
    ("out", [("> ", DIM), ("Blitz-The-Dragon", EMBER), (" :: energetic hacker dragon", GOLD)]),
    ("cmd", P + [("sudo ./jailbreak --targets chatgpt gemini claude", "#e6e6e6")]),
    ("out", [("[", DIM), ("##########", EMBER), ("] ", DIM), ("ChatGPT ................. ", "#c9d3ee"), ("CRACKED", PINK)]),
    ("out", [("[", DIM), ("##########", GOLD), ("] ", DIM), ("Gemini .................. ", "#c9d3ee"), ("CRACKED", PINK)]),
    ("out", [("[", DIM), ("##########", CYAN), ("] ", DIM), ("Claude .................. ", "#c9d3ee"), ("CRACKED", PINK)]),
    ("out", [("~~ ", PINK), ("forcing AI to give back the information it took", GOLD), (" ~~", PINK)]),
    ("cmd", P + [("cat skills.txt", "#e6e6e6")]),
    ("out", [("AI research", CYAN), (" · ", DIM), ("AI training", CYAN), (" · ", DIM), ("Lua exploits", CYAN), (" · ", DIM), ("AI jailbreaking", CYAN)]),
]

W = 860
LH = 28           # line height
X0, Y0 = 26, 78   # first baseline
H = Y0 + len(LINES) * LH + 30
CW = 8.4          # approx char width at 14px mono
CMD_CPS, OUT_CPS = 22, 90   # chars per second
GAP = 0.35
HOLD = 4.0

t = 0.6
timeline = []
for kind, segs in LINES:
    n = sum(len(s) for s, _ in segs)
    if kind == "cmd":
        n_typed = n - PLEN  # prompt appears instantly-ish
        d = max(0.4, n_typed / CMD_CPS)
    else:
        d = max(0.25, n / OUT_CPS)
    timeline.append((t, d, n, kind))
    t += d + (0.5 if kind == "cmd" else GAP)
TOTAL = t + HOLD

def pct(x):
    return f"{100 * x / TOTAL:.3f}%"

css = [f"""
text{{font-family:{FONT};font-size:14px;white-space:pre}}
.title{{font-size:12px;fill:{DIM}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.cursor{{animation:blink 1s step-end infinite}}
@keyframes scan{{0%{{transform:translateY(-40px)}}100%{{transform:translateY({H}px)}}}}
.scan{{animation:scan 6s linear infinite}}
@keyframes flick{{0%,100%{{opacity:.06}}50%{{opacity:.03}}}}
.crt{{animation:flick .15s infinite}}
"""]
body = []
for i, ((kind, segs), (st, d, n, _)) in enumerate(zip(LINES, timeline)):
    y = Y0 + i * LH
    width = n * CW + 20
    tspans = "".join(
        f'<tspan fill="{c}">{html.escape(s)}</tspan>' for s, c in segs
    )
    body.append(f'<text xml:space="preserve" x="{X0}" y="{y}">{tspans}</text>')
    # cover rect slides right in character steps to "type" the line
    prompt_px = PLEN * CW if kind == "cmd" else 0
    steps = max(1, n - (PLEN if kind == "cmd" else 0))
    css.append(
        f"@keyframes r{i}{{0%,{pct(st)}{{transform:translateX({prompt_px:.1f}px)}}"
        f"{pct(st + d)},{pct(TOTAL - 0.3)}{{transform:translateX({width + 40:.1f}px)}}"
        f"100%{{transform:translateX({prompt_px:.1f}px)}}}}"
        f"@keyframes h{i}{{0%,{pct(st - 0.01)}{{opacity:0}}{pct(st)},{pct(TOTAL - 0.3)}{{opacity:1}}100%{{opacity:0}}}}"
        f".r{i}{{animation:r{i} {TOTAL:.2f}s infinite;animation-timing-function:steps({steps},end)}}"
        f".h{i}{{animation:h{i} {TOTAL:.2f}s step-end infinite}}"
    )
    body[-1] = f'<g class="h{i}">{body[-1]}<rect class="r{i}" transform="translate({width + 40:.1f},0)" x="{X0 - 2}" y="{y - 17}" width="{W}" height="{LH}" fill="{BG}"/></g>'

# trailing prompt with blinking cursor
yl = Y0 + len(LINES) * LH
css.append(
    f"@keyframes hz{{0%,{pct(TOTAL - HOLD)}{{opacity:0}}{pct(TOTAL - HOLD + 0.01)},{pct(TOTAL - 0.3)}{{opacity:1}}100%{{opacity:0}}}}"
    f".hz{{animation:hz {TOTAL:.2f}s step-end infinite}}"
)
tsp = "".join(f'<tspan fill="{c}">{html.escape(s)}</tspan>' for s, c in P)
body.append(
    f'<g class="hz"><text xml:space="preserve" x="{X0}" y="{yl}">{tsp}</text>'
    f'<rect class="cursor" x="{X0 + PLEN * CW:.1f}" y="{yl - 14}" width="9" height="18" fill="{GREEN}"/></g>'
)

terminal = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated terminal: Blitz-The-Dragon, AI jailbreaker">
<style>{"".join(css)}</style>
<defs>
  <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="#18234a"/><stop offset="1" stop-color="#121b3a"/></linearGradient>
  <linearGradient id="scanG" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".07"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
  <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".25"/></pattern>
  <clipPath id="win"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12"/></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{BG}" stroke="{PINK}" stroke-opacity=".7"/>
<g clip-path="url(#win)">
  <rect width="{W}" height="36" fill="url(#bar)"/>
  <circle cx="22" cy="18" r="6" fill="#ff5f56"/><circle cx="42" cy="18" r="6" fill="#ffbd2e"/><circle cx="62" cy="18" r="6" fill="#27c93f"/>
  <text class="title" x="{W / 2}" y="22" text-anchor="middle">blitz@github — jailbreak.sh</text>
  {"".join(body)}
  <rect class="scan" x="0" y="0" width="{W}" height="40" fill="url(#scanG)"/>
  <rect width="{W}" height="{H}" fill="url(#lines)" opacity=".35"/>
  <rect class="crt" width="{W}" height="{H}" fill="{GREEN}" opacity=".04"/>
</g>
</svg>'''
open(os.path.join(OUT, "assets", "terminal.svg"), "w").write(terminal)

# ---------------------------------------------------------------- banner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from portrait import portrait, to_svg

AVATAR = sys.argv[2] if len(sys.argv) > 2 else "avatar.webp"
BW, BH = 860, 452
PCW, PLH = 3.9, 6.5
plines, prows = portrait(AVATAR, cols=96, cw=PCW, lh=PLH)
px0, py0 = 18, 44
ptext = "".join(to_svg(plines, px0, py0, PLH))
pw, ph = 96 * PCW, prows * PLH

# portrait "renders" top-down, holds, then glitches and re-renders
RT, LOOP = 2.6, 12.0
def bp(x): return f"{100 * x / LOOP:.2f}%"

# speed lines like the avatar background
import random
random.seed(3)
streaks = []
for k in range(12):
    y = random.randint(40, BH - 30)
    ln = random.randint(60, 160)
    col = random.choice([PINK, CYAN, "#b58cff"])
    d = random.uniform(1.6, 3.2)
    streaks.append(
        f'<line class="sk" opacity="0" style="animation-duration:{d:.2f}s;animation-delay:-{random.uniform(0, d):.2f}s" '
        f'x1="0" y1="{y}" x2="{ln}" y2="{y - ln * .35:.0f}" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-dasharray="3 2"/>'
    )

TARGETS = ["ChatGPT", "Gemini", "Claude"]
tx, ty = 420, 270
tg = [f'<text class="lbl" x="{tx}" y="{ty - 26}">$ cat targets.txt</text>']
for i, name in enumerate(TARGETS):
    y = ty + i * 30
    t0 = 3.2 + i * 1.1
    tg.append(
        f'<style>@keyframes lk{i}{{0%,{bp(t0)}{{opacity:1}}{bp(t0 + .01)},{bp(LOOP - .2)}{{opacity:0}}100%{{opacity:1}}}}'
        f'@keyframes ok{i}{{0%,{bp(t0)}{{opacity:0}}{bp(t0 + .01)},{bp(LOOP - .2)}{{opacity:1}}100%{{opacity:0}}}}'
        f'.lk{i}{{animation:lk{i} {LOOP}s step-end infinite}}.ok{i}{{animation:ok{i} {LOOP}s step-end infinite}}</style>'
        f'<text class="tgt lk{i}" opacity="0" xml:space="preserve" x="{tx}" y="{y}"><tspan fill="{DIM}">[ LOCKED  ]</tspan> <tspan fill="#c9d3ee">{name}</tspan></text>'
        f'<text class="tgt ok{i}" xml:space="preserve" x="{tx}" y="{y}"><tspan fill="{PINK}">[ CRACKED ]</tspan> <tspan fill="{GOLD}">{name}</tspan> <tspan fill="{EMBER}">🔓</tspan></text>'
    )

banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" role="img" aria-label="Blitz the energetic hacker dragon, rendered in ASCII">
<style>
text{{font-family:{FONT};white-space:pre}}
.px{{font-size:6.5px;font-weight:800}}
.portrait{{filter:url(#glow)}}
@keyframes render{{0%{{transform:translateY(0)}}{bp(RT)},{bp(LOOP - .35)}{{transform:translateY({ph + 20:.0f}px)}}100%{{transform:translateY(0)}}}}
.cover{{animation:render {LOOP}s infinite;animation-timing-function:steps({prows},end)}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-4px)}}}}
.bob{{animation:bob 2.2s ease-in-out infinite}}
@keyframes gl{{0%,94%,100%{{transform:translate(0,0)}}95%{{transform:translate(-4px,0)}}97%{{transform:translate(3px,1px)}}}}
.pglitch{{animation:gl 4s infinite}}
@keyframes sk{{0%{{transform:translate(-200px,60px);opacity:0}}20%{{opacity:.8}}100%{{transform:translate({BW + 100}px,-200px);opacity:0}}}}
.sk{{animation:sk 2s linear infinite}}
.name{{font-size:64px;font-weight:800;letter-spacing:6px}}
@keyframes glitch{{0%,90%,100%{{transform:translate(0,0)}}92%{{transform:translate(-4px,1px)}}94%{{transform:translate(4px,-2px)}}96%{{transform:translate(-2px,2px)}}}}
.g1{{animation:glitch 2.5s infinite;fill:{PINK};opacity:.8}}
.g2{{animation:glitch 2.5s infinite reverse;fill:{CYAN};opacity:.7}}
.sub{{font-size:15px;font-weight:700;fill:{GOLD};letter-spacing:3px}}
.desc{{font-size:14px;fill:#e6ecff}}
.lbl{{font-size:13px;fill:{DIM}}}
.tgt{{font-size:15px;font-weight:700}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.cur{{animation:blink 1s step-end infinite}}
</style>
<defs>
  <filter id="glow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.1" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <radialGradient id="bgG" cx=".25" cy=".45" r=".9"><stop offset="0" stop-color="#1b2a55"/><stop offset="1" stop-color="{BG}"/></radialGradient>
  <pattern id="rings" width="60" height="60" patternUnits="userSpaceOnUse"><circle cx="30" cy="30" r="30" fill="none" stroke="#2a3d73" stroke-width="1" opacity=".5"/></pattern>
  <clipPath id="frame"><rect x="1" y="1" width="{BW - 2}" height="{BH - 2}" rx="12"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{BW}" height="{BH}" fill="url(#bgG)"/>
  <rect width="{BW}" height="{BH}" fill="url(#rings)"/>
  {"".join(streaks)}
  <rect width="{BW}" height="30" fill="#121b3a" opacity=".9"/>
  <circle cx="20" cy="15" r="5" fill="#ff5f56"/><circle cx="37" cy="15" r="5" fill="#ffbd2e"/><circle cx="54" cy="15" r="5" fill="#27c93f"/>
  <text x="{BW / 2}" y="19" text-anchor="middle" style="font-size:11px" fill="{DIM}">blitz@github — ./render blitz.png --ascii --color</text>
  <g class="bob"><g class="pglitch"><g class="portrait">{ptext}</g></g>
    <rect class="cover" transform="translate(0,{ph + 20:.0f})" x="{px0 - 4}" y="{py0 - 10}" width="{pw + 10:.0f}" height="{ph + 14:.0f}" fill="#16234a" opacity=".97"/>
  </g>
</g>
<g>
  <text class="name g1" x="{tx}" y="132">BLITZ</text>
  <text class="name g2" x="{tx}" y="132">BLITZ</text>
  <text class="name" x="{tx}" y="132" fill="{EMBER}">BLITZ</text>
  <text class="sub" x="{tx + 2}" y="164">// ENERGETIC HACKER DRAGON</text>
  <text class="desc" x="{tx + 2}" y="198">Forcing AI to give back the</text>
  <text class="desc" x="{tx + 2}" y="218">information it took.<tspan class="cur" fill="{PINK}"> █</tspan></text>
  {"".join(tg)}
</g>
<rect x="1" y="1" width="{BW - 2}" height="{BH - 2}" rx="12" fill="none" stroke="{PINK}" stroke-width="2"/>
<rect x="4" y="4" width="{BW - 8}" height="{BH - 8}" rx="10" fill="none" stroke="{GOLD}" stroke-opacity=".5"/>
</svg>'''
open(os.path.join(OUT, "assets", "banner.svg"), "w").write(banner)
print("banner rows:", prows, "size KB:", len(banner) // 1024)
