"""Procedurally draws the Magos Biologis player sprite sheet.

Output: public/assets/sprites/magos-biologis.png
Layout: 32x32 cells, one clip per row (idle, run, jump, fall), facing right,
feet anchored to the bottom row of each cell.

Run: python3 tools/sprites/magos_biologis.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw

CELL = 32
COLS = 6
CLIPS = [("idle", 4), ("run", 6), ("jump", 2), ("fall", 2)]

OUTLINE = (22, 10, 10, 255)
ROBE_D = (90, 10, 0, 255)
ROBE_M = (139, 42, 42, 255)
ROBE_L = (176, 65, 58, 255)
IRON_D = (26, 26, 26, 255)
IRON_M = (58, 58, 58, 255)
IRON_L = (96, 96, 96, 255)
BRASS_D = (184, 134, 11, 255)
BRASS_L = (212, 175, 55, 255)
FACE = (8, 8, 8, 255)
GREEN_D = (13, 90, 42, 255)
GREEN_M = (31, 168, 74, 255)
GREEN_L = (57, 255, 106, 255)
GREEN_EYE = (150, 255, 170, 255)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(4))


def draw_leg(d, hip, foot, color):
    d.line([hip, foot], fill=color, width=2)
    fx, fy = foot
    d.rectangle([fx - 1, fy - 1, fx + 2, fy], fill=IRON_D)
    d.point((fx + 2, fy - 1), fill=IRON_M)


def draw_mechadendrite(d, base, ctrl, tip, glow):
    pts = []
    for i in range(11):
        t = i / 10
        x = (1 - t) ** 2 * base[0] + 2 * (1 - t) * t * ctrl[0] + t ** 2 * tip[0]
        y = (1 - t) ** 2 * base[1] + 2 * (1 - t) * t * ctrl[1] + t ** 2 * tip[1]
        pts.append((round(x), round(y)))
    d.line(pts, fill=IRON_M, width=1)
    for p in pts[2:-1:3]:
        d.point(p, fill=BRASS_D)
    tx, ty = tip
    d.point((tx + 1, ty - 1), fill=IRON_L)
    d.point((tx + 1, ty + 1), fill=IRON_L)
    d.point((tx + 2, ty), fill=lerp(GREEN_M, GREEN_L, glow))
    d.point((tx + 3, ty), fill=GREEN_L)


def draw_frame(p):
    img = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    dy = p["dy"]
    glow = p["glow"]

    # mechadendrite (behind body), rooted on the bio-tank
    draw_mechadendrite(d, (9, 11 + dy), p["mech_ctrl"], p["mech_tip"], glow)

    # back arm (behind body)
    sx, sy = 13, 15 + dy
    ang = math.radians(p["arm_back"])
    hx, hy = sx + round(5 * math.sin(ang)), sy + round(5 * math.cos(ang))
    d.line([(sx, sy), (hx, hy)], fill=ROBE_D, width=2)
    d.point((hx, hy + 1), fill=IRON_M)

    # legs
    for hip, foot, col in p["legs"]:
        draw_leg(d, (hip[0], hip[1] + dy), (foot[0], foot[1]), col)

    # robe body: shoulders -> flared hem
    hem_y = 25 + dy + p["hem_lift"]
    sway = p["hem_sway"]
    robe = [(11, 13 + dy), (20, 13 + dy), (21 + sway, hem_y), (10 + sway, hem_y)]
    d.polygon(robe, fill=ROBE_M)
    d.line([(12, 12 + dy), (10 + sway, hem_y)], fill=ROBE_D)
    d.line([(13, 13 + dy), (11 + sway, hem_y)], fill=ROBE_D)
    d.line([(18, 13 + dy), (20 + sway, hem_y - 1)], fill=ROBE_L)
    # tattered hem
    for x in range(10 + sway, 22 + sway, 3):
        d.point((x, hem_y + 1), fill=ROBE_D)
        d.point((x + 1, hem_y + 1), fill=ROBE_M)
    # mantle with brass shoulder trim
    d.line([(11, 13 + dy), (20, 13 + dy)], fill=ROBE_L)
    d.line([(11, 14 + dy), (20, 14 + dy)], fill=BRASS_D)
    d.point((19, 14 + dy), fill=BRASS_L)
    # brass belt with cog buckle
    by = 18 + dy
    d.line([(11, by), (20, by)], fill=BRASS_D)
    d.point((17, by), fill=BRASS_L)
    d.point((17, by - 1), fill=BRASS_D)
    d.point((17, by + 1), fill=BRASS_D)
    # sample vials on the belt
    d.line([(14, by + 1), (14, by + 3)], fill=lerp(GREEN_D, GREEN_L, glow * 0.7))
    d.line([(19, by + 1), (19, by + 2)], fill=lerp(GREEN_D, GREEN_M, glow))

    # bio-tank on the back
    d.rectangle([6, 10 + dy, 10, 20 + dy], fill=IRON_M)
    d.line([(6, 10 + dy), (6, 20 + dy)], fill=IRON_D)
    d.rectangle([7, 12 + dy, 9, 18 + dy], fill=lerp(GREEN_M, GREEN_L, glow))
    d.line([(7, 12 + dy), (7, 18 + dy)], fill=GREEN_D)
    bubble = 17 - p["bubble"]
    d.point((9, bubble + dy), fill=(220, 255, 225, 255))
    d.line([(6, 10 + dy), (10, 10 + dy)], fill=BRASS_L)
    d.line([(6, 20 + dy), (10, 20 + dy)], fill=BRASS_D)

    # hood
    hood = [(13, 4 + dy), (17, 3 + dy), (20, 5 + dy), (21, 9 + dy), (20, 12 + dy), (12, 12 + dy), (11, 8 + dy)]
    d.polygon(hood, fill=ROBE_M)
    d.line([(12, 6 + dy), (11, 9 + dy), (12, 12 + dy)], fill=ROBE_D)
    d.line([(14, 4 + dy), (17, 3 + dy)], fill=ROBE_L)
    # face opening + optics
    d.rectangle([17, 6 + dy, 20, 10 + dy], fill=FACE)
    d.point((19, 7 + dy), fill=GREEN_EYE)
    d.point((20, 7 + dy), fill=lerp(GREEN_M, GREEN_L, glow))
    d.point((18, 9 + dy), fill=IRON_M)
    d.point((19, 10 + dy), fill=IRON_L)
    # brass cowl trim
    d.line([(16, 5 + dy), (17, 11 + dy)], fill=BRASS_D)

    # front arm with sleeve and scalpel-claw
    sx, sy = 17, 13 + dy
    ang = math.radians(p["arm_front"])
    ex, ey = sx + round(4 * math.sin(ang)), sy + round(4 * math.cos(ang))
    ang2 = math.radians(p["arm_front"] + p["forearm"])
    hx, hy = ex + round(3 * math.sin(ang2)), ey + round(3 * math.cos(ang2))
    d.line([(sx, sy), (ex, ey)], fill=ROBE_L, width=2)
    d.line([(ex, ey), (hx, hy)], fill=ROBE_M, width=2)
    d.point((hx, hy), fill=IRON_L)
    d.point((hx + 1, hy), fill=IRON_M)
    d.point((hx + 2, hy - 1), fill=lerp(BRASS_D, GREEN_L, glow * 0.5))
    return img


def outline(img):
    px = img.load()
    out = img.copy()
    opx = out.load()
    for y in range(CELL):
        for x in range(CELL):
            if px[x, y][3]:
                continue
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < CELL and 0 <= ny < CELL and px[nx, ny][3]:
                    opx[x, y] = OUTLINE
                    break
    return out


def anchor_feet(img):
    """Shift the frame down so its lowest opaque pixel sits on the bottom row."""
    bbox = img.getbbox()
    if not bbox:
        return img
    shift = CELL - bbox[3]
    if shift == 0:
        return img
    out = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    out.paste(img, (0, shift))
    return out


def base_legs(back_hip_x=14, front_hip_x=17, hip_y=23):
    return [((back_hip_x, hip_y), (back_hip_x, 29), ROBE_D),
            ((front_hip_x, hip_y), (front_hip_x, 29), IRON_M)]


def idle(i):
    glow = 0.5 + 0.5 * math.sin(i / 4 * 2 * math.pi)
    dy = [0, 0, 1, 1][i]
    sway = [0, 1, 1, 0][i]
    legs = base_legs()
    # legs stay planted while body bobs: feet are absolute, hips move with dy
    return dict(dy=dy, glow=glow, legs=legs, hem_lift=0, hem_sway=0,
                arm_back=10, arm_front=20, forearm=50,
                mech_ctrl=(12, -3 + dy), mech_tip=(23 + sway, 3 + dy + sway), bubble=i)


def run(i):
    t = i / 6 * 2 * math.pi
    glow = 0.6 + 0.4 * math.sin(t * 2)
    dy = [0, -1, -1, 0, -1, -1][i]
    stride = math.sin(t)
    lift_a = max(0.0, math.cos(t))
    lift_b = max(0.0, -math.cos(t))
    back = ((15, 22), (15 - round(stride * 4), 29 - round(lift_a * 2)), ROBE_D)
    front = ((17, 22), (17 + round(stride * 4), 29 - round(lift_b * 2)), IRON_M)
    return dict(dy=dy, glow=glow, legs=[back, front], hem_lift=-1, hem_sway=-1,
                arm_back=-30 * stride, arm_front=60 * stride + 20, forearm=60,
                mech_ctrl=(9, -2 + dy), mech_tip=(20 - i % 2, 2 + dy), bubble=(i * 2) % 5)


def jump(i):
    legs = [((14, 22), (12, 27 - i), ROBE_D), ((17, 22), (20, 26 - i), IRON_M)]
    return dict(dy=-1, glow=1.0, legs=legs, hem_lift=-2, hem_sway=-1,
                arm_back=150, arm_front=140, forearm=-30,
                mech_ctrl=(8, 0), mech_tip=(16, 0 + i), bubble=4)


def fall(i):
    legs = [((14, 22), (13, 29), ROBE_D), ((17, 22), (19, 28 + i), IRON_M)]
    return dict(dy=0, glow=0.7, legs=legs, hem_lift=-3 - i, hem_sway=1,
                arm_back=120, arm_front=110 + 10 * i, forearm=20,
                mech_ctrl=(10, -4), mech_tip=(23, 1 + i), bubble=1 + i)


POSES = {"idle": idle, "run": run, "jump": jump, "fall": fall}


def main():
    sheet = Image.new("RGBA", (CELL * COLS, CELL * len(CLIPS)), (0, 0, 0, 0))
    for row, (name, count) in enumerate(CLIPS):
        for col in range(count):
            frame = anchor_feet(outline(draw_frame(POSES[name](col))))
            sheet.paste(frame, (col * CELL, row * CELL))
    out = Path(__file__).resolve().parents[2] / "public/assets/sprites/magos-biologis.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"wrote {out} ({sheet.width}x{sheet.height})")


if __name__ == "__main__":
    main()
