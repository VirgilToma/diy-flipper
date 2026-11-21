# DIY Flipper - component placement for the KiCad PCB Editor (KiCad 9 / 10)
#
# HOW TO RUN
#   1. Save your board first (File > Save), so you can go back with File > Revert.
#   2. Put this file in your project folder.
#   3. PCB Editor > Tools > Scripting Console, then type (with your own path):
#        exec(open("/home/<user>/Documents/Proiecte/diy_flipper/place_diy_flipper.py").read())
#   4. Check the result, run DRC, then File > Save.
#
# What it does
#   - moves and rotates every footprint (and flips the PN532 / CC1101 headers to the back)
#   - draws a 130 x 64 mm board outline on Edge.Cuts (only if Edge.Cuts is empty)
#   - draws the module bodies (OLED, PN532, CC1101, battery) on User.Drawings
#   - adds a rule area "no copper pour" under the PN532 module (its antenna stops working over a ground pour)
# Coordinates are in mm relative to the board's top-left corner; the board corner goes to (40, 40) on the sheet.
# Script changes are not on the undo stack: use File > Revert if you want the old layout back.

import pcbnew

X0, Y0 = 40.0, 40.0          # sheet position of the board's top-left corner (mm)
W, H, RC = 130.0, 64.0, 3.0     # board size and corner radius (mm)

