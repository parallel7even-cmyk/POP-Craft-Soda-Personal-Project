#!/usr/bin/env python3
"""
Export the POP! brand kit as a Behance-ready image set.

Reads behance/presentation.html, splits it into one standalone HTML file per
panel (markers: <!-- PANEL:slug:Name:HEIGHT --> ... <!-- /PANEL -->), renders
each with headless Chrome at 2x, then writes optimised JPEGs next to the PNGs.

Output: behance/exports/
  cover.jpg           1400 x 1050   (Behance cover, 4:3, no GIF allowed for covers)
  01-the-brand.jpg    2800 x 2H     (project modules, retina/lightbox quality)
  ...
"""
import os, re, subprocess, sys, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
BH = os.path.join(ROOT, "behance")
SRC = os.path.join(BH, "presentation.html")
OUT = os.path.join(BH, "exports")
TMP = os.path.join(BH, ".tmp")

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]
SCALE = 2          # 2x -> 2800px wide modules for Behance lightbox
COVER_SCALE = 1    # cover exported at exactly 1400x1050

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>{slug}</title>
<link rel="stylesheet" href="../fonts.css">
<style>
html,body{{margin:0;padding:0;background:{bg}}}
body{{width:1400px}}
#stack .panel{{border:0 !important}}
</style>
<link rel="stylesheet" href="presentation.css">
</head><body><div id="stack">
{panel}
</div></body></html>
"""


def fmt_bytes(n):
    return "%.2f MB" % (n / 1048576.0)


def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.exists(c):
            return c
    sys.exit("No Chromium-based browser found. Install Google Chrome.")


def parse_panels(html):
    panels = []
    for m in re.finditer(
        r"<!--\s*PANEL:([a-z0-9-]+):([^>]+?)\s*-->(.*?)<!--\s*/PANEL\s*-->",
        html, re.S | re.I):
        body = m.group(3).strip()
        h = re.search(r'data-h="(\d+)"', body)
        if not h:
            sys.exit("panel '%s' has no data-h height attribute" % m.group(1))
        panels.append({
            "slug": m.group(1),
            "name": m.group(2).strip(),
            "height": int(h.group(1)),
            "html": body,
        })
    return panels


def verify(chrome):
    """Render the whole case study once and read the diagnostic attributes the
    page writes (per-panel overflow + whether Fredoka/DM Sans actually loaded)."""
    r = subprocess.run([
        chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--no-first-run", "--virtual-time-budget=6000",
        "--allow-file-access-from-files", "--dump-dom", "file://" + SRC,
    ], capture_output=True, text=True)
    dom = r.stdout

    fonts = re.search(r'data-fonts="([^"]*)"', dom)
    print("\nFONT CHECK:", fonts.group(1) if fonts else "diagnostic did not run")
    if fonts and "false" in fonts.group(1):
        print("  WARNING: a brand font did not load - export would use a fallback!")

    print("OVERFLOW CHECK (0 = content fits its panel):")
    problems = 0
    for m in re.finditer(r'<section[^>]*id="([a-z0-9-]+)"[^>]*data-overflow="(-?\d+)"', dom):
        slug, over = m.group(1), int(m.group(2))
        flag = "  <-- OVERFLOWS, content is clipped" if over > 2 else ""
        if over > 2:
            problems += 1
        print("  %-14s %+5d px%s" % (slug, over, flag))
    if problems:
        print("  %d panel(s) need their height bumped or content trimmed." % problems)
    else:
        print("  all panels fit.")


def main():
    chrome = find_chrome()
    html = open(SRC).read()
    panels = parse_panels(html)
    if not panels:
        sys.exit("No panels found - check the <!-- PANEL:... --> markers.")

    for d in (OUT, TMP):
        os.makedirs(d, exist_ok=True)

    rows = []
    for i, p in enumerate(panels, 1):
        is_cover = p["slug"] == "cover"
        scale = COVER_SCALE if is_cover else SCALE
        name = "cover" if is_cover else "%02d-%s" % (i - 1, p["slug"])
        src_html = os.path.join(BH, ".tmp-page-%s.html" % p["slug"])
        # page lives in behance/ so relative ../fonts.css and ../logo-*.svg resolve
        with open(src_html, "w") as fh:
            fh.write(TEMPLATE.format(slug=p["slug"], bg="#FFF4E4", panel=p["html"]))

        png = os.path.join(OUT, name + ".png")
        cmd = [
            chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--no-first-run", "--no-default-browser-check",
            "--force-device-scale-factor=%d" % scale,
            "--window-size=1400,%d" % p["height"],
            "--virtual-time-budget=6000",
            "--default-background-color=FFF4E4",
            "--allow-file-access-from-files",
            "--screenshot=" + png,
            "file://" + src_html,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if not os.path.exists(png):
            print(r.stdout[-800:], r.stderr[-800:])
            sys.exit("render failed for " + p["slug"])

        # JPEG sibling (Behance recommends JPEG, smaller + faster to load)
        jpg = os.path.join(OUT, name + ".jpg")
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "90",
                        png, "--out", jpg], capture_output=True)

        dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", png],
                              capture_output=True, text=True).stdout
        w = re.search(r"pixelWidth: (\d+)", dims).group(1)
        h = re.search(r"pixelHeight: (\d+)", dims).group(1)
        rows.append((name, "%s x %s" % (w, h), fmt_bytes(os.path.getsize(png)),
                     fmt_bytes(os.path.getsize(jpg)), p["name"]))
        os.remove(src_html)
        print("  rendered %-22s %sx%s  png %s  jpg %s" % (name, w, h,
              fmt_bytes(os.path.getsize(png)), fmt_bytes(os.path.getsize(jpg))))

    verify(chrome)

    shutil.rmtree(TMP, ignore_errors=True)
    print("\n%-24s %-14s %-10s %-10s %s" % ("FILE", "PIXELS", "PNG", "JPG", "PANEL"))
    for r in rows:
        print("%-24s %-14s %-10s %-10s %s" % r)
    mp = max(int(r[1].split(" x ")[0]) * int(r[1].split(" x ")[1]) for r in rows)
    print("\nlargest image: %.1f MP (Behance limit 32 MP)" % (mp / 1e6))
    print("exports ->", OUT)


if __name__ == "__main__":
    main()
