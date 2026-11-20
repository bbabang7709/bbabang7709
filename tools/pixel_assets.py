"""README 도트 그래픽 에셋 생성기.

    python tools/pixel_assets.py

assets/pixel/ 아래에 섹션 헤더, 푸터 SVG를 만든다.
"""
import os

import pixel as px

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "pixel")
U = 4  # 도트 1칸 = 4px


def svg(w, h, body, css, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * U}" height="{h * U}" '
            f'viewBox="0 0 {w * U} {h * U}" shape-rendering="crispEdges" role="img" aria-label="{label}">\n'
            f'<title>{label}</title>\n<style>{css}</style>\n{body}\n</svg>\n')


def save(name, data):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("saved", os.path.normpath(path), f"{len(data) // 1024}KB")


def sky(w, h, bands):
    """계단식 하늘 + 경계 디더링."""
    cells = {}
    y = 0
    for i, (color, height) in enumerate(bands):
        for yy in range(y, min(y + height, h)):
            for x in range(w):
                cells[(x, yy)] = color
        if i + 1 < len(bands):          # 다음 색과의 경계에 체커 디더
            nxt = bands[i + 1][0]
            for x in range(0, w, 2):
                cells[(x + (y + height) % 2, y + height - 1)] = nxt
        y += height
    return cells


def ground(w, top, h):
    cells = {}
    for x in range(w):
        cells[(x, top)] = px.GREEN if x % 5 else px.GREEN_D
        cells[(x, top + 1)] = px.GREEN_D
        cells[(x, top + 2)] = px.GREEN_D
        cells[(x, top + 3)] = px.GREEN_DD
        for y in range(top + 4, h):
            cells[(x, y)] = px.DIRT
    # 풀잎 & 흙 무늬
    for x in range(3, w, 9):
        cells[(x, top - 1)] = px.GREEN_D
        cells[(x + 1, top - 2)] = px.GREEN
    for i, x in enumerate(range(4, w, 11)):
        yy = top + 6 + (i * 3) % (h - top - 7)
        cells[(x, yy)] = px.DIRT_D
        cells[(x + 1, yy)] = px.DIRT_D
        cells[(x + 5, yy + 2 if yy + 2 < h else yy)] = px.DIRT_L
    return cells


def flowers(xs, top):
    cells = {}
    for i, x in enumerate(xs):
        petal = px.RED if i % 2 else px.YELLOW
        cells[(x, top - 3)] = petal
        cells[(x - 1, top - 2)] = petal
        cells[(x + 1, top - 2)] = petal
        cells[(x, top - 2)] = px.WHITE
        cells[(x, top - 1)] = px.GREEN_DD
    return cells


# ---------------------------------------------------------------- section headers
HEADERS = [
    ("profile", "PLAYER PROFILE", "01", px.GREEN),
    ("inventory", "INVENTORY", "02", px.YELLOW),
    ("skill-tree", "SKILL TREE", "03", px.RED),
    ("quest-log", "QUEST LOG", "04", px.GREEN),
    ("save-files", "SAVE FILES", "05", px.YELLOW),
    ("achievements", "ACHIEVEMENTS", "06", px.RED),
    ("stats", "STATS", "07", px.GREEN),
    ("multiplayer", "MULTIPLAYER", "08", px.YELLOW),
]


def header(slug, title, stage, accent):
    W, H = 200, 15
    cells = px.frame(0, 0, W, H, px.WINDOW, accent, px.INK, notch=2)
    cells.update(px.text_cells(title, 14, 4, px.WHITE))
    label = f"STAGE {stage}"
    cells.update(px.text_cells(label, W - 6 - px.text_width(label), 4, accent))
    body = px.rects(cells, U) + px.rects(px.text_cells(">", 5, 4, px.RED_D), U, "blink")
    css = ".blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{60%{opacity:0}}"
    save(f"h-{slug}.svg", svg(W, H, body, css, f"{title} — STAGE {stage}"))


# ---------------------------------------------------------------- footer
def footer():
    W, H, G = 240, 38, 28
    body = [px.rects(sky(W, G, [("#EAF8E2", 14), ("#F6FBE4", 14)]), U)]
    body.append(px.rects(ground(W, G, H), U))
    body.append(px.rects(flowers([20, 60, 170, 214], G), U))

    t = "THANKS FOR PLAYING!"
    tx = (W - px.text_width(t)) // 2
    body.append(px.rects(px.text_cells(t, tx, 5, px.INK), U))
    q = "CONTINUE?   YES   NO"
    qx = (W - px.text_width(q)) // 2
    body.append(px.rects(px.text_cells(q, qx, 16, px.RED_D), U))
    yes_x = qx + 12 * px.ADV
    body.append(px.rects(px.text_cells(">", yes_x - 8, 16, px.INK), U, "blink"))
    for i, x in enumerate((8, 30, 202, 224)):
        body.append(px.rects(px.coin(x, 14 + (i % 2) * 2), U, "spin"))

    css = """
.blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{60%{opacity:0}}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 1.2s steps(1) infinite}
@keyframes spin{25%{transform:scaleX(.6)}50%{transform:scaleX(.2)}75%{transform:scaleX(.6)}}
"""
    save("footer.svg", svg(W, H, "\n".join(body), css, "THANKS FOR PLAYING! CONTINUE? YES / NO"))


if __name__ == "__main__":
    for h in HEADERS:
        header(*h)
    footer()
