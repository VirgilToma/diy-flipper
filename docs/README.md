# Docs

Documents and images for the [DIY Flipper-style Multitool](../README.md). Everything here is generated from the KiCad project in [`hardware/`](../hardware/README.md) at **rev 0.5**.

| File | What it is |
|---|---|
| [`schematic.pdf`](schematic.pdf) | Full schematic as a zoomable PDF |
| [`BOM.csv`](BOM.csv) | Bill of materials: references, values, packages, suggested part numbers and notes |
| [`images/pcb_front.png`](images/pcb_front.png) | Render of the PCB front side |
| [`images/pcb_back.png`](images/pcb_back.png) | Render of the PCB back side, seen from the back |
| [`images/pcb_layers.png`](images/pcb_layers.png) | Copper routing: red = front, blue = back (ground pours hidden) |
| [`images/pcb_placement.png`](images/pcb_placement.png) | Where each part and module sits |
| [`images/block_diagram.png`](images/block_diagram.png) | Block diagram of the system |
| [`images/schematic.png`](images/schematic.png) | Schematic preview used in the READMEs |
| [`images/pn532_wiring.png`](images/pn532_wiring.png) | How to wire the PN532 module to J7 |

The images are renders made by a script from the KiCad files. They are not photos of a built board, and the module outlines in them are approximate.

**Keep them up to date:** when the hardware changes, regenerate the files here (for example the PDF from the Schematic Editor with File → Plot) and update the revision above.
