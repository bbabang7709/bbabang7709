"""README 섹션 헤더·푸터 SVG 생성기 (assets/header.svg와 같은 스타일).

    python tools/readme_assets.py

어두운 바탕 + 둥근 모서리 + 밝은 글씨 + 테마 3색 포인트.
"""
import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "ui")

BG = "#1C221E"
INK = "#3D4B3F"       # 캐릭터 눈 등 진한 색
TEXT = "#EEF3EC"
MUTED = "#8FA394"
LINE = "#3A453C"
GROUND = "#5C6B5F"
GREEN, GREEN_D = "#A8E6A3", "#74C27A"
YELLOW, YELLOW_D = "#FFE08A", "#E0B84A"
RED, RED_D = "#FF9AA2", "#F2667A"
ACCENTS = [(GREEN, GREEN_D), (YELLOW, YELLOW_D), (RED, RED_D)]

MONO = 'ui-monospace, "SFMono-Regular", Consolas, monospace'
SANS = '"Pretendard", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", sans-serif'


def save(name, data):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("saved", os.path.normpath(path))


# ---------------------------------------------------------------- section headers
SECTIONS = [
    ("profile", "PLAYER PROFILE", "About Me"),
    ("inventory", "INVENTORY", "Tech Stack"),
    ("skill-tree", "SKILL TREE", "What I'm Learning"),
    ("quest-log", "QUEST LOG", "Goals"),
    ("save-files", "SAVE FILES", "Projects"),
    ("achievements", "ACHIEVEMENTS", "Awards"),
    ("stats", "STATS", "GitHub Activity"),
    ("multiplayer", "MULTIPLAYER", "Contact"),
]


def section(i, slug, title, sub):
    fill, stroke = ACCENTS[i % 3]
    stage = f"STAGE {i + 1:02d}"
    label = escape(f"{title} — {sub}")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="64" viewBox="0 0 960 64" role="img" aria-label="{label}">
  <title>{label}</title>
  <style>
    .t {{ font: 700 17px {MONO}; fill: {TEXT}; letter-spacing: 3px; }}
    .s {{ font: 500 13px {SANS}; fill: {MUTED}; }}
    .n {{ font: 700 12px {MONO}; fill: {MUTED}; letter-spacing: 2px; }}
    .hop {{ transform-box: fill-box; transform-origin: 50% 100%; animation: hop 2.4s ease-in-out infinite; }}
    @keyframes hop {{ 0%, 70%, 100% {{ transform: translateY(0); }} 80% {{ transform: translateY(-7px); }} 90% {{ transform: translateY(0) scaleY(.85); }} }}
  </style>
  <rect width="960" height="64" rx="14" fill="{BG}"/>
  <rect class="hop" x="28" y="22" width="20" height="20" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="2"/>
  <text class="t" x="68" y="38" textLength="{len(title) * 13.2 - 3:.0f}" lengthAdjust="spacing">{escape(title)}</text>
  <text class="s" x="{68 + len(title) * 13.2 + 14:.0f}" y="38">{escape(sub)}</text>
  <rect x="68" y="47" width="28" height="2" fill="{stroke}"/>
  <text class="n" x="932" y="37" text-anchor="end">{stage}</text>
</svg>
'''
    save(f"h-{slug}.svg", svg)


# ---------------------------------------------------------------- footer
def footer():
    dashes = "".join(
        f'<rect x="{x}" y="{y}" width="{w}" height="2"/>'
        for k in range(11)
        for x, y, w in ((10 + k * 102, 132, 18), (62 + k * 102, 140, 8))
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="160" viewBox="0 0 960 160" role="img" aria-label="THANKS FOR PLAYING! CONTINUE? YES / NO">
  <title>THANKS FOR PLAYING! CONTINUE? YES / NO</title>
  <style>
    .t {{ font: 700 17px {MONO}; fill: {TEXT}; letter-spacing: 4px; }}
    .c {{ font: 700 14px {MONO}; fill: {MUTED}; letter-spacing: 3px; }}
    .y {{ fill: {RED_D}; }}
    .blink {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 55% {{ opacity: 0; }} }}
    .idle {{ transform-box: fill-box; transform-origin: 50% 100%; animation: idle 1.6s ease-in-out infinite; }}
    @keyframes idle {{ 0%, 100% {{ transform: scaleY(1); }} 50% {{ transform: scaleY(.92); }} }}
    .wave {{ transform-box: fill-box; transform-origin: 0 50%; animation: wave 1.2s ease-in-out infinite alternate; }}
    @keyframes wave {{ from {{ transform: scaleX(1); }} to {{ transform: scaleX(.8); }} }}
  </style>
  <defs><clipPath id="f"><rect width="960" height="160" rx="18"/></clipPath></defs>
  <g clip-path="url(#f)">
    <rect width="960" height="160" fill="{BG}"/>

    <text class="t" x="480" y="52" text-anchor="middle">THANKS FOR PLAYING!</text>
    <text class="c" x="380" y="84" textLength="100" lengthAdjust="spacing">CONTINUE?</text>
    <path class="blink" d="M492 73 l8 5 -8 5 z" fill="{RED_D}"/>
    <text class="c y" x="506" y="84" textLength="31" lengthAdjust="spacing">YES</text>
    <text class="c" x="561" y="84" textLength="20" lengthAdjust="spacing">NO</text>

    <rect x="0" y="120" width="960" height="2" fill="{GROUND}"/>
    <g fill="{LINE}">{dashes}</g>

    <!-- 플레이어: 스테이지를 끝내고 숨 고르는 중 -->
    <ellipse cx="151" cy="122" rx="13" ry="3" fill="#000000" opacity=".35"/>
    <g class="idle">
      <rect x="140" y="96" width="24" height="24" rx="6" fill="{RED}" stroke="{RED_D}" stroke-width="2"/>
      <rect x="154" y="103" width="4" height="7" rx="1" fill="{INK}"/>
      <rect x="144" y="112" width="5" height="3" rx="1.5" fill="#FFFFFF" opacity=".7"/>
    </g>

    <!-- 골인 깃발 -->
    <rect x="806" y="64" width="3" height="56" fill="{MUTED}"/>
    <circle cx="807.5" cy="62" r="4" fill="{YELLOW}" stroke="{YELLOW_D}" stroke-width="1.5"/>
    <path class="wave" d="M809 68 h30 l-8 9 8 9 h-30 z" fill="{GREEN}" stroke="{GREEN_D}" stroke-width="2" stroke-linejoin="round"/>
    <rect x="796" y="114" width="23" height="6" rx="2" fill="{GREEN}" stroke="{GREEN_D}" stroke-width="2"/>
  </g>
</svg>
'''
    save("footer.svg", svg)


if __name__ == "__main__":
    for i, s in enumerate(SECTIONS):
        section(i, *s)
    footer()
