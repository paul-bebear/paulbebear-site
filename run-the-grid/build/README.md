# run-the-grid data build

`build.py` rebuilds the REE data embedded in `../index.html` (the `const DATA = …;` line).

```
python3 build.py            # fetch from REE again, then inject
python3 build.py --offline  # reuse raw/ (the files retrieved on 16 October 2026)
```

Source: Red Eléctrica, "Seguimiento de la demanda" (demanda.ree.es), peninsular Spain, 5-minute values for 22, 28 and 29 April 2025. Terms: REE legal notice, ree.es/es/aviso-legal (name REE as the source, don't alter the data, state the date). Field notes are at the top of `build.py`.
