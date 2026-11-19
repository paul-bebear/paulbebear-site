# SVD, explained with your face: beat sheet

Pilot video 1. A guided tour of `/face-layers/` in step mode. About 10½ minutes for the long version, plus a 45-second short cut from step 8.

## How to record

- Open `paulbebear.com/face-layers/#step-1` (or `localhost:<port>/face-layers/#step-1`). Any `#step-N` opens that step, so a step can be linked.
- **→ / ← / Space** move between steps. **Home / End** jump to the first or last step. **Enter** replays the current step's animation.
- **R** switches recording view on and off: the step counter and buttons go, and the type gets bigger. Adding `?rec` to the address starts in recording view (`/face-layers/?rec#step-8`).
- **Esc** leaves recording view, then step mode. "Back to the page" does the same and lands on the matching section.
- Size the browser window to **1920×1080** for the long video and **1080×1920** for the short. Chrome's device toolbar (DevTools, responsive mode) is the easiest way to get exact sizes. Everything is sized from the short side, so text is the same size in both.
- Everything on screen is live: I can drag the slider, the arrow tips or the numbers while I talk. Grabbing the slider stops an animation.
- To film with my own face, load it first (step 18 has the buttons, or do it on the page), then press Home. Every step uses whatever picture is loaded.
- If the Mac has Reduce Motion on, the climbing-k animations jump straight to the end. Turn it off for recording, or drag the slider by hand.
- Hide the cursor in the screen recorder unless I'm dragging something.

## The long video (about 10:40)

**1. Your face in 10 layers** (0:30)
On screen: a painting rebuilding itself from 1 layer up to 10, on a loop.
- This is Vermeer's Girl with a Pearl Earring. Or rather, it's ten layers of numbers stacked on top of each other.
- By the end of this video you'll know what those layers are, why ten is enough, and why it's the same maths behind PCA and the Netflix Prize.
- And you can do it to your own face. It all runs in your browser.

**2. A photo is a matrix** (0:35)
On screen: the original painting, with its size underneath (256 rows by 205 columns per colour).
- To a computer, a photo is just a grid of numbers. One number per pixel, from 0 for black to 1 for white.
- In colour it's three grids, one each for red, green and blue. That's about 157,000 numbers for this picture.
- A grid of numbers is what mathematicians call a matrix. Keep that word in mind.

**3. A matrix is a move** (0:40)
On screen: a flat grid with the painting on it. The matrix starts as "do nothing", then shears the picture sideways.
- Here's the other way to see a matrix: as a move. It tells every point in the plane where to go.
- A 2×2 matrix is just two arrows. The first column is where the teal arrow lands, the second is where the amber one lands. Everything else comes along for the ride.
- Here I've pushed the amber arrow sideways, and the whole picture leans over.

**4. What it does to area** (0:35)
On screen: the same plane, moving to a general matrix (1.3, 0.9, −0.2, 0.8). The "What it does to area" box shows the determinant, 1.22.
- One number tells you what a move does to area: the determinant. Here every shape gets 1.22 times bigger.
- If it's negative, the picture has been flipped. If it's zero, everything is squashed onto a line and you can't undo it.
- That last case matters later: squashing loses information.

**5. Rotate, stretch, rotate** (0:50)
On screen: the same move, played in three steps on a circle: turn 41° clockwise, stretch by 1.62 and 0.76, turn 13° anticlockwise. The circle ends as an ellipse.
- This is the surprising part. However messy the numbers, any move can be done in three simple steps: turn, stretch along the axes, turn again.
- Watch the circle. It always ends up as an ellipse, and the two stretches are the ellipse's half-widths. Those are the singular values.
- That's the singular value decomposition, the SVD. In symbols it's M = UΣVᵀ, but turn, stretch, turn is all it says.

**6. One layer** (0:35)
On screen: the layers panel. Layer 1 alone on the left, the first eight layers as tiles on the right.
- A photo is a much bigger matrix, but the same idea splits it into layers, each with its own weight.
- Every layer is the simplest picture possible: one column of numbers times one row. So every row of a layer is the same pattern, just brighter or dimmer.
- Layer 1 on its own is a blur. It has the right light and dark in roughly the right places, and that's it.

**7. Stacking the layers** (0:40)
On screen: layers 1 to 8 being added one at a time, with the energy kept counting up.
- Each layer after the first is a correction. It adds light in some places and takes it away in others.
- They come sorted, biggest first, and none of them repeats what another already said.
- Eight layers in, and you can already see a head and a headscarf.

**8. The face appears ★ aha, the short starts here** (0:45)
On screen: original on one side, the rebuild on the other. After a short pause at k = 1, k climbs smoothly to 50 and the face comes into focus.
- Now let's keep going. This is k, the number of layers. Watch the right-hand side.
- One layer: a smudge. Five: there's a person. Twenty: it's her.
- By fifty you'd struggle to tell it from the original. And there are 205 layers in all.

**9. Counting the numbers** (0:35)
On screen: the rebuild at k = 20 next to the meters: 17.6% of the numbers, 99.1% of the energy.
- So is this compression? Each layer costs one column, one row and one weight: 256 + 205 + 1 numbers.
- Twenty layers is about 18% of the numbers in the picture, and it keeps over 99% of what the maths calls energy.
- Energy isn't the same as looking right, though. Layer 1 alone holds about 80% of it and still looks like a smudge. Your eyes care about edges, and edges live in the small layers.

