# X5 dual degree-recurrence audit

Verdict: there is a new exact D9 obstruction for the **direct** branch, but no
degree-recursive proof for all four branches.  Appending one homogenizing
variable `t=361` to the sealed 38-row D8 direct dual gives a ±1 D9 functional
with `lambda(t^9)=1`; two implementations replay all 46 possibly incident
literal columns over the integers with zero failures.  Every other column is
support-disjoint.  This proves direct-branch characteristic-zero nonmembership
at D9 without a D9 closure or solve.

## Exact extension criterion

For a degree-d functional `lambda`, define `E(lambda)(t*m)=lambda(m)` and set
it to zero on monomials not divisible by `t`.  For a homogeneous generator `g`,
let `C_k(g)` be the sum of terms divisible by `t^k`, divided by `t^k`.  In a
degree `d+n` column write the multiplier as `t^r*q`, with `q` t-free.  If
`r>=n`, the `E^n(lambda)` pairing is an ordinary degree-d ideal pairing.  If
`r<n`, it is exactly `lambda(q*C_(n-r)(g))`.  Therefore the finitely many
degree-compatible contraction equations for `k` up to the generator's
t-valuation are sufficient for all iterated extensions.

The finite criterion fails for every sealed D6-D8 certificate.  For the direct
D8 dual, `C_1` is support-disjoint, which explains the D9 success, but `C_2`
has 58 nonzero pairings and `C_4` has 84; hence this is a one-step proof, not an
induction to all degrees.  Each coloured D8 certificate already fails 18
`C_1` equations across five literal generators.  Concretely, t-valuation-3
carrier rows become t-valuation 4 after extension and meet uncancelled
t-divisible generator layers under t-free multipliers; generator 0 supplies
the first such witness via its `-t^4` term, but is not the only offender.

## Support comparison and bounded D9 diagnosis

Only direct D6→D7 is stable: the D7 certificate is exactly the 10 D6 rows with
one appended `t`.  Direct D7→D8 and every coloured D6→D7/D7→D8 transport keep
only four matching rows and fail literal replay.  At D8 the coloured supports
are instead a common 38-row direct core plus branch-specific 14-row carrier
corrections.

A rational search of the complete span of all distinct D9 transports of the
sealed same-branch and direct D6/D7/D8 certificates finds no normalized
annihilator for any coloured branch.  The fail-closed systems cover 163, 157,
and 151 support-incident columns for triangle-endpoint, third-colour, and
cap-endpoint respectively.  Thus a coloured D9 proof requires genuinely new
support; the incomplete historical D9 CEGAR output is not used as evidence.

Scope: exact direct-branch D9 only.  There is no all-degree or coloured-D9
claim, and no broad D9 computation was launched.
