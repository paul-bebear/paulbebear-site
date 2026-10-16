"""Build the embedded star data for /light-birthday/.

Inputs (paths set by the STELLARIUM and HYG environment variables, see README.md):
  - Stellarium hip_gaia3 star catalogue (stars_0/1/2, type 0 = Star1): position, V, B-V,
    parallax and parallax error per star, picked per star from Gaia DR3 or Hipparcos.
  - HYG v4.1 (Hipparcos-based, CC BY-SA 4.0): names, Bayer/Flamsteed, constellation, spectral type.
  - AT-HYG v3.2 HYGLike subset: Gaia DR3 distances, used to label which source a parallax came from.
  - Stellarium 'modern' sky culture (CC BY-SA 4.0): constellation stick figures.
Output: data.json (compact). Run inject.py to put it into ../index.html.
"""
import json, os, re, struct, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from facts import FACTS

# Where the source data was cloned (see README.md in this folder).
STELLARIUM = os.environ.get('STELLARIUM', os.path.expanduser('~/src/stellarium'))
HYG = os.environ.get('HYG', os.path.expanduser('~/src/hyg-database'))
OUT = os.path.join(HERE, 'data.json')


def load_stellarium():
    """Stellarium hip_gaia3 catalogue, levels 0-2 (all type 0 = 'Star1', 48 bytes per star)."""
    dt = np.dtype([('gaia', '<i8'), ('x0', '<i4'), ('x1', '<i4'), ('x2', '<i4'), ('dx0', '<i4'), ('dx1', '<i4'), ('dx2', '<i4'),
                   ('bv', '<i2'), ('vmag', '<i2'), ('plx', '<u2'), ('plxe', '<u2'), ('rv', '<i2'), ('sp', '<u2'), ('ot', 'u1'), ('hip', 'u1', (3,))])
    base = os.path.join(STELLARIUM, 'stars', 'hip_gaia3')
    out = []
    for fn in sorted(f for f in os.listdir(base) if re.match(r'stars_[012]_0v0_\d+\.cat$', f)):
        b = open(os.path.join(base, fn), 'rb').read()
        magic, typ, major, minor, level, mag_min = struct.unpack('<6I', b[:24])
        assert typ == 0, fn
        nz = 20 * 4 ** level + 1                      # geodesic zones plus one global zone
        sizes = np.frombuffer(b[28:28 + 4 * nz], '<u4')
        off = 28 + 4 * nz
        out.append(np.frombuffer(b[off:off + dt.itemsize * int(sizes.sum())], dt))
    return np.concatenate(out)

LY_PER_PC = 3.261564
MAX_LY = 120.0
MIN_PLX = 1000 * LY_PER_PC / MAX_LY  # 27.18 mas

# ---------- Stellarium catalogue ----------
a = load_stellarium()
h = a['hip'][:, 0].astype(int) | (a['hip'][:, 1].astype(int) << 8) | (a['hip'][:, 2].astype(int) << 16)
x = np.stack([a['x0'], a['x1'], a['x2']], 1) / 2e9
S = pd.DataFrame({
    'hip': h >> 5, 'comp': h & 31, 'gaia': a['gaia'], 'V': a['vmag'] / 1000, 'bv': a['bv'] / 1000,
    'plx': a['plx'] * 0.02, 'e': a['plxe'] / 100,
    'ra': np.degrees(np.arctan2(x[:, 1], x[:, 0])) % 360, 'dec': np.degrees(np.arcsin(np.clip(x[:, 2], -1, 1))),
})

# alpha Centauri A/B: Stellarium carries the 1997 Hipparcos value. Use the modern measurement
# (Kervella et al. 2016, A&A 594, A107: 747.17 +/- 0.61 mas).
for hp in (71683, 71681):
    S.loc[S.hip == hp, ['plx', 'e']] = [747.17, 0.61]
