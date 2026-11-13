# Firmware

USBasp V6 runs the **official USBasp firmware by Thomas Fischl (version 2011-05-28), unchanged**. This repo does not copy it. Download it from the author:

- https://www.fischl.de/usbasp/ → `usbasp.2011-05-28.tar.gz`
- Ready-made hex for this board: `bin/firmware/usbasp.atmega8.2011-05-28.hex`

## Why no change is needed

The pin use below was read from the 2011-05-28 source. V6 keeps all of it:

| Source file | Definition | V6 net |
|---|---|---|
| `usbconfig.h` | D− = PB0, D+ = PB1, interrupt INT0 (PD2) | USB_DN, USB_DP (PB1 and PD2 joined) |
| `isp.h` | RST = PB2, MOSI = PB3, MISO = PB4, SCK = PB5 | RST_M, MOSI_M, MISO_M, SCK_M |
| `usbasp.h` | red LED = PC1 (low = on), green LED = PC0 (low = on) | BUSY_N, LED_G_K |
| `main.c` | red LED on during CONNECT / TPI_CONNECT, off after DISCONNECT | BUSY_N also enables the level shifter (U4 OE#) |
| `main.c` | slow SCK if PC2 reads low; `PORTC = 0xfe` turns on the PC2 pull-up | JP2 from PC2 to GND |

## Fuses (ATmega8A, 12 MHz crystal)

From the USBasp Makefile (`TARGET=atmega8`):

| Fuse | Value |
|---|---|
| High | `0xC9` |
| Low | `0xEF` |

## Flashing a new board (through J4)

A brand-new ATmega8A cannot program itself, so use any working programmer on **J4** (the 6-pin "SELF-PROG" header: 1 MISO, 2 VCC, 3 SCK, 4 MOSI, 5 RST, 6 GND). **Unplug the V6's own USB-C cable first**, because the other programmer supplies 5 V on pin 2.

With another USBasp:

```bash
avrdude -c usbasp -p m8 -B 32 -U hfuse:w:0xc9:m -U lfuse:w:0xef:m
```

```bash
avrdude -c usbasp -p m8 -U flash:w:usbasp.atmega8.2011-05-28.hex:i
```

With an Arduino Uno running the *ArduinoISP* sketch (change COM5 to your port):

```bash
avrdude -c stk500v1 -P COM5 -b 19200 -p m8 -U hfuse:w:0xc9:m -U lfuse:w:0xef:m -U flash:w:usbasp.atmega8.2011-05-28.hex:i
```

Set the fuses before the flash, or in the same command: the low fuse `0xEF` switches the chip to the external 12 MHz crystal that USB needs. `-B 32` slows the clock for the factory 1 MHz internal oscillator.

## Drivers

- **Linux / macOS**: no driver needed. On Linux, add a udev rule for `16c0:05dc` so you don't need `sudo`.
- **Windows 10 / 11**: install the **libusbK** (or libusb-win32) driver for "USBasp" with [Zadig](https://zadig.akeo.ie/), then use avrdude 7.x or the avrdude bundled with the Arduino IDE.

The warning `cannot set sck period` comes from old firmware revisions and is harmless. 2011-05-28 supports `-B`.

## Not tested on V6

TPI programming (ATtiny4/5/9/10) is in the firmware, but it has not been tried through the V6 level shifter, where MOSI and MISO are separate one-way buffers.
