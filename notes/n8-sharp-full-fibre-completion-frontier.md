# The corrected sharp chart-26 full-fibre completion frontier

This note starts from the correction in
`notes/n8-balanced-anchor-chart-cover-frontier.md`: a fixed mixed output word
does **not** restrict physical matching edges to pairs of equal-coloured
vertices.  Every endpoint-coloured aggregate cell

\[
                         A_{uv}(c_u,c_v)
\]

is admissible, including `c_u != c_v`.  The search recorded here therefore
uses all 105 physical perfect matchings in every one of the `3^8` words.  It
does not use the withdrawn diagonal-sector C4/C6 or trinomial claim.

The executable is

```text
computations/search_n8_sharp_full_fibre_completion.py
```

## 1. The exact 16-cell sharp seed

Fix the three pure matchings

```text
colour 0: 01|23|45|67
colour 1: 02|14|36|57
colour 2: 03|15|27|46
```

and adjoin

```text
04;02  15;01  26;02  37;01.
```

This is a 16-cell endpoint-coloured support.  Its pure matching triple is
localization chart 26.  On the word `00002121`, the two complete physical
terms are exactly

```text
01|23|46|57     04|15|26|37.
```

Giving every displayed seed cell weight `+1` except `04;02=-1` cancels this
full fibre and preserves all three pure anchor monomials.  This is the exact
off-diagonal guard which supersedes the former same-colour repair claim.

Full enumeration gives the mixed histogram

\[
                              \{1:11,\ 2:1\}.             \tag{1}
\]

Thus the off-diagonal mate repairs the advertised word but leaves eleven
other singleton obligations.

There is a useful chart-separation check.  The familiar 28-cell diagonal
no-singleton labelling in `notes/monomial-fiber-counterexample.md` has pure
anchor choices only in charts 28--31, with labelled multiplicities

\[
                    \{28:16,29:32,30:16,31:32\}.          \tag{2}
\]

It does not furnish a hidden chart-25 or chart-26 completion.  P5 and the
expanded-prism calculations do lie over chart 26.  D1/D2, by contrast, are
split-residue scalar configurations and are not determined by a pure
matching triple, so assigning the 31 anchor orbits to D1/D2 would be a false
taxonomy.

## 2. Exact all-cell singleton CEGAR

There is one Boolean support variable for every one of the 252 cells
`uv;ab`; the 16 seed variables are fixed.  When a semantic model has one
supported matching `M` in a mixed word `c`, the program adds the implication

\[
 \bigwedge_{e\in M}X_e
 \quad\Longrightarrow\quad
 \bigvee_{N\ne M}\ \bigwedge_{e\in N\setminus M}X_e,     \tag{3}
\]

where `N` runs over all other 104 physical matchings.  At a fixed support
cap, a mate is omitted only if `seed union M union N` already exceeds the
cap.  A requirement is also omitted when it strictly contains another
requirement for the same trigger.  Both reductions preserve the projection
onto support variables exactly.

Consequently every genuine support with mixed fibre sizes `0` or at least
`2` satisfies every learned clause.  `UNSAT` is therefore an exact bounded
obstruction, while `NO_SINGLETON` is independently re-enumerated against all
105 matchings before it is printed.

## 3. First exact bound and current stopping point

The cap-25 replay terminates after four semantic rounds and 98 distinct
singleton gadgets:

```text
UNSAT cap=25 rounds=4 singleton_gadgets=98
```

Hence every no-singleton extension of this corrected 16-cell chart-26 seed
has at least 26 cells: at least ten further endpoint-coloured cells are
necessary before coefficient cancellation is even possible.  This is a
solver-replay theorem; no portable DRUP trace is claimed.

Cap 26 and the global minimum remain open in this checkpoint.  Exploratory
optimization reached substantially larger learned lower layers, but those
interrupted runs are deliberately not frozen as results.  The exact cap-25
replay is the last independently completed boundary.

For every future semantic survivor the program immediately forms all exact
binomial exponent rows.  An odd signed Laurent dependency is already a
characteristic-zero obstruction; the program reports the number of unit
three-row circuits and the first circuit's words.  Only if that guard is
consistent should the larger coefficient ideal be attempted.

The disproof fast path after such a survivor is precise:

1. reduce every three-or-more-term mixed polynomial in the signed Laurent
   quotient of its binomial rows;
2. solve the residual torus scheme over small `F_p`, retaining nonzero pure
   coefficients;
3. compute its local Jacobian **and** a local standard-basis/codimension
   certificate;
4. a smooth `F_p` point then Hensel-lifts to a `Q_p` point and proves that the
   characteristic-zero ideal is proper; recover an algebraic certificate by
   rational-univariate or exact elimination methods.

Jacobian rank by itself is not enough when the displayed equations are
redundant, so step 3 must not be skipped.  No finite-field point is claimed
here because the corrected chart has not yet produced a semantic survivor.
In particular, this checkpoint is neither a counterexample to Krenn's
conjecture nor a proof of the eight-site case.

## 4. Reproduction

The dependency-free semantic/chart audit (apart from the repository's
installed exact search environment) is

```bash
PYTHONPATH=computations .venv/bin/python \
  computations/search_n8_sharp_full_fibre_completion.py --audit-seed
```

The completed exact boundary is the default run:

```bash
PYTHONPATH=computations .venv/bin/python \
  computations/search_n8_sharp_full_fibre_completion.py \
  --cap 25 --solver glucose42
```

Larger caps use the same source-faithful encoding and may be continued
without changing the mathematical projection.
