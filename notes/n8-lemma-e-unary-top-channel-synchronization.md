# The one-bad response channels have one silent two-centre topology

## Outcome

In the normalized one-bad packet, choose one nonzero matching summand from
each of the two required diagonal rows

\[
 p_1s_1Q^{[2]}=X_1,\qquad p_2s_2Q^{[2]}=X_2.          \tag{1}
\]

Each summand consists of an ordered pair of holes, occupied respectively by
the `p`- and `s`-star, and a monochromatic near-perfect matching on the other
four sites.  Suppose the two ordered hole pairs are disjoint.  There are
exactly 3,240 labelled pairs of such channels.  They have the exhaustive
classification

| channel type | union graph | count |
|---|---|---:|
| two mixed top matchings | `3 K2` | 360 |
| one mixed top matching | `P4 + P2` | 1,440 |
| both off-diagonal response cofactors visible | `P3 + P3` | 720 |
| silent two-centre packet | `P3 + P3` | 720 |

Thus 2,520 of the 3,240 selected cores already occur in a forbidden mixed
top coefficient or in one of the two zero rows

\[
 p_1s_2Q^{[2]}=p_2s_1Q^{[2]}=0.                       \tag{2}
\]

The remaining 720 are not a missed support case.  They are one precise
topology: two disjoint length-two paths.  Their two mixed two-edge products
miss the same-endpoint hole pairs `{p1,p2}` and `{s1,s2}`, rather than either
off-diagonal `p-s` pair.  This is the unique principal-channel configuration
invisible to both (2) and the mixed part of `Q^[3]`.

This is a support-free classification of *selected response channels*, but
not an aggregate noncancellation theorem.  In a full source, a visible core
term can be cancelled by additional matching terms in the same coefficient.
The result therefore isolates the site-synchronization gate; it does not by
itself exclude the one-bad packet.

## Exact channel classification

Write the ordered hole pairs as

\[
 P_1=(u_1,v_1),\qquad P_2=(u_2,v_2),                   \tag{3}
\]

where `u_i` is occupied by `p_i` and `v_i` by `s_i`.  Let `M_i` be the
selected two-edge colour-`i` matching on the complement of `P_i`.  For
disjoint `P1,P2`, the graph `M1 union M2` has only three possible component
types.

1. `3 K2`: it has two decorated mixed perfect matchings, in two different
   mixed output words.
2. `P4 + P2`: it has one decorated mixed perfect matching.
3. `P3 + P3`: it has no perfect matching.  Its two disjoint cross-colour
   edge products have two possible orientation patterns.  In one pattern
   they miss exactly `{u1,v2}` and `{u2,v1}`, giving one core term in each
   off-diagonal zero row.  In the other they miss exactly `{u1,u2}` and
   `{v1,v2}`.  Only this second, same-endpoint pattern is silent.

No coefficient division or cancellation assumption enters this
classification.  It is a finite statement about two literal matching
summands already known to be nonzero because they occur in the two diagonal
pure coefficients.  Its exact consequence for a full packet is a
dichotomy:

> every disjoint selected pair either pays an additional same-word
> cancellation in a mixed top/off-diagonal fibre, or has the silent
> two-centre `P3+P3` incidence.

The first branch is cancellation-rich; the second is synchronized at two
physical centres but is not yet a source descent.

## A literal silent common-cofactor model

The silent topology is algebraically real before the unary top equation is
imposed.  On sites `0,...,5`, take ordered holes

```text
(p1,s1) = (0,1),       (p2,s2) = (2,3)
```

and put

```text
Q = 24:11 + 35:11 + 05:22 + 14:22,
p1 = e1 at 0,   s1 = e1 at 1,
p2 = e2 at 2,   s2 = e2 at 3,
p0 = s0 = 0.
```

The colour-one and colour-two edge families form the paths

```text
2--4--1       and       3--5--0.
```

Literal perfect-matching expansion gives

\[
 p_is_jQ^{[2]}=\delta_{ij}X_i\quad(i,j=0,1,2),          \tag{4}
\]

where only the `11` and `22` rows are nonzero, while

\[
                         Q^{[3]}=0.                     \tag{5}
\]

The nonzero dependent-line sites of `(p1,p2)` are distinct lines `e1` at
site 0 and `e2` at site 2; those of `(s1,s2)` are `e1` at site 1 and `e2`
at site 3.  Hence the exact common `Q^[2]` provenance and all nine response
rows do **not** force the two colour channels to share a star hole, even in
the strongest coordinate-spoke specialization.

Let

\[
 D=(01{:}11)+(23{:}22).                                  \tag{6}
\]

Then the same literal expansion gives

\[
                         (Q+D)^{[3]}=X_1+X_2.            \tag{7}

The missing datum is exactly the unary top `Q^[3]=X0`.  Adding any one of
the fifteen three-cell all-zero perfect matchings to this sparse core creates
at least one mixed word in `(Q+D)^[3]`; the exact numbers of completions
with `1,2,3,5,6` distinct mixed words are respectively `3,6,1,3,2`.
Therefore even the silent core cannot be completed by simply adjoining a
pure-zero factor.  Extra same-word cancellation is unavoidable.

This model is not a Krenn counterexample: (5), not `Q^[3]=X0`, is its top
equation.  It is a sharp counterguard to any proof which tries to derive
site intersection from the nine response rows and `Q^[2]` provenance alone.

## Remaining theorem

The support-free one-bad packet still needs an aggregate version of the
channel dichotomy:

> **Two-centre cancellation/descent lemma (open).**  Under
> `Q^[3]=X0` and all nine rows, either the visible channel terms cannot all
> cancel, or the silent `P3+P3` channels assemble into an anchor-preserving
> two-centre source modification.

The singular-spoke line-hitting theorem in
[`n8-lemma-e-unary-top-translated-faces.md`](n8-lemma-e-unary-top-translated-faces.md)
does not identify its line sites with the holes of a chosen diagonal
matching summand.  That identification is an additional missing step and
must not be inferred termwise.

## Reproduction and scope

Run

```text
.venv/bin/python computations/verify_n8_lemma_e_unary_top_channel_synchronization.py
.venv/bin/python -O computations/verify_n8_lemma_e_unary_top_channel_synchronization.py
```

The checker enumerates all 3,240 ordered disjoint channel pairs, verifies the
four topology counts and the same-side form of every silent cross cofactor,
then expands the rational model and all fifteen pure-zero completions in the
literal site-square-zero algebra.  It reproduces ledger

```text
27738a4135c5507a9fee355ea2d0772cc4e8720b210611e76d541d8fd7b15642
```

It proves the selected-channel classification and the exact common-`Q^[2]`
counterguard.  It does not prove aggregate noncancellation, identify every
line-hitting singular spoke with a response hole, construct an exact source,
or settle Krenn's conjecture at `N=8`.
