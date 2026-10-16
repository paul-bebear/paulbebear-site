# Light-birthday: data build

`../index.html` is the page and the source of truth for all code. It embeds the star data on one line (`const DATA = ...;`). These scripts rebuild that line.

## Sources

| What | Where | Licence |
|---|---|---|
| Positions, V magnitude, B-V, parallax and parallax error | Stellarium `stars/hip_gaia3/stars_{0,1,2}_0v0_*.cat` (Hipparcos stars with Gaia DR3 astrometry where Stellarium judged it reliable) | Gaia: CC BY-SA 3.0 IGO; Stellarium data: GPL/CC BY-SA |
| Names, Bayer/Flamsteed, constellation, spectral type | HYG v4.1 `hyg/CURRENT/hygdata_v41.csv` | CC BY-SA 4.0 |
| Which parallax is Gaia DR3 (for source labels) | AT-HYG v3.2 HYGLike subset `hyg/athyg_v3/hyglike_from_athyg_v32.csv.gz` | CC BY-SA 4.0 |
| Zodiac stick figures | Stellarium `skycultures/modern/index.json` | CC BY-SA 4.0 |
| Alpha Centauri A/B parallax | Kervella et al. 2016, A&A 594, A107 (747.17 ± 0.61 mas), hard-coded | |
| One-line facts | `facts.py`, written by hand | |

The embedded data is a derived work of CC BY-SA sources, so it is CC BY-SA 4.0 too.

## Rebuild

```sh
# Stellarium: only the files we need (about 9 MB)
git clone --depth 1 --filter=blob:none --no-checkout https://github.com/Stellarium/stellarium ~/src/stellarium
cd ~/src/stellarium && git sparse-checkout set --no-cone 'stars/hip_gaia3/stars_[012]_0v0_*.cat' skycultures/modern/index.json && git checkout
# HYG (the GitHub mirror; the live repo is codeberg.org/astronexus/hyg)
git clone --depth 1 https://github.com/astronexus/hyg-database ~/src/hyg-database

cd paulbebear-site/light-birthday/build
STELLARIUM=~/src/stellarium HYG=~/src/hyg-database python3 build_data.py   # writes data.json
python3 inject.py                                                          # puts it into ../index.html
```

Needs Python 3 with numpy and pandas. If Stellarium renames its catalogue files (the `v0_NN` suffix changes between releases), the glob in `load_stellarium()` still picks them up; check the printed counts (3,795 stars within 120 ly as of October 2026).

## What gets selected

- Every star with parallax ≥ 27.18 mas (120 light-years).
- Every star in the 13 zodiac stick figures, however far.
- Every star brighter than V 4.5 beyond 120 ly (the map's "Farther stars" layer).

Source label per star: Gaia DR3 if the parallax matches AT-HYG's Gaia DR3 value within max(0.05 mas, 2σ); Hipparcos if it matches HYG's 2007 Hipparcos value or the star has no Gaia ID; otherwise "Gaia or Hipparcos".
