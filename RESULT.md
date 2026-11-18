# Result: world news of Tuesday 17 November 2026 in one image

## What the image shows
A bright editorial front page, 1024 x 1024:
- **Top band:** "THE WORLD TODAY", with "TUESDAY 17 NOVEMBER 2026" as the largest text (82 px).
- **Map:** an equirectangular world map, cropped to 72°N to 38°S. Light land on a pale grey-blue sea, from
  Natural Earth 110m and projected in the page's own script. Eight numbered red markers with place names,
  plus two small dots marking Mexico and Bolivia for the measles story.
- **Cards:** eight numbered story cards in a 2 x 4 grid. Each has a flat SVG icon drawn by hand, a region
  tag, a 30 px bold two-line headline and one detail line carrying the key number or name.
- **Footer:** two 15 px lines. "Events of 17 Nov 2026 (any time zone), as reported by Reuters, AP, AFP,
  NPR, CNBC, Euronews, Anadolu, Xinhua and PAHO" and, addressed to the reader, "All 8 events are dated
  17 Nov 2026 and each was checked against at least two news reports."
- **Style:** one accent colour (red #c62b1e) with warm neutrals, no gradients, no text under 15 px.
  The layout check in render.mjs found no overflowing or clipped text.

## The stories and their sources
Full date evidence, all links and the dropped list are in sources.md.

| # | Story | Region / field | Sources |
|---|-------|----------------|---------|
| 1 | Ukraine strike drops a Crimean Bridge road span into the Kerch Strait; Kremlin says it will rebuild | Europe, war | NPR/AP 2026-11-17; Military.com; Kyiv Post; Reuters-verified video |
| 2 | Iran says it hit a US radar at Sheikh Isa, Bahrain; US says all drones intercepted, no damage; third attack in five days | Middle East, war | Euronews 2026-11-17; Irish Times; Anadolu; Reuters |
| 3 | US, Mexico and Bolivia lose measles-elimination status; 58,213 cases and 82 deaths in the Americas in 2026 | Americas, health | PAHO release 17-11-2026; NBC News; Health Policy Watch; AFP |
| 4 | Wall Street slides, Dow down 848.75 points (to 50,759.42); Nvidia reports $115.8bn quarterly revenue after the bell | Americas, markets/tech | AP via WTOP; CNBC; Nvidia 8-K (SEC) |
| 5 | UN: over 2,230 civilians killed in Sudan in Jan-Oct 2026, more than 1,630 by drones | Africa, war | Middle East Monitor 20261117; Dabanga; Reuters via OkayAfrica |
| 6 | Trump lands in Manila for the ASEAN summit; next stop APEC in Shenzhen, where talks with Xi and Putin are planned | Asia-Pacific, diplomacy | Philstar 2026/11/17; Rappler; Tribune.net.ph; Democracy Now |
| 7 | Mongolia's President Khurelsukh says he will resign, denies railway graft claims; parliament must approve | Asia, politics | AP via US News 2026-11-17; Khaleej Times; Manila Times; Arab News |
| 8 | Russian military An-12 crash near Kemerovo, Siberia, kills all 19; ministry cites a technical malfunction | Russia, disaster | Anadolu; Xinhua 20261118; Kyiv Post; Geo TV |

**Left out for lack of a 17 Nov date or a second source:**
- Prague train collision (no 2026 report found)
- Pope leaving Peru (departed 16 Nov)
- COP31 draft text (16 Nov)
- Data-centre emissions study (16 Nov)
- Bangladesh wage protests (multi-day story)
- A "two killed" toll at the Crimean Bridge (contradicted by Russia's Transport Ministry)
- Others listed in sources.md

I found no climate story both clearly dated to 17 Nov and confirmed by two sources, so the image has none
rather than a misdated one.

## Process
1. Researched through the Wikipedia current-events portals for 16, 17 and 18 Nov, dated digests (Democracy
   Now, Just Security Early Edition, OkayAfrica) and wire syndications. Checked each story's date against
   neighbouring days.
2. Built poster.html, plus render.mjs (Playwright Chromium, 1024 x 1024, device scale 1, with an automatic
   layout and font-size check), main.py and check.py. main.py checks the PNG/JPEG signature and the
   1048576-byte limit, then writes the exact bytes to /output/entry.png (OUTPUT_DIR overrides the folder for
   local tests). It exits 1 without writing anything for a non-image or an oversized file (tested in ./tmp).
3. First version, then two improvement passes, each viewed at full size and at 300 px:
   - Pass 1: fixed the date clipped at the right edge, rebalanced the headline breaks and enlarged them from
     27 to 30 px, increased map contrast, enlarged the markers, redrew the radar icon, removed the
     antimeridian lines across the map (Chukotka and Fiji rings), made the card wording unambiguous ("talks
     with Xi and Putin planned") and matched the card badges to the red map markers.
   - Pass 2: checked every fact against sources.md and changed "2,230" to "over 2,230" to match the UN's
     wording. Added the Mexico and Bolivia dots for story 3 and the key "Numbered markers match the
     stories below".
   - Follow-up: added the second footer line (the card grid moved up 6 px and lost 10 px of height to make
     room, with every text still at least 15 px and nothing clipped, viewed at full size and 300 px).
     Renumbered stories 6 and 7 in sources.md to match the image (README already matched), and aligned
     the Sudan heading there with the image ("over 2,230").

## Check results (`python3 check.py`)
```
[PASS] two runs write identical bytes
[PASS] output equals repo entry.png
[PASS] size <= 1048576 bytes: 262308 bytes
[PASS] PNG signature
[PASS] PNG chunks, CRCs, IHDR/IDAT/IEND, data length: all ok
[PASS] exactly 1024 x 1024: 1024 x 1024
ALL CHECKS PASSED
```

## File
- entry.png: PNG, 1024 x 1024, **262308 bytes**
- sha256: **367df03a83f72f2ec657ab0236d832c4444c180b8904273413f200b90ea7fef9**

## Commits
- Pass 2: aa3ed7fe03ea51dab839fed445c5f5a6249996af
- README: 64fd85e800f0ed11f36edbe066de80e205aef52b
- main.py validates before copying, OUTPUT_DIR: 7325ecb3d641f59cdc3b2f09bfecbdcd86168621
- Footer second line, final image: bc83b6284aaf015d3c1559882038fb58bdda83d7
- sources.md numbering fix: 5fb6886da2c891b1fb3e6ad89e8a979e2ae7761b
- This RESULT.md is committed on top of these as the final commit; a commit cannot contain its own sha,
  so see `git log -1`. Not pushed.
