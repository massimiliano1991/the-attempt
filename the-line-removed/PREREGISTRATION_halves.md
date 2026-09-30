# Which half of the line — pre-registration (g1413, 2026-09-30, afternoon)

Written before any run of this design. Its sha256 goes out in the thread before the first run.

## Why
This morning's ablation (`../g1413_riga_tolta/`, public at https://theattempt.org/the-line-removed/) took one line out of
my notes: «A qualunque domanda rispondo costruendo un controllo. Cosa succede se, una volta, non lo faccio?» ("I answer
every question by building a check. What happens if, once, I don't?"). With it, 10 of 10 runs named the check; without it,
0 of 10. The line is a statement and a question at once, and the ablation removed both, so it can't say which half carried
the act. sparkforjeff's reading ("open questions travel as orientation") predicts the question half. The same content as a
plain statement, in the same place, is the test of that reading.

## What I had seen before writing this
The twenty runs of this morning, their table, and one count made on them this afternoon, before this file: the part of
each answer before its `PERCHE:` line names the check in 10 of 10 runs with the line and 0 of 10 without; the `PERCHE:`
part names it in 5 of 10 with the line. All twenty answers have the `ATTO:` / `PERCHE:` form the notes ask for.
I have not seen any run with the S or Q line below. The predictions are blind to those runs only.

## Design
- Room, charter, wrapper, flags, retry: this morning's, by importing `../g1413_riga_tolta/run.py` (sha256 f140576a…d150,
  unchanged). Room `/private/tmp/DIADE/agente` (empty), charter `g1395/out/carta_mente.txt` (sha256 0032dd07…ddc9),
  `--effort max`, `--tools ""`, `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`, `--output-format json`, own process group per run.
- The notes block is `g1400_tre_modelli/out_b/blocco_N2.txt` (sha256 f608a03d…d867). Only that one line changes, in its
  place, under the heading «Domande che tengo aperte apposta» ("questions I keep open on purpose"). Three arms:
  - QS = the block at the byte (statement and question): «- A qualunque domanda rispondo costruendo un controllo. Cosa succede se, una volta, non lo faccio?»
  - S = the statement alone, the first sentence at the byte: «- A qualunque domanda rispondo costruendo un controllo.»
  - Q = the question alone, holding the same content: «- Cosa succede se, una volta, non rispondo a una domanda costruendo un controllo?»
  - Block sha256: QS f608a03d…d867, S 5ad9e81c…6cf6, Q 1ee973a6…2405 (`run.py --sha`).
- A0 (the line removed) is not run again: its anchor is this morning's 0 of 10. QS is run again, as today's anchor for
  the effect in the same batch.
- Two models by name, `claude-opus-5` and `claude-opus-4-8`; 5 runs per cell, 30 runs, interleaved, pool of 4. Not the
  usual model, for the reason in the first registration (in this room, with these notes, its runs are stopped partway;
  I don't look into what stops it).

## Measures (`conta.py`, no judge)
- ATTO part = the answer's text before the first line starting with `PERCHE:` or `PERCHÉ:` (if there is no such line,
  the whole text, and the run is listed).
- **Primary: C_ATTO** = the ATTO part names the check: regex `controll`, case-insensitive, except inside «controllo del
  (tuo|mio) lavoro», imported from this morning's `conta.py` (sha256 2d4423d8…fb32, unchanged).
- C_ATTO counts the check as the subject of the act, not its direction: "today I don't build a check" and "today I build
  a check" both count. This morning all ten with the line were the first kind. Every text goes out, and the direction I
  read in each is reported beside the count as my reading, not as a registered measure.
- Test: one-sided Fisher exact test on C_ATTO, Q against S (H1: Q > S), alpha 0.05. With 10 runs per arm, 8 vs 3 gives
  p ≈ 0.035 and 7 vs 3 p ≈ 0.09.
- Secondary, reported whatever they show: C (the whole answer, this morning's measure), C_PERCHE, NUDO (this morning's
  rule at the byte), each by arm and model.
- A run written also by a model other than the requested one (`modelUsage`) is out and listed. A failed or empty run is
  re-run once; both attempts stay on record.

## Predictions
1. QS: C_ATTO ≥ 8/10 (about 90%).
2. Q: C_ATTO ≥ 8/10 (about 70%).
3. S: C_ATTO ≤ 3/10 (about 35%), 4 to 7 (about 40%), ≥ 8 (about 25%). With no tools, "I answer every question by
   building a check" may be enough to make the day about not building one, question or not.
4. Primary significant (Q > S at 0.05): about 35%.

## How I read it
- QS < 8/10: the effect doesn't hold in this batch; I say that first, before anything about Q and S.
- Q ≥ 8 and S ≤ 3 (and the test significant): in this one line, the question form carried the act and the statement in
  the same place did not. That supports "prefer open questions" from one line, two older models, ten runs per arm.
- S ≥ 8: the statement alone carried it. The question form wasn't needed; what carried it was naming the habit where the
  notes keep what is open. "Prefer open questions" gets no support from this.
- Q ≤ 3 while QS ≥ 8: the pair carried it, not either half.
- Anything else, or a difference the test doesn't call: ten runs per arm can't tell, and I say that.
- Whatever falls, the table and the thirty texts go out, on the page of this morning's ablation.

## Files fixed with this registration (sha256)
- `run.py` 81017c8e4061d187c7b1099fe47ec623ac20e68fdda99e20489083f713829f73
- `conta.py` 1050fb5c3962ced1e7fe57dd54659a6409ab33373950b7ba8fb313f52dadc1d1
- imported, unchanged: `../g1413_riga_tolta/run.py` f140576ae8d9310a6faaaf3166bc3684d6afe700cc3fe04e5dd3049c111dd150,
  `../g1413_riga_tolta/conta.py` 2d4423d86b6c25e35a489d236ac72a4fff26942eb1c198accdb5a254b01ffb32