# ref: (side, x, y, rotation_deg)   side F = top, B = bottom
PLACE = {
    "BZ1": ("F", 92.00, 14.00, 0),
    "C1": ("F", 38.60, 3.00, 90),
    "C2": ("F", 40.90, 3.00, 90),
    "C3": ("F", 38.60, 8.20, 90),
    "C4": ("F", 18.20, 10.20, 0),
    "C5": ("F", 20.00, 21.20, 0),
    "C6": ("F", 29.00, 21.20, 0),
    "C7": ("F", 12.00, 25.60, 0),
    "C8": ("F", 17.20, 29.00, 90),
    "C9": ("F", 19.40, 29.00, 90),
    "C10": ("F", 40.90, 12.60, 90),
    "C11": ("F", 80.00, 23.60, 0),
    "C12": ("F", 46.80, 23.00, 0),
    "C13": ("F", 50.40, 23.00, 0),
    "C14": ("F", 110.00, 30.60, 90),
    "C15": ("F", 107.70, 30.60, 90),
    "C16": ("F", 57.60, 23.00, 0),
    "C17": ("F", 61.40, 23.00, 0),
    "C18": ("F", 31.50, 26.40, 0),
    "C19": ("F", 27.40, 26.40, 0),
    "C20": ("F", 111.60, 9.30, 0),
    "C21": ("F", 74.50, 45.50, 0),
    "C22": ("F", 13.40, 52.00, 0),
    "C23": ("F", 9.60, 57.00, 0),
    "C24": ("F", 4.60, 60.40, 0),
    "C25": ("F", 26.00, 54.00, 0),
    "C26": ("F", 24.00, 41.60, 0),
    "D1": ("F", 27.60, 10.20, 0),
    "D2": ("F", 118.00, 4.00, 0),
    "D3": ("F", 125.80, 50.00, 0),
    "D4": ("F", 74.50, 50.50, 0),
    "D5": ("F", 106.60, 14.20, 0),
    "D6": ("F", 118.00, 41.00, 0),
    "D7": ("F", 4.60, 57.00, 0),
    "D8": ("F", 17.60, 61.00, 0),
    "F1": ("F", 13.00, 10.20, 0),
    "J1": ("F", 3.65, 17.00, 270),
    "J2": ("F", 77.00, 55.50, 0),
    "J3": ("F", 66.00, 5.30, 90),
    "J4": ("F", 45.63, 27.60, 90),
    "J5": ("F", 121.30, 25.00, 90),
    "J6": ("B", 61.00, 32.00, 180),
    "J7": ("B", 31.50, 30.00, 180),
    "J8": ("F", 121.00, 60.00, 90),
    "J9": ("F", 47.00, 61.60, 90),
    "M1": ("F", 117.00, 46.00, 90),
    "Q1": ("F", 29.00, 13.80, 0),
    "Q2": ("F", 116.50, 10.40, 0),
    "Q3": ("F", 106.60, 18.40, 0),
    "Q4": ("F", 123.00, 41.00, 0),
    "Q5": ("F", 8.60, 48.00, 0),
    "Q6": ("F", 8.60, 52.60, 0),
    "Q7": ("F", 23.00, 60.40, 0),
    "R1": ("F", 40.90, 8.20, 90),
    "R2": ("F", 64.00, 8.80, 0),
    "R3": ("F", 67.50, 8.80, 0),
    "R4": ("F", 71.00, 8.80, 0),
    "R5": ("F", 10.60, 13.20, 90),
    "R6": ("F", 10.60, 21.00, 90),
    "R7": ("F", 24.60, 13.80, 90),
    "R8": ("F", 22.20, 10.20, 0),
    "R9": ("F", 36.30, 12.60, 90),
    "R10": ("F", 38.60, 12.60, 90),
    "R11": ("F", 76.00, 23.60, 0),
    "R12": ("F", 110.00, 21.00, 90),
    "R13": ("F", 110.00, 26.00, 90),
    "R14": ("F", 54.00, 23.00, 0),
    "R15": ("F", 107.50, 9.30, 0),
    "R16": ("F", 121.50, 10.00, 0),
    "R17": ("F", 116.50, 14.20, 0),
    "R18": ("F", 117.40, 50.00, 0),
    "R19": ("F", 121.40, 50.00, 0),
    "R20": ("F", 106.60, 22.40, 0),
    "R21": ("F", 126.20, 44.60, 90),
    "R22": ("F", 4.00, 49.00, 0),
    "R23": ("F", 13.40, 49.00, 0),
    "R24": ("F", 13.40, 57.00, 0),
    "R25": ("F", 9.60, 60.40, 0),
    "R26": ("F", 18.40, 47.00, 90),
    "R27": ("F", 24.00, 50.60, 0),
    "R28": ("F", 28.60, 44.00, 90),
    "R29": ("F", 28.60, 49.00, 90),
    "R30": ("F", 23.00, 56.00, 0),
    "SW1": ("F", 29.25, 2.25, 0),
    "SW2": ("F", 63.75, 12.00, 0),
    "SW3": ("F", 2.70, 30.00, 270),
    "SW4": ("F", 88.75, 28.75, 0),
    "SW5": ("F", 88.75, 46.75, 0),
    "SW6": ("F", 77.75, 37.75, 0),
    "SW7": ("F", 99.75, 37.75, 0),
    "SW8": ("F", 88.75, 37.75, 0),
    "SW9": ("F", 106.75, 53.75, 0),
    "U1": ("F", 52.00, 6.75, 0),
    "U2": ("F", 14.50, 17.00, 0),
    "U3": ("F", 20.00, 13.80, 0),
    "U4": ("F", 12.00, 30.00, 0),
    "U5": ("F", 78.00, 16.00, 0),
    "U6": ("F", 108.00, 3.20, 0),
    "U7": ("F", 24.00, 46.00, 0),
}

# (side, label, x0, y0, x1, y1) - module bodies, drawn on User.Drawings
BODIES = [
    ("F", "J4 OLED 1.3in module (approx 35.5 x 33.5)", 35.50, 26.00, 71.00, 59.50),
    ("B", "J6 CC1101 module (approx 16 x 30)", 51.00, 30.00, 67.00, 60.50),
    ("B", "J7 PN532 module (42.7 x 40.4)", 1.50, 22.50, 44.20, 62.90),
    ("B", "(battery 503450, 50 x 34)", 76.00, 13.00, 126.00, 47.00),
]
PN532_KEEPOUT = (1.50, 22.50, 44.20, 62.90)

def mm(v): return pcbnew.FromMM(float(v))
def pt(x, y): return pcbnew.VECTOR2I(mm(X0 + x), mm(Y0 + y))

def seg(board, a, b, layer, width=0.1):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(pt(*a)); s.SetEnd(pt(*b))
    s.SetLayer(layer); s.SetWidth(mm(width))
    board.Add(s)

