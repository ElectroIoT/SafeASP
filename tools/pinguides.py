"""Footprint-style pin guides for SafeASP (USBasp V6): U1 ATmega8A TQFP-32 (top view, pad numbers from the Microchip datasheet figure 1-1)
and pin tables for U4 74LVC8T245PW, U5 74LVC1T45GW and J1 USB-C. Used by gen_docs.py (schematic page)."""
import html
import data as D

e = html.escape
INK, MUTE = "var(--ink)", "var(--mute)"
COL = {"gnd": "#475569", "pwr": "#ea580c", "usb": "#8e24aa", "isp": "#00bcd4", "ctl": "#7c3aed", "xtal": "#0f766e", "nc": "#dc2626"}
KNAME = {"gnd": "GND", "pwr": "+5V", "usb": "USB", "isp": "ISP (to U4 / U5)", "ctl": "LED / jumper / reset", "xtal": "crystal", "nc": "not connected"}


def kind(net):
    if net is None: return "nc"
    if net == "GND": return "gnd"
    if net.startswith("+"): return "pwr"
    if net.startswith("USB"): return "usb"
    if net.endswith("_M"): return "isp"
    if net.startswith("XTAL"): return "xtal"
    return "ctl"


def where(net, self_ref):
    if not net: return ""
    if net in ("GND", "+5V"): return "rail"
    return ", ".join(f"{r}.{p.split(' ')[0]}" for r, p in D.nets()[net] if r != self_ref)


def u1_pins():
    out = {}
    for pin, net in D.pins_of("U1"):
        n, *name = pin.split(" ")
        out[int(n)] = (" ".join(name), net)
    return out


def tx(x, y, s, size=11, anchor="start", color=INK, weight="400", mono=True):
    fam = ' font-family="Consolas,monospace"' if mono else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}"{fam}>{e(str(s))}</text>'


def cross(x, y, c=COL["nc"]):
    return (f'<line x1="{x-6}" y1="{y-6}" x2="{x+6}" y2="{y+6}" stroke="{c}" stroke-width="3"/>'
            f'<line x1="{x-6}" y1="{y+6}" x2="{x+6}" y2="{y-6}" stroke="{c}" stroke-width="3"/>')


def u1_svg():
    """TQFP-32 top view: pins 1-8 down the left, 9-16 along the bottom, 17-24 up the right, 25-32 along the top (right to left)."""
    P = u1_pins()
    cx, cy, half, pitch = 470, 400, 150, 34
    o = []
    xx = 20
    for k in ("gnd", "pwr", "usb", "isp", "ctl", "xtal"):
        o.append(f'<rect x="{xx}" y="14" width="14" height="14" rx="3" fill="{COL[k]}" fill-opacity=".25" stroke="{COL[k]}" stroke-width="2"/>' + tx(xx + 20, 25, KNAME[k], 11.5, mono=False))
        xx += 34 + len(KNAME[k]) * 6.6
    o.append(cross(xx + 8, 21) + tx(xx + 22, 25, "= No-Connect flag", 11.5, "start", COL["nc"], "700", mono=False))
    o.append(f'<rect x="{cx-half}" y="{cy-half}" width="{2*half}" height="{2*half}" rx="8" fill="#64748b" fill-opacity=".10" stroke="#475569" stroke-width="2.5"/>')
    o.append(f'<circle cx="{cx-half+22}" cy="{cy-half+22}" r="7" fill="#475569"/>' + tx(cx, cy - 6, "ATmega8A-AU", 15, "middle", INK, "700", False) + tx(cx, cy + 14, "TQFP-32, top view", 12, "middle", MUTE, "400", False))
    off = [(i - 3.5) * pitch for i in range(8)]

    def one(n, px, py, side):
        name, net = P[n]
        k = kind(net)
        c = COL[k]
        s = f'<rect x="{px-13}" y="{py-11}" width="26" height="22" rx="3" fill="{c}" fill-opacity=".2" stroke="{c}" stroke-width="2"/>' + tx(px, py + 4, n, 11, "middle", c, "700")
        lab = (net or "") + "  " + name
        if side == "l":
            s += (cross(px - 30, py) if not net else f'<line x1="{px-13}" y1="{py}" x2="{px-40}" y2="{py}" stroke="{c}" stroke-width="2"/>') + tx(px - 46, py + 4, lab if net else name, 11, "end", c, "700" if net else "400")
        elif side == "r":
            s += (cross(px + 30, py) if not net else f'<line x1="{px+13}" y1="{py}" x2="{px+40}" y2="{py}" stroke="{c}" stroke-width="2"/>') + tx(px + 46, py + 4, lab if net else name, 11, "start", c, "700" if net else "400")
        else:
            up = side == "t"
            y2 = py - 40 if up else py + 40
            s += (cross(px, py - 26 if up else py + 26) if not net else f'<line x1="{px}" y1="{py-11 if up else py+11}" x2="{px}" y2="{y2}" stroke="{c}" stroke-width="2"/>')
            ty = y2 - 6 if up else y2 + 14
            s += f'<text transform="translate({px+4},{ty}) rotate({-60 if up else 60})" font-size="11" fill="{c}" font-weight="{"700" if net else "400"}" font-family="Consolas,monospace" text-anchor="start">{e(lab if net else name)}</text>'
        return s
    for i in range(8):
        o.append(one(1 + i, cx - half - 14, cy + off[i], "l"))
        o.append(one(9 + i, cx + off[i], cy + half + 14, "b"))
        o.append(one(17 + i, cx + half + 14, cy - off[i], "r"))
        o.append(one(25 + i, cx - off[i], cy - half - 14, "t"))
    return f'<svg viewBox="0 0 960 800" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,sans-serif" style="max-width:100%;height:auto">{"".join(o)}</svg>'


def pin_table(ref):
    rows = ""
    for pin, net in D.pins_of(ref):
        k = kind(net)
        c = COL[k]
        what = f'<b style="color:{c}">{e(net)}</b>' if net else '<b style="color:#dc2626">No-Connect flag</b>'
        rows += f"<tr><td><b>{e(pin)}</b></td><td>{what}</td><td>{e(where(net, ref))}</td></tr>"
    return f'<div class="scroll"><table><thead><tr><th>Pin</th><th>Net</th><th>Also on this net</th></tr></thead><tbody>{rows}</tbody></table></div>'


def u1_table():
    return pin_table("U1")