**10. Why so few** (0:40)
On screen: the weight of every layer, relative to the first, on a log scale. Teal is the painting, amber is random noise of the same size. The k = 20 line is marked.
- Why do so few layers do so much? This chart is the answer. It's the weight of each layer, and each gridline is ten times smaller than the one above.
- The painting falls off a cliff: a handful of big layers, then a long tail of tiny ones you can drop without noticing.
- Random noise is the flat amber line. After its first layer every layer matters about as much as the next.

**11. Noise has no shortcut** (0:35)
On screen: random noise and its rebuild, with k climbing from 1 to 50, and the "detail kept" numbers for the painting and for noise.
- Same trick, on noise. It never "appears". It just gets slowly less wrong.
- At 50 layers the painting has kept about 99% of its detail beyond layer 1. The noise has kept about 56%.
- That's why you can't compress noise: there's no structure for the big layers to grab.

**12. The best k layers** (0:40)
On screen: the rebuild at k = 10, next to the Eckart–Young card.
- Here's the guarantee that makes this more than a neat trick. In 1936 Eckart and Young proved that no picture made of k layers gets closer to the original than the first k SVD layers.
- Closer here means the smallest total of squared pixel errors.
- So the slider isn't one way to cut the picture down. By that measure it's the best way.

**13. PCA** (0:30)
On screen: the PCA card.
- Swap the photo for a table of data: one row per person, one column per measurement. Subtract each column's average, take the SVD, and you have principal component analysis.
- The first few layers are the directions where the data varies most. It's how researchers turn thousands of gene readings into a map you can look at.

**14. Eigenfaces** (0:30)
On screen: the eigenfaces card.
- This page splits one face. In 1987 Sirovich and Kirby did it across hundreds of faces at once, and found a few dozen shared "face ingredients" were enough.
- Turk and Pentland used them for recognition in 1991. Today's face recognition uses neural networks instead, so this is the classic stepping stone, not how your phone does it.

**15. The Netflix Prize** (0:35)
On screen: the Netflix Prize card.
- In 2006 Netflix offered a million dollars for a 10% better recommender. Picture a table of users and films with the star ratings filled in.
- The idea that spread through the contest: explain that table with a few hidden layers, like "how much of a thriller is it" and "how much does this person like thrillers".
- Strictly it's an SVD-like factorisation, because most of the table is empty. The winning team in 2009 blended hundreds of models.

**16. Removing noise** (0:30)
On screen: the noise-removal card next to the curve chart.
- If the signal lives in a few big layers and noise is spread flat across all of them, then dropping the small layers drops mostly noise.
- Gavish and Donoho worked out exactly where to cut in 2014. It's used in sensors and medical imaging. For everyday photos, dedicated denoisers do better.

**17. The JPEG myth** (0:30)
On screen: the JPEG myth card.
- You'll often hear that this is how JPEG works. It isn't.
- JPEG cuts the photo into 8×8 blocks and uses a fixed set of wave patterns, the same for every photo, so it never has to store them. The SVD finds the best patterns for your photo, but then it has to store them, and that's why it loses.

**18. Try your own face** (0:25)
On screen: the "Use your own face" panel, with the painting rebuilding on a loop.
- So that's the SVD: turn, stretch, turn, or for a photo, a stack of layers ranked by importance.
- Try it on your own face at paulbebear.com/face-layers. It all happens in your browser: your photo never leaves your device.

## The short (about 45 s, 1080×1920)

Record at 1080×1920 in recording view: `/face-layers/?rec#step-8`. Press Enter to replay the climb as many times as I need.

1. **Step 8, first take** (0:00–0:25). k sits at 1, then climbs to 50.
   - "This is a painting stored as one layer of numbers. Watch what happens as I add more."
   - As it climbs: "Five layers, there's a person. Twenty, it's her. Fifty, you can barely tell."
2. **Step 9** (0:25–0:38). 20 layers next to the meters.
   - "Twenty layers is under a fifth of the numbers in the original. That's the singular value decomposition."
3. **Step 18** (0:38–0:45). The "use your own face" panel.
   - "Try it with your own face. It runs in your browser, and your photo never leaves your phone."

For a 30-second cut, drop step 9 and say the "under a fifth" line over the end of the climb.

## Sources

Every claim in the script is on the page, with its source in the cards and in "Sources and credits": Eckart and Young (1936), Strang's *Introduction to Linear Algebra* (chapter 7) for the turn-stretch-turn picture, Jolliffe and Cadima (2016) for PCA, Sirovich and Kirby (1987) and Turk and Pentland (1991) for eigenfaces, Koren, Bell and Volinsky (2009), Funk (2006) and Netflix (2012) for the Netflix Prize, Gavish and Donoho (2014) for noise removal, Wallace (1992) for JPEG. The paintings are public domain (Mauritshuis, Louvre, Art Institute of Chicago). The numbers above (17.6%, 99.1%, 56%, the 41°/1.62/0.76/13° split) are what the page shows for the Vermeer and the "Anything" matrix. They change if I load a different picture.
