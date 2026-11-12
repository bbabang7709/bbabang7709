"""README용 업적(수상) 카드 SVG 생성기.

사용 예:
    python tools/achievement_card.py --tier encouragement --title 장려상 \
        --desc "KuneKune · 쿠네쿠네를 피해 탈출하는 공포게임" \
        --tags Unity C# --out assets/achievement-kunekune.svg

tier: grand(대상) / gold(최우수상) / silver(우수상) / bronze(장려상) / special(특별상·입선)
"""
import argparse
from xml.sax.saxutils import escape

# 16x16 픽셀 트로피. '#' 본체, 'S' 장식(별) 자리
TROPHY = [
    "................",
    "..############..",
    ".#.####SS####.#.",
    ".#.###SSSS###.#.",
    ".#.####SS####.#.",
    "..#.########.#..",
    "....########....",
    ".....######.....",
    "......####......",
    ".......##.......",
    ".......##.......",
    ".....######.....",
    "....########....",
    "....########....",
    "................",
    "................",
]

# 상 종류별 색: (하이라이트, 본체, 그림자, 카드 테두리, 장식 표시 여부)
TIERS = {
    "grand":   dict(hi="#FFF6CC", base="#FFD966", shade="#E0A93A", accent="#FFD966", star="#FF8FA3", sparkle=True),
    "gold":    dict(hi="#FFF3C4", base="#FFE08A", shade="#E0B84A", accent="#FFE08A", star=None, sparkle=False),
    "silver":  dict(hi="#FFFFFF", base="#DDE5EE", shade="#A9B6C6", accent="#C9D4E2", star=None, sparkle=False),
    "bronze":  dict(hi="#FBE0CC", base="#EDB48E", shade="#C98A62", accent="#EDB48E", star=None, sparkle=False),
    "special": dict(hi="#E6F8E1", base="#A8E6A3", shade="#74C27A", accent="#A8E6A3", star=None, sparkle=False),
}

S = 3          # 픽셀 1칸 크기(px)
BOX = (16, 16, 72)   # 아이콘 칸 x, y, 크기


def trophy_rects(t):
    cells = [(x, y, ch) for y, row in enumerate(TROPHY) for x, ch in enumerate(row) if ch != "."]
    xs = [x for x, _, _ in cells]
    ys = [y for _, y, _ in cells]
    w = (max(xs) - min(xs) + 1) * S
    h = (max(ys) - min(ys) + 1) * S
    cx = BOX[0] + BOX[2] / 2
    cy = BOX[1] + BOX[2] / 2
    ox = cx - w / 2 - min(xs) * S
    oy = cy - h / 2 - min(ys) * S
    out = []
    for x, y, ch in cells:
        if ch == "S":
            col = t["star"] or t["base"]
        elif y == 1 or (x in (3, 4) and 2 <= y <= 4) or (y in (12, 13) and x == 4):
            col = t["hi"]
        elif x in (1, 14) or (y == 5 and x in (2, 13)) or (11 <= x <= 12 and 2 <= y <= 8) \
                or y == 13 or (x == 8 and 6 <= y <= 10):
            col = t["shade"]
        else:
            col = t["base"]
        out.append(f'<rect x="{ox + x * S:g}" y="{oy + y * S:g}" width="{S}" height="{S}" fill="{col}"/>')
    if t["sparkle"]:
        for sx, sy in ((24, 24), (78, 30), (76, 74)):
            out.append(f'<rect x="{sx - 1}" y="{sy - 4}" width="2" height="8" fill="{t["hi"]}"/>')
            out.append(f'<rect x="{sx - 4}" y="{sy - 1}" width="8" height="2" fill="{t["hi"]}"/>')
    return "\n    ".join(out)


def tag_svg(tags, right=540, top=15):
    if not tags:
        return ""
    text = " · ".join(t.upper() for t in tags)
    width = round(len(text) * 6.4 + 20)
    x = right - width
    return (f'<rect x="{x}" y="{top}" width="{width}" height="20" rx="10" fill="#FFE08A"/>\n'
            f'  <text class="tag" x="{x + width / 2:g}" y="{top + 10}" text-anchor="middle" '
            f'dominant-baseline="central">{escape(text)}</text>')


def card(tier, title, desc, tags):
    t = TIERS[tier]
    label = escape(f"Achievement unlocked: {title} — {desc}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="104" viewBox="0 0 560 104" role="img" aria-label="{label}">
  <title>{label}</title>
  <defs>
    <linearGradient id="shine" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="card"><rect x="2" y="2" width="556" height="100" rx="12"/></clipPath>
  </defs>
  <style>
    .k {{ font: 700 11px ui-monospace, "SFMono-Regular", Consolas, monospace; letter-spacing: 2.2px; fill: {t["accent"]}; }}
    .t {{ font: 700 24px "Pretendard", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", sans-serif; fill: #FFFFFF; }}
    .d {{ font: 400 13px "Pretendard", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", sans-serif; fill: #C9D3CB; }}
    .tag {{ font: 700 10px ui-monospace, Consolas, monospace; letter-spacing: 0.3px; fill: #3D4B3F; }}
    .sweep {{ animation: sweep 4.5s ease-in-out infinite; }}
    @keyframes sweep {{ 0% {{ transform: translateX(-220px); }} 45%, 100% {{ transform: translateX(600px); }} }}
  </style>
  <rect x="2" y="2" width="556" height="100" rx="12" fill="#262E28" stroke="{t["accent"]}" stroke-opacity="0.6" stroke-width="2"/>
  <g clip-path="url(#card)">
    <rect class="sweep" x="0" y="0" width="160" height="104" fill="url(#shine)"/>
  </g>
  <rect x="{BOX[0]}" y="{BOX[1]}" width="{BOX[2]}" height="{BOX[2]}" rx="10" fill="#3D4B3F"/>
  <g shape-rendering="crispEdges">
    {trophy_rects(t)}
  </g>
  <text class="k" x="108" y="29">ACHIEVEMENT UNLOCKED</text>
  <text class="t" x="108" y="59">{escape(title)}</text>
  <text class="d" x="108" y="81">{escape(desc)}</text>
  {tag_svg(tags)}
</svg>
'''


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", choices=TIERS, required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--desc", required=True)
    ap.add_argument("--tags", nargs="*", default=[])
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(card(a.tier, a.title, a.desc, a.tags))
    print("saved", a.out)
