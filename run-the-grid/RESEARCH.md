# Run the grid: research brief on the 28 April 2025 Iberian blackout

The blackout was an overvoltage cascade, not a frequency or "too much solar" failure. The ENTSO-E Expert Panel's **final report (20 March 2026)** describes multiple interacting factors. Voltages rose quickly in a grid with too little fast, dynamic reactive-power absorption. Generators tripped on overvoltage protection, and each trip pushed voltage higher. Iberia then lost synchronism with Europe at 12:33:19–21 CEST and collapsed seconds later. The game should therefore model **voltage and reactive power** as carefully as frequency.

## TL;DR
- **Cause.** Both the ENTSO-E final report (20 Mar 2026) and the Spanish government committee (17 Jun 2025) describe a "multifactorial" overvoltage cascade with three main parts:
  - not enough dynamic voltage control;
  - oscillation-mitigation actions that raised voltages;
  - generator disconnections, some of them improper.

  Blame is still disputed. REE says generators failed their voltage-control obligations. On the utilities' side, AELEC blames REE's planning, and Endesa CEO José Bogas said on 12 Feb 2026 (El Español) that "la causa central y determinante del apagón es la programación por Red Eléctrica de un número reducido de grupos con capacidad de gestionar dinámicamente la tensión".
- **Timeline.**
  - 12:32:00: voltages start climbing.
  - 12:32:57.140: first big trip (Granada, 355 MW).
  - 12:33:16–18: Badajoz and Seville trips.
  - About 2.5 GW was lost by 12:33:18.
  - 12:33:21: the AC lines to France trip.
  - 12:33:24: the HVDC link to France stops.
  - Spain reached 99.95% of demand restored at 07:00 on 29 April and 100% at 14:36. Portugal's restoration was complete at 00:22 on 29 April.
- **Building the game.** Use the Spanish committee report for millisecond timestamps and the ENTSO-E reports for causes. Use REE REData (no token) or ESIOS (token required) for demand and mix data. Treat the inertia and frequency lever as a "myth-buster": the final report's simulations say higher inertia alone would not have avoided the loss of synchronism.

## Key Findings

### Report versions used (cite these labels on the page)
| Label | Document | Date | Status |
|---|---|---|---|
| ENTSO-E SO ESC | ENTSO-E slides "28 April 2025 incident in the Iberian peninsula", System Operation European Stakeholder Committee | 4 Jun 2025 | Preliminary |
| GOV | "Informe no confidencial del Comité de Análisis 28-A" (Spanish government committee) | 17 Jun 2025 (approved by the Council of Ministers) | Official national report; redacted |
| REE | Red Eléctrica, "Incidente en el Sistema Eléctrico Peninsular Español el 28 de abril de 2025" / English "Blackout in Spanish Peninsular Electrical System the 28th of April 2025" | 18 Jun 2025 | TSO report under P.O. 9 |
| FACTUAL | ENTSO-E Expert Panel Factual Report, plus press-briefing deck | 3 Oct 2025 | Facts only, no root causes (panel of 45 experts) |
| FINAL | ENTSO-E Expert Panel Final Report on the Grid Incident in Spain and Portugal on 28 April 2025 | 20 Mar 2026 | Root causes and recommendations (472 pages). Per REE's 20 Mar 2026 release, the panel had 49 experts: 30 from European and national regulators (including the CNMC) and 19 from TSOs and Regional Coordination Centres. |
| ARXIV | Albustami & Taha, "The Iberian Blackout: A Black Swan or a Gray Rhino?" (arXiv 2511.17433) | Nov 2025 | Academic analysis, not official |

Limitation: this brief could not open the FINAL PDF (48.4 MB) directly. FINAL figures come from ENTSO-E's own page and from detailed secondary summaries (POWER Magazine, pv magazine, GO15, Science Media Centre Spain). Before shipping, the coding session should check each figure marked "FINAL" against the PDF.

---

## 1. The blackout timeline (28 April 2025, CEST)

