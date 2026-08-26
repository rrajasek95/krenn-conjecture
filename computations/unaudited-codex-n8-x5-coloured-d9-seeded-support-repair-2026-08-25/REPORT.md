# Three coloured X5 D9 seeded support repair

Verdict: **PASS—exact characteristic-zero D9 obstructions for all three
coloured branches**.  Together with the separately sealed direct certificate,
all four canonical X5 branches are now excluded through degree nine.

The seed is not a restart of the historical 15,273-column partial system.  For
each branch, the sealed D8 ±1 dual is transported by one `t`, its exact 18
t-free `C_1` violations are inserted, and the transported values are retained
on free coordinates while the incremental basis repairs pivot coordinates.
Only newly exposed violating columns are then inserted.  The first-prime runs
closed globally with 135/228/60 selected columns and 69/69/63 support in
0.219/0.235/0.131 seconds.  No run approached the 100,000-column, 175-second,
or 8 GiB limits.

The builder's separately retained `postrepair_resume_dual.tsv` controls are
explicitly superseded: an unconstrained 18-equation solve sets all transported
free coordinates to zero and collapses to `t^9` alone.  Production never used
those files; `SEED_SUPERSESSION.json` pins the distinction.

The conditionally triggered second prime independently reproduced the same
selected sets and the same signed ±1 maps.  Exact integer certificates have
support 69 (triangle endpoint), 69 (third colour), and 63 (cap endpoint),
coefficient `+1` on `t^9`, and replay respectively 99, 99, and 90 exhaustive
support-incident literal columns over the integers with zero failures.  Every
other column is support-disjoint.  An independent validator reproduces both
modular reductions and every integer pairing under standard and isolated
Python; optimized assertions fail closed.

Scope: D9 only.  No D10 computation or claim was made.
