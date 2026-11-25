#!/usr/bin/env python3
"""
Custom 3D / Cyberpunk Telemetry Design System Generator for Rakib Hasan Piyas (rhpiyas).
Inspired by the industrial, isometric 3D plate architecture of Shafiur0/Shafiur0.
"""

import os

W = 1000
MARGIN = 48

BG      = "#0A0A0C"
PANEL   = "#101014"
PANEL2  = "#17171D"
HAIR    = "#2A2A32"
HAIR2   = "#3A3A44"
INK     = "#F2F1EC"
INK2    = "#9C9CA6"
INK3    = "#5C5C67"
ACC     = "#FF4B1F"      # Cyber Orange Accent
ACC_DIM = "#7A2410"
CYAN    = "#00E5FF"      # Electric Cyan

MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "ds")
os.makedirs(OUT_DIR, exist_ok=True)


def svg_wrap(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" fill="none" role="img">'
            f'<defs>{defs}</defs>{body}</svg>')


def plate(w, h, rx=16, fill=BG, stroke=HAIR):
    return f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'


def grid(w, h, step_x=62.5, step_y=55, opacity=0.032):
    lines = []
    x = step_x
    while x < w:
        lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="#FFFFFF" stroke-width="1" opacity="{opacity}"/>')
        x += step_x
    y = step_y
    while y < h:
        lines.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#FFFFFF" stroke-width="1" opacity="{opacity}"/>')
        y += step_y
    return "".join(lines)


def rule(x1, y1, x2, y2, stroke=HAIR, stroke_width=1):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}"/>'


def txt(text, x, y, size=10, fill=INK, font=MONO, weight=400, letter_spacing=1.5, anchor="start"):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{letter_spacing}" fill="{fill}" '
            f'text-anchor="{anchor}">{text}</text>')


def arrow(x, y, s=7.0, color=ACC, w=1.25):
    return (f'<path d="M{x-s} {y} L{x} {y-s} M{x-s*0.45} {y-s} L{x} {y-s} L{x} {y-s*0.45}" '
            f'stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="square"/>')


def _stack(ox, oy, h=65, yf=0.34, spacing=61, th=8, n=5):
    """Exploded isometric 3D stack of 5 floating slabs."""
    C = 0.866

    def P(x, y, z):
        return (ox + (x - y) * C, oy + (x + y) * yf - z)

    def pts(seq):
        return " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in seq)

    out = []
    out.append(f'<line x1="{ox}" y1="{oy - (n-1)*spacing - 2*h*yf - 30}" x2="{ox}" '
               f'y2="{oy + 2*h*yf + 26}" stroke="{ACC}" stroke-width="1" '
               f'opacity="0.28" stroke-dasharray="2 7"/>')

    for i in range(n):
        z = i * spacing
        top = [P(-h, -h, z + th), P(h, -h, z + th), P(h, h, z + th), P(-h, h, z + th)]
        left = [P(-h, h, z + th), P(h, h, z + th), P(h, h, z), P(-h, h, z)]
        right = [P(h, -h, z + th), P(h, h, z + th), P(h, h, z), P(h, -h, z)]

        top_slab = (i == n - 1)
        op = 0.95 if top_slab else 0.66 + 0.07 * i
        g = [f'<g opacity="{op:.2f}">']
        g.append(f'<polygon points="{pts(left)}" fill="#0D0D12" stroke="#31313A" stroke-width="0.8"/>')
        g.append(f'<polygon points="{pts(right)}" fill="#101016" stroke="#31313A" stroke-width="0.8"/>')
        g.append(f'<polygon points="{pts(top)}" fill="#191921" stroke="#3C3C47" stroke-width="0.9"/>')

        for t in (-0.5, 0.0, 0.5):
            a, b = P(-h, h * t, z + th), P(h, h * t, z + th)
            g.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#3A3A45" stroke-width="0.55"/>')
            a, b = P(h * t, -h, z + th), P(h * t, h, z + th)
            g.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#3A3A45" stroke-width="0.55"/>')

        if top_slab:
            s = 20
            ctop = [P(-s, -s, z + th + 46), P(s, -s, z + th + 46), P(s, s, z + th + 46), P(-s, s, z + th + 46)]
            cbot = [P(-s, -s, z + th + 18), P(s, -s, z + th + 18), P(s, s, z + th + 18), P(-s, s, z + th + 18)]
            g.append(f'<polygon points="{pts(ctop)}" fill="{ACC}" fill-opacity="0.15" stroke="{ACC}" stroke-width="1.2"/>')
            g.append(f'<polygon points="{pts(cbot)}" fill="none" stroke="{ACC}" stroke-width="0.8" stroke-dasharray="2 3"/>')
            for p1, p2 in zip(ctop, cbot):
                g.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="{ACC}" stroke-width="1"/>')
            cp = P(0, 0, z + th + 32)
            g.append(f'<circle cx="{cp[0]:.1f}" cy="{cp[1]:.1f}" r="3.5" fill="{ACC}"/>')
            g.append(f'<circle cx="{cp[0]:.1f}" cy="{cp[1]:.1f}" r="3.5" fill="none" stroke="{ACC}" stroke-width="1">'
                     f'<animate attributeName="r" values="3.5;14" dur="2.4s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0.8;0" dur="2.4s" repeatCount="indefinite"/></circle>')

        out.append(f'<g><animateTransform attributeName="transform" type="translate" '
                   f'values="0 0; 0 -4; 0 0" dur="6.2s" begin="{-i * 0.6:.1f}s" '
                   f'repeatCount="indefinite"/>{"".join(g)}</g>')
    return "".join(out)