### 1a. Before the event (09:00–12:32)
| Time | Event | Value | Source |
|---|---|---|---|
| 06:00 | Schedule change on the France interconnection | From 2,590 MW export to 1,600 MW export | GOV |
| 09:02 | Frequency deviation caused by schedule changes in Europe | −148 mHz | GOV |
| 09:00 → 10:30 | Voltage variability increases, with larger excursions from 10:30. Voltages stay within limits. | 400 kV band 380–435 kV; 220 kV band 205–245 kV (P.O. 1.1/1.3) | GOV; FACTUAL |
| 05:49, 08:52, 10:30, 11:06, 11:23 | Five small oscillations at about 0.2 Hz | Voltage swings up to 4 kV p-p (10:32), 7 kV (11:03), about 6 kV (11:23) | GOV |
| 11:08, 11:17, 11:20 | Three 400 kV circuits connected to improve damping (Pinar–Tajo, Arcos–Cabra, Pierola–Vandellós) | — | GOV |
| 12:03 | **Oscillation 1.** GOV gives 0.6 Hz with 70 mHz amplitude, damped in 4 min 42 s. FINAL gives 0.63 Hz, 12:03–12:08, a "converter-driven forced oscillation". | Voltage swings: Almaraz 31.2 kV p-p, Arroyo de San Serván 32.7 kV p-p; Almaraz briefly below 375 kV | GOV; FINAL (via POWER) |
| 12:04–12:05 | Shunt reactors disconnected because voltages were low: Villaviciosa, Guadame 220, Rueda, Aragón | — | GOV |
| 12:07–13:00 | France exchange cut by 800 MW to a 1,500 MW export schedule. NREL slides instead say "1500 → 800 MW". **Conflict; use GOV.** | — | GOV; NREL |
| 12:07–12:08 | Five more 400 kV circuits connected (meshing) | — | GOV |
| 12:11 | Spain–France HVDC switched from AC-emulation (PMODE3) to fixed power (PMODE1) | 1,000 MW export (2 × 500 MW), held until the collapse | GOV |
| 12:16:45 | The 0.6 Hz mode reappears | About 30 mHz | GOV |
| 12:19 | **Oscillation 2.** GOV: 0.2 Hz with up to 200 mHz amplitude, damped in 3 min 20 s. FINAL: 12:19–12:22. This is the East–Centre–West inter-area mode. | Almaraz 23 kV p-p | GOV; FINAL |
| 12:19–12:20 | France exchange reduced to 1,000 MW (12:20–14:00). Portugal asked to go to 2,000 MW from 12:30. | Portugal schedule 2,545.2 → 2,000 MW | GOV |
| 12:17–12:24 | More reactors disconnected: Cabra, Peñaflor, Palos 220, Morata | — | GOV |
| 12:21, 12:25 | Two more 400 kV circuits. GOV counts 10 circuits added since 11:10. | — | GOV |
| 12:26 | REE orders a voltage-controlling thermal unit in the south. The fastest available needed **1 h 30 min** (it was hot after shutting down at 09:00), so it was scheduled from 14:00 and never connected. | — | GOV |
| 12:26–12:28 | Five reactors reconnected as voltages rise: Vitoria, Peñaflor, Guadame 220/400, Morata | — | GOV |
| 12:30 | Voltages 410–420 kV and falling; frequency about 50 Hz; low damping | — | GOV |

Every report agrees on the side effect: the mitigation measures (meshing, lower exports, fixed-power HVDC) damped the oscillations but raised voltages. The FACTUAL deck says "voltages increased, though still within operational range."

