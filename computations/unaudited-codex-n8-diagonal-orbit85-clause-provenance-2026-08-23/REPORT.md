# Orbit-85 literal clause-provenance audit

## Verdict

All certified orbit-85 clause families admit uniform, characteristic-free
polynomial compilation on the exact constructible branch, while retaining the
Boolean selectors and hafnian inverses. There is no intrinsic clause-
provenance gap inside this branch. Combining these identities with the
RUP-to-PC DAG from the preceding audit yields mechanically a unit certificate
in an extended orbit-85 source ring.

The certified package did not freeze the constructible branch as an algebraic
interface. The first missing payload is at C0: seven outside-free star
positions require 224 generalized Rabinowitsch witnesses and seven equations
of the form sum_j r_j P_j - 1. Once these exact complement witnesses are
added, every clause family compiles. Selector elimination and gluing the 87
orbit branches are deliberately not attempted here.

## Conventions

For each literal hafnian h, write

    Z_h = (1-p_h)h,
    R_h = p_h(h u_h - 1),
    B_h = p_h^2-p_h.

These are respectively the zero-side link, guarded inverse link, and Boolean
axiom. A positive literal p has falsity factor 1-p; a negative literal not-p
has falsity factor p. All identities below have integral coefficients and
remain valid in characteristic two.

## First nontrivial literal certificate: A2

The first orbit-85 A2 clause is certified CNF row 11,791, with partition masks
(0,252,3) and literals (-3644,-3733). Put

    h = haf_1({2,3,4,5,6,7}),   p = p_(1,252),
    k = haf_2({0,1}),           q = p_(2,3),
    F = h*k,
    R_p = p(h*u-1),             R_q = q(k*v-1).

The source mixed-amplitude row is F=0, and the clause polynomial is pq. The
explicit localized identity is

    pq = (p*q*u*v) F - q R_p - (p*h*u) R_q.                 (A2)

The checker expands this identity over Z exactly. The same telescoping formula
handles every two- or three-factor A2 row and every FR row once its branch
product equation is present.

## Laplace clauses A3/A3g

Use the conservative definitional extension

    G_i = g_i - a_i*b_i,

where a_i,b_i select the two factors of the ith Laplace term h_i*k_i. Every
source point has this canonical g lift. The two small clauses compile as

    g_i(1-a_i) = (1-a_i)G_i - b_i B_(a_i),
    g_i(1-b_i) = (1-b_i)G_i - a_i B_(b_i).                  (A3g)

For the big clause put Q=product_i(1-g_i), Q_i=Q/(1-g_i), and K=p_H Q.
Laplace gives E=H-sum_i h_i k_i=0, and

    (1-g_i)h_i k_i
      = k_i Z_(h_i) + a_i h_i Z_(k_i) - h_i k_i G_i.

Consequently, with R_H=p_H(Hu_H-1),

    K = u_H p_H [Q E
          + sum_i Q_i(k_i Z_(h_i)+a_i h_i Z_(k_i)-h_i k_i G_i)]
        - Q R_H.                                             (A3)

The checker expands this for all actual arities 3, 5, and 7. Thus the CNF's
Laplace auxiliaries are not a provenance gap; they need 5,208 quadratic
definitions G_i.

## Case clauses and exact branch interface

Orbit 85 has free-set triple

    F_0={0,3,4,5}, F_1={1,3,4,5,6}, F_2={2,3,4,5,6}.

There are 14 inside-free positions and seven outside-free positions.

For each inside position, its 32 defining residual products P_j vanish. These
are the 448 FR branch equations. Their selector clauses compile by the A2
telescoping identity.

For an outside position, exact nonmembership in the free set means its 32
residual products are not all zero. Introduce witnesses r_j and the one
generalized Rabinowitsch equation

    L = sum_j r_j P_j - 1 = 0.

The mixed source rows are A_j=x P_j=0, where x is the corresponding star
entry. Then

    x = sum_j r_j A_j - x L.

Thus x=0, and its negative selector clause follows from
p_x = p_x u_x x - R_x. This compiles every C0 clause without selecting a
particular nonzero residual product. The seven sites require exactly
7*32=224 new witnesses.

The Cnz, Ch, and pure A1 positive unit clauses use their already present
hafnian inverse as an unguarded branch/open localizer L_h=h u_h-1:

    1-p_h = u_h Z_h - (1-p_h)L_h.

A0 is simply Z_empty=1-p_empty because the empty hafnian is one.

## Excess-free biconditional XF

After the derived C0 star zeros, literal Laplace reduces to E=H-xh=0, with the
witness star x live through rx-1=0. If a,b select h,H respectively, then both
falsity polynomials have explicit identities:

    a(1-b)
     = a u r Z_H - (1-b)R_h
       - a(1-b)u h(rx-1) - a(1-b)u r E,

    (1-a)b
     = b v x Z_h - (1-a)R_H + (1-a)b v E.

The checker expands both. This guards the load-bearing fact that the reverse
implication uses the true nonzero witness star.

## Size of the composable branch system

Before substituting the 13,905 derived clause equations into the Boolean PC
DAG, a direct orbit-85 antecedent packet can be taken to have:

| packet | equations |
|---|---:|
| mixed diagonal amplitude rows | 1,638 |
| Boolean selector/witness axioms | 5,592 |
| selector-hafnian links | 768 |
| g=a*b definitions | 5,208 |
| inside-free product equations | 448 |
| outside-free complement localizers | 7 |
| pure and selected-witness open localizers | 9 |
| total | 13,670 |

It uses 6,284 variables: the previous 6,060-variable selector/Rabinowitsch
ring plus 224 complement witnesses. The maximum antecedent degree is six; the
expanded input has 39,949 monomial occurrences. These are interface counts,
not a claim that fully composed static multipliers remain compact.

## Remaining work

The formulas above are a source-labelled compiler for every clause family,
and the prior audit gives the RUP/PC DAG. Emitting their composition is now
bookkeeping rather than solving. The genuinely later steps are eliminating
the selectors/inverses and algebraically gluing the constructible case/orbit
cover; neither is claimed here.

Replay:

    python3 computations/unaudited-codex-n8-diagonal-orbit85-clause-provenance-2026-08-23/check_provenance.py
    python3 -O computations/unaudited-codex-n8-diagonal-orbit85-clause-provenance-2026-08-23/check_provenance.py
    python3 -I -S computations/unaudited-codex-n8-diagonal-orbit85-clause-provenance-2026-08-23/check_provenance.py
