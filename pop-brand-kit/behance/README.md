# POP! Craft Soda Co. — Behance upload kit

Everything in `behance/exports/` is sized for Behance and ready to drag in.
Text modules to paste are below — copy them straight into Behance's text
modules between the images.

> **Why images and not the HTML?** Behance strips HTML/CSS/JS — it only accepts
> images, text, video and embeds. So the interactive kit (`guidelines.html`) is
> exported here as a static, scroll-friendly case study.

---

## Specs used (verified against Behance's help center, 2026)

| Thing | Behance spec | What we shipped |
|---|---|---|
| Project images | displayed at 1400px; upload up to 2800px for lightbox/retina | **2800px wide** (2x), retina-sharp |
| Project image file size | ≤10MB recommended, 50MB max, 32MP max | largest is 9.5 MP / 0.74MB — comfortable |
| Formats | JPEG (recommended), PNG, GIF | PNG + JPEG of every module |
| Animated GIF | allowed in project content | not used (no GIFs in this kit) |
| Cover image | 4:3, 1400×1050 recommended · min 808×632 · **no GIF** | `cover.jpg` / `cover.png` @ **1400×1050** |
| Title | 80 characters max | 63 characters (below) |
| Colour mode | convert CMYK → **RGB before upload** | all exports RGB |

---

## 1. Cover

Upload **`exports/cover.jpg`** (1400×1050). Don't use a GIF for the cover — Behance
rejects them there. It's designed to read at 202×158 in the grid view: the logo is
the only element that matters at that size.

## 2. Title + tagline

```
Title:    POP! Craft Soda Co. — Bold & Playful Brand Identity
Tagline:  A craft soda identity built from circles, one stroke width, and a restless exclamation mark.
```

## 3. Project description

```
POP! is a fictional small-batch craft soda brand — and a full identity system
designed to feel like the first sip: loud, cold, refreshing, a little mischievous.

The whole mark is built from one unit: a single stroke width. Circles make the
bubble O, round caps make the letters, and the exclamation mark leans 10° so it
never sits still. Cream and ink carry 85% of every layout; bubblegum, tangerine
and fizzy yellow are punctuation, not wallpaper.

The kit covers logo construction and clearspace, a 6-colour palette with usage
ratios, Fredoka + DM Sans typography, voice and tone, plus packaging for three
launch flavours, business cards, social templates and a rotating "fizz seal".
```

## 4. Image order

Upload in this order (numbers match the filenames):

| # | File | Panel | Pixels | Why it's here |
|---|---|---|---|---|
| 1 | `01-brand.jpg` | The Brand | 2800×3120 | Positioning + personality sliders |
| 2 | `02-mark.jpg` | The Mark | 2800×3400 | All four lockups |
| 3 | `03-construction.jpg` | Construction | 2800×3360 | **Process** — geometry, x-unit, clearspace, scale |
| 4 | `04-color.jpg` | Colour | 2800×3280 | Swatches with RGB + the 60/25/8/4/3 ratio |
| 5 | `05-type.jpg` | Typography | 2800×3120 | Fredoka + DM Sans, full type scale |
| 6 | `06-cans.jpg` | Packaging | 2800×3120 | Three flavour cans |
| 7 | `07-print.jpg` | In the Wild | 2800×3120 | Cards, social post, fizz seal |
| 8 | `08-closing.jpg` | Closing | 2800×2300 | "Drink the fizz." + credits + tags |

Every module is also exported as a PNG (`01-brand.png` …) if you prefer lossless
for the lightbox. Total upload ≈ 5MB as JPEG.

> Behance shows the **first image as the project's opening statement** in some
> feeds — if you'd rather lead with the mark, swap images 1 and 2 after upload
> (drag to reorder).

## 5. Text modules to drop between images

**After image 1 (The Brand):**
```
The brief I set myself: craft soda sits on a beige shelf. Make the opposite of
beige, without looking cheap. Everything is drawn from one stroke width, so the
system scales from a 32px favicon to a 2m wall mural.
```

**After image 3 (Construction):**
```
Construction detail — stroke = x, cap height = 2.3x, counter = x. Clearspace is
the height of the exclamation dot on all sides. Minimum width: 120px digital,
30mm print.
```

**After image 6 (Packaging):**
```
Flavour recognition happens by colour before the wordmark is read, so each SKU
owns one palette entry. The stacked lockup sits high on the can to survive
shelf occlusion.
```

## 6. Tags (up to 10)

```
branding · brand identity · logo design · packaging · typography · illustration
· art direction · graphic design · soda · design system
```

## 7. Tools & credits

- **Tools:** set as HTML, CSS and SVG (hand-coded vectors — no raster, no effects)
- **Type:** Fredoka, DM Sans (both self-hosted in the kit)
- **Credits:** concept, art direction, design & build — *your name here*
- **Optional attachment:** upload `logo-pop-primary.svg` + `brand-tokens.css` as
  project attachments (Behance accepts SVG/CSS/text under 500MB) so people can
  grab the raw assets.

## 8. Pre-publish checklist

- [ ] Cover uploaded (JPG/PNG, 1400×1050, **not** a GIF)
- [ ] 8 modules in order, all 2800px wide → sharp when clicked to lightbox
- [ ] Each image under 10MB (they are — largest is 0.74MB)
- [ ] Title ≤80 chars, tagline + description pasted
- [ ] Tags added (≤10), creative fields set to Graphic Design / Branding
- [ ] Tools listed, credits filled in
- [ ] Viewed the project on **mobile** — Behance crops the first image in the feed

---

## Print conversions (referenced on the Colour panel)

| Swatch | Hex | CMYK (approx.) | Note |
|---|---|---|---|
| Cream Soda | `#FFF4E4` | 0 / 4 / 11 / 0 | |
| Midnight Ink | `#191022` | 26 / 53 / 0 / 87 | For solid areas use a rich black: 60 / 40 / 40 / 100 |
| Bubblegum | `#FF3F8E` | 0 / 75 / 44 / 0 | Out of CMYK gamut — use a spot (Pantone bridge) for brand-critical print |
| Electric Tangerine | `#FF6B2C` | 0 / 58 / 83 / 0 | Out of CMYK gamut — bridge to spot |
| Fizzy Yellow | `#FFC93C` | 0 / 21 / 76 / 0 | |
| Grape Fizz | `#6C2BD9` | 50 / 80 / 0 / 15 | Out of CMYK gamut — bridge to spot |

CMYK figures are naive RGB→CMYK conversions for layout reference only — always
proof RIPs/spot colours against a physical Pantone bridge before press.

---

## Regenerating the exports

```bash
cd pop-brand-kit
python3 export_behance.py      # re-renders behance/exports/ from presentation.html
```

Edit `behance/presentation.html` (each panel is wrapped in
`<!-- PANEL:slug:Name:HEIGHT -->` markers) then re-run. The script renders every
panel at 2x with headless Chrome, emits PNG **and** optimised JPEG, and prints
the pixel dimensions + file sizes so you can check the limits.
