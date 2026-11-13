"""USBasp V6 PCB placement (planning data). Board 84 x 32 mm, origin lower-left, y up, mm.
ref -> (x_center, y_center, width, height, rotation). Sizes are estimates, NOT EasyEDA footprints.
Every block has a fixed rectangle (its top-silkscreen box); parts must lie inside their own rectangle.
Signal flow left to right: USB-C -> V-USB -> ATmega8A -> level shifter -> ISP headers on the right edge."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import REF_SEC

BOARD_W, BOARD_H = 84.0, 32.0
HOLES = [(3.5, 3.5), (3.5, 28.5)]
R1206 = (4.6, 2.6)
C0805 = (3.0, 1.8)
S603 = (2.6, 1.6)
SOT6 = (3.4, 3.2)
L = {}


def put(ref, x, y, w, h, rot=0):
    L[ref] = (x, y, w, h, rot)


def small(ref, x, y, size=R1206, rot=0):
    put(ref, x, y, size[0], size[1], rot)


# ---- USB-C (left edge)
put("J1", 3.75, 16, 7.5, 9)
put("U2", 11.5, 16, *SOT6)
small("R1", 11.5, 20.4)
small("R2", 11.5, 11.6)
small("F1", 11.5, 23.4)
small("C2", 11.5, 8.8)
# ---- V-USB interface
small("R3", 18.5, 19.5)
put("D1", 23.9, 19.5, 3.8, 1.8)
small("R4", 18.5, 12.5)
put("D2", 23.9, 12.5, 3.8, 1.8)
small("R5", 18.5, 8.6)
small("C1", 18.5, 24.4)
# ---- ATmega8A core
put("U1", 37, 16, 9.2, 9.2)
put("Y1", 29.6, 12.6, 2.7, 3.4)
small("C3", 29.6, 9.0, C0805)
small("C4", 29.6, 16.4, C0805)
small("C5", 37.6, 23.0)
small("C7", 42.6, 23.0)
small("R6", 31.0, 23.0)
small("C6", 37.0, 9.0)
put("LED1", 31, 26.8, *S603)
small("R7", 36, 26.8)
put("LED2", 31, 29.6, *S603)
small("R8", 36, 29.6)
put("J4", 37.5, 3.6, 7.6, 5.1)
put("JP2", 29.8, 4.0, 5.1, 2.5)
# ---- level shifter
put("U4", 50.2, 10.2, 6.6, 8.4)
small("C10", 50.2, 16.6)
put("U5", 55.6, 16.4, 2.6, 2.6)
small("R10", 55.6, 11.6, rot=90)
small("R11", 55.6, 5.0, rot=90)
small("C12", 59.4, 16.0, rot=90)
small("R12", 59.4, 9.6, rot=90)
small("R13", 59.4, 3.6, rot=90)
small("C13", 63.0, 16.0, rot=90)
small("C11", 63.0, 9.6, rot=90)
# ---- target power
put("U3", 48.8, 29.2, 3.0, 3.0)
small("C8", 53.4, 29.2)
small("C9", 58.2, 29.2)
put("LED3", 48.6, 25.4, *S603)
small("R9", 53.4, 25.4)
small("F2", 58.2, 25.4)
put("JP1", 51.0, 21.7, 7.6, 2.5)
# ---- ISP headers (right edge)
put("J2", 79.05, 16, 8.9, 20.3)
put("J3", 68.4, 16, 5.1, 7.6)

# id, title, colour, refs, (x0, y0, x1, y1) silkscreen rectangle
BLOCKS = [
    ("usb", "USB-C", "#4895ef", ["J1", "U2", "R1", "R2", "F1", "C2"], (0.0, 7.4, 14.6, 24.8)),
    ("vusb", "V-USB", "#8e24aa", ["R3", "D1", "R4", "D2", "R5", "C1"], (15.4, 6.0, 26.6, 27.0)),
    ("mcu", "ATMEGA8A", "#a66cff", ["U1", "Y1", "C3", "C4", "C5", "C6", "C7", "R6", "LED1", "R7", "LED2", "R8", "J4", "JP2"], (27.2, 0.6, 46.0, 31.4)),
    ("shift", "LEVEL SHIFT", "#00bcd4", ["U4", "C10", "U5", "R10", "R11", "C12", "R12", "R13", "C13", "C11"], (46.6, 0.6, 64.4, 19.0)),
    ("tpwr", "TARGET POWER", "#ff9f43", ["U3", "C8", "C9", "LED3", "R9", "F2", "JP1"], (46.6, 19.6, 64.4, 31.4)),
    ("isp", "ISP 10 / 6 PIN", "#2fbf71", ["J2", "J3"], (65.0, 4.0, 83.6, 28.0)),
]
REF_BLOCK = {r: b[0] for b in BLOCKS for r in b[3]}


def rect(v):
    x, y, w, h, r = v
    if r in (90, 270):
        w, h = h, w
    return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)


def box_of(block_id):
    return [b for b in BLOCKS if b[0] == block_id][0][4]


def check():
    prob = []
    rs = {k: rect(v) for k, v in L.items()}
    keys = list(rs)
    edge = {"J1", "J2"}
    for i in range(len(keys)):
        a = rs[keys[i]]
        inside = a[0] >= 0.5 and a[1] >= 0.5 and a[2] <= BOARD_W - 0.5 and a[3] <= BOARD_H - 0.5
        on_board = a[0] >= -0.01 and a[1] >= -0.01 and a[2] <= BOARD_W + 0.01 and a[3] <= BOARD_H + 0.01
        if not inside and not (keys[i] in edge and on_board):
            prob.append(f"{keys[i]} outside board {tuple(round(t, 1) for t in a)}")
        for j in range(i + 1, len(keys)):
            b = rs[keys[j]]
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 0.2 and oy > 0.2:
                prob.append(f"overlap {keys[i]} / {keys[j]} ({ox:.1f} x {oy:.1f})")
        for (hx, hy) in HOLES:
            cx = min(max(hx, a[0]), a[2])
            cy = min(max(hy, a[1]), a[3])
            if (cx - hx) ** 2 + (cy - hy) ** 2 < 3.4 ** 2:
                prob.append(f"{keys[i]} touches mounting hole at ({hx},{hy})")
    for r in REF_SEC:
        if r not in L:
            prob.append(f"part {r} has no placement")
    for ref, a in rs.items():
        if ref not in REF_BLOCK:
            prob.append(f"part {ref} is in no block")
            continue
        own = box_of(REF_BLOCK[ref])
        if a[0] < own[0] - 0.01 or a[1] < own[1] - 0.01 or a[2] > own[2] + 0.01 or a[3] > own[3] + 0.01:
            prob.append(f"part {ref} sticks out of its silkscreen box ({REF_BLOCK[ref]})")
        for b in BLOCKS:
            if b[0] == REF_BLOCK[ref]:
                continue
            bx = b[4]
            ox = min(a[2], bx[2]) - max(a[0], bx[0])
            oy = min(a[3], bx[3]) - max(a[1], bx[1])
            if ox > 0.05 and oy > 0.05:
                prob.append(f"part {ref} lies inside the silkscreen box of {b[0]}")
    ids = [b[0] for b in BLOCKS]
    for i in range(len(ids)):
        bi = box_of(ids[i])
        for (hx, hy) in HOLES:
            cx = min(max(hx, bi[0]), bi[2])
            cy = min(max(hy, bi[1]), bi[3])
            if (cx - hx) ** 2 + (cy - hy) ** 2 < 3.4 ** 2:
                prob.append(f"silkscreen box {ids[i]} touches a mounting hole")
        for j in range(i + 1, len(ids)):
            a, b = bi, box_of(ids[j])
            if min(a[2], b[2]) - max(a[0], b[0]) > -0.3 and min(a[3], b[3]) - max(a[1], b[1]) > -0.3:
                prob.append(f"silkscreen boxes {ids[i]} / {ids[j]} overlap or are closer than 0.3 mm")
    return prob


if __name__ == "__main__":
    pr = check()
    print(len(L), "parts,", len(BLOCKS), "blocks,", len(pr), "problems")
    for p in pr:
        print(" ", p)
