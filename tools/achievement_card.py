"""README용 업적(수상) 카드 SVG 생성기.

사용 예:
    python tools/achievement_card.py --tier encouragement --title 장려상 \
        --desc "KuneKune · 쿠네쿠네를 피해 탈출하는 공포게임" \
        --tags Unity C# --out assets/achievement-kunekune.svg

tier: grand(대상) / gold(최우수상) / silver(우수상) / bronze(장려상) / special(특별상·입선)
"""
import argparse
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pixel as px  # noqa: E402

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


def tag_svg(tags, right=540, top=14):
    """도트 글씨 태그 (2px 단위)."""
    if not tags:
        return ""
    text = "·".join(t.upper() for t in tags)
    tw = px.text_width(text)
    w, h = tw + 10, 11
    x0 = (right // 2) - w
    y0 = top // 2
    cells = px.frame(x0, y0, w, h, px.YELLOW, px.YELLOW, px.YELLOW_D, notch=1)
    cells.update(px.text_cells(text, x0 + 5, y0 + 2, px.INK))
    return px.rects(cells, 2)


def card(tier, title, desc, tags):
    t = TIERS[tier]
    label = escape(f"Achievement unlocked: {title} — {desc}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="104" viewBox="0 0 560 104" shape-rendering="crispEdges" role="img" aria-label="{label}">
  <title>{label}</title>
  <defs>
    <linearGradient id="shine" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="card"><rect x="8" y="8" width="544" height="88"/></clipPath>
  </defs>
  <style>
    .t {{ shape-rendering: auto; font: 700 24px "Pretendard", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", sans-serif; fill: #FFFFFF; }}
    .d {{ shape-rendering: auto; font: 400 13px "Pretendard", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", sans-serif; fill: #C9D3CB; }}
    .sweep {{ animation: sweep 4.5s ease-in-out infinite; }}
    @keyframes sweep {{ 0% {{ transform: translateX(-220px); }} 45%, 100% {{ transform: translateX(600px); }} }}
  </style>
  {px.rects(px.frame(0, 0, 140, 26, "#262E28", t["accent"], px.INK, notch=2), 4)}
  <g clip-path="url(#card)">
    <rect class="sweep" x="0" y="0" width="160" height="104" fill="url(#shine)"/>
  </g>
  {px.rects(px.frame(4, 4, 18, 18, "#3D4B3F", "#4D5E50", "#1C221E", notch=1), 4)}
  <g>
    {trophy_rects(t)}
  </g>
  {px.rects(px.text_cells("ACHIEVEMENT UNLOCKED", 54, 8, t["accent"]), 2)}
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
