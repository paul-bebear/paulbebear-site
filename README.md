# paulbebear.com

Static site. No build step. Vercel serves the folder as-is.

```
index.html              home: about-me hero, bio, Work (five folders that pan sideways as you scroll), CV links
half-line/index.html    The Half Line
premium-ladder/index.html  The Premium Ladder (companion to The Half Line)
bottom-wage/index.html  The Bottom Wage (minimum wage vs real bottom wage, 8 US cities)
spacex-ipo/index.html   SpaceX IPO teardown
capex-opex-da/index.html  Capex, Opex and D&A
not-so-cosmic-cycles/index.html  Not-so-cosmic cycles (when beliefs and habits lock in; 9 tabs, plain-language glossary)
light-birthday/index.html  Your light-birthday stars (stars whose light left them when you were born; data build in light-birthday/build/)
run-the-grid/index.html  Run the grid (balance a real Spanish grid day, replay the 28 April 2025 Iberian blackout; research brief in RESEARCH.md, REE data build in build/)
france-2027/index.html  The 2027 fork (LFI vs RN against the Macron baseline; programme texts, costings and the 14-bracket tax calculator are embedded in the page)
face-layers/index.html  Your face in 10 layers (SVD of a photo, in the browser; the SVD runs in face-layers/svd-worker.js, sample paintings in face-layers/samples/)
assets/                 thumbnails (1200x750 webp); cv.webp and indexable.webp are screenshots of the live sites
vercel.json             redirects: /cv to cv.paulbebear.com, /archive to /#work
```

Atlas Through Time, Indexable and beBEARlifts link out to their own live sites. beBEARlifts lives at lifts.paulbebear.com, served by its own Vercel project (bebearlifts) from github.com/paul-bebear/beBEARlifts.

## How pieces stay current

Each piece has one source of truth. The site copy is the published version.

| Piece | Source of truth | URL on the site |
|---|---|---|
| The Half Line | `~/Downloads/The Half Line.html` (move to its own folder) | /half-line/ |
| SpaceX teardown | `~/Downloads/spacex-ipo-teardown.html` | /spacex-ipo/ |
| Capex, Opex and D&A | Claude artifact RU9kPwZPtANiyG2pynjb5G | /capex-opex-da/ |
| The Premium Ladder | built from scripts in a Claude session (data, tax model, page template); the page embeds all data | /premium-ladder/ |
| The Bottom Wage | built from scripts in a Claude session (model.py, template.html); the page embeds all data | /bottom-wage/ |
| Atlas Through Time | github.com/paul-bebear/atlas-through-time | external, already live |
| Not-so-cosmic cycles | built from scripts in a Claude session (template, Gallup/NBER/Damodaran data, logo geometry); the page embeds all data. Glossary terms live in the GLOSS object in the script | /not-so-cosmic-cycles/ |
| Your light-birthday stars | `light-birthday/index.html` itself. Star data is one embedded line, rebuilt by `light-birthday/build/` (see its README) | /light-birthday/ |
| Run the grid | `run-the-grid/index.html` itself. REE data is one embedded line, rebuilt by `run-the-grid/build/build.py`; facts trace to `run-the-grid/RESEARCH.md` | /run-the-grid/ |
| The 2027 fork | `france-2027/index.html` itself. Dated "Updated 19 October 2026"; refresh after LFI's 2027 programme (6 Nov 2026), the RN pension plan and the Cassation ruling on Le Pen | /france-2027/ |
| Your face in 10 layers | `face-layers/index.html` itself, plus `svd-worker.js` (a port of JAMA's public-domain SVD). No data build: everything is computed from the image in the browser | /face-layers/ |

When a piece changes: replace its `index.html` here, refresh the thumbnail if the top of the page changed, commit, push. Vercel redeploys in about a minute. URLs never change.

Local fix carried in the site copy: `capex-opex-da` has `align-content:start` on `.branch` (the "No" tag stretched into a tall pill). Re-apply it if the page is replaced, or fix it in the artifact.

## Adding a piece
Everything lives on the home page now, in one of five folders inside the Work section: Explore (discovery tools), Learn (explainers), Just for fun, Apps, For work. There is no archive page any more (/archive redirects to /#work).

To add a piece, copy a `file row` block into the right folder's `.rows` list and bump the number in that folder's tab. A folder with 4 or more items uses the `files feature` layout (one big card plus rows); a folder with 2 uses `files cols-2`. Pieces with no screenshot get a `thumb tile` with a Phosphor icon.

The sideways pan only runs on screens at least 900px wide and 620px tall, with motion allowed. Everywhere else the folders stack and slide in from the right. Check both after a change.

Every page also carries a `<!-- seo, previews, analytics -->` block just before `</head>`. When you add or replace a piece:

1. Copy that block from another piece into the new page and change the description, canonical, og:title, og:description, og:url and og:image.
2. Make the preview image: a JPG copy of the thumbnail in `assets/og/<slug>.jpg`. LinkedIn and some chat apps ignore webp.
3. Add the URL to `sitemap.xml`.
4. Add an `<item>` to the top of `feed.xml`.

If you replace a page's `index.html` with a fresh export, its block is gone, so re-add it.

Analytics is Vercel Web Analytics (`/_vercel/insights/script.js`). It must be switched on in the Vercel dashboard (Project, Analytics, Enable). Until then the script 404s harmlessly.