### 1b. The final 90 seconds (12:32:00–12:33:30)
| Time | Event | Value | Source |
|---|---|---|---|
| 12:32:00 | Voltages rise almost linearly across the grid | Olmedilla 413 → 428 kV in 57 s; Arroyo de San Serván 411 → 424 kV | GOV |
| 12:32:00–12:32:55 | Small losses spread across the grid | 525 MW in total, of which 317 MW is distributed generation under 1 MW and 208 MW is identified plants | GOV; FACTUAL ("about 525 MW") |
| 12:32:00–12:32:48 | FINAL's breakdown of the same window: large RES (>5 MW) running at fixed power factor reduce output | About 500 MW, plus 208 MW of distributed wind/solar and a +317 MW net-load rise (rooftop PV tripping) | FINAL (via POWER, pv magazine) |
| 12:32:57.140 | **Event 1, Granada.** A 400/220 kV generation transformer trips on overvoltage on the generation (secondary) side. | 355 MW injected and 165 MVAr absorbed at the moment of trip; 417.9 kV on the 400 kV side. ARXIV cites 242 kV on the collector side. | GOV; FACTUAL |
| ~12:33:00 | Some nodes exceed 430 kV, below the 435 kV limit | — | GOV |
| 12:33:16.460 / 12:33:17.520 | **Event 2, Badajoz.** Two renewable collector substations trip. | GOV: about 730 MW (582 MW + 118 MW given separately). FACTUAL: about 725 MW of PV and thermo-solar. FINAL: 727 MW. REE press (via review-energy): 582 + 324 MW. **Figures differ.** Frequency drop of 55 mHz; the France flow turns to 895 MW import. | GOV; FACTUAL; FINAL |
| 12:33:17.368 | Wind farms trip, Segovia | 22.87 MW | GOV |
| 12:33:17.780 | **Event 3, Seville** (renewable evacuation position) | GOV: 550 MW. FACTUAL: about 930 MW across Segovia, Huelva, Badajoz, Seville and Cáceres (or >1,100 MW as implied by the frequency change). FINAL: 928 MW. Frequency −75 mHz, not recovered; France import +1,510 MW. | GOV; FACTUAL; FINAL |
| By 12:33:18 | Cumulative loss | About 2.5 GW in Spain; no disconnections in Portugal | FACTUAL |
| 12:33:18.380 | A plant trips with 443.8 kV on the 400 kV grid, above the ride-through obligation. GOV says the cascade is "expected" from here. | 443.8 kV | GOV |
| 12:33:19 | Loss of synchronism with Continental Europe begins | — | FACTUAL; FINAL |
| 12:33:19.620 | Peak import from France | Net 3,807 MW (4,609 MW over AC, −802 MW over HVDC) | GOV |
| 12:33:20.180 | First pumping-shed threshold crossed | 49.50 Hz | GOV |
| 12:33:20.229–.473 | Morocco lines trip (under-frequency relay on the Moroccan side) | 49.314 Hz; Morocco was supplying 314 MW | GOV |
| 12:33:20.520 | Synchronism swing: flow peaks at export to France | 5,587 MW | GOV |
| 12:33:20.600 | First demand LFDD step | 49.00 Hz | GOV |
| 12:33:20.650 | Overvoltage trip | 456 kV, 48.914 Hz | GOV |
| 12:33:20.760 / 21.000 / 21.380 / 21.820 / 22.040 | LFDD steps 2–6 | 48.8 / 48.6 / 48.4 / 48.2 / 48.0 Hz | GOV |
| 12:33:21.407 | Vic–Baixas 400 kV opens on loss-of-synchronism protection | — | GOV |
| 12:33:21.535 | Hernani–Argia opens. **Iberia is separated from France on AC.** About 1,000 MW still flowing out over the HVDC. | 48.458 Hz | GOV |
| 12:33:22.330 | Trip | 465 kV | GOV |
| 12:33:22.702 | Trip near the generator under-frequency limit | 436 kV, 47.79 Hz (limit 47.5 Hz) | GOV |
| 12:33:23.076 | Line trips on overvoltage | 485 kV measured; setting 1.2 Un = 480 kV | GOV |
| 12:33:23.515 | Under-frequency trip | 46.15 Hz; that plant had earlier seen 469.3 kV | GOV |
| 12:33:23.520 | Peninsula–Mallorca HVDC blocks | Balearics lose 96.5 MW, fall to 49.009 Hz, no customers lost | GOV |
| 12:33:23.960 | Voltage collapses at Santa Llogaia and the France HVDC blocks | — | GOV |
| 12:33:24 | ENTSO-E's time for complete collapse | — | ENTSO-E SO ESC; FINAL |
| 12:33:27.930 | Andorra disconnects | — | GOV |
| 12:33:29.741 / 12:33:30 | "Zero voltage" in peninsular Spain | — | GOV |

Load shedding (GOV): 2,037 MW of pumping was shed in the first two steps. About 1,402.5 MW of transmission-connected consumers had been shed by the third step. Portugal (ENTSO-E SO ESC) shed "six more levels" after 49.5 Hz, and its last step operated at 12:33:22.

**RoCoF:** no single official value was found. An approximation from GOV timestamps (calculated for this brief, not published) is 49.0 Hz at 12:33:20.600 and 48.0 Hz at 12:33:22.040, an average of about −0.7 Hz/s. A secondary source quoting energy-charts data shows the Iberian frequency drifting from 49.9758 Hz (12:32:59) to 49.9439 Hz (12:33:17). Treat that as unverified.

