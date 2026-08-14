# Complete-row common-core projection is controlled by one centered charge

## Verdict

The unconditional recurrent-core projection theorem is false, even after
all tail monomials are inverted and even when the companion component is

```text
finite,
connected,
pair-complete,
flat with even holonomy,
free of singleton companion coordinates,
and placed in one fixed path-independent bistar.
```

The exact obstruction is a **centered transported charge**.  The smallest
simple face-complete guard is a `K2,2` of four complete rows.  Its common
core cannot be projected, its complete-row ideal is not the unit ideal, and
tail saturation does not change either fact.

There is, however, a sharp uniform positive theorem.  In a connected
pair-complete flat companion component, transport the unique alternating
charge `lambda`.  The common core projects source-validly exactly when the
total common-core coefficient of `lambda` is a unit.  After normalizing the
tails over a field, this is simply

\[
                         \sum_v\lambda_v\ne0.          \tag{1}
\]

Exact checker:
[`verify_uniform_recurrent_core_complete_row_projection_boundary.py`](../computations/verify_uniform_recurrent_core_complete_row_projection_boundary.py).

## 1. The projection ideal

Let `R` be a domain and let `C` denote the fixed decorated `C4` core supplied
by the recurrent component of `bcfa7d8`.  Write the complete source rows as

\[
                F_v=t_v C+a_v\qquad(v\in V),          \tag{2}
\]

where `t_v` is the retained tail monomial and `a_v` is the sum of every
other matching occurrence in that complete coefficient row.  Collect the
companion terms in a free quotient `Q` and define

\[
 A:R^V\longrightarrow Q,
 \qquad A(e_v)=a_v,
 \qquad t(\lambda)=\sum_v\lambda_vt_v.                \tag{3}
\]

A row combination `sum lambda_v F_v` equals `C` precisely when

\[
                       A\lambda=0,
 \qquad                t(\lambda)=1.                  \tag{4}
\]

Thus the exact source projection ideal is

\[
                         \mathfrak p=t(\ker A).        \tag{5}
\]

The core projects if and only if `1 in mathfrak p`.  This formulation keeps
the complete companion sums; it does not throw away individual matching
terms or assume binomial rows.

On the nonzero tail chart, divide (2) by `t_v` and put