# ══════════════════════════════════════════════════════════════════════════════
# 1. COVER PLATE
# ══════════════════════════════════════════════════════════════════════════════
def gen_cover():
    H = 580
    b = [plate(W, H), f'<g clip-path="url(#coverClip)">{grid(W, H)}</g>']

    # Corner brackets
    for cx in (13, W - 13):
        b.append(f'<path d="M{cx + 9} 13 L{cx} 13 L{cx} 22" stroke="{INK3}" stroke-width="1" opacity="0.35" fill="none"/>')

    # 3D isometric stack
    b.append(f'<ellipse cx="838" cy="272" rx="145" ry="215" fill="url(#stackGlow)"/>')
    b.append(_stack(838, 386, h=65, yf=0.34, spacing=61, th=8, n=5))

    # Top metadata
    b.append(txt("SOFTWARE ENGINEER &amp; AI ENTHUSIAST — PORTFOLIO INDEX", MARGIN, 44, 9.5, INK3, letter_spacing=2.3))
    b.append(txt("ED. 2026  /  DHAKA, BANGLADESH  ·  23.8103°N 90.4125°E", W - MARGIN, 44, 9.5, INK3, letter_spacing=2.3, anchor="end"))
    b.append(rule(MARGIN, 58, W - MARGIN, 58))

    # Kicker
    b.append(f'<rect x="{MARGIN}" y="112" width="7" height="7" fill="{ACC}"/>')
    b.append(txt("RAKIB HASAN", MARGIN + 17, 120, 12, ACC, letter_spacing=4.2))

    # Main Big Name
    b.append(txt("PIYAS", MARGIN, 280, 160, "url(#inkG)", font=SANS, weight=900, letter_spacing=-4.0))

    # Animated blinking cursor block
    b.append(f'<rect x="{MARGIN + 460}" y="200" width="22" height="78" fill="{ACC}">'
             f'<animate attributeName="opacity" values="1;1;0.12;1" dur="3.5s" repeatCount="indefinite" keyTimes="0;0.87;0.94;1"/></rect>')

    # Horizontal divider under name
    b.append(rule(MARGIN, 320, MARGIN + 520, 320, HAIR2))
    b.append(f'<line x1="{MARGIN}" y1="320" x2="{MARGIN+64}" y2="320" stroke="{ACC}" stroke-width="2"/>')

    # Subtitles
    b.append(txt("FULL-STACK DEVELOPMENT · MACHINE LEARNING · COMPETITIVE PROGRAMMING",
                 MARGIN, 356, 11.5, INK2, letter_spacing=2.4))
    b.append(txt("B.SC. SOFTWARE ENGINEERING — DAFFODIL INTERNATIONAL UNIVERSITY  /  CODEFORCES: RH_PIYAS",
                 MARGIN, 380, 9.5, INK3, letter_spacing=1.9))

    # Bottom strip with metrics
    b.append(rule(MARGIN, 500, W - MARGIN, 500))
    stats = [("05+", "CORE BUILDS"), ("100+", "CP PROBLEMS"), ("2023", "ACTIVE SINCE")]
    x = MARGIN
    for i, (num, lab) in enumerate(stats):
        b.append(txt(num, x, 532, 20, INK, font=SANS, weight=800, letter_spacing=-0.5))
        lx = x + len(num) * 14 + 10
        b.append(txt(lab, lx, 530, 8.5, INK3, letter_spacing=1.7))
        x = lx + len(lab) * 7.0 + 36
        if i < len(stats) - 1:
            b.append(rule(x - 18, 516, x - 18, 540, HAIR))

    px = W - MARGIN - 210
    b.append(f'<circle cx="{px+6}" cy="527" r="3.2" fill="{ACC}"/>'
             f'<circle cx="{px+6}" cy="527" r="3.2" fill="none" stroke="{ACC}" stroke-width="1">'
             f'<animate attributeName="r" values="3.2;15" dur="2.8s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0.65;0" dur="2.8s" repeatCount="indefinite"/></circle>')
    b.append(txt("OPEN TO COLLABORATE", px + 22, 530, 9.5, INK2, letter_spacing=2.1))

    # Sweep scanline
    b.append(f'<g clip-path="url(#coverClip)"><g><rect x="0" y="-170" width="{W}" height="170" fill="url(#sweep)"/>'
             f'<animateTransform attributeName="transform" type="translate" from="0 0" to="0 {H+170}" dur="14s" repeatCount="indefinite"/></g></g>')

    defs = (f'<clipPath id="coverClip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15"/></clipPath>'
            f'<linearGradient id="inkG" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="#FFFFFF"/><stop offset="60%" stop-color="#F2F1EC"/>'
            f'<stop offset="100%" stop-color="#9E9EA8"/></linearGradient>'
            f'<linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{ACC}" stop-opacity="0"/>'
            f'<stop offset="70%" stop-color="{ACC}" stop-opacity="0.055"/>'
            f'<stop offset="100%" stop-color="{ACC}" stop-opacity="0"/></linearGradient>'
            f'<radialGradient id="stackGlow" cx="0.5" cy="0.5" r="0.5">'
            f'<stop offset="0%" stop-color="{ACC}" stop-opacity="0.14"/>'
            f'<stop offset="55%" stop-color="{ACC}" stop-opacity="0.04"/>'
            f'<stop offset="100%" stop-color="{ACC}" stop-opacity="0"/></radialGradient>')

    with open(os.path.join(OUT_DIR, "cover.svg"), "w") as f:
        f.write(svg_wrap(W, H, "".join(b), defs))