### 1c. What caused it: positions side by side
| Actor | Position | Source |
|---|---|---|
| **ENTSO-E FINAL** | Multiple interacting factors: oscillations, gaps in voltage and reactive-power control, fast output changes, and disconnections. Specific findings: renewables ran in fixed power-factor mode (reactive absorption fell as output fell); in POWER Magazine's summary (23 Mar 2026), "the reactive power output of several large synchronous generators reached the required reference value less than 75% of the time" and the rules "imposed no economic consequences for non-compliance" (no unit count was published); shunt reactors were switched by hand and too slowly; Spain's transient 435 kV limit left little or no margin before 435/440 kV ride-through limits; some protection settings were below requirements or had no delay; small PV was unmonitored. Simulations say larger reactive margins could have prevented the cascade. ENTSO-E president Damián Cortinas: "It's not about renewables, it's about voltage control." Recommendations: POWER counts 21, pv magazine 22; check the PDF. | FINAL via POWER, pv magazine, GRA |
| **Spanish government (GOV)** | "Multifactorial" overvoltage. Three causes: (1) not enough dynamic voltage control, "either because they were not sufficiently programmed, or because those that were programmed did not adequately provide what the standard said, or a combination of both"; (2) oscillation measures raised voltages; (3) some disconnections "apparently improper". REE scheduled 10 thermal units (3 nuclear, 7 CCGT) for voltage control. One south-west unit dropped out at 19:47 on 27 April and was not replaced for the midday hours. No evidence of a cyberattack. | La Moncloa, 17 Jun 2025; GOV |
| **REE** | Generation subject to P.O. 7.4 "failed to comply with its dynamic voltage control obligations". On the incorrect trips, REE's summary of FINAL (reported by EFE on 20 Mar 2026) cites "al menos, 9 desconexiones incorrectas de generación"; this count is REE's reading and should be checked against the FINAL PDF. "Not caused by an inertia problem": inertia was above the ENTSO-E recommendation. Its scheduling was sufficient. REE's 20 Mar 2026 press release ("Red Eléctrica no falló"), issued the day FINAL was published, states "no existe causa atribuible a Red Eléctrica que condujera al cero eléctrico del 28 de abril de 2025" and says FINAL does not name its scheduling as a cause. | REE press releases 18 Jun 2025 and 20 Mar 2026; EFE |
| **AELEC** (Iberdrola, Endesa, EDP) | REE was "solely responsible" through "poor management/planning". It "opted to manage voltage with limited synchronous capacity and an unbalanced geographical distribution". AELEC's plants met the rules. It says voltage fluctuations fell 37–52% in the days after, once more CCGTs ran. Endesa CEO José Bogas (El Español, 12 Feb 2026): "la causa central y determinante del apagón es la programación por Red Eléctrica de un número reducido de grupos con capacidad de gestionar dinámicamente la tensión". | Ara.cat; E&T/Reuters; El Español |
| **FACTUAL (neutral)** | The Andalusian unit's unavailability is recorded. On the morning of 28 April REE "concluded that it was not necessary to replace it." Q compliance allows a 25% time margin outside the reference band (per the CNMC). | FACTUAL deck |
| **CNMC** | Approved the new P.O. 7.4 on 12 Jun 2025, letting renewables be enabled for dynamic voltage control. In Oct 2025 it approved temporary urgent changes to P.O. 3.1/3.2/7.2 for 30 days, but **rejected** REE's urgent P.O. 7.4 change (raising compliance from 75% to 90% of the time) because synchronous units could not meet it. On 10 Jul 2026, after a consultation from 8 to 25 May 2026, it approved P.O. 7.4/14.4 changes (DCOOR/DE/006/26). These add "una nueva modalidad de prestación básica basada en el seguimiento de consignas fijas de tensión o potencia reactiva" for plants "que no disponen de los sistemas de comunicación necesarios para recibir consignas variables en tiempo real". The proposal annex sets basic-mode setpoints of 400 kV on the 400 kV grid and 223 kV on the 220 kV grid, with setpoint changes ramped at 0.33% Un per minute; check these against the final text. | UNEF; pv magazine ES; CNMC; elperiodicodelaenergia |
| **REN (Portugal)** | Blackout was "the result of a significant voltage fluctuation in the Spanish grid at a time when Portugal was importing energy from Spain." REN denied the "atmospheric" statement. ERSE's position: not researched for this brief. | Live Science/Euronews; AFP |

How to frame it in the game: REE says generators should have absorbed more. AELEC says REE should have scheduled more. FINAL says both contributed and adds the rules themselves (fixed power factor, the 435 kV margin, no penalties) and manual reactor switching. Present all three; do not pick a winner.