\[
                     \bar F_v=C+z_v.                  \tag{6}

Then `A` is the matrix with columns `z_v`, and (4) becomes

\[
             \sum_v\lambda_vz_v=0,
 \qquad      \sum_v\lambda_v=1.                      \tag{7}

Equivalently, the affine span of the normalized companions must contain
the origin.  Ordinary `S`-pairs only supply the differences `z_v-z_w`.
They determine the translation space of that affine span, but do not force
the affine origin to lie in it.  That distinction is the complete-row
obstruction.

## 2. Uniform pair-complete theorem

Assume every collected companion coordinate occurs in exactly two rows.
Let `G` be the resulting connected incidence graph.  Allow arbitrary
nonzero weights: for an edge `e=uv`, its coefficient equation in a row
combination is

\[
                 A_{e,u}\lambda_u+A_{e,v}\lambda_v=0. \tag{8}
\]

If transport around every cycle is flat, (8) has a one-dimensional kernel,
spanned by the path-transported charge `lambda`.  Therefore (7) has a
solution if and only if

\[
                            s=\sum_v\lambda_v          \tag{9}
\]

is nonzero.  In that case the literal complete-row projector is

\[
                         C=s^{-1}\sum_v\lambda_v\bar F_v. \tag{10}
\]

No support census or termwise deletion is used.  Every companion coordinate
cancels because of (8), and (9) normalizes the surviving core coefficient.

For unweighted unsigned incidence, `G` is flat exactly on the bipartite
branch, and `lambda` is `+1` on one shore and `-1` on the other.  Formula
(9) becomes

\[
                      s=|V_+|-|V_-|.                  \tag{11}

Hence every connected unbalanced bipartite component projects.  A balanced
component is the sharp residual.

The checker exhausts every labelled connected simple graph on two through
six vertices.  In each bipartite case it verifies incidence corank one and
tests (10) by exact rational rank.  In each centered case it also verifies
that the affine equations `F_v=0,C=1` have a solution.  The first balanced
simple component with minimum degree two occurs at four vertices; its three
labelled realizations are the single isomorphism type `C4=K2,2`.

## 3. The smallest face-complete guard

Use shores `{A0,A1}` and `{B0,B1}` and four internal companion coordinates
`z00,z01,z10,z11`.  The complete normalized rows are

\[
\begin{aligned}
 F_{A0}&=C+z_{00}+z_{01},\\
 F_{A1}&=C+z_{10}+z_{11},\\
 F_{B0}&=C+z_{00}+z_{10},\\
 F_{B1}&=C+z_{01}+z_{11}.                            \tag{12}
\end{aligned}
\]

Every companion occurs in two rows and every row contains two companions.
The incidence matrix has rank three and kernel

\[
                       \lambda=(1,1,-1,-1).           \tag{13}
\]

Its total is zero.  The only complete-row relation is the centered one

\[
                  F_{A0}+F_{A1}-F_{B0}-F_{B1}=0,      \tag{14}
\]

which cancels `C` together with all four companions.  It does not project
`C`.

The failure is certified by the exact rational point

\[
                    C=1,
 \qquad z_{00}=z_{01}=z_{10}=z_{11}=-\tfrac12.        \tag{15}
\]

All four rows in (12) vanish at (15), while `C` remains `1`.  Consequently

```text
C is not in the complete-row ideal,
1 is not in the complete-row ideal,
there is no scalar/Laurent unit contradiction.
```

The same point is the normalized dual detector

\[
                       (1,-\tfrac12,-\tfrac12,
                            -\tfrac12,-\tfrac12),      \tag{16}
\]

which annihilates every complete-row column and takes value one on `C`.

This guard is even and face-complete.  Its incidence graph is a `C4`, so
the alternating transport returns with sign `+1`; there is no odd
holonomy.  No companion coordinate is private.  All four may be assigned
to internal families on the same fixed bistar, so the abstract complete-row
algebra carries no outside-fan label.

There is a smaller two-row algebraic guard,

\[
                         F_0=C+z,
 \qquad                  F_1=C+z,                    \tag{17}
\]

but its one companion has degree one at each row and it is not a primitive
simple face-complete component.  Condition “simple and minimum row degree
two” makes (12) the smallest relevant guard.

## 4. Tail saturation does not help

Before localization, attach independent tail factors and use rows

\[
                           t_vF_v.                    \tag{18}

\]

Colon saturation by `T=product_v t_v` removes the four tail factors and
gives exactly the normalized ideal generated by (12).  Since (15) is a
point of that saturated ideal with `C=1`, even maximal tail saturation does
not project the core.  The obstruction is not a forgotten denominator; it
is the surviving affine companion class.

The tail-saturated `S`-pairs are differences `F_v-F_w`.  Their span has
rank two.  The common affine class of the four companion stars survives
that difference span, which is why a Buchberger calculation based only on
pairwise row differences stops at the same class.

## 5. Topology is not enough

The same physical `K2,2` topology can project.  Give its four incidence
rows weights

```text
edge 02 : (1 at 0, 1 at 2),
edge 03 : (1 at 0, 1 at 3),
edge 12 : (1 at 1, 2 at 2),
edge 13 : (1 at 1, 2 at 3).
```

The flat transported charge is now

\[
                         (1,2,-1,-1),                 \tag{19}
\]

whose total is one.  Formula (10) gives the exact projector

\[
                         F_0+2F_1-F_2-F_3=C.          \tag{20}
\]

Thus neither a common bistar, `K2,2` topology, nor flatness decides the
question.  The load-bearing invariant is evaluation of the transported
charge on the common-core coefficient row.

## 6. Consequence for the recursive primitive-`C4` route

The fixed-tail recurrences of `72974b5`/`bcfa7d8` solve physical placement,
but placement alone does not solve complete-row projection.  The shortest
remaining theorem is now:

> In the first complete companion component attached to either recurrent
> bistar, transport the exact weighted flat charge.  If it is uncentered,
> apply (10).  If transport has odd multiplicative holonomy, take the
> Laurent unit.  If a companion coordinate is private or leaves the anchor
> union, apply the singleton/deletion or active-fan gate.  The sole residual
> is a centered, balanced, entirely internal component such as (12); a
> higher physical boundary must either make its charge uncentered or type a
> terminal companion.

This is stronger and narrower than asking arbitrary companion terms to
project automatically.  The latter statement is refuted by (12)--(16).
The proof effort should target physical exclusion or terminal landing of
the centered balanced component.

## Scope and verification

The `K2,2` guard is an exact complete-row/S-pair algebra over the rationals,
not a full ternary decorated hafnian source.  It refutes an implication from
the stated complete-row incidence hypotheses; it does not refute the Krenn
conjecture or assert that physical hafnian boundary rows realize every
abstract companion module.

Run

```text
python3 computations/verify_uniform_recurrent_core_complete_row_projection_boundary.py
python3 -O computations/verify_uniform_recurrent_core_complete_row_projection_boundary.py
python3 -I -S computations/verify_uniform_recurrent_core_complete_row_projection_boundary.py
```

The checker uses exact rational arithmetic, verifies the projection ideal,
exhausts all connected graphs through six rows, proves minimality of the
face-complete guard, evaluates its saturated ideal at (15), and checks the
weighted uncentered projector (20).