# ══════════════════════════════════════════════════════════════════════════════
# 2. NAV & CTA CHIPS
# ══════════════════════════════════════════════════════════════════════════════
def gen_chips():
    cw, ch = 172, 50
    x0, y0, iw, ih = 7, 7, 158, 36

    nav_items = [
        ("01", "PROFILE"),
        ("02", "STACK"),
        ("03", "WORK"),
        ("04", "CP"),
        ("05", "STATS"),
        ("06", "CONTACT")
    ]

    for i, (num, label) in enumerate(nav_items):
        b = [f'<rect x="{x0+0.5}" y="{y0+0.5}" width="{iw-1}" height="{ih-1}" rx="4" fill="{PANEL}" stroke="{HAIR}" stroke-width="1"/>']
        # Number + label centered
        b.append(txt(num, x0 + 26, y0 + 23, 9, ACC, letter_spacing=1.4))
        b.append(txt(label, x0 + 58, y0 + 23, 10.5, INK2, letter_spacing=2.0))
        filename = f"nav-{i+1:02d}.svg"
        with open(os.path.join(OUT_DIR, filename), "w") as f:
            f.write(svg_wrap(cw, ch, "".join(b)))

    cta_items = ["EMAIL", "PORTFOLIO", "LINKEDIN", "GITHUB", "CODEFORCES", "INSTAGRAM"]
    for i, label in enumerate(cta_items):
        b = [f'<rect x="{x0+0.5}" y="{y0+0.5}" width="{iw-1}" height="{ih-1}" rx="4" fill="{PANEL}" stroke="{HAIR}" stroke-width="1"/>']
        b.append(arrow(x0 + 28, y0 + 24, 6.5, ACC))
        b.append(txt(label, x0 + 44, y0 + 23, 9.5, INK2, letter_spacing=1.8))
        filename = f"cta-{i+1:02d}.svg"
        with open(os.path.join(OUT_DIR, filename), "w") as f:
            f.write(svg_wrap(cw, ch, "".join(b)))