### 1d. System state at 12:30 (peninsular Spain unless noted)
| Item | Value | Scope | Source |
|---|---|---|---|
| Demand | 25,184 MW | Spain peninsular | GOV |
| Pumped-storage consumption | 2,978 MW | Spain peninsular | GOV |
| Demand (ICS classification, pumping excluded) | 25,200 MW Spain; 5,900 MW Portugal | Per country | ENTSO-E SO ESC |
| Portugal pumping | ~2 GW | Portugal | ENTSO-E SO ESC |
| Mix shares | Renewables 82%; nuclear 10% (4 reactors connected, 2 at full load); gas 3% (6 plants); coal 1%; cogeneration and waste 4% | Spain peninsular | GOV |
| Solar PV | ~18 GW (55%) | Spain peninsular | NERC/FERC slides citing REE dashboard (rounded) |
| Solar thermal | ~1.5 GW (5%) | Spain peninsular | NERC/FERC (rounded) |
| Wind | ~3.5 GW (11%) | Spain peninsular | NERC/FERC (rounded) |
| Hydro | ~3.2 GW (10%) | Spain peninsular | NERC/FERC (rounded) |
| Nuclear | ~3.4 GW (10%) | Spain peninsular | NERC/FERC (rounded) |
| Cogeneration and waste | ~1.4 GW (4%) | Spain peninsular | NERC/FERC (rounded) |
| Combined-cycle gas | Exact MW not published in the sources reviewed (3% share per GOV). Secondary sources give 1.6–2.2 GW, unverified. | Spain peninsular | GOV |
| Exports at 12:30 (5-min data) | France 868 MW; Portugal 2,652 MW; Morocco 782 MW | Spain borders | Secondary (REE REData via Substack); confirm in REData |
| Exports at 12:32 (rounded) | France 1,000 MW; Portugal 2,000 MW; Morocco 800 MW | Spain borders | ENTSO-E SO ESC |
| Thermal units with voltage-control duty connected | 11: 4 nuclear, 1 coal, 6 gas (plus hydro) | Spain peninsular | GOV |
| Capacity declared unavailable for 28 April | CCGT 7,426.3 of 24,562 MW; nuclear 3,078.6 of 7,117 MW; coal 903.5 of 1,820 MW; pumped turbining 1,392.1 of 3,331 MW | Spain peninsular | GOV Tables 1–2 |
| Day-ahead price | Daily average €18.50/MWh; zero or negative in central hours | Spain | GOV (OMIE) |
| System inertia | H_tot = 2.21–2.71 s (FACTUAL p.36, as cited by ARXIV). NREL slides: 2.3 s against a 2 s floor. REE: "higher than the Entso-e recommendation". | Spain | ARXIV; NREL; REE |

### 1e. Restoration
| Time | Milestone | Source |
|---|---|---|
| 12:44 | First Spain–France 400 kV line energised (Hernani, west) | GOV; ENTSO-E SO ESC |
| 12:45 | Castelo do Bode (PT hydro) energises REN's 220 kV | ENTSO-E SO ESC |
| 13:04 | Morocco interconnection energised; ONEE support 100 MW (southern island restarted after a trip at 14:34) | GOV |
| 13:07 | First Spanish load supplied (Irún, 31 MW) | GOV |
| 13:35 | Eastern France line energised (Vic) | GOV |
| 14:46 | All nuclear plants have external auxiliary supply | GOV |
| 15:14 | First thermal unit synchronised | GOV |
| 15:59 / 21:58 | HVDC Baixas–Santa Llogaia link 1 / circuit 2 transmitting | GOV |
| 16:11 / 16:31 | Castelo do Bode restarts; first Portuguese consumers connected | ENTSO-E SO ESC |
| 17:26 | Tapada do Outeiro (PT CCGT) black start succeeds on its second attempt | ENTSO-E SO ESC |
| 18:36 | Aldeadávila–Pocinho 220 kV: Portugal gets European frequency | GOV; FINAL |
| 21:34–21:37 | 400 kV Puebla de Guzmán–Tavira and Cartelle–Lindoso | GOV |
| 22:30–23:32 (28 Apr) | About 50% of Spanish demand restored; 21 thermal units connected at 23:32 | GOV |
| 00:22 (29 Apr) | Portugal restoration complete | ENTSO-E SO ESC; FINAL |
| 00:30 | Madrid fully restored | GOV |
| ~04:00 | Spain transmission system restored | ENTSO-E SO ESC; FINAL |
| 07:00 | 99.95% of Spanish demand restored | GOV |
| 14:36 | Spain moves from Emergency to Alert; 100% considered restored | GOV |

Strategy (GOV): islands built around France (Catalonia, Basque Country) and Morocco (South), plus black-start hydro islands in Duero, Galicia and Asturias-Cantabria. Planned zones: Sur, Tajo-Centro, Levante, Galicia-León, Asturias-Cantabria, Aragón-Cataluña, Duero-Francia. Hydro plants were named only generically; Ribarroja appears in an island operation plan. FINAL lists failed bottom-up attempts in Galicia, East Asturias, Cantabria, Levante, Toledo and Andalucía.

