# paulbebear.com

Static site. No build step. Vercel serves the folder as-is.

```
index.html              home: hero, Work, Now, About
half-line/index.html    The Half Line
spacex-ipo/index.html   SpaceX IPO teardown
capex-opex-da/index.html  Capex, Opex and D&A
archive/index.html      full list of linked work (nav: Archive)
labour-economics/index.html  Labour economics study guide
assets/                 thumbnails (1200x750 webp)
```

Atlas Through Time and Indexable link out to their own live sites.

## How pieces stay current

Each piece has one source of truth. The site copy is the published version.

| Piece | Source of truth | URL on the site |
|---|---|---|
| The Half Line | `~/Downloads/The Half Line.html` (move to its own folder) | /half-line/ |
| SpaceX teardown | `~/Downloads/spacex-ipo-teardown.html` | /spacex-ipo/ |
| Capex, Opex and D&A | Claude artifact RU9kPwZPtANiyG2pynjb5G | /capex-opex-da/ |
| Atlas Through Time | github.com/paul-bebear/atlas-through-time | external, already live |

When a piece changes: replace its `index.html` here, refresh the thumbnail if the top of the page changed, commit, push. Vercel redeploys in about a minute. URLs never change.

Local fix carried in the site copy: `capex-opex-da` has `align-content:start` on `.branch` (the "No" tag stretched into a tall pill). Re-apply it if the page is replaced, or fix it in the artifact.

## Adding a piece
Home page Work section: 4-6 pieces max. Every published piece also gets an entry in archive/index.html.