# ══════════════════════════════════════════════════════════════════════════════
# 3. SECTION HEADERS
# ══════════════════════════════════════════════════════════════════════════════
def gen_headers():
    H = 100
    headers_data = [
        ("01", "PROFILE", "SYSTEM CORE — IDENTITY, DISCIPLINE, INTENT"),
        ("02", "STACK", "TECH MATRIX — ARCHITECTURE, LAYERS, DEPTH"),
        ("03", "WORK", "SELECTED BUILDS — REPOSITORIES & SYSTEMS"),
        ("04", "CP", "ALGORITHMIC DISCIPLINE — COMPETITIVE PROGRAMMING"),
        ("05", "STATS", "TELEMETRY — LIVE GITHUB SIGNAL & ANALYTICS"),
        ("06", "CONTACT", "UPLINK — OPEN COMMS & NETWORK CHANNELS"),
    ]

    for idx, (num, title, sub) in enumerate(headers_data):
        b = [plate(W, H, rx=12),
             f'<g clip-path="url(#hc)">{grid(W, H, 62.5, 50)}</g>']
        b.append(rule(MARGIN, 34, MARGIN, 64, HAIR2))
        b.append(rule(MARGIN + 44, 34, MARGIN + 44, 64, HAIR2))
        b.append(txt(num, MARGIN + 12, 54, 18, ACC, letter_spacing=0.5))
        b.append(txt(title, MARGIN + 64, 55, 26, INK, font=SANS, weight=800, letter_spacing=-0.5))
        b.append(txt(sub, MARGIN + 64, 78, 9, INK3, letter_spacing=2.2))
        b.append(txt(f"SEC. {num} / 06", W - MARGIN, 55, 9, INK3, letter_spacing=2.0, anchor="end"))
        b.append(f'<line x1="{MARGIN}" y1="90" x2="{MARGIN+64}" y2="90" stroke="{ACC}" stroke-width="2"/>')

        defs = f'<clipPath id="hc"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="11"/></clipPath>'
        filename = f"head-{idx+1:02d}.svg"
        with open(os.path.join(OUT_DIR, filename), "w") as f:
            f.write(svg_wrap(W, H, "".join(b), defs))


