"""Rebuild the REE data embedded in run-the-grid/index.html.

    python3 build.py            # fetch from REE, write data.json, inject into ../index.html
    python3 build.py --offline  # reuse the raw files in ./raw

Source: Red Eléctrica, "Seguimiento de la demanda" (demanda.ree.es), peninsular Spain, 5-minute values.
Terms: REE legal notice (ree.es/es/aviso-legal): name REE as the source, don't alter the data, state the date.

Field notes (checked against the government 28-A report at 12:30 on 28 April 2025):
  dem   demand, pumping excluded (25,184 MW at 12:30, same as the report)
  hid   hydro NET of pumped storage, so conventional hydro = hid - turb - conb
  turb  pumped-storage turbining (+), conb pumping consumption (-)
  inter net exchanges (+ import), icb Balearic link
  other = coal + cogeneration + biomass + the remainder REE does not break out (about 300 MW)
"""
import json, os, re, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw')
DAYS = ['2025-04-22', '2025-04-28', '2025-04-29']
URL = 'https://demanda.ree.es/WSvisionaMovilesPeninsulaRest/resources/demandaGeneracionPeninsula?callback=cb&curva=DEMANDAAU&fecha={}'
K = ['dem', 'pv', 'st', 'wind', 'nuc', 'gas', 'other', 'hydro', 'pump', 'ex']

def fetch(d):
    os.makedirs(RAW, exist_ok=True)
    p = os.path.join(RAW, f'{d}.txt')
    if '--offline' not in sys.argv:
        with urllib.request.urlopen(URL.format(d), timeout=30) as r: open(p, 'wb').write(r.read())
    t = open(p).read()
    return {r['ts']: r for r in json.loads(t[t.index('(') + 1:t.rindex(')')])['valoresHorariosGeneracion']}

def row(r):
    ex = r['inter'] + r['icb']
    listed = (r['solFot'] + r['solTer'] + r['eol'] + r['nuc'] + r['cc'] + r['car'] + r['cogenResto'] + r['bio'] + r['hid']
              + ex + r['bat'] + r['consBat'] + r['gf'] + r['aut'] + r['vap'])
    return dict(dem=r['dem'], pv=r['solFot'], st=r['solTer'], wind=r['eol'], nuc=r['nuc'], gas=r['cc'],
                other=r['dem'] - listed + r['cogenResto'] + r['bio'] + r['car'],
                hydro=r['hid'] - r['turb'] - r['conb'], pump=r['turb'] + r['conb'], ex=ex)

def series(d):
    m = fetch(d); out = {k: [] for k in K}
    for h in range(24):
        for mi in range(0, 60, 5):
            r = m.get(f'{d} {h:02d}:{mi:02d}'); rr = row(r) if r else None
            for k in K: out[k].append(rr[k] if rr else None)
    return out

d22, d28, d29 = (series(d) for d in DAYS)
for k in K:                       # 28 April: generation mix up to 12:30 only; demand for the whole day (restoration)
    if k != 'dem': d28[k] = d28[k][:151]
data = json.dumps(dict(d22=d22, d28=d28, dem29=d29['dem']), separators=(',', ':'))
open(os.path.join(HERE, 'data.json'), 'w').write(data)
page = os.path.join(HERE, '..', 'index.html')
html = open(page).read()
html, n = re.subn(r'^const DATA = .*;$', lambda m: 'const DATA = ' + data + ';', html, count=1, flags=re.M)
assert n == 1, 'DATA line not found'
open(page, 'w').write(html)
print('injected', len(data), 'bytes; 28 Apr 12:30:', {k: d28[k][150] for k in K})
