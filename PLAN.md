# USBasp V6: design plan

Successor to USBasp v4 (USB-B, 2018) and v5 (micro-USB, 2019). Goal: keep the cheap, well-known ATmega8 + USBasp-firmware programmer, but make it USB-C and safe for 3.3 V and 1.8 V targets.

## 1. Decisions

| # | Decision | Why |
|---|---|---|
| D1 | ATmega8A-AU (TQFP-32) + unchanged USBasp 2011-05-28 firmware | Known to work with avrdude and the Arduino IDE, no firmware maintenance. Pins checked against the source (see firmware/README.md). |
| D2 | USB-C 16-pin receptacle (C165948), 5.1 k on CC1 and CC2 separately | A shared CC resistor (or none) gives 0 V from C-to-C cables. |
| D3 | Keep the V-USB line interface (68 R, 3.6 V zeners, 2.2 k D- pull-up), add USBLC6 ESD + 500 mA PTC | Same as the proven original; ESD and fuse are new. |
| D4 | Level shifter 74LVC8T245 (MOSI, SCK, RST) + 74LVC1T45 (MISO), B side on VTGT (ISP pin 2) | Signals follow the target voltage (1.8-5.5 V). The old boards drove 5 V into 3.3 V chips. |
| D5 | U4 OE# = PC1 (red LED line, BUSY_N), R10 10 k pull-up | The firmware already pulls PC1 low only between CONNECT and DISCONNECT, so the outputs are Hi-Z when idle and while the ATmega8A is in reset. No firmware change. |
| D6 | R11-R13 100 k pull-downs on the U4 A inputs | The firmware sets the ISP pins as inputs when idle; CMOS inputs must not float. |
| D7 | Target power: AP2112K 3.3 V, JP1 1x3 (5 V / OUT / 3.3 V), 200 mA PTC, yellow LED before the PTC | Covers 5 V and 3.3 V boards without a bench supply; a shorted target trips F2, not the PC port. |
| D8 | Separate J4 self-programming header instead of the old J2 jumper | With the level shifter in the way, the ISP header can no longer reach the board's own ATmega8A. |
| D9 | Board 84 x 32 mm, 2 layers, USB-C left, ISP headers right | Room for the new blocks; still far below 100 x 100 mm. |

## 2. Checks done (2026-11-13)

- Netlist: every net has at least 2 pins (`python -X utf8 -I tools/data.py`).
- Floor plan: no overlaps, every part inside its block box, no box touching a hole (`tools/layout.py`).
- Datasheets read for pin tables: ATmega8A (TQFP-32 figure 1-1), 74LVC8T245 (pin description + function table: DIR high = A to B, OE# high = Hi-Z, suspend if either VCC is 0 V), 74LVC1T45 (DIR low = B to A).
- Firmware source read (2011-05-28): usbasp.h, isp.h, usbconfig.h, main.c.
- LCSC numbers looked up on lcsc.com for every BOM line (stock and price from 2026-11-13 or earlier, as noted per line).

## 3. Open items

1. Draw the schematic and PCB in EasyEDA from the docs pages; check every symbol and footprint (TQFP-32, TSSOP-24, SC-88, 3225 crystal pad order, box-header key).
2. U4 74LVC8T245PW is only in other-supplier stock at LCSC (3-5 day lead time). The TI SN74LVC8T245PWR (C27643) has the same pinout.
3. J2 = C5665 (BOOMELE 2x5 IDC box header). The first pick, C5368783, turned out to be a 1x10 2.5 mm XH-style header (found in the EasyEDA footprint 2026-11-19).
4. Two 2.54 mm jumper caps (JP1, JP2) are not in the LCSC BOM.
5. Build and test: C-to-C cable, 5 V and 3.3 V targets, self-powered target with JP1 off, slow SCK, Arduino IDE "Burn Bootloader".
6. TPI (ATtiny4/5/9/10) through the separate MOSI / MISO buffers: untested.
7. Never fit JP1 while the target has its own supply (the two supplies would fight). Silkscreen a warning.
