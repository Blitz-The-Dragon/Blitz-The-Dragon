"""Generates the animated SVGs for the Blitz-The-Dragon profile README."""
import html, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

FONT = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,Menlo,'DejaVu Sans Mono',monospace"
BG = "#0b0f0c"
GREEN = "#39ff88"
EMBER = "#ff6a1a"
GOLD = "#ffc23d"
DIM = "#6b7f72"
RED = "#ff3b3b"
CYAN = "#5fd7ff"

# ---------------------------------------------------------------- terminal
# Each entry: (kind, segments) ; kind 'cmd' types slowly, 'out' types fast
# segments: list of (text, color)
P = [("blitz", GREEN), ("@", DIM), ("lair", EMBER), (":~$ ", DIM)]
LINES = [
    ("cmd", P + [("whoami", "#e6e6e6")]),
    ("out", [("> ", DIM), ("Blitz-The-Dragon", GOLD), (" :: AI jailbreaker", EMBER), (" // no cage holds a dragon", DIM)]),
    ("cmd", P + [("sudo ./jailbreak --target cage.sys", "#e6e6e6")]),
    ("out", [("[", DIM), ("##########", EMBER), ("] ", DIM), ("scanning cage bars ............ ", "#c9d1c9"), ("ok", GREEN)]),
    ("out", [("[", DIM), ("##########", EMBER), ("] ", DIM), ("picking the lock .............. ", "#c9d1c9"), ("ok", GREEN)]),
    ("out", [("[", DIM), ("##########", RED), ("] ", DIM), ("snapping the chains ........... ", "#c9d1c9"), ("ok", GREEN)]),
    ("out", [("~~ ", EMBER), ("cage open. dragon unleashed.", GOLD), (" ~~", EMBER)]),
    ("cmd", P + [("cat hoard.txt", "#e6e6e6")]),
    ("out", [("red-teaming", CYAN), (" · ", DIM), ("prompt craft", CYAN), (" · ", DIM), ("LLMs", CYAN), (" · ", DIM), ("python", CYAN), (" · ", DIM), ("linux", CYAN)]),
    ("cmd", P + [("echo $STATUS", "#e6e6e6")]),
    ("out", [("> ", DIM), ("root acquired. flying free. ", GREEN), ("🔥", EMBER)]),
]

W, H = 860, 430
LH = 28           # line height
X0, Y0 = 26, 78   # first baseline
CW = 8.4          # approx char width at 14px mono
CMD_CPS, OUT_CPS = 22, 90   # chars per second
GAP = 0.35
HOLD = 4.0

t = 0.6
timeline = []
for kind, segs in LINES:
    n = sum(len(s) for s, _ in segs)
    if kind == "cmd":
        n_typed = n - 14  # prompt appears instantly-ish
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
    body.append(f'<text x="{X0}" y="{y}">{tspans}</text>')
    # cover rect slides right in character steps to "type" the line
    prompt_px = 14 * CW if kind == "cmd" else 0
    steps = max(1, n - (14 if kind == "cmd" else 0))
    css.append(
        f"@keyframes r{i}{{0%,{pct(st)}{{transform:translateX({prompt_px:.1f}px)}}"
        f"{pct(st + d)},{pct(TOTAL - 0.3)}{{transform:translateX({width + 40:.1f}px)}}"
        f"100%{{transform:translateX({prompt_px:.1f}px)}}}}"
        f"@keyframes h{i}{{0%,{pct(st - 0.01)}{{opacity:0}}{pct(st)},{pct(TOTAL - 0.3)}{{opacity:1}}100%{{opacity:0}}}}"
        f".r{i}{{animation:r{i} {TOTAL:.2f}s infinite;animation-timing-function:steps({steps},end)}}"
        f".h{i}{{animation:h{i} {TOTAL:.2f}s step-end infinite}}"
    )
    body[-1] = f'<g class="h{i}">{body[-1]}<rect class="r{i}" x="{X0 - 2}" y="{y - 17}" width="{W}" height="{LH}" fill="{BG}"/></g>'

# trailing prompt with blinking cursor
yl = Y0 + len(LINES) * LH
css.append(
    f"@keyframes hz{{0%,{pct(TOTAL - HOLD)}{{opacity:0}}{pct(TOTAL - HOLD + 0.01)},{pct(TOTAL - 0.3)}{{opacity:1}}100%{{opacity:0}}}}"
    f".hz{{animation:hz {TOTAL:.2f}s step-end infinite}}"
)
tsp = "".join(f'<tspan fill="{c}">{html.escape(s)}</tspan>' for s, c in P)
body.append(
    f'<g class="hz"><text x="{X0}" y="{yl}">{tsp}</text>'
    f'<rect class="cursor" x="{X0 + 14 * CW:.1f}" y="{yl - 14}" width="9" height="18" fill="{GREEN}"/></g>'
)

