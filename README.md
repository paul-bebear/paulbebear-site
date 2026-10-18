# paulbebear.com

Static site. No build step. Vercel serves the folder as-is.

```
index.html              home: hero, Work, Now, About
half-line/index.html    The Half Line
premium-ladder/index.html  The Premium Ladder (companion to The Half Line)
bottom-wage/index.html  The Bottom Wage (minimum wage vs real bottom wage, 8 US cities)
spacex-ipo/index.html   SpaceX IPO teardown
capex-opex-da/index.html  Capex, Opex and D&A
not-so-cosmic-cycles/index.html  Not-so-cosmic cycles (when beliefs and habits lock in; 9 tabs, plain-language glossary)
archive/index.html      full list of linked work (nav: Archive)
labour-economics/index.html  Labour economics study guide
light-birthday/index.html  Your light-birthday stars (stars whose light left them when you were born; data build in light-birthday/build/)
run-the-grid/index.html  Run the grid (balance a real Spanish grid day, replay the 28 April 2025 Iberian blackout; research brief in RESEARCH.md, REE data build in build/)
france-2027/index.html  Three plans for France (government vs RN vs LFI, sector by sector; status as of 17 Oct 2026)
face-layers/index.html  Your face in 10 layers (SVD of a photo, in the browser; the SVD runs in face-layers/svd-worker.js, sample paintings in face-layers/samples/)
assets/                 thumbnails (1200x750 webp)
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
| Three plans for France | `france-2027/index.html` itself. Sector content lives in the SECTORS array in the script; tax scales in CUR and LFI; RTE costs in RTE. Re-check after LFI's 2027 programme (6 Nov 2026) and the final RN platform | /france-2027/ |
| Your face in 10 layers | `face-layers/index.html` itself, plus `svd-worker.js` (a port of JAMA's public-domain SVD). No data build: everything is computed from the image in the browser | /face-layers/ |

When a piece changes: replace its `index.html` here, refresh the thumbnail if the top of the page changed, commit, push. Vercel redeploys in about a minute. URLs never change.

Local fix carried in the site copy: `capex-opex-da` has `align-content:start` on `.branch` (the "No" tag stretched into a tall pill). Re-apply it if the page is replaced, or fix it in the artifact.

## Adding a piece
Home page Work section: 4-6 pieces max. Every published piece also gets an entry in archive/index.html.

Every page also carries a `<!-- seo, previews, analytics -->` block just before `</head>`. When you add or replace a piece:

1. Copy that block from another piece into the new page and change the description, canonical, og:title, og:description, og:url and og:image.
2. Make the preview image: a JPG copy of the thumbnail in `assets/og/<slug>.jpg`. LinkedIn and some chat apps ignore webp.
3. Add the URL to `sitemap.xml`.
4. Add an `<item>` to the top of `feed.xml`.

If you replace a page's `index.html` with a fresh export, its block is gone, so re-add it.

Analytics is Vercel Web Analytics (`/_vercel/insights/script.js`). It must be switched on in the Vercel dashboard (Project, Analytics, Enable). Until then the script 404s harmlessly.

premium-ladder and labour-economics have no thumbnail yet. Their previews use half-line.jpg as a stand-in.
