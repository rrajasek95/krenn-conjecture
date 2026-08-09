# The adjacent-power inventory reaches the cap defect only in the prolonged Hasse cone

Research obstruction and candidate only.  This does not construct the
physical relative generator, prove the curved OO overlap lemma, or prove
Krenn's conjecture.

## Outcome

The target-augmented filtered calculation asks for a source-provenant chain

\[
 d n_c=+\kappa Yw,\qquad
 \operatorname {tgt}(n_c)=\operatorname {ores}(n_c)=0,       \tag{1}
\]

to cancel its defect \(-\kappa Yw\).  The exact inventory of the already
committed adjacent-power candidates has a sharp answer.

* The physical adjacent-power Euler/Bianchi identity of `bcb7ddf` is a
  genuine source identity, but both divided-power brackets vanish.  It has
  zero ordinary boundary and supplies no relative generator.
* The quotient resets of `befda3f` give normalized nonzero values on
  EqSystem **failures**.  On a true source their input equation is zero, so
  they do not define a physical secondary cell.
* The fourth Hasse/Spencer cone of `5d4b8c5` and `3adf375` contains the exact
  positive chain

  \[
       n_I=s_I-T,\qquad
       d(\kappa n_I)=+\kappa Yw,qquad
       (\operatorname {tgt},\operatorname {ores})(\kappa n_I)=(0,0).
                                                               \tag{2}
  \]

  All sixteen Hasse faces are present.  Its top has literal pq-direct and
  pr-two-star sectors, and all fifteen denominator columns have the audited
  support ladder `5,3,3,1`.

Thus (2) is the unique positive item in the present inventory, with the
right sign and chart-sector provenance.  It is not an underived physical
source syzygy.  Diagonal projection gives

\[
 d\bigl(\kappa(r_0-T)\bigr)
   =\kappa(H_0-u)e_{\rm Eq}+\kappa Yw,                  \tag{3}
\]

and the selected fourth operator sends the physical mixed equation (H_m)
to the unit.  Consequently it does not descend to the source quotient.
The missing object is now specific: a source-valid fourth Spencer/Hasse
lift, with every proper face, that cancels the Eq term in (3).  It is not
another same-power connection or another bare Bianchi row.

## The smallest exact physical cokernel

Keep only the two boundary coordinates `(Eq,w)`.  The diagonal image of the
formal candidate and the required boundary are

\[
 v=\bigl(\kappa(H_0-u),\ \kappa Y\bigr),\qquad
 q=\bigl(0,\ \kappa Y\bigr).                            \tag{4}
\]

The integral polynomial covector

\[
             \lambda=\bigl(Y,-(H_0-u)\bigr)             \tag{5}
\]

satisfies

\[
        \lambda(v)=0,\qquad
        \lambda(q)=-\kappa(H_0-u)Y\ne0.                 \tag{6}
\]

At the unit specialization \(\kappa=H_0-u=Y=1\), adjoining (q) raises
the boundary rank from one to two.  An old two-row repair would require

\[
                     bH_m=-\kappa(H_0-u).               \tag{7}
\]

This is impossible in the universal polynomial presentation: killing every
mixed source cell kills (H_m) while retaining the nonzero pure polynomial
(H_0-u).  Equation (7) is the smallest exact cokernel, and the stronger
source-ideal defect is the unit equation
\(\partial_IH_m=1\).  Passing to a scalar fixed-word quotient does not make
that differential operator source-linear.

## Word and provenance scope

The committed Hasse candidate uses the word

```text
01211222
```

whose colour-count partition is `(4,3,1)`.  The nine OO common-triple words
`(a,0,1,ell,2,2,2,2)` split into the following unlabelled
\(S_8\times S_3\) word orbits:

| partition | normalized `(a,ell)` pairs |
|---|---|
| `(4,3,1)` | `(0,0)`, `(1,1)` |
| `(4,2,2)` | `(0,1)`, `(1,0)` |
| `(5,2,1)` | `(0,2)`, `(1,2)`, `(2,0)`, `(2,1)` |
| `(6,1,1)` | `(2,2)` |

Therefore the exact committed formal chain even meets the OO family at the
coarse word-orbit level only for two of the nine normalizations.  Equality
of unlabelled word orbits is not a labelled chart/source map, so it does not
promote (2) physically even in those two cases.  The other seven cases need
either a relabelled physical construction with different colour counts or a
separate argument.

## Consequence and reproduction

The inventory finds the right relative boundary **formally** and proves the
old physical presentation misses it by one exact Eq direction.  This is a
useful stopping datum: the next proof step must construct the source-valid
fourth mixed-row Spencer tower (or an equivalent cross-quotient relative
generator), not extend the same-power Maurer--Cartan calculation.

Run

```text
python3 computations/verify_oo_adjacent_power_relative_generator_inventory.py
python3 -O computations/verify_oo_adjacent_power_relative_generator_inventory.py
```

The checker independently reruns the physical adjacent-power ledger, both
reset packets, all fifteen fourth-Hasse cells, all strict chart-sector
checks, and all fifteen denominator faces.  It then verifies (4)--(7), the
generic rank jump, and the nine-word orbit census.  Frozen ledger digest:

```text
1ea40b149d701b272cea40f57e6271e6d92767d737f7cf39847b4f4d4b0a3534
```