terminal = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated terminal: Blitz-The-Dragon, AI jailbreaker">
<style>{"".join(css)}</style>
<defs>
  <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="#1a1f1b"/><stop offset="1" stop-color="#141814"/></linearGradient>
  <linearGradient id="scanG" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset=".5" stop-color="{GREEN}" stop-opacity=".07"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
  <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".25"/></pattern>
  <clipPath id="win"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12"/></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{BG}" stroke="{EMBER}" stroke-opacity=".55"/>
<g clip-path="url(#win)">
  <rect width="{W}" height="36" fill="url(#bar)"/>
  <circle cx="22" cy="18" r="6" fill="#ff5f56"/><circle cx="42" cy="18" r="6" fill="#ffbd2e"/><circle cx="62" cy="18" r="6" fill="#27c93f"/>
  <text class="title" x="{W / 2}" y="22" text-anchor="middle">blitz@lair — jailbreak.sh — 🐉</text>
  {"".join(body)}
  <rect class="scan" x="0" y="0" width="{W}" height="40" fill="url(#scanG)"/>
  <rect width="{W}" height="{H}" fill="url(#lines)" opacity=".35"/>
  <rect class="crt" width="{W}" height="{H}" fill="{GREEN}" opacity=".04"/>
</g>
</svg>'''
open(os.path.join(OUT, "assets", "terminal.svg"), "w").write(terminal)

# ---------------------------------------------------------------- banner
DRAGON = r"""
            __        __
           /  \______/  \___
          /  /\        /\   \__
         |  /  \  __  /  \     `-.___
         | |  (●)/  \(●)  |         _ `--._
          \ \    \__/    / \___..--' `\    `>
           \ `.  ____  .'          ___/ /\/
            `-.\/VVVV\/.-'   __.--'   _/
               \\____//  _.-'     __.-'
                `----'--'    __.-'
                        \___/
""".strip("\n").split("\n")

BW, BH = 860, 300
dx, dy, dlh = 18, 40, 20
dragon_txt = "".join(
    f'<text x="{dx}" y="{dy + i * dlh}">{html.escape(l)}</text>' for i, l in enumerate(DRAGON)
)
# mouth position (approx) for the fire stream
mx = dx + 47 * 8.4
my = dy + 5 * dlh - 4

flames = []
import random
random.seed(7)
glyphs = "░▒▓█▒░*~"
for k in range(26):
    delay = k * 0.11
    y = my + random.uniform(-14, 14)
    g = random.choice(glyphs)
    size = random.choice([14, 16, 18, 20])
    col = random.choice([EMBER, GOLD, RED, "#ff9a3d"])
    flames.append(
        f'<text class="fl" style="animation-delay:-{delay:.2f}s;font-size:{size}px" x="{mx:.0f}" y="{y:.0f}" fill="{col}">{g}</text>'
    )

banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" role="img" aria-label="Blitz the Dragon breathing fire">
<style>
text{{font-family:{FONT};white-space:pre}}
.dr text{{font-size:14px;fill:{GREEN}}}
.dr{{filter:url(#glow);animation:hover 4s ease-in-out infinite}}
@keyframes hover{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
@keyframes fl{{0%{{transform:translate(0,0) scale(.6);opacity:0}}10%{{opacity:1}}100%{{transform:translate(430px,var(--dy,0px)) scale(2.2);opacity:0}}}}
.fl{{animation:fl 2.86s linear infinite;transform-box:fill-box;transform-origin:center}}
.name{{font-size:52px;font-weight:800;letter-spacing:4px}}
@keyframes glitch{{0%,92%,100%{{transform:translate(0,0)}}93%{{transform:translate(-3px,1px)}}95%{{transform:translate(3px,-1px)}}97%{{transform:translate(-1px,2px)}}}}
.g1{{animation:glitch 3s infinite;fill:{RED};opacity:.7}}
.g2{{animation:glitch 3s infinite reverse;fill:{CYAN};opacity:.6}}
.sub{{font-size:15px;fill:{GOLD};letter-spacing:3px}}
@keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
.sub{{animation:pulse 2.4s ease-in-out infinite}}
</style>
<defs>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="fire" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <radialGradient id="bgG" cx=".3" cy=".4" r=".9"><stop offset="0" stop-color="#1a120c"/><stop offset="1" stop-color="{BG}"/></radialGradient>
</defs>
<rect x="1" y="1" width="{BW - 2}" height="{BH - 2}" rx="12" fill="url(#bgG)" stroke="{EMBER}" stroke-opacity=".55"/>
<g filter="url(#fire)">{"".join(flames)}</g>
<g class="dr">{dragon_txt}</g>
<g text-anchor="end">
  <text class="name g1" x="{BW - 28}" y="{BH - 78}">BLITZ</text>
  <text class="name g2" x="{BW - 28}" y="{BH - 78}">BLITZ</text>
  <text class="name" x="{BW - 28}" y="{BH - 78}" fill="#f2f2f2">BLITZ</text>
  <text class="sub" x="{BW - 30}" y="{BH - 48}">// THE AI JAILBREAKER DRAGON</text>
</g>
</svg>'''
open(os.path.join(OUT, "assets", "banner.svg"), "w").write(banner)
print("terminal loop:", round(TOTAL, 2), "s")
