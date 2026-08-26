# Three-copy alternating invariant versus the 31 matching geometries

## Terminal result

The rank-respecting rainbow refinement eliminates **none** of the 31
`S8 x S3` matching-triple geometries.  For every representative
`(M0,M1,M2)`, the exact diagonal construction

`A_e = diag(1[e in M0], 1[e in M1], 1[e in M2])`

has rank equal to the multiplicity of `e`, has local factor vectors
`e0,e1,e2` at every vertex, and gives a nonzero selected alternating
contribution `Phi`.  The 31 values of `Phi` range from 1 to 1296; the exact
ledger digest is

`0987c5f409fb1e1d98ee446910ce89b69ce64e8f71e72914e1ffd9ac8c11c0c0`.

This construction is a countermodel to excluding a matching geometry from
the strengthened *local consequence*.  It is not a counterexample to the
conjecture: in each of the 31 sparse diagonal constructions every supported
mixed term is a singleton, so the output is not GHZ.

## Finite census

- 23 orbits use a repeated physical edge; the displayed block gives every
  required 2x2 or 3x3 minor equal to one.  Eight are pairwise edge-disjoint.
- 19 orbits have a fourth physical perfect matching in the simple union;
  12 do not.  All eight edge-disjoint orbits do have a fourth matching.
- Every one of the 31 bare diagonal supports has mixed singleton words (from
  2 through 78 depending on the orbit), and in fact every supported mixed
  term is a singleton.
- These singleton statements are confined to the selected twelve cells.
  An unrestricted source completion can add other perfect-matching terms to
  the same word, so none is a full-source singleton contradiction.
- No orbit forces a literal support6, support8, or clean-cap signature.  The
  matching condition is open/nonvanishing, whereas the frozen mate units
  require complete `(X,C,Q,H)` zero/nonzero signatures (of sizes `12/4/6`
  and `18/8/8` in the two audited controls).

## SAT audit

The earlier 31-branch SAT abstraction did **not** encode the new condition.
It has Boolean variables for cell presence and forces the selected `(c,c)`
cells.  It has neither coefficient values nor determinant variables, so it
cannot assert local factor independence or repeated-edge rank.  Nonzero
selected diagonal entries alone do not make the corresponding minor nonzero
when off-diagonal entries are allowed.  Also, the alternating witness triple
need not be the independently chosen pure-diagonal triple.

Thus the missing step is a source-faithful localization theorem tying the
decorated alternating witness to a complete coefficient fibre or a literal
`(X,C,Q,H)` signature.  Cycle switches and rank minors alone do not supply
that localization.

## Replay

Run `audit_three_copy_matching_orbits.py` in standard, `-O`, and `-I -S`
modes.  The checker reconstructs all 31 representatives, their labelled
orbit-size sum `105^3`, exact rank witnesses, determinant-term sums, physical
matchings, and coloured fibres.  Three hostile mutations—dropping an orbit,
promoting a local singleton to a global contradiction, and falsely crediting
SAT with determinant clauses—must all fail.
