# Minimal active full-target completion of the alternating-C8 OO chart

The complete opposite-shore audit shows that activity cannot be added to
the alternating-C8 two-anchor packet without creating a mixed singleton.
This note crosses the next boundary: it permits new cells on **all** 28
physical pairs and imposes the missing third pure anchor together with the
literal mixed target equations.

## Two new cells cannot reach the full target

There are 241 unoccupied endpoint-colour cells in the packet:

\[
 51\text{ left--left},\qquad136\text{ cross-shore},\qquad
 54\text{ right--right}.                                  \tag{1}
\]

Shore balance in either deleted-arm cofactor requires at least one new
right--right cell.  Among all two-cell supports containing such a cell,
4,815 make both arm cofactors support-nonempty.  Their shore types are

\[
918\ (LL,RR),\qquad2934\ (LR,RR),\qquad963\ (RR,RR).       \tag{2}

Every one fails the literal full target equations.  At this layer the
reason is elementary but important for minimality: two new cells cannot
create the missing pure word `1^8`, so its target residual is the constant
unit `-1`.

## The minimal third-anchor layer

The only old `11` cells are `04` and `24`, and they share vertex 4.  A
pure-1 perfect matching can use at most one of them, hence it requires at
least three new `11` cells.  At exactly three cells there are 30 possible
completions: choose one of `04,24` and a perfect matching on its six-site
complement.  Their shore census is

\[
24\ (LR,LR,RR),\qquad6\ (LL,RR,RR).                       \tag{3}

Nineteen of the 30 make both selected deleted cofactors support-nonempty:
14 of the first shore type and five of the second.  Thus this layer really
reaches the activity divisors missed by the old guard.

Nevertheless every one of the 30 supports has a literal mixed target row
consisting of a single Laurent monomial.  The pure anchor equation is

\[
                              xyz=1,                      \tag{4}

\]

so all three added weights are units.  A mixed row `m(x,y,z)=0` with
`m` a nonzero monomial is therefore impossible over `C`.  The numbers of
such unit rows per support are

\[
\begin{array}{c|rrrrrr}
\#\text{ unit rows}&3&4&5&6&7&8\\ \hline
\#\text{ supports}&1&4&8&5&8&4.
\end{array}                                                \tag{5}

A smallest replayable both-active certificate adds

\[
 (03)_{11}=x,\qquad(15)_{11}=y,\qquad(67)_{11}=z.
\]

Together with the old `(24)_{11}` cell, the pure row gives `xyz=1`, while
the mixed word

\[
                         11001111

\]

has coefficient `yz` and is required to vanish.  Hence `1=0` after torus
localization.

## Scope

This is the smallest source-faithful active/full-nine completion test of
the C8 packet.  It is stronger than a fixed star-rank saturation: the
mixed monomial units exclude every coefficient choice before imposing the
four good-star minors or curvature localization.  The rank-one direct
arms and curvature cell themselves are unchanged.

It does not cover supports with four or more new cells.  Such a support can
add mates for the private mixed rows.  Equivalently, the hard
cross-cofactor branch in

\[
Q_{02}=t z^{[2]},\quad Q_{04}=y z^{[2]},\quad D=A t-B y
\]

first becomes nontrivial beyond this minimal third-anchor layer.  Full-nine
head-column subtraction must control those additional mates or upgrade
slice annihilation `D z^[2]=0` to a genuine cofactor dependence; star
irredundancy alone does not make that upgrade.

## Reproduction

```text
python computations/verify_oo_c8_two_cell_activity_frontier.py
python -O computations/verify_oo_c8_two_cell_activity_frontier.py
python computations/verify_oo_c8_minimal_third_anchor_activity.py
python -O computations/verify_oo_c8_minimal_third_anchor_activity.py
```

Both checkers enumerate physical perfect matchings and retain exact
symbolic variable masks with rational coefficients.  No coefficient grid
or finite-field specialization is used.