# ══════════════════════════════════════════════════════════════════════════════
# 4. SPEC SHEET
# ══════════════════════════════════════════════════════════════════════════════
def gen_spec():
    rows = [
        ("NAME", "RAKIB HASAN PIYAS", False),
        ("ROLE", "SOFTWARE ENGINEERING STUDENT · FULL-STACK & AI DEVELOPER", False),
        ("BASE", "DHAKA, BANGLADESH  ·  23.8103°N  90.4125°E", False),
        ("STUDYING", "B.SC. SOFTWARE ENGINEERING — DAFFODIL INTERNATIONAL UNIVERSITY (DIU)", False),
        ("FOCUS", "COMPETITIVE PROGRAMMING · WEB ARCHITECTURE · MACHINE LEARNING", False),
        ("STATUS", "OPEN TO INTERNSHIPS, RESEARCH & OPEN-SOURCE COLLABORATION", True),
    ]
    top, rh = 26, 46
    H = top + rh * len(rows) + 16
    b = [plate(W, H)]
    for i, (lab, val, hot) in enumerate(rows):
        y = top + i * rh
        b.append(txt(lab, MARGIN, y + 27, 9, INK3, letter_spacing=2.1))
        b.append(txt(val, 210, y + 27, 11, ACC if hot else INK, letter_spacing=0.9))
        b.append(txt(f"{i+1:02d}", W - MARGIN, y + 27, 8.5, INK3, letter_spacing=1.3, anchor="end"))
        if i:
            b.append(rule(MARGIN, y, W - MARGIN, y))
    b.append(rule(MARGIN, top + rh * len(rows), W - MARGIN, top + rh * len(rows)))
    with open(os.path.join(OUT_DIR, "spec.svg"), "w") as f:
        f.write(svg_wrap(W, H, "".join(b)))


# ══════════════════════════════════════════════════════════════════════════════
# 5. STACK MATRIX
# ══════════════════════════════════════════════════════════════════════════════
def gen_stack():
    rows = [
        ("L01", "LANGUAGES", 18, "C · C++ · PYTHON · JAVA · JAVASCRIPT"),
        ("L02", "FRONTEND", 17, "HTML5 · CSS3 · REACT · TAILWIND CSS · ELECTRON.JS"),
        ("L03", "BACKEND & DB", 16, "NODE.JS · EXPRESS · MYSQL · REST APIS"),
        ("L04", "TOOLS & OS", 17, "GIT · GITHUB · VS CODE · LINUX · BASH"),
        ("L05", "AI & ALGO", 15, "OPENCV · COMPUTER VISION · DATA STRUCTURES · CP"),
    ]
    top, rh = 26, 58
    H = top + rh * len(rows) + 14
    b = [plate(W, H), f'<g clip-path="url(#clipStack)">{grid(W, H, 62.5, 58)}</g>']

    b.append(txt("LAYER", MARGIN, 18, 8, INK3, letter_spacing=1.8))
    b.append(txt("DEPTH", 300, 18, 8, INK3, letter_spacing=1.8))
    b.append(txt("TOOLING & TECHNOLOGIES", 528, 18, 8, INK3, letter_spacing=1.8))

    for i, (code, name, level, tools) in enumerate(rows):
        y = top + i * rh
        cy = y + rh / 2
        b.append(txt(code, MARGIN, cy + 3.4, 8.5, ACC, letter_spacing=1.3))
        b.append(txt(name, 96, cy + 5, 14, INK, font=SANS, weight=700, letter_spacing=-0.2))

        # 20-segment meter
        for s in range(20):
            sx = 300 + s * 10
            on = s < level
            b.append(f'<rect x="{sx}" y="{cy-4}" width="7" height="8" rx="1" '
                     f'fill="{ACC if on else HAIR2}" opacity="{1 if on else 0.85}"/>')
        b.append(txt(tools, 528, cy + 3.4, 9.5, INK2, letter_spacing=0.8))
        if i:
            b.append(rule(MARGIN, y, W - MARGIN, y))

    b.append(rule(MARGIN, top + rh * len(rows), W - MARGIN, top + rh * len(rows)))
    defs = f'<clipPath id="clipStack"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15"/></clipPath>'
    with open(os.path.join(OUT_DIR, "stack.svg"), "w") as f:
        f.write(svg_wrap(W, H, "".join(b), defs))