### 1f. Myths
| Claim | Evidence |
|---|---|
| Cyberattack | The government's cybersecurity review, which Aagesen called "the largest cybersecurity investigation that has ever taken place in our country", found "no evidence of cyber-incident or cyber-attack". It did find vulnerabilities. |
| "Induced atmospheric vibration" / rare atmospheric phenomenon | REN: "REN confirms we did not put out this statement." AEMET found no unusual phenomena and no sudden temperature changes. EDMO traced the claim to a deleted Reuters alert and a CGTN quote. |
| "Renewables / too much solar caused it" | FINAL: "It's not about renewables, it's about voltage control." But most of the units that tripped were inverter-based, and fixed power-factor rules made renewables worsen voltage swings. The fair framing is that the rules and settings governing renewables mattered, not the solar share itself. A similar day, 22 April, had PV at 51% at 12:30 without a blackout (Maldita, citing REE). |
| "Low inertia caused it" | REE: inertia was above the ENTSO-E recommendation. FINAL simulations: even with higher inertia, loss of synchronism would not have been avoided. The cascade started at about 50 Hz. |
| Nuclear claims | 3,078.6 MW of nuclear was declared unavailable (refuelling or maintenance per GOV). 4 reactors were connected, 2 at full load. Synchronous units, nuclear included, were among those that did not meet the reactive reference. More nuclear does not automatically mean more voltage control unless the units actually absorb reactive power. |

---

## 2. The physics to simulate

### Frequency and the swing equation
Frequency rises when generation exceeds load and falls when load exceeds generation. Use the aggregated swing equation:

df/dt = (P_gen − P_load) · f0 / (2 · H · S)

- f0 = 50 Hz
- P in MW
- H = inertia constant in seconds (stored kinetic energy divided by rating)
- S = rated MVA of the synchronous fleet online
- H·S = stored energy in MWs

The per-machine form is 2H·dω/dt = Pm − Pe − D·Δω (ARXIV eq. 12).

Who provides inertia: synchronous machines (nuclear, CCGT/OCGT, coal, hydro, solar thermal, synchronous condensers). Inverter-based PV, wind and batteries provide none unless they are grid-forming or synthetic-inertia controlled. Typical H per technology was **not sourced in this research**. Pull a table from a power-systems textbook (e.g. Kundur, *Power System Stability and Control*) and cite it.

