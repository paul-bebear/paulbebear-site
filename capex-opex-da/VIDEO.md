# Capex, Opex and D&A: video beat sheet

Pilot video 2. A guided tour of this page, in the page's own order. About 9 minutes at the times below, plus a 45-second short cut from step 5.

## Running it

- Open `/capex-opex-da/#step-1`. Any `#step-N` link opens that step.
- `→` / `←` (or PageDown / PageUp, or the bar at the bottom) move between steps. `Home` and `End` jump to the first and last. `A` jumps to the aha step.
- `R` toggles the recording view: only the current visual and its one-line caption, sized off the window. Size the browser window to 1920×1080 for the main video and 1080×1920 for the short.
- `T` flips light and dark. `Esc` leaves the recording view, then step mode.
- The charts stay live. Each step sets the sliders to the values it needs; I can still drag them on camera. In the recording view, letting go of a slider hands the arrow keys back to the steps.
- Going back a step and forward again replays the aha animation, for retakes.
- With reduced motion turned on, the aha step shows its end state straight away.

## The beats

| # | On screen | Time |
|---|---|---|
| 1 | Title and the one-line summary | 0:20 |
| 2 | Flow diagram, question only | 0:25 |
| 3 | Flow diagram, both answers | 0:30 |
| 4 | Part 2 §1: the asset test, and "labels don't make capex" | 0:35 |
| 5 | **Aha.** The €900k project, years appearing one by one, with a running total | 0:45 |
| 6 | Part 2 §2: D&A, and the straight-line formula | 0:25 |
| 7 | Timing chart at a 6-year life, sliders showing | 0:25 |
| 8 | Net book value line, 3-year life | 0:25 |
| 9 | Part 2 §3: the journal entries | 0:30 |
| 10 | The three-statement matrix | 0:30 |
| 11 | Part 2 §4: where EBITDA sits | 0:25 |
| 12 | Timing stats: year-one EBITDA, profit and cash, both routes | 0:25 |
| 13 | Part 2 §5: allowed revenue formula | 0:25 |
| 14 | Regulated chart: depreciation plus return vs opex | 0:30 |
| 15 | Regulated stats at a 10-year life, with the shortcut | 0:25 |
| 16 | Part 2 §5: the capex bias, and "the WACC is not pure margin" | 0:30 |
| 17 | Things that catch people out, 1 to 4 | 0:35 |
| 18 | Things that catch people out, 5 to 8 | 0:35 |
| 19 | "Total profit is identical either way", plus the sources | 0:20 |
| | | **≈ 9:00** |

### 1. Title
Every company spends money, and accountants have two ways to book it. The money leaves the bank the same day either way.
What changes is when that cost shows up in profit. And for a regulated grid operator, whether that euro earns anything back.

### 2. The one question
Accounting only asks one question about each euro you spend.
Does it buy something that keeps producing value after this year? And does the company actually control it?

### 3. The two answers
If the answer is no, it's opex. The whole cost goes into this year's profit and loss, and that's it.
If it's yes, it's capex. It goes on the balance sheet as an asset, and the cost comes out bit by bit over the asset's life. That bit-by-bit cost is D&A.

### 4. The asset test
Under IFRS, something is an asset if you control it, it brings future benefits, and you can measure what it cost. For software there's an extra test: it has to be identifiable.
Control is the one people skip. A licence you control is an asset even if you don't own the code. A subscription you lose the day you stop paying is a service, so it's opex.
And calling a project "strategic" doesn't change any of that. Only the asset test does.

### 5. Same euros, different timing (the aha)
Here's one project. A €900k software integration, paid in cash on day one. Let me book it both ways.
Year one: expensed, all €900k hits profit at once. Capitalised, only €300k does. Year two, nothing on one side, €300k on the other. Year three, same again.
Now look at the running total. Both end at €900k. The total cost never changes, only the year it lands in.

### 6. D&A
Depreciation and amortisation are the same mechanism with two names. Depreciation for physical things like cables and servers, amortisation for intangibles like software.
The default is straight-line: cost minus whatever it's worth at the end, divided by the useful life. For software the end value is usually zero.

### 7. Useful life
The useful life is an estimate, and it gets reviewed every year.
Stretch it to six years and the yearly slice gets thinner. Shorten it and the cost hits profit faster. Same €900k either way.

### 8. What sits on the balance sheet
On the capex route, an asset appears at €900k and shrinks by the D&A slice each year until it's gone. That shrinking number is the net book value.
On the opex route there's nothing on the balance sheet at all. The dashed line just sits at zero.

