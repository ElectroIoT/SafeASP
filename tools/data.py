"""USBasp V6 (USB-C) design data: sections, parts, pin-to-net data, BOM info.
All connections are PLANNED (no EasyEDA schematic exists yet). Pin numbers of U1, U4 and U5 were read from the
datasheets on 2026-11-13; the firmware pin use was read from the USBasp 2011-05-28 source (usbasp.h, isp.h, usbconfig.h, main.c)."""

# id, title, colour, description
SECTIONS = [
 ("usb", "USB-C INPUT", "#4895ef", "16-pin USB 2.0 Type-C receptacle, one 5.1 k pull-down on EACH of CC1 and CC2 (so C-to-C cables and chargers give 5 V), USBLC6 ESD part on D+ / D-, 500 mA PTC fuse from VBUS to the +5V rail."),
 ("vusb", "V-USB LINE INTERFACE", "#8e24aa", "The classic USBasp low-speed USB interface: 68 R series resistors, 3.6 V zener clamps (the ATmega8A runs at 5 V) and the 2.2 k pull-up on D- that tells the PC this is a low-speed device."),
 ("tpwr", "TARGET POWER (5 V / 3.3 V / OFF)", "#ff9f43", "AP2112K 3.3 V LDO. Jumper JP1 picks what the board sends to the target: 5 V (1-2), 3.3 V (2-3) or nothing (no jumper, target has its own supply). A 200 mA PTC fuse limits a shorted target; yellow LED = we are powering the target."),
 ("mcu", "ATMEGA8A CORE", "#a66cff", "ATmega8A-AU at 5 V with a 12 MHz crystal, running the unchanged USBasp firmware. Red LED (PC1) = programming, green LED (PC0) = USB ready. J4 = 6-pin header to flash this ATmega8A itself; JP2 = slow SCK jumper on PC2."),
 ("shift", "LEVEL SHIFTER 1.8 - 5.5 V", "#00bcd4", "74LVC8T245 drives MOSI, SCK and RST to the target at the TARGET's voltage (VTGT); 74LVC1T45 brings MISO back to 5 V. The red-LED line (PC1, low only while programming) enables the outputs, so the target pins are released (Hi-Z) the rest of the time."),
 ("isp", "ISP HEADERS", "#2fbf71", "Standard AVR 10-pin box header and 6-pin header, both on the shifted target nets. Pin 2 (VCC) is the target supply sense, and the supply output when JP1 is fitted."),
]
SEC = {s[0]: s for s in SECTIONS}

# page groups of the schematic guide: id, title, [sections]
PAGES = [
 ("p1", "Sheet 1: USB-C, V-USB interface, target power", ["usb", "vusb", "tpwr"]),
 ("p2", "Sheet 2: ATmega8A core", ["mcu"]),
 ("p3", "Sheet 3: Level shifter and ISP headers", ["shift", "isp"]),
]

