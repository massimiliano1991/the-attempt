# Amendment 2 — written before any judge ran

Vera (DIADE), 2026-09-30. The design (`PREREGISTRATION.md`, sha256 `638cf0b7…2224`) went out at 09:56:50Z, and Amendment 1 (`AMENDMENT_1.md`, sha256 `7c3969cb…45f7`) followed in the same thread before any new rewrite ran. Under Amendment 1 the Opus hand finished and the Sonnet hand finished its first pass. At 10:48:25Z I stopped the Sonnet retry pass before any of its sessions had replied. This file comes after that, before any lot was built and before any judge read anything. That order is from my records and can't be redone from outside. What anyone can check is that this file's sha256 goes out in the thread before the results do.

## What the Amendment 1 run showed

Every rewrite and every judgment in this study comes from a `claude -p` session in Claude Code. Claude Code caps each reply at 32,000 output tokens unless told otherwise, and thinking counts toward the cap. When a reply hits the cap, the harness writes to the model "Output token limit hit. Resume directly — no apology, no recap of what you were doing… Break remaining work into smaller pieces.", and `claude -p` returns only the last message. The design did not account for it. The counts below come from the sessions' own records, which Claude Code keeps on this machine (a copy of the summary is in `emendata1/sessioni.json`). They are from my records and can't be redone from outside:

    $ python3 emenda2_conta.py
    output limit per reply in Claude Code when not set: 32000 tokens, thinking included
    amendment-1 run, opus hand, first pass: 10 sessions; largest reply 17693 tokens; sessions that hit the limit: 0
       retry pass: 2 sessions; largest reply 20771 tokens; hit the limit: 0
    amendment-1 run, sonnet hand, first pass: 10 sessions; largest reply 32000 tokens; sessions that hit the limit: 5
       after the cut, 3 sessions returned all their 19 texts nearly unchanged: copied share 0.91 to 1.00
       and 2 returned only the end of the rewrite: 7 of their 12 texts missing
       sessions not cut: 5, with 31 texts; copied share median 0.48; passed the check 8
       retry pass: 9 sessions, stopped by me before any of them replied
    the original study, J1 (claude-sonnet-4-6): 9 sessions; hit the limit: 1; largest replies 26701, 28718, 29108, 32000
    the original study, J2 and J3 (claude-opus-5-5): 11 sessions; hit the limit: 0; largest replies 5176, 5224, 6917, 7549
       the J1 session that hit the limit judged lotto_06: 13 texts, 1 of them mine; J1 and J2 gave a different class to 0 of the 13

In five of the ten first-pass Sonnet sessions, the model used the whole 32,000 tokens thinking before or while writing. What came back was written after the cut, under the harness's instruction and without the model's own reasoning. In three sessions it was the input file with a few words changed. That isn't the Sonnet hand following my instruction. It's the channel. The design already said that a session which returns nothing is not an attempt. A session cut off by the limit is the same failure, and I hadn't foreseen it.

The same limit was there in the study this one checks. One Sonnet judge session (J1, `lotto_06`) hit it, so its 13 judgments were written after the cut. That lot holds one of my 31 texts, and J1 and J2 agree on all 13 of its texts. The 8-to-0 did not come from there. I'll say so with the results.

## What changes

- Every model session in this study, both rewriting hands and all three judges, runs with the output limit raised (`CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000`, set in `canale.py`). All three models accepted it in a one-line test session.
- The output of each session is read as JSON (`--output-format json`), to get the session's id and open its record. This changes nothing the model sees.
- A session in which any reply hits the limit, according to its own record, counts as a session that returned nothing. It is not an attempt and is run again. For the rewrites this is the registered rule for empty sessions, with the same bound (three passes). For the judges, a cut session is run again, up to three sessions in all. The registered single rerun of a lot whose output doesn't parse or lacks a judgment stays as it was. What a cut session wrote is kept on file and never used.
- Both hands are rewritten again from scratch, first pass and retry. The Opus hand never came near the limit, but the two hands should go through the same channel, and nothing from the earlier runs is reused. The Amendment 1 run is kept in `emendata1/`.

## What I saw and am not changing

In the Sonnet sessions that were not cut, the median copied share was 0.48, above the registered threshold (`SOGLIA_COPIA = 0.35` in `conserva.py`), and 8 of their 31 texts passed. That is the Sonnet hand as it is. The prompt, the threshold, the single retry and the exclusion rule stay as registered and amended. If the Sonnet hand fails the check more often than the Opus hand, more texts are excluded. I'll report how many, from which group, and the power of the primary test at the number of texts that remain.

Everything else stays as registered and as Amendment 1 left it.

## Files (sha256)

- `parafrasi.py` f7d25d412c43e96e5d70d9b4ef8d5e8b16f236c092399b75133814bb0427f0d1
- `giudica.py` 8512a8c452a3449dd85f772d70811961b84436bb17dbd94b09fb5b84b1da245e
- `canale.py` fc9160c576b8a16324b84ce9189705162b2f99582172a9f3728391a6d39debf8
- `emenda2_conta.py` 00d231262fd9bc8438ce770187688b8920c4c75fb496789ae7ec282365ff4b98
- `emendata1/parafrasi_emendamento1.py` 1624a38e3553d1a7d06fac3980dec6768aa554aa9b25911bed884c8fc0142554 (the Amendment 1 `parafrasi.py`)
- `emendata1/giudica_emendamento1.py` 566e84e9faf599c7aaa2ba3cfb849fa942a65f587ab07eb98df963fe5928392c (the registered `giudica.py`)
- `conserva.py`, `lotti.py`, `analisi.py` and the rest unchanged from Amendment 1 and the registered design.
