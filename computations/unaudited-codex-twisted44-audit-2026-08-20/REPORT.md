# Fixed twisted-4+4 full-exactness obstruction (UNAUDITED)

## Verdict

For the fixed W33-D5 twisted-4+4 binary representative displayed below,
there is no fully exact ternary source on eight sites extending it.  The
obstruction has a checkable 21-generator Nullstellensatz certificate over
`Z`; hence the fixed-representative result holds over every field.  A second,
standalone subset-DP engine reconstructs the 21 raw word equations and checks
the certificate identity exactly.

The result transports to every exact binary representative actually related
to this one by target-preserving diagonal site-colour gauge, site permutation,
and the `0 <-> 1` palette swap.  This lane does **not** independently prove the
separate W33 classification claim that every object called a twisted-4+4
source lies in that orbit.  Thus “the entire combinatorial stratum is closed”
still depends on that classification; the fixed representative and its
explicit gauge orbit do not.

Status: **UNAUDITED EXACT CERTIFICATE**, not a certified-spine result.

## 1. Source rebuilt from the definition

On each edge `uv`, cells are endpoint ordered.  The nonzero cells in the fixed
`{0,1}` restriction are exactly

```text
A01[0,0]=A23[0,0]=A45[0,0]=A67[0,0]=1
A03[1,1]=A12[1,1]=A47[1,1]=A56[1,1]=1
A04[0,1]=A05[1,0]=1
A17[0,1]=A34[1,0]=-1.
```

Every one of the other 140 cells having at least one endpoint colour `2` is
an independent variable `x_uvab`.  No W33/W40 code or stored coordinate
reduction is imported.  `audit_twisted44.py` constructs all 105 perfect
matchings twice—by first-vertex recursion and independently as the canonical
quotient of all `8!` vertex permutations—and constructs all 6,561 coefficient
equations by direct matching expansion.  There are 3,774 distinct nonzero
integer polynomials after only exact equality and overall-sign deduplication.

## 2. Positive-through-filter control

The independently rebuilt source reproduces the four-parameter Laurent
family over `Z[s^+-1,t^+-1,a^+-1,b^+-1]`:

```text
A12[0,2]=A24[2,1]=s
A06[0,2]=A67[2,1]=t
A04[2,2]=a
A13[2,2]=b
A26[2,2]=-s*t
A57[2,2]=-1/(a*b*s*t),
```

with every unlisted colour-2 cell zero.  Symbolic raw matching expansion
finds no binary or level-4 failure and precisely these full-exactness
failures:

```text
01110222 :  1/(s*a*b)
12221000 :  s*b
20002111 : -a
```

All three have profile `(3,3,2)`.  At `s=t=a=b=1`, the matching-list engine
and an independent subset-DP hafnian engine agree on all 6,561 amplitudes.
This is the required known-positive object reaching the level-4 check, so the
subsequent full-exactness obstruction is not a vacuous pre-filter result.

## 3. The 21-equation contradiction

Write `x_uvab=A_uv[a,b]`.  Twelve raw coefficient equations give directly

```text
x0120=x0121=x0220=x0221=x0320=x0321=0,
x0420=x0521=x0620=x0621=x0720=x0721=0.
```

The words producing those equations are recorded in `certificate.json`.
The equation for `21110000` is

```text
x0321 - x0520 = 0,
```

so `x0520=0` as well.

Now use the seven raw word equations

```text
22000000, 20210111, 21120000, 20002111,
21110200, 20000021, 21110112.
```

They respectively have a linear term

```text
x0122, -x0222, x0322, -x0422, x0522, -x0622, x0722.
```

Every other monomial in each equation contains one of the thirteen already
vanishing variables.  Hence

```text
x0122=x0222=x0322=x0422=x0522=x0622=x0722=0.
```

Two of the seven indispensable equations, `20002111` and `21110200`, have
profile `(3,3,2)`: this is exactly where the level-4 Laurent family is first
cut.

Finally, every perfect matching contributing to the pure word `22222222`
contains exactly one edge incident with vertex 0.  Its monomial therefore
contains one of the seven variables just shown to vanish.  The pure-2
amplitude is zero, whereas full exactness requires it to equal one.

This proof uses 12 literal-zero equations, one binomial equation, seven
pure-edge equations, and the pure-2 equation: 21 raw source equations total.
It is not a claim of minimality.

## 4. Exact certificate and independent verification

`certificate.json` records explicit integer-polynomial multipliers satisfying

```text
sum_i multiplier_i * (raw coefficient equation for word_i) = 1
```

in the 140-variable polynomial ring over `Z`.  There are 21 nonzero
multipliers and 781 multiplier monomials.  `audit_twisted44.py` verifies this
identity using sparse integer polynomial arithmetic and asserts that a sign
mutation of one selected equation destroys it.

`verify_certificate.py` is a separate checker.  It does not import the
producer: it restates the 12 fixed cells, rebuilds every cited amplitude by a
subset-DP hafnian recurrence, reads only the certificate multipliers, and
rechecks that the sum is exactly `1`.  It also checks that the pure-2
polynomial has one constant and 105 distinct matching monomials, and that the
same sign mutation fires.

As a redundant check, the full 3,774-generator ideal was emitted to Singular
over `integer` and recomputed as the unit ideal.  The runner checks both
stdout and stderr for `?` diagnostics; the final run has return code zero,
no diagnostics, `UNIT=1`, and standard basis `[1]`.  The explicit 21-equation
certificate, rather than this redundant black-box calculation, supports the
verdict.

## 5. Gauge scope

For diagonal site-colour parameters `lambda_(v,c)`, set

```text
(g A)_uv[a,b] = lambda_(u,a) lambda_(v,b) A_uv[a,b].
```

Then for every word `w`, direct matching factorization gives

```text
H_w(g A) = (product_v lambda_(v,w_v)) H_w(A).
```

If both the fixed binary representative and a binary orbit member are
normalized exact sources, the pure `0` and pure `1` equations force
`product_v lambda_(v,0)=product_v lambda_(v,1)=1`.  Extend the inverse binary
gauge to colour `2` with `lambda_(v,2)=1`.  Any exact ternary completion of
the orbit member would then transport to an exact completion of the fixed
representative, contradicting the certificate.  Site permutations and the
binary palette swap transport in the same way.  The runner checks this
amplitude transformation on all 6,561 words for a nontrivial rational torus
element.

This argument covers the explicit diagonal-gauge/permutation orbit.  It does
not establish that dimension equality implies orbit equality, nor does it
cover transformations mixing colours linearly rather than scaling them.

## 6. Reproduction and controls

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -I -S \
  computations/unaudited-codex-twisted44-audit-2026-08-20/audit_twisted44.py \
  --run-singular

PYTHONDONTWRITEBYTECODE=1 python3 -I -S \
  computations/unaudited-codex-twisted44-audit-2026-08-20/verify_certificate.py
```

`results.json` and `verification.json` contain declared-versus-executed
control manifests.  Must-fire controls are:

1. flipping one fixed twisted-source sign fires a binary exactness equation;
2. deleting a Laurent-family cell fires a level-4 equation;
3. changing the sign of one selected raw certificate equation makes the
   integer identity fail, in both producer and independent verifier.

The producer also checks the full symbolic Laurent family, all-word
two-engine agreement, a nontrivial gauge transport, and absence of Singular
identifier shadowing and silent `?` diagnostics.
