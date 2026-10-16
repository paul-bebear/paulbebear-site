# Light-birthday: data build

`../index.html` is the page and the source of truth for all code. It embeds the star data on one line (`const DATA = ...;`). These scripts rebuild that line.

## Sources and credits

Every source behind the page, with its licence and what it is used for. The page's "Sources and credits" section lists the same.

| Source | Used for | Licence |
|---|---|---|
| [Stellarium](https://github.com/Stellarium/stellarium) `stars/hip_gaia3/stars_{0,1,2}_0v0_*.cat` (Hipparcos stars with Gaia DR3 astrometry where Stellarium judged it reliable) | Positions, V magnitude, B-V, parallax and parallax error | Stellarium: GPL-2.0-or-later; carries the Gaia and Hipparcos credits below |
| [Stellarium "modern" sky culture](https://github.com/Stellarium/stellarium/tree/master/skycultures/modern) `skycultures/modern/index.json` | Constellation lines (the 13 zodiac stick figures) | CC BY-SA 4.0 (text and data) |
| [Gaia DR3](https://doi.org/10.1051/0004-6361/202243940), Gaia Collaboration, Vallenari et al. 2023, A&A 674, A1 | Most parallaxes, via Stellarium | [Free to use with credit to ESA/Gaia/DPAC](https://www.cosmos.esa.int/web/gaia-users/license) |
| [Hipparcos](https://doi.org/10.1051/0004-6361:20078357), van Leeuwen 2007, A&A 474, 653; ESA 1997, SP-1200 | Parallaxes of bright stars, via Stellarium | ESA public data, free to use with credit |
| [HYG v4.1](https://codeberg.org/astronexus/hyg) `hyg/CURRENT/hygdata_v41.csv` (D. Nash, astronexus) | Names, Bayer/Flamsteed, constellation, spectral type | CC BY-SA 4.0 |
| [AT-HYG v3.2](https://codeberg.org/astronexus/athyg) HYGLike subset `hyg/athyg_v3/hyglike_from_athyg_v32.csv.gz` | Which parallax is Gaia DR3 (source labels) | CC BY-SA 4.0 |
| [Kervella et al. 2016](https://doi.org/10.1051/0004-6361/201629201), A&A 594, A107 | Alpha Centauri A/B parallax (747.17 ± 0.61 mas), hard-coded | Published measurement, cited |
| [Ballesteros 2012](https://doi.org/10.1209/0295-5075/97/34008), EPL 97, 34008 | Temperature from B-V (in the page code) | Published formula, cited |
| [Mitchell Charity, blackbody colours](http://www.vendian.org/mncharity/dir3/blackbody/) | Star colour from temperature (in the page code) | Published table, used with credit |
| [IAU Working Group on Star Names](https://www.iau.org/public/themes/naming_stars/) | Proper names (via HYG); IAU constellation boundaries for the Sun's zodiac dates | Names standardised by the IAU, credited |
| `facts.py`, written by hand from NASA, ESA and ESO press material | One-line facts | Original text, CC BY-SA 4.0 |
| [Geist and Geist Mono](https://vercel.com/font), via Google Fonts | Typefaces | SIL Open Font License 1.1 |

The embedded star data (`const DATA = ...;`) is a derived work of CC BY-SA sources, so it is released under CC BY-SA 4.0.

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