# ══════════════════════════════════════════════════════════════════════════════
# 6. PROJECT CARDS
# ══════════════════════════════════════════════════════════════════════════════
def glyph(kind, cx, cy):
    if kind == "biometric":
        return (f'<circle cx="{cx}" cy="{cy}" r="32" stroke="{HAIR2}" stroke-width="1"/>'
                f'<circle cx="{cx}" cy="{cy}" r="20" stroke="{HAIR2}" stroke-width="1"/>'
                f'<circle cx="{cx}" cy="{cy}" r="8" stroke="{ACC}" stroke-width="1"/>'
                f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="{ACC}"/>'
                f'<path d="M{cx-36} {cy} H{cx+36} M{cx} {cy-36} V{cy+36}" stroke="{HAIR2}" stroke-width="1" opacity="0.6"/>')
    elif kind == "stream":
        return (f'<rect x="{cx-24}" y="{cy-24}" width="48" height="48" rx="6" stroke="{HAIR2}" stroke-width="1"/>'
                f'<line x1="{cx}" y1="{cy-16}" x2="{cx}" y2="{cy+10}" stroke="{ACC}" stroke-width="2"/>'
                f'<path d="M{cx-8} {cy+4} L{cx} {cy+12} L{cx+8} {cy+4}" stroke="{ACC}" stroke-width="2" fill="none"/>'
                f'<line x1="{cx-16}" y1="{cy+16}" x2="{cx+16}" y2="{cy+16}" stroke="{HAIR2}" stroke-width="2"/>')
    elif kind == "grid":
        return (f'<rect x="{cx-24}" y="{cy-24}" width="48" height="48" rx="4" stroke="{HAIR2}" stroke-width="1"/>'
                f'<line x1="{cx-24}" y1="{cy}" x2="{cx+24}" y2="{cy}" stroke="{HAIR2}" stroke-width="1"/>'
                f'<line x1="{cx}" y1="{cy-24}" x2="{cx}" y2="{cy+24}" stroke="{HAIR2}" stroke-width="1"/>'
                f'<circle cx="{cx-12}" cy="{cy-12}" r="4" fill="{ACC}"/>'
                f'<circle cx="{cx+12}" cy="{cy+12}" r="4" fill="{HAIR2}"/>')
    else:  # counter / pulse
        return (f'<rect x="{cx-26}" y="{cy-20}" width="52" height="40" rx="4" stroke="{HAIR2}" stroke-width="1"/>'
                f'<path d="M{cx-20} {cy} L{cx-8} {cy} L{cx-2} {cy-12} L{cx+4} {cy+10} L{cx+10} {cy} L{cx+20} {cy}" '
                f'stroke="{ACC}" stroke-width="1.8" fill="none"/>')