ALPHA_CEN = {71683, 71681}
COMP_SP = {(32349, 2): 'DA2', (37279, 2): 'DQZ'}
OVERRIDE = {98505: 'HD 189733', 104214: '61 Cygni A', 104217: '61 Cygni B', 71683: 'Alpha Centauri A', 71681: 'Alpha Centauri B',
            16537: 'Epsilon Eridani', 53721: '47 Ursae Majoris', 113357: '51 Pegasi', 43587: '55 Cancri'}
OVERRIDE_ALT = {71683: 'Rigil Kentaurus · α¹ Cen', 71681: 'Toliman · α² Cen', 16537: 'Ran · ε Eri', 53721: 'Chalawan · 47 UMa',
                113357: 'Helvetios · 51 Peg', 43587: 'Copernicus · 55 Cnc', 98505: 'HIP 98505'}

H4 = pd.read_csv(os.path.join(HYG, 'hyg', 'CURRENT', 'hygdata_v41.csv'), low_memory=False)
HL = pd.read_csv(os.path.join(HYG, 'hyg', 'athyg_v3', 'hyglike_from_athyg_v32.csv.gz'), low_memory=False)
h4 = H4.dropna(subset=['hip']).drop_duplicates('hip').set_index('hip')
hl = HL.dropna(subset=['hip']).drop_duplicates('hip').set_index('hip')

GREEK = dict(Alp=('α', 'Alpha'), Bet=('β', 'Beta'), Gam=('γ', 'Gamma'), Del=('δ', 'Delta'), Eps=('ε', 'Epsilon'),
             Zet=('ζ', 'Zeta'), Eta=('η', 'Eta'), The=('θ', 'Theta'), Iot=('ι', 'Iota'), Kap=('κ', 'Kappa'),
             Lam=('λ', 'Lambda'), Mu=('μ', 'Mu'), Nu=('ν', 'Nu'), Xi=('ξ', 'Xi'), Omi=('ο', 'Omicron'),
             Pi=('π', 'Pi'), Rho=('ρ', 'Rho'), Sig=('σ', 'Sigma'), Tau=('τ', 'Tau'), Ups=('υ', 'Upsilon'),
             Phi=('φ', 'Phi'), Chi=('χ', 'Chi'), Psi=('ψ', 'Psi'), Ome=('ω', 'Omega'))
