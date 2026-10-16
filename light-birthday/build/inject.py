"""Replace the embedded star data in ../index.html with build/data.json. The page itself is the source of truth for code."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
page = os.path.join(HERE, '..', 'index.html')
data = open(os.path.join(HERE, 'data.json'), encoding='utf-8').read().strip()
html = open(page, encoding='utf-8').read()
new, n = re.subn(r'^const DATA = .*;$', lambda m: f'const DATA = {data};', html, count=1, flags=re.M)
assert n == 1, 'could not find the "const DATA = ...;" line'
open(page, 'w', encoding='utf-8').write(new)
print(f'wrote {len(new.encode()):,} bytes to index.html')
