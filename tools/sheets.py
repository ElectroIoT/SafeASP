"""USBasp V6 schematic sheets drawn as simplified SVG symbols (planning drawings, not an EasyEDA project).
Every reference designator and net name matches tools/data.py. Run via gen_docs.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schem_lib import *   # noqa: F401,F403

C_TGT, C_SH, C_ISP = "#0891b2", "#00bcd4", "#16a34a"
MUTE = "var(--mute)"


def stub(p, net, color=INK, right=True, L=34):
    """Short wire from a pin end plus a net label."""
    x, y = p
    x2 = x + L if right else x - L
    return line([(x, y), (x2, y)], color) + label(x2 + (6 if right else -6), y + 4, net, color, "start" if right else "end")


def gnd_at(p, right=True):
    x, y = p
    x2 = x + 16 if right else x - 16
    return line([(x, y), (x2, y)], C_GND) + gnd(x2, y)


def sheet1():
    """USB-C -> ESD -> PTC -> +5V; V-USB resistors and zeners; target power selector."""
    o = []
    # --- USB-C
    j1, p = ic(20, 30, 160, 250, "J1 USB-C", "TYPE-C-31-M-12", [], ["VBUS", "GND", "CC1", "CC2", "D+ (A6,B6)", "D- (A7,B7)"], C_USB, y0=54, step=34)
    o.append(j1)
    vb = p["VBUS"]
    o.append(line([vb, (560, vb[1])], C_5V) + label(vb[0] + 6, vb[1] - 8, "VBUS", C_5V))
    o.append(gnd_at(p["GND"]))
    for nm, rf in (("CC1", "R1"), ("CC2", "R2")):
        c = p[nm]
        o.append(line([c, (c[0] + 20, c[1])], C_USB) + res(c[0] + 20, c[1], rf + " 5.1k", "", True, 70, C_USB) + line([(c[0] + 90, c[1]), (c[0] + 104, c[1])], C_USB) + gnd(c[0] + 104, c[1]))
    o.append(dot(330, vb[1], C_5V) + cap(330, vb[1], "C2", "100n", False, 40) + gnd(330, vb[1] + 40))
    dp, dn = p["D+ (A6,B6)"], p["D- (A7,B7)"]
    u2, p2 = ic(380, dp[1] - 40, 150, 110, "U2", "USBLC6-2SC6", ["I/O1 1,6", "I/O2 3,4"], [], C_USB, top=["VBUS 5"], bottom=["GND 2"], y0=40, step=34)
    o.append(u2)
    o.append(line([p2["VBUS 5"], (p2["VBUS 5"][0], vb[1])], C_5V) + dot(p2["VBUS 5"][0], vb[1], C_5V) + gnd(*p2["GND 2"]))
    o.append(line([dp, (300, dp[1]), (300, p2["I/O1 1,6"][1]), p2["I/O1 1,6"]], C_USB) + label(dp[0] + 6, dp[1] - 6, "USB_DP_J", C_USB))
    o.append(line([dn, (280, dn[1]), (280, p2["I/O2 3,4"][1]), p2["I/O2 3,4"]], C_USB) + label(dn[0] + 6, dn[1] + 16, "USB_DN_J", C_USB))
    o.append(dot(300, p2["I/O1 1,6"][1], C_USB) + dot(280, p2["I/O2 3,4"][1], C_USB))
    # --- PTC to +5V
    o.append(res(560, vb[1], "F1", "PTC 500 mA", True, 90, C_5V))
    o.append(line([(650, vb[1]), (1080, vb[1])], C_5V) + label(660, vb[1] - 10, "+5V", C_5V))
    o.append(dot(700, vb[1], C_5V) + cap(700, vb[1], "C1", "10u", False, 50) + gnd(700, vb[1] + 50))
    # --- V-USB line interface
    Y0 = 330
    o.append(box(20, Y0, 1060, 230, "", "", "#8e24aa", "8 6", False) + text(34, Y0 + 20, "V-USB line interface (as the original USBasp): 68 R series, 3.6 V zener clamps, 2.2 k pull-up on D-", 12, "start", "#8e24aa", "700"))
    for i, (src, dst, rr, dd) in enumerate((("USB_DP_J", "USB_DP", "R3", "D1"), ("USB_DN_J", "USB_DN", "R4", "D2"))):
        y = Y0 + 70 + i * 90
        o.append(label(40, y + 4, src, C_USB) + line([(130, y), (180, y)], C_USB) + res(180, y, rr, "68R", True, 90, C_USB))
        o.append(line([(270, y), (560, y)], C_USB) + dot(380, y, C_USB) + diode(380, y, dd, "3.6 V zener", False, 40, INK, True) + gnd(380, y + 40))
        o.append(label(566, y + 4, dst, C_USB))
    yn = Y0 + 160
    o.append(dot(480, yn, C_USB) + res(480, yn, "R5", "2.2k", False, 44, C_USB) + label(480, yn + 60, "+5V", C_5V, "middle"))
    o.append(text(680, Y0 + 70, "USB_DP goes to PB1 (pin 13) AND PD2 / INT0 (pin 32)", 12, "start", MUTE))
    o.append(text(680, Y0 + 90, "USB_DN goes to PB0 (pin 12)", 12, "start", MUTE))
    o.append(text(680, Y0 + 110, "(USBasp usbconfig.h: D- = PB0, D+ = PB1, interrupt INT0)", 12, "start", MUTE))
    o.append(text(680, Y0 + 150, "Zener: cathode (bar) on the data line, anode to GND.", 12, "start", MUTE))
    # --- target power
    T = 600
    o.append(box(20, T, 1060, 250, "", "", C_TGT, "8 6", False) + text(34, T + 20, "Target power: JP1 picks 5 V, 3.3 V or nothing; F2 limits a shorted target", 12, "start", C_TGT, "700"))
    u3, p3 = ic(120, T + 50, 150, 110, "U3", "AP2112K-3.3", ["VIN 1", "EN 3"], ["VOUT 5"], C_3V3, bottom=["GND 2"], y0=40, step=34)
    o.append(u3 + rail(60, p3["VIN 1"][1], "+5V", C_5V) + line([(60, p3["VIN 1"][1]), p3["VIN 1"]], C_5V) + line([p3["EN 3"], (80, p3["EN 3"][1]), (80, p3["VIN 1"][1])], C_5V) + dot(80, p3["VIN 1"][1], C_5V))
    o.append(dot(60, p3["VIN 1"][1], C_5V) + cap(40, p3["VIN 1"][1] + 30, "C8", "10u", False, 40) + line([(60, p3["VIN 1"][1]), (60, p3["VIN 1"][1] + 30), (40, p3["VIN 1"][1] + 30)], C_5V) + gnd(40, p3["VIN 1"][1] + 70))
    o.append(gnd(*p3["GND 2"]))
    vo = p3["VOUT 5"]
    o.append(line([vo, (400, vo[1])], C_3V3) + label(vo[0] + 6, vo[1] - 8, "+3V3", C_3V3) + dot(330, vo[1], C_3V3) + cap(330, vo[1], "C9", "10u", False, 40) + gnd(330, vo[1] + 40))
    jp, pj = ic(400, T + 40, 130, 150, "JP1", "1x3 header", ["1 5V", "2 OUT", "3 3V3"], [], C_TGT, y0=40, step=40)
    o.append(jp)
    o.append(line([pj["1 5V"], (360, pj["1 5V"][1])], C_5V) + label(356, pj["1 5V"][1] + 4, "+5V", C_5V, "end"))
    o.append(line([pj["3 3V3"], (382, pj["3 3V3"][1]), (382, vo[1])], C_3V3) + dot(382, vo[1], C_3V3))
    o.append(text(560, T + 70, "jumper 1-2 = 5 V to the target", 12, "start", MUTE) + text(560, T + 88, "jumper 2-3 = 3.3 V to the target", 12, "start", MUTE) + text(560, T + 106, "no jumper = target has its own supply", 12, "start", MUTE))
    po = pj["2 OUT"]
    o.append(line([po, (370, po[1]), (370, T + 210), (560, T + 210)], C_TGT) + label(380, T + 204, "VTGT_SUP", C_TGT))
    o.append(res(560, T + 210, "F2", "PTC 200 mA", True, 90, C_TGT) + line([(650, T + 210), (760, T + 210)], C_TGT) + label(766, T + 214, "VTGT", C_TGT) + text(766, T + 232, "to U4 / U5 VCCB and ISP pin 2", 10.5, "start", MUTE))
    o.append(res(980, T + 100, "R9", "1k", False, 40, C_TGT) + led(980, T + 140, "LED3", "yellow", 40, "#ca8a04") + gnd(980, T + 180) + line([(980, T + 100), (980, T + 80), (950, T + 80)], C_TGT) + label(944, T + 84, "VTGT_SUP", C_TGT, "end"))
    o.append(text(30, T + 245, "LED3 shows that THIS board is powering the target (it sits before F2, so it does not load a self-powered target).", 11.5, "start", MUTE))
    return svg(1100, T + 260, "".join(o))


def sheet2():
    """ATmega8A core."""
    o = []
    left = ["29 RESET", "7 XTAL1", "8 XTAL2", "4 VCC", "6 VCC", "18 AVCC", "3 GND", "5 GND", "21 GND"]
    right = ["12 PB0", "13 PB1", "32 PD2/INT0", "14 PB2", "15 PB3/MOSI", "16 PB4/MISO", "17 PB5/SCK", "23 PC0", "24 PC1", "25 PC2"]
    u1, p = ic(420, 30, 240, 330, "U1", "ATmega8A-AU (TQFP-32)", left, right, C_SIG, y0=50, step=28)
    o.append(u1)
    rn = {"12 PB0": ("USB_DN", C_USB), "13 PB1": ("USB_DP", C_USB), "32 PD2/INT0": ("USB_DP", C_USB), "14 PB2": ("RST_M", C_SH), "15 PB3/MOSI": ("MOSI_M", C_SH),
          "16 PB4/MISO": ("MISO_M", C_SH), "17 PB5/SCK": ("SCK_M", C_SH), "23 PC0": ("LED_G_K", C_SIG), "24 PC1": ("BUSY_N", "#dc2626"), "25 PC2": ("SLOW_SCK", C_SIG)}
    for k, (n, c) in rn.items():
        o.append(stub(p[k], n, c))
    for k in ("4 VCC", "6 VCC", "18 AVCC"):
        x, y = p[k]
        o.append(line([(x, y), (x - 40, y)], C_5V) + label(x - 46, y + 4, "+5V", C_5V, "end"))
    for k in ("3 GND", "5 GND", "21 GND"):
        o.append(gnd_at(p[k], right=False))
    o.append(stub(p["29 RESET"], "MCU_RST", C_SIG, right=False))
    o.append(stub(p["7 XTAL1"], "XTAL1", INK, right=False) + stub(p["8 XTAL2"], "XTAL2", INK, right=False))
    o.append(text(540, 385, "Not connected (No-Connect flag): pins 1, 2, 9, 10, 11 (PD3-PD7), 19, 22 (ADC6/7), 20 (AREF), 26-28 (PC3-PC5), 30, 31 (PD0/PD1).", 11, "middle", MUTE))
    # --- crystal
    B = 420
    o.append(box(20, B, 330, 230, "", "", C_SIG, "8 6", False) + text(34, B + 20, "12 MHz crystal", 12, "start", C_SIG, "700"))
    o.append(label(40, B + 64, "XTAL1", INK) + line([(100, B + 60), (250, B + 60)]) + dot(140, B + 60) + cap(140, B + 60, "C3", "22p", False, 50) + gnd(140, B + 110))
    o.append(label(40, B + 164, "XTAL2", INK) + line([(100, B + 160), (250, B + 160)]) + dot(200, B + 160) + cap(200, B + 160, "C4", "22p", False, 30) + gnd(200, B + 190))
    o.append(f'<rect x="240" y="{B+95}" width="20" height="30" fill="none" stroke="{INK}" stroke-width="2"/>' + line([(250, B + 60), (250, B + 95)]) + line([(250, B + 125), (250, B + 160)]) + text(270, B + 108, "Y1", 11, "start", INK, "700") + text(270, B + 121, "12 MHz", 10.5, "start", MUTE))
    o.append(text(34, B + 215, "Y1 pads 2 and 4 (case) to GND", 10.5, "start", MUTE))
    # --- reset + decoupling
    o.append(box(370, B, 330, 230, "", "", C_SIG, "8 6", False) + text(384, B + 20, "Reset and decoupling", 12, "start", C_SIG, "700"))
    o.append(rail(420, B + 60, "+5V", C_5V) + res(420, B + 60, "R6", "10k", False, 50) + dot(420, B + 110, C_SIG) + line([(420, B + 110), (470, B + 110)], C_SIG) + label(476, B + 114, "MCU_RST", C_SIG))
    for i, (rf, nt) in enumerate((("C5", "pin 4"), ("C6", "pin 6"), ("C7", "AVCC 18"))):
        x = 420 + i * 95
        o.append(rail(x, B + 150, "+5V", C_5V) + cap(x, B + 150, rf, "100n " + nt, False, 40) + gnd(x, B + 190))
    # --- LEDs
    o.append(box(720, B, 360, 230, "", "", C_SIG, "8 6", False) + text(734, B + 20, "Status LEDs (active low, as the USBasp firmware)", 12, "start", C_SIG, "700"))
    for i, (rf, ld, col, net, txt) in enumerate((("R7", "LED1", "#dc2626", "BUSY_N", "red: programming"), ("R8", "LED2", "#16a34a", "LED_G_K", "green: USB ready"))):
        x = 790 + i * 150
        o.append(rail(x, B + 60, "+5V", C_5V) + res(x, B + 60, rf, "1k", False, 40) + led(x, B + 100, ld, txt, 50, col) + line([(x, B + 150), (x, B + 175)], col) + label(x, B + 192, net, col, "middle"))
    o.append(text(734, B + 215, "BUSY_N (PC1) also drives U4 OE# on sheet 3.", 10.5, "start", "#dc2626"))
    # --- J4 + JP2
    C = 680
    o.append(box(20, C, 1060, 170, "", "", C_SIG, "8 6", False) + text(34, C + 20, "J4: port to flash THIS ATmega8A (another programmer plugs in here). JP2: slow SCK jumper.", 12, "start", C_SIG, "700"))
    j4, q = ic(170, C + 35, 160, 120, "J4", "2x3 header", ["1 MISO", "3 SCK", "5 RST"], ["2 VCC", "4 MOSI", "6 GND"], C_SIG, y0=45, step=30)
    o.append(j4 + stub(q["1 MISO"], "MISO_M", C_SH, False) + stub(q["3 SCK"], "SCK_M", C_SH, False) + stub(q["5 RST"], "MCU_RST", C_SIG, False))
    o.append(line([q["2 VCC"], (q["2 VCC"][0] + 30, q["2 VCC"][1])], C_5V) + label(q["2 VCC"][0] + 36, q["2 VCC"][1] + 4, "+5V", C_5V) + stub(q["4 MOSI"], "MOSI_M", C_SH) + gnd_at(q["6 GND"]))
    jp2, r = ic(560, C + 50, 130, 90, "JP2", "1x2 header", ["1", "2"], [], C_SIG, y0=40, step=30)
    o.append(jp2 + stub(r["1"], "SLOW_SCK", C_SIG, False) + gnd_at(r["2"], False))
    o.append(text(700, C + 70, "Fit JP2 when the target clock is below 1.5 MHz", 12, "start", MUTE) + text(700, C + 88, "(SCK drops from 375 kHz to about 8 kHz;", 12, "start", MUTE) + text(700, C + 106, "PC2 uses the firmware's internal pull-up).", 12, "start", MUTE)
             + text(700, C + 134, "Unplug USB-C while flashing through J4.", 12, "start", "#dc2626", "700"))
    return svg(1100, C + 190, "".join(o))


def sheet3():
    """74LVC8T245 + 74LVC1T45 level shifter and the two ISP headers."""
    o = []
    left = ["1 VCCA", "2 DIR", "3 A1", "4 A2", "5 A3", "6-10 A4..A8", "22 OE#"]
    right = ["24,23 VCCB", "21 B1", "20 B2", "19 B3", "18-14 B4..B8", "11-13 GND"]
    u4, p = ic(380, 30, 260, 260, "U4", "74LVC8T245PW (TSSOP-24)", left, right, C_SH, y0=50, step=30)
    o.append(u4)
    o.append(line([p["1 VCCA"], (p["1 VCCA"][0] - 40, p["1 VCCA"][1])], C_5V) + label(p["1 VCCA"][0] - 46, p["1 VCCA"][1] + 4, "+5V", C_5V, "end"))
    o.append(line([p["2 DIR"], (p["2 DIR"][0] - 40, p["2 DIR"][1])], C_5V) + label(p["2 DIR"][0] - 46, p["2 DIR"][1] + 4, "+5V (A to B)", C_5V, "end"))
    for k, n in (("3 A1", "MOSI_M"), ("4 A2", "SCK_M"), ("5 A3", "RST_M")):
        o.append(stub(p[k], n, C_SH, False))
    o.append(gnd_at(p["6-10 A4..A8"], False) + text(p["6-10 A4..A8"][0] - 30, p["6-10 A4..A8"][1] - 12, "unused A inputs to GND", 10.5, "end", MUTE))
    o.append(stub(p["22 OE#"], "BUSY_N", "#dc2626", False))
    o.append(stub(p["24,23 VCCB"], "VTGT", C_TGT))
    for k, n in (("21 B1", "MOSI_T"), ("20 B2", "SCK_T"), ("19 B3", "RST_T")):
        o.append(stub(p[k], n, C_ISP))
    x, y = p["18-14 B4..B8"]
    o.append(text(x + 6, y + 4, "no connect", 10.5, "start", "#dc2626", "700"))
    o.append(gnd_at(p["11-13 GND"]))
    u5, q = ic(380, 330, 260, 130, "U5", "74LVC1T45GW (SC-88)", ["1 VCCA", "3 A", "5 DIR"], ["6 VCCB", "4 B", "2 GND"], C_SH, y0=40, step=30)
    o.append(u5 + line([q["1 VCCA"], (q["1 VCCA"][0] - 40, q["1 VCCA"][1])], C_5V) + label(q["1 VCCA"][0] - 46, q["1 VCCA"][1] + 4, "+5V", C_5V, "end"))
    o.append(stub(q["3 A"], "MISO_M", C_SH, False) + gnd_at(q["5 DIR"], False) + text(q["5 DIR"][0] - 30, q["5 DIR"][1] + 26, "DIR low = B to A", 10.5, "end", MUTE))
    o.append(stub(q["6 VCCB"], "VTGT", C_TGT) + stub(q["4 B"], "MISO_T", C_ISP) + gnd_at(q["2 GND"]))
    # --- support parts
    S = 500
    o.append(box(20, S, 1060, 200, "", "", C_SH, "8 6", False) + text(34, S + 20, "Decoupling, OE# pull-up, A-side pull-downs", 12, "start", C_SH, "700"))
    for i, (rf, rl, nm) in enumerate((("C10", "+5V", "U4 VCCA"), ("C11", "VTGT", "U4 VCCB"), ("C12", "+5V", "U5 VCCA"), ("C13", "VTGT", "U5 VCCB"))):
        x = 70 + i * 100
        o.append(rail(x, S + 70, rl, C_5V if rl == "+5V" else C_TGT) + cap(x, S + 70, rf, "100n", False, 40) + gnd(x, S + 110) + text(x, S + 150, nm, 10.5, "middle", MUTE))
    o.append(rail(520, S + 70, "+5V", C_5V) + res(520, S + 70, "R10", "10k", False, 50) + line([(520, S + 120), (520, S + 140)], "#dc2626") + label(520, S + 158, "BUSY_N", "#dc2626", "middle"))
    for i, (rf, nt) in enumerate((("R11", "MOSI_M"), ("R12", "SCK_M"), ("R13", "RST_M"))):
        x = 680 + i * 120
        o.append(label(x, S + 62, nt, C_SH, "middle") + line([(x, S + 68), (x, S + 80)], C_SH) + res(x, S + 80, rf, "100k", False, 50) + gnd(x, S + 130))
    o.append(text(34, S + 188, "R10 keeps OE# high (outputs off) while the ATmega8A is in reset or unprogrammed. R11-R13 stop the A inputs floating when the firmware releases the ISP pins.", 11, "start", MUTE))
    # --- headers
    H = 740
    j2, a = ic(200, H, 220, 200, "J2", "2x5 box header (10-pin ISP)", ["1 MOSI", "3 NC", "5 RST", "7 SCK", "9 MISO"], ["2 VCC", "4 GND", "6 GND", "8 GND", "10 GND"], C_ISP, y0=50, step=30)
    o.append(j2)
    for k, n in (("1 MOSI", "MOSI_T"), ("5 RST", "RST_T"), ("7 SCK", "SCK_T"), ("9 MISO", "MISO_T")):
        o.append(stub(a[k], n, C_ISP, False))
    x, y = a["3 NC"]
    o.append(text(x - 6, y + 4, "no connect", 10.5, "end", "#dc2626", "700"))
    o.append(stub(a["2 VCC"], "VTGT", C_TGT))
    for k in ("4 GND", "6 GND", "8 GND", "10 GND"):
        o.append(gnd_at(a[k]))
    j3, b = ic(720, H, 200, 140, "J3", "2x3 header (6-pin ISP)", ["1 MISO", "3 SCK", "5 RST"], ["2 VCC", "4 MOSI", "6 GND"], C_ISP, y0=50, step=30)
    o.append(j3)
    for k, n in (("1 MISO", "MISO_T"), ("3 SCK", "SCK_T"), ("5 RST", "RST_T")):
        o.append(stub(b[k], n, C_ISP, False))
    o.append(stub(b["2 VCC"], "VTGT", C_TGT) + stub(b["4 MOSI"], "MOSI_T", C_ISP) + gnd_at(b["6 GND"]))
    o.append(text(600, H + 175, "Pin 1 = the corner with the square pad / the arrow on the box header.", 11, "start", MUTE))
    return svg(1100, H + 230, "".join(o))


SHEETS = {"p1": sheet1, "p2": sheet2, "p3": sheet3}