def gen_cards():
    cards_data = [
        dict(num="01", kicker="AI & COMPUTER VISION", title="FACEENTRYPRO", glyph="biometric",
             sub="SMART ATTENDANCE & FACIAL RECOGNITION SYSTEM",
             desc=["Automated biometric verification platform using facial feature",
                   "landmarks and OpenCV real-time video inference pipeline."],
             tags=["PYTHON", "OPENCV", "AI/ML", "COMPUTER VISION"], note="PRODUCTION ARCHITECTURE"),

        dict(num="02", kicker="DESKTOP & SYSTEMS", title="DOWNLOAD MANAGER", glyph="stream",
             sub="MULTI-THREADED DESKTOP DOWNLOAD ENGINE",
             desc=["High-performance desktop accelerator featuring multi-chunking,",
                   "pause/resume handling, and responsive queue lifecycle."],
             tags=["ELECTRON.JS", "NODE.JS", "JAVASCRIPT", "DESKTOP"], note="DESKTOP SOFTWARE"),

        dict(num="03", kicker="SYSTEM ARCHITECTURE", title="SMART PARKING", glyph="grid",
             sub="INTELLIGENT SPACE RESERVATION SYSTEM",
             desc=["Automated vehicle slot allocation, real-time availability tracking,",
                   "and database architecture for modern parking facilities."],
             tags=["SOFTWARE ENG", "MYSQL", "SYSTEM DESIGN", "DATABASE"], note="ACADEMIC PROJECT"),

        dict(num="04", kicker="WEB UTILITY", title="COUNT ME", glyph="counter",
             sub="REAL-TIME RESPONSIVE COUNTING SUITE",
             desc=["Modern, lightweight web application built for seamless real-time tallying,",
                   "data persistence, and intuitive responsive user interfaces."],
             tags=["HTML5", "CSS3", "JAVASCRIPT", "UI/UX"], note="WEB APPLICATION"),
    ]

    CW, CH = 480, 306
    for i, c in enumerate(cards_data):
        b = [plate(CW, CH, rx=12, fill=PANEL)]
        b.append(f'<g clip-path="url(#cc{i})">{grid(CW, CH, 60, 51, opacity=0.028)}</g>')
        b.append(glyph(c["glyph"], 410, 78))
        b.append(txt(f'{c["num"]} / {c["kicker"]}', 28, 40, 8.5, ACC, letter_spacing=2.0))
        b.append(txt(c["title"], 28, 102, 23, INK, font=SANS, weight=800, letter_spacing=-0.5))
        b.append(txt(c["sub"], 28, 126, 8.5, INK3, letter_spacing=1.8))
        for j, line in enumerate(c["desc"]):
            b.append(txt(line, 28, 164 + j * 18, 10, INK2, letter_spacing=0.4))
        b.append(rule(28, 216, CW - 28, 216))

        tx = 28
        for t in c["tags"]:
            tw = len(t) * 6.0 + 16
            b.append(f'<rect x="{tx}" y="234" width="{tw:.0f}" height="20" rx="3" fill="{PANEL2}" stroke="{HAIR}" stroke-width="1"/>')
            b.append(txt(t, tx + 8, 248, 7.6, INK2, letter_spacing=1.2))
            tx += tw + 6

        b.append(txt(c["note"], 28, 282, 8, INK3, letter_spacing=1.6))
        b.append(txt("OPEN", CW - 48, 282, 8, ACC, letter_spacing=1.6, anchor="end"))
        b.append(arrow(CW - 30, 284, 6.4))

        defs = f'<clipPath id="cc{i}"><rect x="1" y="1" width="{CW-2}" height="{CH-2}" rx="11"/></clipPath>'
        filename = f"card-{i+1:02d}.svg"
        with open(os.path.join(OUT_DIR, filename), "w") as f:
            f.write(svg_wrap(CW, CH, "".join(b), defs))


