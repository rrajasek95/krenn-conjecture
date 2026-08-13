# The full Hasse shadow of `J_D` is exact, but its physical proper faces and uniform lift remain

## Outcome

The six tau-plus pure columns have a stronger common structure than the
coarse `(private,Eq,Q_tail)` model shows.  They are six distinct three-edge
multiplier monomials `P_i` times the same literal 90-term pure full-nine row
`H_0`.  Therefore

\[
 \sum_iD_iB_i=P_DH_0,
 \qquad
 P_D=\sum_iD_iP_i,
 \qquad
 D=(-1,2,-1,-1,2,-1).                         \tag{1}
\]

Although `sum(D)=0`, the six `P_i` are distinct.  Hence `P_D` is a nonzero
six-monomial polynomial, and (1) has 540 distinct literal features.  The
cofactor/Hasse contraction has exactly the wanted formal shadow

\[
                       P_DH_0\longmapsto P_D,           \tag{2}
\]

while the endpoint Bianchi aggregate supplies the corresponding bare
`Q_tail` polynomial.  Thus the proposed relative mapping cone has formal
row signature

```text
J_D = (pure D, Eq 0, Q_tail -D).
```

This still does not construct a physical source cell.  A complete
seven-occurrence cobar top has `2^7-2=126` ordered nontrivial faces.  The two
orientations of the displayed `P_i|H_0` split account for only two.  The
committed totalization identifies the first uncancelled physical packet:
residual word `012112`, no selected midpoint landing, ridge rank six, and
primitive Omega rank five.  Since these word coordinates are free over the
six distinct `P_i`, taking the `D` aggregate leaves coefficient `P_D`; the
augmentation-zero scalar identity does not cancel the word face.

The executable audit is
[`verify_h3_jd_hasse_bianchi_totalization_uniform_spectator_gate.py`](../computations/verify_h3_jd_hasse_bianchi_totalization_uniform_spectator_gate.py).

## The sharp local construction target

The old full-nine/Hasse/Bianchi inventory therefore reaches the formal
mapping-cone shadow but stops at one physical total cell:

> Construct one rho-even, source-labelled `J_D` in the actual tau-plus
> word/fine/repeated grade, totalizing its remaining Hasse sectors into
> physical word-change and ridge/Omega caps, with
> `target=ainc=W=ores=wrong-word=ridge=0`.

This is not a search for four unrelated loop bars.  The abstract rank-four
loop-label kernel has already collapsed to one selected rho-even line.  It
is also not enough to declare only the 540-feature top: the nondegenerate
bar necessarily retains its proper faces.

## What happens to `chi_D`

On the committed `h=3` totalization, extend

\[
       \chi_D=\sum_iD_i(\operatorname{private}_i-operatorname{Eq}_i)
                                                               \tag{3}
\]

by zero on `Q_tail`, word-change, and ridge/Omega rows.  Complete rows still
have type `(x,x,0)`, endpoint bars have type `(0,0,q)`, and the proper-face
caps live in the added face summands.  Hence the extension kills the whole
committed block and reads

\[
                              \chi_D(J_D)=12.           \tag{4}
\]

So `chi_D` remains a primitive **bounded h=3 codomain separator** after the
full Hasse/Bianchi attempt.  It is not presently a physical terminal or
Macaulay functional.  That stronger conclusion would require an exhaustive
comparison with the actual source-terminal quotient, annihilation of every
higher Macaulay multiplier, and a physical domain `q`/Fredholm promotion.
The zero extension over known proper faces supplies none of these.

## `P_f` and `J_D` are two cells in one theorem

The pointed conormal and excess bridge are independent associated-graded
directions:

```text
P_f : degree-one Koszul generator of the degree-zero relation u_f-u,
J_D : the next oriented-diagonal/common-tail comparison cell.
```

Thus neither one homogeneous cell nor a linear combination can replace the
other.  This is a statement about the domain resolution, not a split into
two conjecture-level assumptions.  The target remains one pointed,
`k[beta]`-linear, rho-equivariant comparison theorem `Phi_beta` whose source
resolution contains both generators and their common `d^2`/coherence laws.

## Why the result is still only `h=3`

Let `T=q^[h-3]` be a matching tail on disjoint spectator sites.  At the
static polynomial-boundary level, multiplication is injective:

\[
       T\,dJ_D
       =(T P_D)H_0-(T P_D),                            \tag{5}
\]

and word, fine, and repeated grades all acquire the same additive spectator
degree.  Zero protected rows remain zero at this level.

This is only a fixed-word-sector statement.  It does not preserve the full
GHZ target: tensoring the eight-site GHZ vector with independent spectator
pair colours creates off-target word sectors.  The committed spectator
no-go already rules out that stronger bare factorization.

But site suspension is not a chain map in the Hasse/PP complex.  The product
rule gives

\[
          d(TJ_D)=T\,dJ_D+(dT)J_D.                    \tag{6}
\]

The second term is already nonzero at `h=4`, where `T` is one spectator
edge and its first Hasse derivative is one.  For general `q^[h-3]`, every
selected spectator edge leaves the matching polynomial on the remaining
sites, so the extra faces persist.

A complete monoidal Eilenberg--Zilber/shuffle comparison would totalize the
`dT` faces canonically.  Such a structure has not been descended to the
literal physical relative source complexes.  Moreover, a fixed
`T`-divisible sector does not exhaust the intrinsic order-`h` Macaulay
block: cross-tail columns can pair nontrivially with a covector extended by
zero outside that sector.  The arbitrary-tail residue and labelled Kähler
ridge audits also explicitly fail without invariant normalized tails and
transported labels.

Consequently even a future physical `h=3` construction of `J_D` would not
by itself prove `PAComp(h)`.  The uniform theorem must add:

1. a monoidal physical comparison that totalizes every spectator Hasse
   face;
2. covariant word/fine/repeated and ridge labels under that product; and
3. descent to the full source-provenant terminal/Macaulay quotient.

## Verification

Run:

```text
python3 computations/verify_h3_jd_hasse_bianchi_totalization_uniform_spectator_gate.py
python3 -O computations/verify_h3_jd_hasse_bianchi_totalization_uniform_spectator_gate.py
python3 -I -S computations/verify_h3_jd_hasse_bianchi_totalization_uniform_spectator_gate.py
```

The checker prints its frozen ledger SHA-256.

```text
91e579e9a7f9230b896460cda606af25bafef64dc5b74506062663ca238ab8c8
```