### 9. The bookkeeping
Here are the actual entries, in thousands. Expensed: debit an expense, credit cash. Done.
Capitalised: debit an asset, credit cash. Then each year, debit amortisation expense and credit accumulated amortisation, €300k at a time.
Cash leaves on the same day in both cases. What changes is what the other side of that entry is.

### 10. Where each route shows up
Three statements, two routes. Opex hits the P&L all at once, above EBITDA. Capex hits it as a slice of D&A each year, below EBITDA.
Opex creates nothing on the balance sheet; capex creates an asset that shrinks. And the cash shows up in operating cash flow for one, investing cash flow for the other. Same cash, different line.

### 11. Why managers like capitalising
The P&L runs top to bottom: revenue, minus operating costs, gives EBITDA. Take off D&A and you get EBIT. Take off interest and tax and you get net profit.
Opex sits above EBITDA. D&A sits below it. So capitalising takes the cost out of EBITDA completely, and that's the number lenders, investors and bonus schemes often watch.

### 12. Year one, in numbers
Back to the €900k project, year one. EBITDA: minus €900k if you expense it, zero if you capitalise it.
Net profit before tax: minus €900k against minus €300k. Cash out: €900k both ways. Total cost over the life: €900k both ways.

### 13. How a grid operator gets paid
Now a different world. A regulated grid operator can't set its own prices. The regulator decides how much revenue it's allowed.
Roughly: an allowance for opex, plus depreciation on its assets, plus a return on its regulated asset base, the RAB, at a rate called the WACC.

### 14. Why a grid operator prefers capex
Same €900k, booked two ways. As opex, the best case is you get the €900k back once, often late, sometimes cut by efficiency targets.
As capex, it goes into the RAB. You get the €900k back as depreciation, the return of your capital. And you get paid a return on the balance that's still outstanding, the return on your capital. At Spain's 6.58% over three years, that's about €118k on top.

### 15. Longer life, bigger return
Stretch the regulatory life to ten years and the return grows, because the money sits in the RAB for longer.
There's a shortcut: the total return is roughly the WACC, times the spend, times life plus one, divided by two. Here that's about €326k.

### 16. The capex bias
That gap is the capex bias. Capitalised spend makes money; expensed spend doesn't. Regulators push back with TOTEX, which treats all spending alike, or, in Italy, by capitalising a fixed share of everything regardless of its label.
One caveat: the WACC isn't pure profit. It pays lenders and shareholders. The operator's real gain is only the gap between the allowed rate and what its capital actually costs.

### 17. Things that catch people out (1 of 2)
Upkeep is never capex. Keeping an asset running is opex; only adding new capability can be capitalised, and IAS 38 says that's rare.
You can't relabel later. Once something's been expensed, it stays expensed.
A prepayment isn't capex either; it unwinds as the service arrives. But staff time spent building an asset can be capitalised, which is one reason companies build in-house instead of buying SaaS.

### 18. Things that catch people out (2 of 2)
If an asset loses its value early, what's left is written off in one hit. That's the risk of capitalising.
Statutory accounts, tax and the regulator can each use different lives for the same asset.
A signed contract isn't a liability until it's performed, unless it turns loss-making. And EBITDA isn't defined by IFRS, so check how each company computes it before comparing.

### 19. The one thing to remember
Over the asset's life, total profit is the same either way. Only the timing and the line it sits on change.
The sources are on screen and on the page: the IFRS standards, Spain's rate from CNMC Circular 8/2025, and the German software lives from StromNEV. The page is linked below if you want to move the sliders yourself.

## The short (45 s, from step 5)

Record at 1080×1920 in the recording view, starting on step 5 (`#step-5`, then `R`). The years appear about 1.3 seconds apart and the closing line fades in at about 5 seconds, so start talking as the first bars rise. Go back a step and forward again to replay it.

> Here's one project. €900k of software, paid in cash on day one. Accountants can book it two ways.
> Expense it, and year one takes the whole €900k. Capitalise it, and year one only takes €300k. Then €300k the next year. Then €300k the year after.
> Look at the running total. Both end at €900k. Same euros. The total cost never changes, only the year it lands in.
> Why does that matter? Because the capitalised version doesn't touch EBITDA at all, and EBITDA is what a lot of people get paid on. The full video walks through it.

The last two lines can play over a hold on the end frame, or over step 12 (the year-one EBITDA numbers) if the short needs a second shot.
