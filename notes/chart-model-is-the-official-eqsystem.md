# The chart model is the official formalization at eight vertices

Reference note.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE` is
untouched, and no certified dependency changes.

## 1. Outcome

Every \(h=3\) artifact in this repository works with a **chart**: six residual
sites plus two endpoints, rows indexed by a label pair \((i,j)\) and a
six-letter colour word \(w\), with the direct/star/internal decomposition

\[
 \operatorname{Row}(i,j,w)=d_{ij}\operatorname{haf}_w(q)
  +\sum_{x<y}\bigl[p_i(x,w_x)s_j(y,w_y)+p_i(y,w_y)s_j(x,w_x)\bigr]
   \operatorname{haf}_w\bigl(q|_{W\setminus\{x,y\}}\bigr).
\]

Google DeepMind's `formal-conjectures` states the Krenn–Gu conjecture instead
as `EqSystemN N D W`, a single perfect-matching recursion over all \(N\)
vertices with no chart structure at all.  That is the formalization the
external Lean development proves impossible at \(N=6\); see
[the external certificate note](external-six-site-lean-certificate.md).

> **The two coincide at \(N=8\).**  Proved for **arbitrary weights over any
> commutative ring**: with every weight entry a formal variable, the two sides
> agree as polynomials on all \(6561\) rows.  Additionally checked numerically
> on the committed seven-row guard, the alternating eight-cycle, and three dense
> packets exercising every edge and every colour pair including cross-colour
> internal edges: **zero mismatches**.

So this project's guards are statements about the community-standard object,
and can be quoted as such.

## 2. Why this is not a tautology

The official recursion pairs the head vertex with each later vertex and
recurses, over all eight vertices at once.  It has no notion of a "direct",
"star" or "internal" edge — those are the chart's own bookkeeping, and the
chart evaluator splits the \(105\) perfect matchings of \(K_8\) into the
\(15\) that use the direct edge and the \(90\) that use one star at each
endpoint.  Agreement therefore tests that decomposition, including the factor
of two in the star term and the endpoint-colour conventions, rather than
restating it.

The dense packets are load-bearing rather than decorative: all three
endpoint-colour-convention mutations — swapping the endpoints in the star term,
swapping \(i\) and \(j\) there, and swapping them in the direct term — are
caught **only** by them, the seven-row guard and the eight-cycle missing all
three.

As a second, sharper check, the committed guards' ledgers are reproduced
**from the official system alone**, with the chart evaluator not consulted:

* the seven-row guard fails exactly two of \(6561\), at \(0^8\) and \(1^8\);
* the alternating eight-cycle fails exactly one, at \(2^8\).

Those are the committed ledgers \((00,0^6,-1)\), \((11,1^6,-1)\) and
\((22,2^6,-1)\), re-derived through a different definition.

## 3. What this is for

Three uses, none of them mathematical progress on the conjecture.

1. **Quotability.**  Results here can be stated against the standard
   formalization rather than against a local convention.
2. **A formalization bridge.**  The external work formalized \((6,3)\) in Lean
   over these definitions.  Anything from this project aimed at Lean has to
   cross exactly this correspondence, and it is now checked rather than assumed.
3. **A conventions guard.**  A silent mismatch — a transposed endpoint colour,
   a missing factor of two, a wrong target — would invalidate every \(h=3\)
   artifact at once while leaving each individually self-consistent.  This rules
   that out.

## 4. What this does not say

It is a statement about definitions, not about solutions.  It gives no
information about whether the \((8,3)\) system has a solution, and nothing here
bears on the conjecture in either direction.  The chart decomposition being
correct was never seriously in doubt; the value is that it is now machine-checked
against an external standard rather than internally consistent.

## 5. Audit

The dependency-free checker
[`verify_chart_model_is_official_eqsystem.py`](../computations/verify_chart_model_is_official_eqsystem.py)
transcribes the official recursion from the Lean source; confirms the
**literal** recursion counts \(105=7!!\) perfect matchings on all-ones weights,
and that the extracted matching list has \(105\) distinct entries each
partitioning the eight vertices; checks the extracted list reproduces the
literal recursion on three colourings of a dense packet; compares chart against
official **as polynomials in formal weights** on all \(6561\) rows and
numerically for five packets; and re-derives both committed ledgers from the
official side.

Standard library only, exact `Fraction` arithmetic, about thirteen seconds,
passing normal, `-O` and `-I -S`, deterministic across hash seeds.