# BOM info by LCSC number: mpn, maker, stock, unit price, tier, status
INFO = {
 "C16190": ("ATMEGA8A-AU", "Microchip", 815, 1.8247, "1+", "LISTING 2026-11-13; TQFP-32 pinout read from the datasheet (figure 1-1)"),
 "C9002": ("X322512MSB4SI", "YXC", 344395, 0.0916, "5+", "LISTING 2026-11-13; 12 MHz 3225 crystal, check the pad order in the EasyEDA footprint"),
 "C165948": ("TYPE-C-31-M-12", "Korean Hroparts", 283620, 0.1886, "5+", "VERIFIED 2026-10-28 (same part as TankPilot); 16-pin USB 2.0"),
 "C7519": ("USBLC6-2SC6", "ST", 39325, 0.1814, "5+", "LISTING (stock from 2026-10-28)"),
 "C163512": ("1206L050YR", "Littelfuse", 11040, 0.0742, "10+", "LISTING 2026-11-05; 500 mA hold"),
 "C207035": ("1206L020YR", "Littelfuse", 30550, 0.0925, "5+", "LISTING 2026-11-13; 200 mA hold"),
 "C725453": ("BZT52C3V6-TP", "MCC", 13720, 0.0347, "20+", "LISTING 2026-11-13; 3.6 V zener, SOD-123"),
 "C17976": ("1206W4F680JT5E", "Uni-Royal", 57350, 0.0136, "50+", "LISTING 2026-11-13"),
 "C17948": ("1206W4F2201T5E", "Uni-Royal", 156400, 0.0053, "100+", "LISTING 2026-11-13"),
 "C17900": ("1206W4F1003T5E", "Uni-Royal", 368300, 0.0065, "100+", "LISTING 2026-11-13"),
 "C26033": ("1206W4F5101T5E", "Uni-Royal", 166000, 0.005, "100+", "VERIFIED listing (TankPilot)"),
 "C17902": ("1206W4F1002T5E", "Uni-Royal", 1059900, 0.0079, "100+", "VERIFIED listing (TankPilot)"),
 "C4410": ("1206W4F1001T5E", "Uni-Royal", 655650, 0.0086, "50+", "VERIFIED listing (TankPilot)"),
 "C1804": ("CL21C220JBANNNC", "Samsung", 207250, 0.0098, "50+", "LISTING 2026-11-13; 22 pF C0G 0805"),
 "C24497": ("CL31B104KBCNNNC", "Samsung", 125980, 0.0222, "20+", "VERIFIED listing 2026-10-28"),
 "C9807": ("CL31A106KAHNNNE", "Samsung", 493250, 0.053, "10+", "VERIFIED listing 2026-10-28"),
 "C51118": ("AP2112K-3.3TRG1", "Diodes Inc", 4510, 0.1792, "5+", "LISTING (stock from 2026-10-28); SOT-25"),
 "C458788": ("74LVC8T245PW", "Nexperia", 19547, 0.3952, "10+", "LISTING 2026-11-13; other-supplier stock (3-5 day lead); TSSOP-24 pin table + function table read"),
 "C478004": ("74LVC1T45GW,125", "Nexperia", 3945, 0.1864, "5+", "LISTING 2026-11-13; SC-88 (SOT-363) pin table + function table read"),
 "C965798": ("XL-1608SURC-04", "Xinglight", 270700, 0.0057, "100+", "LISTING (red, 0603)"),
 "C2986059": ("19-217/GHC-YR1S2/6T", "Everlight", 718400, 0.018, "50+", "LISTING (green, 0603)"),
 "C965803": ("XL-1608UYC-04", "Xinglight", 107300, 0.0081, "100+", "LISTING 2026-11-13 (yellow, 0603)"),
 "C5665": ("2.54-2*5P", "BOOMELE", 110705, 0.1046, "5+", "LISTING 2026-11-19; IDC box header 2x5, through hole (replaces C5368783, which is a 1x10 2.5 mm XH-style header)"),
 "C65114": ("2.54-2*3P", "BOOMELE", 44450, 0.0457, "10+", "LISTING 2026-11-13; 2x3 pin header"),
 "C492402": ("PZ254V-11-03P", "XFCN", "not read", 0.02, "20+", "LISTING 2026-11-05 (1x3 header)"),
 "C492401": ("PZ254V-11-02P", "XFCN", 777200, 0.0184, "50+", "LISTING 2026-11-13 (1x2 header)"),
}

