# N=8 one-bad successor parallel-collision guard

## Verdict

The twelve singleton-successor identities from the orbit-1 one-bad packet
share one exact Laurent form, but they do **not** extend to a unit identity in
the presence of arbitrary extra matching terms.  The valid algebraic lemma is
the following source-provenance statement.  In a consistent Laurent quotient,
if two source rows reduce to

\[
  cM+T=0,\qquad uT=0,
\]

where \(c,u,M\) are units, subtraction leaves the unit \(cM\).  In contrast,
the single equation \(cM+N=0\), with \(N/M\) a new character, is torus
consistent: set \(M=1\) and \(N=-c\).  Thus the parallel homogeneous source
row is load-bearing; an uncontrolled tail cannot simply be ignored.

The exact successor palette is:

- eight three-term reductions with surviving coefficient \(c=1\);
- two six-term reductions with surviving coefficient \(c=2\);
- two six-term reductions with surviving coefficient \(c=-2\).

## First exact contaminant

For the first canonical successor, the top word `000102` reduces to the unit
class \(M\).  Adding `x25_02` activates the matching

```
x03_01 * x14_00 * x25_02
```

which reduces to a distinct positive Laurent class \(N\).  The contaminated
target row is therefore \(M+N\), not a unit.  The original plus-binomial
character lattice has rank 24; adjoining the relation \(N/M=-1\) raises it to
rank 25 and creates no inconsistent character dependency.  A source-faithful
search through every live top/response row on this support finds no row whose
old-quotient reduction is supported only on \(N\).  This matching is the
precise obstruction to the proposed arbitrary-extra-term parallel-collision
lemma.

This is not a coefficient counterexample.  On the actual finite support a
different translated target, top word `002101`, becomes a one-class Laurent
unit (source record 4, coefficient 1).  The packet remains empty by **target
migration**, not by a parallel companion for the original contaminating tail.
A theorem completing this lane must therefore couple several translated
targets globally; another local repair layer would not prove the required
support-independent statement.

## Reproduction and scope

Run:

```bash
uv run python computations/verify_n8_one_bad_successor_parallel_collision_guard.py
python -O computations/verify_n8_one_bad_successor_parallel_collision_guard.py
```

The checker pins the repair-mask theorem by SHA-256, reconstructs all twelve
successor reductions, verifies the abstract cancellation and its two-class
torus countermodel, reconstructs the contaminating source matching, checks the
rank-24-to-25 character extension and absence of bad holonomy or a parallel
\(N\)-row, and verifies the translated-target unit in the full finite source.
Its frozen ledger digest is
`8bb0a7d0d95969de62a1f85002873e66d37932b5ce7650d81bfe9b9ce73a5448`.

The result is a sharp guard, not a new repair census: it proves the conditional
parallel-tail lemma and falsifies its arbitrary-tail strengthening at the first
exact contaminant.  It neither supplies a coefficient point nor rules out a
stronger identity involving multiple translated targets.
