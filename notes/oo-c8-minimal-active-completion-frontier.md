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

## The complete four-cell layer

The next coefficient-complete census allows one further cell anywhere.
There are 105 pure-1 matching cores: 30 require three new cells and 75
require four.  Completing the former by one arbitrary extra cell and
deduplicating gives 7,200 four-cell supports carrying the missing anchor.
Of these, 5,110 make both arm cofactors support-nonempty.  Their shore types
are

\[
\begin{array}{c|rrrrrr}
\text{type}&LL,LL,RR,RR&LL,LR,LR,RR&LL,LR,RR,RR&LL,RR,RR,RR&
LR,LR,LR,RR&LR,LR,RR,RR\\ \hline
\text{count}&258&744&716&296&2030&1066.
\end{array}                                                \tag{6}

All 5,110 have at least one literal monomial mixed row.  Thus the fourth
cell never supplies enough mates even before Laurent-lattice elimination;
the exact active target remains empty through this layer.

For the proposed leading-cofactor filtration, choose the lexicographically
largest decorated matching term in each arm cofactor.  Their two-coloured
union is an alternating path from `q` to `r` plus even cycles.  Exactly

\[
2955\,[P_2+C_2+C_2],\qquad1853\,[P_4+C_2],\qquad302\,[P_6]
                                                               \tag{7}

occur.  In 5,103 cases a monomial-unit exponent is either one leading
cofactor exponent or their union.  Seven exact supports are counterguards
to that simplest identification: they are still killed by other private
monomial rows, but the chosen leading masks do not directly equal the unit
mask.  Therefore activity is behaving like a leading Koszul boundary on
this chart, while a proof must allow a change of pivot/Čech face rather
than demand one fixed lex-leading boundary.  The seven exceptions have a
particularly small common form: three added cells are the pure-1 matching
completion and the sole exceptional cell is `(34)_(0,1)`.  That cell's
own exponent is a private monomial unit in every case.  Hence the finite
alternate rule is explicit: if neither cofactor leader nor their union is
a pivot, pivot on the unique non-anchor `34:01` cell.

At the five-cell layer this becomes stronger.  For every one of the 7,200
four-cell parents, at least one private mixed word has **no possible
one-cell mate anywhere among the 241 source coordinates**.  The terminal
row count per parent ranges from two to eleven.  It follows without
enumerating all five-cell supports that no fifth cell can remove every
inherited monomial unit.  Thus the exact active/full-target chart is empty
through five added cells.  For the 5,110 both-active parents this terminal
statement holds in each of the three cofactor-union types in (7).

The audit does not cover supports with five or more new cells.  Such a
support can finally add several mates for the private mixed rows.
Equivalently, the hard
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
python computations/verify_oo_c8_four_cell_activity_frontier.py
python -O computations/verify_oo_c8_four_cell_activity_frontier.py
python computations/verify_oo_c8_five_cell_activity_frontier.py
python -O computations/verify_oo_c8_five_cell_activity_frontier.py
```

The checkers enumerate physical perfect matchings and retain exact
symbolic variable masks with rational coefficients.  No coefficient grid
or finite-field specialization is used.