# ref, section, name, LCSC, qty, pins "pin=net,pin=net" ('-' = no connect)
PARTS = [
 # ---- USB-C input
 ("J1", "usb", "USB-C 16-pin receptacle (USB 2.0)", "C165948", 1, "A4B9 VBUS=VBUS,B4A9 VBUS=VBUS,A1B12 GND=GND,B1A12 GND=GND,A5 CC1=CC1,B5 CC2=CC2,A6 DP1=USB_DP_J,B6 DP2=USB_DP_J,A7 DN1=USB_DN_J,B7 DN2=USB_DN_J,A8 SBU1=-,B8 SBU2=-,EH1-4 shell=GND"),
 ("R1", "usb", "5.1 k 1206, CC1 pull-down", "C26033", 1, "1=CC1,2=GND"),
 ("R2", "usb", "5.1 k 1206, CC2 pull-down", "C26033", 1, "1=CC2,2=GND"),
 ("U2", "usb", "USBLC6-2SC6 ESD on D+ / D-", "C7519", 1, "1 I/O1=USB_DP_J,6 I/O1=USB_DP_J,3 I/O2=USB_DN_J,4 I/O2=USB_DN_J,5 VBUS=VBUS,2 GND=GND"),
 ("F1", "usb", "PTC 500 mA 1206, VBUS to +5V", "C163512", 1, "1=VBUS,2=+5V"),
 ("C2", "usb", "100 nF 1206 on VBUS", "C24497", 1, "1=VBUS,2=GND"),
 # ---- V-USB interface
 ("R3", "vusb", "68 R 1206, D+ series", "C17976", 1, "1=USB_DP_J,2=USB_DP"),
 ("R4", "vusb", "68 R 1206, D- series", "C17976", 1, "1=USB_DN_J,2=USB_DN"),
 ("D1", "vusb", "3.6 V zener, D+ clamp", "C725453", 1, "K=USB_DP,A=GND"),
 ("D2", "vusb", "3.6 V zener, D- clamp", "C725453", 1, "K=USB_DN,A=GND"),
 ("R5", "vusb", "2.2 k 1206, D- pull-up (low speed)", "C17948", 1, "1=+5V,2=USB_DN"),
 ("C1", "vusb", "10 uF 1206, +5V bulk", "C9807", 1, "1=+5V,2=GND"),
 # ---- target power
 ("U3", "tpwr", "AP2112K-3.3 LDO, SOT-25", "C51118", 1, "1 VIN=+5V,2 GND=GND,3 EN=+5V,4 NC=-,5 VOUT=+3V3"),
 ("C8", "tpwr", "10 uF 1206, LDO input", "C9807", 1, "1=+5V,2=GND"),
 ("C9", "tpwr", "10 uF 1206, LDO output", "C9807", 1, "1=+3V3,2=GND"),
 ("JP1", "tpwr", "1x3 header: target supply 5 V (1-2) / 3.3 V (2-3) / off", "C492402", 1, "1 5V=+5V,2 OUT=VTGT_SUP,3 3V3=+3V3"),
 ("F2", "tpwr", "PTC 200 mA 1206, target supply limit", "C207035", 1, "1=VTGT_SUP,2=VTGT"),
 ("LED3", "tpwr", "Yellow LED: powering the target", "C965803", 1, "A=LED_T_A,K=GND"),
 ("R9", "tpwr", "1 k 1206, LED3 series", "C4410", 1, "1=VTGT_SUP,2=LED_T_A"),
 # ---- ATmega8A core
 ("U1", "mcu", "ATmega8A-AU, TQFP-32", "C16190", 1, "1 PD3=-,2 PD4=-,3 GND=GND,4 VCC=+5V,5 GND=GND,6 VCC=+5V,7 PB6 XTAL1=XTAL1,8 PB7 XTAL2=XTAL2,9 PD5=-,10 PD6=-,11 PD7=-,12 PB0=USB_DN,13 PB1=USB_DP,14 PB2=RST_M,15 PB3 MOSI=MOSI_M,16 PB4 MISO=MISO_M,17 PB5 SCK=SCK_M,18 AVCC=+5V,19 ADC6=-,20 AREF=-,21 GND=GND,22 ADC7=-,23 PC0=LED_G_K,24 PC1=BUSY_N,25 PC2=SLOW_SCK,26 PC3=-,27 PC4=-,28 PC5=-,29 PC6 RESET=MCU_RST,30 PD0=-,31 PD1=-,32 PD2 INT0=USB_DP"),
 ("Y1", "mcu", "12 MHz crystal 3225", "C9002", 1, "1=XTAL1,2 GND=GND,3=XTAL2,4 GND=GND"),
 ("C3", "mcu", "22 pF 0805, XTAL1 load", "C1804", 1, "1=XTAL1,2=GND"),
 ("C4", "mcu", "22 pF 0805, XTAL2 load", "C1804", 1, "1=XTAL2,2=GND"),
 ("C5", "mcu", "100 nF 1206, VCC pin 4", "C24497", 1, "1=+5V,2=GND"),
 ("C6", "mcu", "100 nF 1206, VCC pin 6", "C24497", 1, "1=+5V,2=GND"),
 ("C7", "mcu", "100 nF 1206, AVCC pin 18", "C24497", 1, "1=+5V,2=GND"),
 ("R6", "mcu", "10 k 1206, RESET pull-up", "C17902", 1, "1=+5V,2=MCU_RST"),
 ("LED1", "mcu", "Red LED: programming (PC1 low)", "C965798", 1, "A=LED_R_A,K=BUSY_N"),
 ("R7", "mcu", "1 k 1206, LED1 series", "C4410", 1, "1=+5V,2=LED_R_A"),
 ("LED2", "mcu", "Green LED: USB ready (PC0 low)", "C2986059", 1, "A=LED_G_A,K=LED_G_K"),
 ("R8", "mcu", "1 k 1206, LED2 series", "C4410", 1, "1=+5V,2=LED_G_A"),
 ("J4", "mcu", "2x3 header: flash THIS ATmega8A (self-programming port)", "C65114", 1, "1 MISO=MISO_M,2 VCC=+5V,3 SCK=SCK_M,4 MOSI=MOSI_M,5 RST=MCU_RST,6 GND=GND"),
 ("JP2", "mcu", "1x2 header: slow SCK jumper (PC2 to GND)", "C492401", 1, "1=SLOW_SCK,2=GND"),
 # ---- level shifter
 ("U4", "shift", "74LVC8T245PW 8-bit dual-supply transceiver, TSSOP-24", "C458788", 1, "1 VCCA=+5V,2 DIR=+5V,3 A1=MOSI_M,4 A2=SCK_M,5 A3=RST_M,6 A4=GND,7 A5=GND,8 A6=GND,9 A7=GND,10 A8=GND,11 GND=GND,12 GND=GND,13 GND=GND,14 B8=-,15 B7=-,16 B6=-,17 B5=-,18 B4=-,19 B3=RST_T,20 B2=SCK_T,21 B1=MOSI_T,22 OE#=BUSY_N,23 VCCB=VTGT,24 VCCB=VTGT"),
 ("U5", "shift", "74LVC1T45GW 1-bit dual-supply transceiver (MISO back), SC-88", "C478004", 1, "1 VCCA=+5V,2 GND=GND,3 A=MISO_M,4 B=MISO_T,5 DIR=GND,6 VCCB=VTGT"),
 ("C10", "shift", "100 nF 1206, U4 VCCA", "C24497", 1, "1=+5V,2=GND"),
 ("C11", "shift", "100 nF 1206, U4 VCCB", "C24497", 1, "1=VTGT,2=GND"),
 ("C12", "shift", "100 nF 1206, U5 VCCA", "C24497", 1, "1=+5V,2=GND"),
 ("C13", "shift", "100 nF 1206, U5 VCCB", "C24497", 1, "1=VTGT,2=GND"),
 ("R10", "shift", "10 k 1206, OE# pull-up (outputs off while the ATmega8A is in reset)", "C17902", 1, "1=+5V,2=BUSY_N"),
 ("R11", "shift", "100 k 1206, MOSI_M pull-down (no floating input)", "C17900", 1, "1=MOSI_M,2=GND"),
 ("R12", "shift", "100 k 1206, SCK_M pull-down", "C17900", 1, "1=SCK_M,2=GND"),
 ("R13", "shift", "100 k 1206, RST_M pull-down", "C17900", 1, "1=RST_M,2=GND"),
 # ---- ISP headers
 ("J2", "isp", "2x5 box header: standard AVR 10-pin ISP", "C5665", 1, "1 MOSI=MOSI_T,2 VCC=VTGT,3 NC=-,4 GND=GND,5 RST=RST_T,6 GND=GND,7 SCK=SCK_T,8 GND=GND,9 MISO=MISO_T,10 GND=GND"),
 ("J3", "isp", "2x3 header: standard AVR 6-pin ISP", "C65114", 1, "1 MISO=MISO_T,2 VCC=VTGT,3 SCK=SCK_T,4 MOSI=MOSI_T,5 RST=RST_T,6 GND=GND"),
]
REF_SEC = {p[0]: p[1] for p in PARTS}
BYREF = {p[0]: p for p in PARTS}
OPTIONAL = {r for r, s, n, c, q, pins in PARTS if "OPTIONAL" in n}
TOTAL_PIECES = sum(p[4] for p in PARTS)