SUP = {'1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
GEN = dict(And='Andromedae', Ant='Antliae', Aps='Apodis', Aqr='Aquarii', Aql='Aquilae', Ara='Arae', Ari='Arietis',
           Aur='Aurigae', Boo='Boötis', Cae='Caeli', Cam='Camelopardalis', Cnc='Cancri', CVn='Canum Venaticorum',
           CMa='Canis Majoris', CMi='Canis Minoris', Cap='Capricorni', Car='Carinae', Cas='Cassiopeiae',
           Cen='Centauri', Cep='Cephei', Cet='Ceti', Cha='Chamaeleontis', Cir='Circini', Col='Columbae',
           Com='Comae Berenices', CrA='Coronae Australis', CrB='Coronae Borealis', Crv='Corvi', Crt='Crateris',
           Cru='Crucis', Cyg='Cygni', Del='Delphini', Dor='Doradus', Dra='Draconis', Equ='Equulei', Eri='Eridani',
           For='Fornacis', Gem='Geminorum', Gru='Gruis', Her='Herculis', Hor='Horologii', Hya='Hydrae', Hyi='Hydri',
           Ind='Indi', Lac='Lacertae', Leo='Leonis', LMi='Leonis Minoris', Lep='Leporis', Lib='Librae', Lup='Lupi',
           Lyn='Lyncis', Lyr='Lyrae', Men='Mensae', Mic='Microscopii', Mon='Monocerotis', Mus='Muscae',
           Nor='Normae', Oct='Octantis', Oph='Ophiuchi', Ori='Orionis', Pav='Pavonis', Peg='Pegasi', Per='Persei',
           Phe='Phoenicis', Pic='Pictoris', Psc='Piscium', PsA='Piscis Austrini', Pup='Puppis', Pyx='Pyxidis',
           Ret='Reticuli', Sge='Sagittae', Sgr='Sagittarii', Sco='Scorpii', Scl='Sculptoris', Sct='Scuti',
           Ser='Serpentis', Sex='Sextantis', Tau='Tauri', Tel='Telescopii', Tri='Trianguli', TrA='Trianguli Australis',
           Tuc='Tucanae', UMa='Ursae Majoris', UMi='Ursae Minoris', Vel='Velorum', Vir='Virginis', Vol='Volantis',
           Vul='Vulpeculae')


def isnan(v):
    return v is None or (isinstance(v, float) and np.isnan(v)) or (isinstance(v, str) and not v.strip())


def names(hip, comp):
    """Return (display name, short designation, spectral type, constellation)."""
    if hip not in h4.index:
        return None, None, None, None
    r = h4.loc[hip]
    con = None if isnan(r.con) else r.con
    bay = None
    if not isnan(r.bayer) and con:
        g, *n = r.bayer.split('-')
        if g in GREEK:
            sym, full = GREEK[g]
            sup = SUP.get(n[0], '') if n else ''
            bay = (f'{sym}{sup} {con}', f'{full}{sup} {GEN.get(con, con)}')
    fl = None
    if not isnan(r.flam) and con:
        fl = (f'{int(r.flam)} {con}', f'{int(r.flam)} {GEN.get(con, con)}')
    prop = None if isnan(r.proper) else r.proper
    gl = None if isnan(r.gl) else r.gl.replace('Gl ', 'Gliese ').replace('GJ ', 'GJ ')
    hd = None if isnan(r.hd) else f'HD {int(r.hd)}'
    if prop:
        name = prop
    elif bay:
        name = bay[1]
    elif fl:
        name = fl[1]
    elif gl:
        name = gl
    elif hd:
        name = hd
    else:
        name = f'HIP {int(hip)}'
    alt = [d for d in [bay and bay[0], fl and fl[0], gl if gl and gl != name else None, hd if hd != name else None,
                       f'HIP {int(hip)}' if name != f'HIP {int(hip)}' else None] if d]
    sp = None
    for src in (r.spect, hl.loc[hip].spect if hip in hl.index else None):
        if not isnan(src):
            sp = str(src).strip()
            break
    return name, ' · '.join(alt[:2]), sp, con


def source(row):
    """0 = Gaia DR3, 1 = Hipparcos, 2 = Gaia DR3 or Hipparcos as compiled by Stellarium (could not tell)."""
    if row.hip in ALPHA_CEN:
        return 3  # Kervella et al. 2016
    if row.gaia == 0:
        return 1
    tol = max(0.05, 2 * row.e)
    if row.hip in hl.index and hl.loc[row.hip].dist_src == 'G_R3' and abs(row.plx - 1000 / hl.loc[row.hip].dist) <= tol:
        return 0
    if row.hip in h4.index and abs(row.plx - 1000 / h4.loc[row.hip].dist) <= tol:
        return 1
    if row.hip == 0:
        return 0  # Gaia-only star in Stellarium's list: Gaia DR3 astrometry
    return 2


# ---------- Gaia-only stars: name them from HYG (Gliese) by position where possible ----------
gl4 = H4[H4.gl.notna() & (H4.dist < 40)][['ra', 'dec', 'mag', 'gl', 'spect', 'con']].copy()
gl4['ra'] = gl4.ra * 15


def gaia_only_name(r):
    d = np.hypot((gl4.ra - r.ra) * np.cos(np.radians(r.dec)), gl4.dec - r.dec) * 3600
    j = d.idxmin()
    if d[j] < 90 and abs(gl4.loc[j].mag - r.V) < 1.5:
        g = gl4.loc[j]
        return g.gl.replace('Gl ', 'Gliese '), None if isnan(g.spect) else g.spect, g.con
    return f'Gaia DR3 {r.gaia}', None, None


# ---------- zodiac figures ----------
sc = json.load(open(os.path.join(STELLARIUM, 'skycultures', 'modern', 'index.json')))
ZOD = ['Ari', 'Tau', 'Gem', 'Cnc', 'Leo', 'Vir', 'Lib', 'Sco', 'Sgr', 'Cap', 'Aqr', 'Psc', 'Oph']
lines = {}
for c in sc['constellations']:
    ab = c['id'].split()[-1]
    if ab in ZOD:
        lines[ab] = [[int(v) for v in pl] for pl in c['lines']]
line_hips = {v for ab in lines for pl in lines[ab] for v in pl}

# ---------- select stars ----------
S['near'] = S.plx >= MIN_PLX
# One row per HIP for line stars / bright far stars: prefer the brightest component.
S_sorted = S.sort_values('V')
first_comp = ~S_sorted.duplicated('hip') | (S_sorted.hip == 0)
far_line = S_sorted[first_comp & S_sorted.hip.isin(line_hips) & ~S_sorted.near]
far_bright = S_sorted[first_comp & (S_sorted.V <= 4.5) & ~S_sorted.near & (S_sorted.hip > 0) & ~S_sorted.hip.isin(line_hips)]
near = S[S.near]
print('near', len(near), 'far line', len(far_line), 'far bright', len(far_bright), file=sys.stderr)

# Components of the same HIP within 120 ly: add A/B suffix to the name.
comp_counts = near[near.hip > 0].groupby('hip').size()

rows = []
hip_to_idx = {}
for kind, df in (('near', near), ('line', far_line), ('far', far_bright)):
    for r in df.itertuples():
        if r.hip > 0:
            name, alt, sp, con = names(r.hip, r.comp)
            if name is None:
                name, alt, sp, con = f'HIP {r.hip}', '', None, None
            if comp_counts.get(r.hip, 1) > 1 and r.comp > 1:
                name = f'{name} {chr(64 + r.comp)}'
            name = OVERRIDE.get(int(r.hip), name).replace(' G. ', ' ')
            if name == f'HIP {r.hip}':
                name = ''
            alt = OVERRIDE_ALT.get(int(r.hip), (alt or '').replace(' G. ', ' '))
            if r.comp > 1:
                sp = COMP_SP.get((int(r.hip), int(r.comp)), '')
            if not name or name.startswith(('HD ', 'Gliese', 'GJ')) and not FACTS.get(int(r.hip)):
                alt = ''
        else:
            name, sp, con = gaia_only_name(r)
            alt = ''
        flag = 0
        if kind != 'near':
            flag |= 1
        if r.hip in line_hips:
            flag |= 2
        src = source(r)
        fact = FACTS.get(int(r.hip), '') if (r.hip > 0 and (r.comp <= 1 or comp_counts.get(r.hip, 1) == 1 or r.hip in ALPHA_CEN)) else ''
        idx = len(rows)
        if r.hip > 0 and (r.hip not in hip_to_idx or r.V < rows[hip_to_idx[int(r.hip)]][2]):
            hip_to_idx[int(r.hip)] = idx
        sp = (sp or '').split(' ')[0].split('+')[0].split('/')[0][:7]
        rows.append([round(r.ra, 2), round(r.dec, 2), round(r.V, 1), round(r.bv, 2), round(r.plx, 2), round(max(r.e, 0.02), 2),
                     src, name, alt or '', sp, con or '', int(r.hip), flag, fact])

# Facts: make sure every fact landed somewhere
used = {r[11] for r in rows if r[13]}
missing = set(FACTS) - used
print('facts not placed:', sorted(missing), file=sys.stderr)

zl = {ab: [[hip_to_idx[v] for v in pl if v in hip_to_idx] for pl in lines[ab]] for ab in ZOD}
for ab in ZOD:
    miss = [v for pl in lines[ab] for v in pl if v not in hip_to_idx]
    if miss:
        print('line stars missing', ab, miss, file=sys.stderr)

out = {'stars': rows, 'zod': zl}
json.dump(out, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
print('rows', len(rows), file=sys.stderr)