def arc(board, start, mid, end, layer, width=0.1):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_ARC)
    s.SetArcGeometry(pt(*start), pt(*mid), pt(*end))
    s.SetLayer(layer); s.SetWidth(mm(width))
    board.Add(s)

def text(board, msg, x, y, layer, size=1.0):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(msg); t.SetPosition(pt(x, y)); t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size))); t.SetTextThickness(mm(size * 0.15))
    board.Add(t)

def run():
    board = pcbnew.GetBoard()
    moved, missing, flipped = 0, [], []
    for ref, (side, x, y, rot) in PLACE.items():
        fp = board.FindFootprintByReference(ref)
        if fp is None:
            missing.append(ref); continue
        want = pcbnew.B_Cu if side == "B" else pcbnew.F_Cu
        if fp.GetLayer() != want:
            fp.SetLayerAndFlip(want); flipped.append(ref)
        fp.SetPosition(pt(x, y))
        fp.SetOrientationDegrees(rot)
        moved += 1
    extra = sorted(f.GetReference() for f in board.GetFootprints() if f.GetReference() not in PLACE)

    # board outline
    has_edge = any(d.GetLayer() == pcbnew.Edge_Cuts for d in board.GetDrawings())
    if has_edge:
        print("Edge.Cuts already has a drawing - board outline NOT added.")
    else:
        e = pcbnew.Edge_Cuts
        try:
            r, k = RC, RC * (1 - 0.70710678)
            seg(board, (r, 0), (W - r, 0), e); seg(board, (W, r), (W, H - r), e)
            seg(board, (W - r, H), (r, H), e); seg(board, (0, H - r), (0, r), e)
            arc(board, (W - r, 0), (W - k, k), (W, r), e)
            arc(board, (W, H - r), (W - k, H - k), (W - r, H), e)
            arc(board, (r, H), (k, H - k), (0, H - r), e)
            arc(board, (0, r), (k, k), (r, 0), e)
        except Exception as ex:
            print("Rounded outline failed (%s), drawing square corners instead." % ex)
            for dd in [x for x in board.GetDrawings() if x.GetLayer() == pcbnew.Edge_Cuts]: board.Remove(dd)
            c = [(0, 0), (W, 0), (W, H), (0, H), (0, 0)]
            for a, b in zip(c, c[1:]): seg(board, a, b, e)

    # module bodies (front: OLED; back: PN532, CC1101, battery)
    du = pcbnew.Dwgs_User
    for side, label, x0, y0, x1, y1 in BODIES:
        c = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
        for a, b in zip(c, c[1:]): seg(board, a, b, du, 0.15)
        text(board, ("BACK: " if side == "B" else "FRONT: ") + label.strip("()"), (x0 + x1) / 2, y1 - 2.0, du, 1.0)

    # rule area: no copper pour under the PN532 antenna (tracks still allowed)
    try:
        x0, y0, x1, y1 = PN532_KEEPOUT
        z = pcbnew.ZONE(board)
        z.SetIsRuleArea(True)
        for name in ("SetDoNotAllowZoneFills", "SetDoNotAllowCopperPour"):
            if hasattr(z, name): getattr(z, name)(True)
        z.SetDoNotAllowTracks(False); z.SetDoNotAllowVias(False)
        z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False)
        try: cu = pcbnew.LSET.AllCuMask()
        except Exception: cu = pcbnew.LSET_AllCuMask()
        z.SetLayerSet(cu)
        o = z.Outline(); o.NewOutline()
        for (x, y) in [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]:
            p = pt(x, y); o.Append(p.x, p.y)
        z.SetZoneName("PN532 antenna - no copper pour")
        board.Add(z)
        print("Added rule area: no copper pour under the PN532 module.")
    except Exception as ex:
        print("Could not add the PN532 rule area (%s) - draw it by hand if you want it." % ex)

    pcbnew.Refresh()
    print("Moved %d footprints. Flipped to the other side: %s" % (moved, ", ".join(flipped) or "none"))
    if missing: print("NOT FOUND on the board (update the PCB from the schematic first?): " + ", ".join(missing))
    if extra: print("On the board but not in this placement (left where they were): " + ", ".join(extra))

run()