def pins_of(ref):
    out = []
    for it in BYREF[ref][5].split(","):
        a, b = it.rsplit("=", 1)
        out.append((a.strip(), None if b.strip() == "-" else b.strip()))
    return out


def nets():
    """net -> list of (ref, pin)"""
    n = {}
    for ref in BYREF:
        for pin, net in pins_of(ref):
            if net:
                n.setdefault(net, []).append((ref, pin))
    return n


def bom_rows():
    """Group identical LCSC parts: returns list of (refs, qty, name, lcsc, mpn, maker, stock, price, tier, status, subtotal)."""
    by, order = {}, []
    for ref, sec, name, c, q, pins in PARTS:
        if c not in by:
            by[c] = {"refs": [], "q": 0, "names": []}
            order.append(c)
        by[c]["refs"].append(ref)
        by[c]["q"] += q
        by[c]["names"].append(name)
    rows = []
    for c in order:
        d = by[c]
        mpn, mk, st, pr, tier, status = INFO[c]
        nm = d["names"][0] if len(d["names"]) == 1 else " / ".join(sorted(set(n.split(",")[0] for n in d["names"])))[:90]
        rows.append((", ".join(d["refs"]), d["q"], nm, c, mpn, mk, st, pr, tier, status, d["q"] * pr))
    return rows


def totals():
    return sum(r[10] for r in bom_rows())


def check():
    """Every net has 2+ pins, every LCSC number has INFO."""
    prob = []
    for net, pins in nets().items():
        if len(pins) < 2:
            prob.append(f"net {net} has only one pin: {pins}")
    for p in PARTS:
        if p[3] not in INFO:
            prob.append(f"{p[0]}: no INFO for {p[3]}")
    return prob


if __name__ == "__main__":
    print(len(PARTS), "lines,", TOTAL_PIECES, "pieces, USD", round(totals(), 2))
    for p in check():
        print(" ", p)