### Voltage and reactive power (the core mechanic for 28 April)
- Voltage is local and set by reactive power (Q) balance. A quasi-static model: ΔV ≈ −J_QV⁻¹ · ΔQ (ARXIV eq. 6). When a plant that was absorbing Q trips, nodes nearby go up in voltage.
- Under the old rules renewables ran at **fixed power factor**, so Q fell with P (FINAL). The synchronous units with P.O. 7.4 duty had a dead band of 405–410 kV with no obligation in between (ARXIV's reading of REE).
- Shunt reactors absorb Q = B·V² but were switched by hand (FINAL).
- Load shedding removes reactive load and so raises voltage further (ARXIV, citing REE).

### Response layers (Continental Europe)
| Layer | Value | Source |
|---|---|---|
| Reference incident | 3,000 MW | ENTSO-E FCR explanatory note; Artelys/ENTSO-E |
| FCR | Sized to the reference incident in both directions; keeps frequency within 50 ± 0.2 Hz; full activation within 30 s | ENTSO-E RfG LFSM guidance; Artelys |
| LFSM-U / LFSM-O activation | 49.8 Hz / 50.2 Hz | ENTSO-E LFSM guidance |
| aFRR / mFRR timings and Spain volumes | Not captured in this research | — |

### Protection thresholds
| Item | Value | Source |
|---|---|---|
| ENTSO-E CE LFDD | Steps between 49.0 and 48.0 Hz; at least 6 steps including 49.0 Hz; 100–200 mHz between steps recommended; reconnect above 49.8 Hz | ENTSO-E SAFA Policy on Emergency & Restoration |
| % of load per step (NC ER) | Not captured | — |
| Spain pumping shed | 49.5 Hz and 49.3 Hz | GOV |
| Spain demand LFDD | 49.0 / 48.8 / 48.6 / 48.4 / 48.2 / 48.0 Hz (6 steps) | GOV |
| Generator under-frequency withstand | Down to 47.5 Hz (Orden TED/749/2020) | GOV |
| Over-frequency trip settings | Not captured | — |
| Spain 400 kV band | 380–435 kV (P.O. 1.1/1.3); EU harmonised band 380–420 kV; Portugal upper limit 420 kV | GOV; FINAL; FACTUAL |
| Spain 220 kV band | 205–245 kV | GOV |
| Generator overvoltage ride-through | 435 kV or 440 kV depending on commissioning date; ARXIV cites 440 kV for 60 min | FINAL; ARXIV |
| Example line overvoltage protection | 1.2 Un = 480 kV | GOV |
| RoCoF protection settings in Spain | Not published in the sources reviewed | — |

### Demand range
- Historic peninsular peak: 44,876 MW (17 Dec 2007) (GOV).
- Typical daily and annual minimum and maximum: not captured. Derive them from REData (section 3).

### Ramp rates and lead times
Only one sourced value: a hot CCGT needed 1 h 30 min to synchronise (GOV). REE recommends 10-minute fixed ramps for schedule changes (REE report). All other ramp rates are not sourced here and must be taken from cited literature.

---

## 3. Data sources

| Source | Access | What to use | Terms |
|---|---|---|---|
| **REE REData** (apidatos.ree.es) | No token | `https://apidatos.ree.es/es/datos/demanda/demanda-tiempo-real?start_date=2025-04-28T00:00&end_date=2025-04-28T23:50&time_trunc=hour` returns real, programmed and forecast demand at 10-min steps. `/es/datos/generacion/estructura-generacion` gives the mix, but third-party users report it is daily-only and rejects hourly. Example parameters: `geo_limit=peninsular`. | Terms point to the REE aviso legal (ree.es/es/aviso-legal). Exact licence text not verified; credit "Red Eléctrica (REE)". |
| **ESIOS** (api.esios.ree.es) | Free personal token, requested from consultasios@ree.es; header `x-api-key` | `GET /indicators/1293?start_date=2025-04-28T00:00&end_date=2025-04-28T23:59` for real demand (MW). Search `/indicators` for per-technology generation and exchanges. Some users report REE asks for a company tax ID (CIF), unverified. | ESIOS terms not verified; credit REE/ESIOS. |
| **ENTSO-E Transparency Platform** | Account, then email transparency@entsoe.eu, then generate a security token; endpoint `https://web-api.tp.entsoe.eu/api` | Actual generation per type, load, cross-border physical flows (15-min/hourly) | Terms of Use (approved 29 Mar 2023). The open-data list is CC BY 4.0 (added 18 Feb 2022). Name "the ENTSO-E Transparency Platform" as the source; do not imply ENTSO-E endorsement. |
| **High-resolution traces** | — | FACTUAL/FINAL figures (PMU data from REE, REN and RTE; Carmona voltage and frequency; Swissgrid frequency); GOV charts (REE source) | Reuse terms for report figures not verified. Raw PMU data not published. |
| ARXIV replication code | GitHub abdallahbustami/Iberian_blackout | IEEE-39 cascade model | Licence not verified |

---

## 4. Game design input

### Normal day
An hourly or 15-minute spring profile was **not retrieved**. Generate it from REData `demanda-tiempo-real` for 22 April 2025, a comparable weekday with about 27,000 MW demand and PV at 51% at 12:30 (Maldita, citing REE). Use the ENTSO-E per-type generation series for the same day.

### Player levers and real constraints
| Lever | Realistic constraint (sourced) |
|---|---|
| Start a CCGT for voltage control | Hot start took 1 h 30 min (GOV); cold start not sourced. Installed 24,562 MW, 7,426.3 MW unavailable that day (GOV). |
| Keep nuclear online | 7,117 MW installed; 3,078.6 MW unavailable (GOV) |
| Pumped storage | 3,331 MW turbining installed; 2,978 MW pumping at 12:30; shed at 49.5/49.3 Hz (GOV) |
| France exchange | Schedules of 2,590 → 1,600 → 1,500 → 1,000 MW seen that day; HVDC 2 × 500 MW (GOV). Commercial NTC: not verified. |
| Shunt reactors | Manual switching took minutes; FINAL recommends automation |
| Renewables in voltage-control mode | Allowed from the 12 Jun 2025 P.O. 7.4 (CNMC); a "basic" fixed-setpoint mode was added in July 2026 |
| Synchronous condensers / STATCOM | GOV notes no synchronous condensers on the mainland (per a secondary reading); REE recommends deploying them |

### "What if" levers for the replay
| Lever | Expected effect | Confidence and source |
|---|---|---|
| More reactive-power margin (dynamic Q) | Cascade prevented | **High**: FINAL simulations |
| Renewables in voltage-control mode, not fixed power factor | Removes the "Q drops with P" amplifier | **High**: FINAL recommendation; GOV; REE |
| Protection settings aligned with requirements and time delays | Fewer premature trips | **High**: FINAL found divergent settings |
| Automatic shunt reactors | Faster absorption | **Medium–high**: FINAL recommendation |
| Synchronous units meeting their P.O. 7.4 reference | More absorption | **Medium**: REE and GOV; disputed by AELEC |
| Extra CCGT scheduled the night before | More voltage control in the south-west | **Disputed**: GOV/AELEC yes; REE/FINAL do not name scheduling as a cause |
| HVDC left in AC-emulation mode | Possibly less stress | **Low**: ARXIV argument only |
| More inertia only | Does **not** save the grid | FINAL simulations (myth-buster lever) |

---

## 5. Sources (credit on the page)
- ENTSO-E Expert Panel, *Final Report on the Grid Incident in Spain and Portugal on 28 April 2025*, 20 Mar 2026: https://www.entsoe.eu/publications/blackout/28-april-2025-iberian-blackout/ (reuse terms not verified)
- ENTSO-E Expert Panel, *Factual Report*, 3 Oct 2025, and press-briefing deck: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/Publications/2025/iberian-blackout/251003_ENTSO-E-Media%20briefing%20on%20Factual%20Report.pdf
- ENTSO-E, SO ESC slides, 4 Jun 2025: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/Network%20codes%20documents/GC%20ESC/GC%20ESC%20MEETING%20DOCS/2025/250604_SO_ESC_meeting_28_April_2025_incident.pdf
- Gobierno de España, *Informe no confidencial del Comité de Análisis 28-A*, 17 Jun 2025: https://www.lamoncloa.gob.es/consejodeministros/resumenes/Documents/2025/Informe-no-confidencial-Comite-de-analisis-28A.pdf ; press release: https://www.lamoncloa.gob.es/lang/en/gobierno/councilministers/paginas/2025/20250617-council-press-conference.aspx (Spanish public-sector reuse law, Ley 37/2007: cite the source and do not distort it)
- REE, incident report, 18 Jun 2025: https://d1n1o4zeyfu21r.cloudfront.net/WEB_Incident_%2028A_SpanishPeninsularElectricalSystem_18june25.pdf ; press release: https://www.ree.es/en/press-office/news/press-release/2025/06/red-electrica-presents-report-incident-28-april-and-proposes-recommendations
- REE, "Red Eléctrica no falló", 20 Mar 2026: https://www.ree.es/es/sala-de-prensa/actualidad/nota-de-prensa/2026/03/red-electrica-no-fallo-el-informe-del-expert-panel-europeo-confirma-las-causas-del-incidente-identificadas-por-el-os
- CNMC, DCOOR/DE/008/25: https://www.cnmc.es/sites/default/files/editor_contenidos/Energia/Consulta%20Publica/1_DCOOR_DE_008_25_Resolucion%20.pdf ; CNMC DCOOR/DE/006/26 press release (10 Jul 2026); UNEF summary on P.O. 7.4: https://www.unef.es/es/comunicacion/comunicacion-post/el-control-de-tension-de-las-renovables-la-actualizacion-del-po-74
- Albustami & Taha, arXiv:2511.17433: https://arxiv.org/html/2511.17433v1 (arXiv licence per paper; check before reusing figures)
- POWER Magazine, "Anatomy of a Blackout" (23 Mar 2026): https://www.powermag.com/anatomy-of-a-blackout-findings-from-the-spain-portugal-grid-collapse-final-report/ ; pv magazine (23 Mar 2026); Ara.cat (AELEC); El Español (Bogas, 12 Feb 2026); EFE (20 Mar 2026); E&T (IET); EDMO; The Local/AFP; NERC/FERC slides (Jun 2025); NREL slides (docs.nrel.gov 95103)
- REE REData docs: https://www.ree.es/en/datos/apidata ; ESIOS API docs: https://api.esios.ree.es/doc/ ; ENTSO-E TP legal terms: https://transparencyplatform.zendesk.com/hc/en-us/articles/40921911218961-Legal-Terms-and-Conditions
- ENTSO-E SAFA Policy on Emergency & Restoration; ENTSO-E LFSM implementation guidance (NC RfG)

## Open questions / uncertain
- **Exact MW per technology at 12:30.** Only GOV percentages and rounded NERC values are available here. CCGT MW is not published in the sources reviewed.
- **Size of Events 2 and 3.** 725 / 727 / 730 / >900 MW for Badajoz, and 550 MW (GOV) against about 930 MW (FACTUAL/FINAL). The sources group trips differently.
- **Collapse time.** 12:33:24 (ENTSO-E), 12:33:27 (ARXIV), 12:33:30 (GOV).
- **Source of the 0.63 Hz oscillation.** REE points to a PV plant in Badajoz. ENTSO-E (FACTUAL) did not confirm it. FINAL calls it converter-driven in a specific area.
- **FINAL missing data.** FINAL could not determine the cause of some early trips because recordings were missing. The number of recommendations is also unconfirmed (21 per POWER, 22 per pv magazine).
- **Not captured in this research:** official RoCoF values, H by technology, ramp rates, NC ER % per LFDD step, Spain–France NTC, licences for reusing REE/ESIOS data and report figures.
- **Responsibility.** Still contested between REE and the utilities. Legal and CNMC sanction proceedings were not reviewed.
