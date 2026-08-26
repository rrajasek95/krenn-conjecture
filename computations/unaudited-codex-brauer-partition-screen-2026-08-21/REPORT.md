# Brauer / partition-algebra matching-map screen

Status: **exact negative screen; no new low-isotypic source identity**.

The 105-dimensional perfect-matching permutation module is the classical
multiplicity-free matching scheme

```text
Ind_(S2 wr S4)^S8(1)
 = [8] + [6,2] + [4,4] + [4,2,2] + [2,2,2,2],
dimensions 1 + 20 + 14 + 56 + 14.
```

The degree-four monomial module is
`P=Q[PM8] tensor Q[{0,1,2}^8]`, of dimension 688,905.  Its hafnian-row
inclusion is exactly

```text
iota(e_w) = (sum_M e_M) tensor e_w.
```

Therefore only the invariant `[8]` matching line occurs in the amplitude
rows.  Its Brauer idempotent returns the original row.  The other four
idempotents annihilate every amplitude row: their 682,344-dimensional total
kernel consists of unconstrained differences between matching monomials,
not additional equations implied by GHZ.

Exact `S8 x S3` character decompositions give 28 irreducible types in the
6,558 mixed-word module and 23 types in the 1,638 even mixed module.  The
six-site 729-word residual module has 19 `S6 x S3` types.  Candidate pair
and cell modules do overlap these rows—`Hom(pair,even)=9` and
`Hom(cell,even)=58`—but every such covariant is only a linear recombination
of existing amplitude rows.  Clean-pair activity is nonlinear response
incidence and is absent from these representations.

Two exact duplication guards make the failure decisive.

1. Distinct physical words have disjoint matching-monomial supports.  Hence
   the raw incidence ranks are exactly 6,561, 6,558, 1,638, and 270 for the
   full, mixed, even-mixed, and master packets; there are no cross-word
   linear circuits.
2. The full `S8 x S3` closure of the 270-row master is all 1,638 even rows,
   because the master meets each of the `620`, `440`, and `422` profiles.
   Thus full-symmetry projection assumes the missing equations rather than
   deriving them.  Under the source-faithful `B4 x S3` stabilizer the master
   has five orbits and the full packet ten, exactly reproducing the frozen
   five-orbit gap.

Likewise, the 729 residual words are already a complete coordinate basis;
partition-algebra projection produces no row outside their span.  The next
operation would have to be a nonlinear response-incidence/reinsertion map
coupling a fixed pair to its six-site residual, not a central idempotent.

No 688,905-column matrix or syzygy search was assembled.  Standard,
optimized, and isolated/no-site modes agree at logical SHA
`6076271abfba697f01fd2ec3719d466aa2b9c5f42eea45b1a0033932143a645a`.

