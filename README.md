# DIY Flipper-style Multitool

An open hardware, ESP32-S3 based pocket multitool for exploring radio, NFC, RFID, infrared and 1-Wire, inspired by the Flipper Zero. It is designed in KiCad, built mostly from off-the-shelf modules so it can be hand-soldered at home, and runs its own custom firmware.

> **Status: work in progress.** The schematic (rev 0.4) passes ERC and imports cleanly into the PCB editor. Component placement (v1) is done; the board is **not routed and has not been built or tested yet**. Always check pinouts against the datasheets of the parts you actually buy.

> **Note:** This is an independent hobby project. It is **not** affiliated with Flipper Devices and is **not** compatible with the official Flipper Zero firmware.

## Features

| Function | Hardware |
|---|---|
| MCU, Wi-Fi, Bluetooth LE | ESP32-S3-WROOM-1-N16R2 (16 MB flash, 2 MB PSRAM) |
| USB | USB-C, native USB for flashing, serial console and HID |
| Display | 1.3" SH1106 128x64 SPI OLED module |
| Sub-GHz radio | CC1101 module (one band per module) |
| NFC (13.56 MHz) | PN532 module over I2C |
| RFID (125 kHz) | Discrete front end: driver, LC tank, diode detector, MCP6561 comparator *(experimental)* |
| Infrared | TSOP38238 receiver + 940 nm IR LED |
| iButton | 1-Wire contacts |
| Storage | microSD card (SPI) |
| Controls | D-pad (Up / Down / Left / Right / OK) + Back, via a PCF8574 I/O expander |
| Feedback | SK6812 RGB LED, buzzer, vibration motor |
| Expansion | 2x9 GPIO header (UART, free GPIOs, 3.3 V, 5 V) |
| Power | Li-Po battery, MCP73832 USB charger, power-path circuit, 3.3 V LDO, battery voltage monitoring |

## Hardware overview

- **Board:** 130 x 64 mm, 2 layers, rounded corners.
- **Assembly-friendly:** all SMD parts sit on the front side, so the board can be soldered by hand or on a hot plate.
- **Modules on the back:** the PN532, CC1101 and Li-Po battery (503450) mount on the back side, behind the display and the D-pad.
- **Front layout:** OLED in the centre-left, D-pad to the right of it, ESP32 at the top edge with its antenna hanging over the board edge, GPIO header and IR at the top right, USB-C and power switch on the left edge, microSD slot on the right edge.

### Power chain

```
USB-C -> MCP73832 charger (500 mA) -> power path (P-FET + Schottky) -> slide switch -> TLV75733 3.3 V LDO
                                   \-> Li-Po battery (VBAT/2 -> ADC for voltage readout)
```

### ESP32-S3 pin map

| GPIO | Signal | GPIO | Signal |
|---|---|---|---|
| 0 | BOOT button | 15 | RFID carrier |
| 1 / 2 | I2C SDA / SCL | 16 / 17 | RFID modulation / data |
| 3 | Header (strapping pin) | 18 | NFC reset |
| 4 | NFC IRQ | 19 / 20 | USB D- / D+ |
| 5 | Battery voltage (ADC) | 21 | Display reset |
| 6 / 7 | CC1101 GDO2 / GDO0 | 38 / 39 | IR TX / IR RX |
| 8 | CC1101 CS | 40 | iButton |
| 9 | microSD CS | 41 | I/O expander interrupt |
| 10 | Display CS | 42 | Buzzer |
| 11 / 12 / 13 | SPI MOSI / SCK / MISO | 43 / 44 | UART TX / RX (header) |
| 14 | Display D/C | 47 / 48 | Vibration motor / RGB LED |

GPIO 35-37 and 45-46 are routed to the header (35-37 are only free on quad-PSRAM module variants; 45/46 are strapping pins).

**PCF8574 (I2C address 0x20):** P0 Up, P1 Down, P2 Left, P3 Right, P4 OK, P5 Back, P6 charge status, P7 SD card detect.

## Repository contents

- KiCad project (schematic and PCB), saved in KiCad 9 format (opens in KiCad 9 and 10)
- `place_diy_flipper.py` - KiCad scripting-console script that applies the v1 component placement

## Limitations

Compared with a real Flipper Zero:

- Each CC1101 module covers a single Sub-GHz band.
- PN532 card emulation is limited.
- 5 V on the GPIO header is available only while USB is connected.
- No fuel gauge; battery level is estimated from voltage only.
- The 125 kHz RFID front end is experimental.

## Roadmap

- [x] Schematic (ERC clean)
- [x] Footprints assigned, netlist imported into PCB
- [x] Component placement v1
- [ ] PCB routing and DRC
- [ ] First prototype build and bring-up
- [ ] Custom firmware (display UI, input, SD card, IR, NFC, Sub-GHz, RFID, iButton)
- [ ] Enclosure

## Responsible use

This device is meant for learning and for working with your own hardware, cards and remotes. Transmitting on radio frequencies, and reading or copying access cards you do not own, may be restricted or illegal where you live. Check your local regulations and only use it on equipment you are authorized to test.

## License

*To be added* (for example CERN-OHL-S for hardware and MIT/GPL for firmware).