# ══════════════════════════════════════════════════════════════════════════════
# 7. WORK INDEX
# ══════════════════════════════════════════════════════════════════════════════
def gen_work_index():
    rows = [
        ("01", "FACEENTRYPRO", "PYTHON · OPENCV · AI/ML", "AI · BIOMETRICS"),
        ("02", "DOWNLOAD MANAGER", "ELECTRON.JS · NODE.JS · JAVASCRIPT", "DESKTOP · UTILITY"),
        ("03", "SMART PARKING SYSTEM", "SOFTWARE ENG · MYSQL · DATABASE", "SYSTEMS · INFRA"),
        ("04", "COUNT ME", "HTML5 · CSS3 · JAVASCRIPT", "FRONTEND · WEB APP"),
        ("05", "CP REPOSITORY", "C++ · STL · ALGORITHMS · DSA", "PROBLEM SOLVING · CP"),
    ]
    top, rh = 50, 46
    H = top + rh * len(rows) + 16
    b = [plate(W, H)]
    for x, lab in [(MARGIN, "NO."), (100, "PROJECT"), (420, "STACK"), (760, "DOMAIN")]:
        b.append(txt(lab, x, 32, 8, INK3, letter_spacing=1.9))
    b.append(rule(MARGIN, 42, W - MARGIN, 42, HAIR2))

    for i, (no, proj, stack_txt, dom) in enumerate(rows):
        y = top + i * rh
        cy = y + rh / 2 + 5
        b.append(txt(no, MARGIN, cy, 8.5, ACC, letter_spacing=1.3))
        b.append(txt(proj, 100, cy + 1, 14, INK, font=SANS, weight=700, letter_spacing=-0.2))
        b.append(txt(stack_txt, 420, cy, 8.4, INK2, letter_spacing=0.9))
        b.append(txt(dom, 760, cy, 8.4, INK3, letter_spacing=1.1))
        if i:
            b.append(rule(MARGIN, y, W - MARGIN, y))
    b.append(rule(MARGIN, top + rh * len(rows), W - MARGIN, top + rh * len(rows)))
    with open(os.path.join(OUT_DIR, "work-index.svg"), "w") as f:
        f.write(svg_wrap(W, H, "".join(b)))


# ══════════════════════════════════════════════════════════════════════════════
# 8. CAPTION GRID & FOOTER
# ══════════════════════════════════════════════════════════════════════════════
def gen_cap_grid():
    H = 36
    b = [txt("CONTRIBUTION ACTIVITY — ANIMATED GRID", MARGIN, 24, 8.5, ACC, letter_spacing=2.2),
         txt("REGENERATED EVERY 12 HOURS", W - MARGIN, 24, 8.5, INK3, letter_spacing=2.0, anchor="end")]
    with open(os.path.join(OUT_DIR, "cap-grid.svg"), "w") as f:
        f.write(svg_wrap(W, H, "".join(b)))


def gen_footer():
    H = 240
    b = [plate(W, H), f'<g clip-path="url(#fc)">{grid(W, H, 62.5, 48)}</g>']
    b.append(txt("END OF TRANSMISSION", MARGIN, 40, 8.5, INK3, letter_spacing=2.2))
    b.append(txt("06 / 06", W - MARGIN, 40, 8.5, INK3, letter_spacing=2.2, anchor="end"))
    b.append(rule(MARGIN, 52, W - MARGIN, 52))

    b.append(txt("LET'S BUILD", MARGIN, 120, 56, "url(#fg)", font=SANS, weight=900, letter_spacing=-1.5))
    b.append(txt("SOMETHING EXTRAORDINARY.", MARGIN, 172, 56, ACC, font=SANS, weight=900, letter_spacing=-1.5))

    b.append(rule(MARGIN, 202, W - MARGIN, 202))
    b.append(txt("RAKIB HASAN PIYAS  ·  DHAKA, BANGLADESH  ·  ENGINEERED FOR EXCELLENCE",
                 MARGIN, 222, 8.6, INK3, letter_spacing=1.8))
    b.append(txt("© 2026", W - MARGIN, 222, 8.6, INK3, letter_spacing=1.8, anchor="end"))

    defs = (f'<linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#888894"/></linearGradient>'
            f'<clipPath id="fc"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15"/></clipPath>')

    with open(os.path.join(OUT_DIR, "footer.svg"), "w") as f:
        f.write(svg_wrap(W, H, "".join(b), defs))


if __name__ == "__main__":
    print("Generating 3D Design System plates for Rakib Hasan Piyas...")
    gen_cover()
    gen_chips()
    gen_headers()
    gen_spec()
    gen_stack()
    gen_cards()
    gen_work_index()
    gen_cap_grid()
    gen_footer()
    print(f"Done! All SVGs successfully emitted to {OUT_DIR}")
