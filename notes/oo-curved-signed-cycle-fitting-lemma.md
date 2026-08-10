# The curved OO critical Fitting class is a signed cycle invariant

## Outcome

The smallest critical source component suggested by `b942209` has a closed
uniform formula.  For a cyclic two-class module

\[
              f_i=u_iX_i+v_iX_{i+1},\qquad i\in\mathbb Z/\ell,
                                                               \tag{1}
\]

its coefficient matrix has determinant

\[
 \boxed{
       \det M=\prod_i u_i+(-1)^{\ell-1}\prod_i v_i.
 }                                                             \tag{2}
\]

When the matching exponent circuit closes,

\[
                         \prod_i u_i=\prod_i v_i=:K,           \tag{3}
\]

and all active cells are nonzero, (2) gives

\[
 \det M=
 \begin{cases}
  2K,&\ell\text{ odd},\\
  0,&\ell\text{ even}.
 \end{cases}                                                   \tag{4}
\]

Thus nonvanishing of the odd hafnian triangle is automatic.  It does not
need curvature, goodness, activity, generic coefficients, or a chosen term
order once the source-labelled odd circuit exists.

The negative half is equally sharp: curvature, four good stars, both active
cofactors, and ruling alignment do **not** force the parity or character of
the critical component.  The very same 177-cell packet contains both

- the three-word off-diagonal triangle with Fitting determinant (2K); and
- a parallel two-word component with identical Laurent ratio and Fitting
  determinant zero.

Therefore the proof-completing global lemma cannot be “curvature makes the
Fitting class nonzero.”  It must prove that, after private/unit pivots, every
reachable critical SCC contains an odd cycle or a nontrivial coefficient
character.  This is a global source-circuit statement, not a local OO rank
statement.

The dense-Segre cancellation theorem of `e3c52ae` does not supply the
missing nonzero minor.  Exact cancellation of a recombination cube forces
the aggregate mate sums to have rank one, so **all** of their flattening
minors vanish.  The nonzero invariant must therefore be signed holonomy
between several source rows, as in the odd triangle, rather than a local
minor of one mate-sum cube.

## 1. Uniform signed-cycle determinant

Order the columns by (X_0,\ldots,X_{\ell-1}).  The matrix in (1) has (u_i)
on the diagonal and (v_i) on the cyclic superdiagonal.  Exactly two
permutations contribute to its determinant: the identity and the cyclic
shift.  Their signs give (2).

More generally, if the literal source coefficients are
(\alpha_i u_i,\beta_i v_i), then

\[
 \det M=K\left(\prod_i\alpha_i
      +(-1)^{\ell-1}\prod_i\beta_i\right).             \tag{5}
\]

The parenthesis is the multiplicative character holonomy of the SCC.  A
nonzero value gives a saturated unit.  A zero value is the exact surviving
Fitting class.  For ordinary hafnian rows every matching coefficient is
(+1), so (4) follows.

This formula is invariant under arbitrary nonzero rescaling of physical
cell variables.  Such a rescaling multiplies both products in (3) by the
same monomial value.  It cannot tune an odd plus-cycle determinant to zero
in characteristic zero.

## 2. The actual minimal triangle

In the packet of `b942209`, use the mixed source words

```text
20120121
22100121
22120101
```

and write their two matching terms as

\[
                         A+B,\qquad C+D,\qquad E+F.
\]

Every word is off-diagonal in both the (pq) and (pr) chart.  Literal
matching exponents give

\[
                         A D E=B C F=K.                 \tag{6}
\]

With the three matching classes ordered cyclically, the coefficient matrix
is

\[
 M_3=
 \begin{pmatrix}
 A&B&0\\
 0&D&C\\
 F&0&E
 \end{pmatrix},
 \qquad
                         \det M_3=2K.                  \tag{7}
\]

Equation (7) is the Fitting form of the ordinary identity

\[
        D E f_0-B E f_1+B C f_2=2K.                    \tag{8}
\]

It is the smallest nonzero **balanced plus-hafnian** critical SCC: a
one-class row is already a private monomial pivot, while a balanced
two-cycle has determinant zero.  A two-cycle with nontrivial coefficient
character can of course have a nonzero determinant by (5).

## 3. A same-packet zero-Fitting component

Now take source words

```text
20120121
21120121
```

Their rows have different active common factors but the same two core
matching classes.  Write them as

\[
                         A+B,\qquad C+D.
\]

Direct exponent comparison gives

\[
                              A D=B C.                 \tag{9}
\]

Hence

\[
             M_2=\begin{pmatrix}A&B\\C&D\end{pmatrix},
             \qquad \det M_2=AD-BC=0.                  \tag{10}
\]

All local data are literally identical to (7), because (7) and (10) are
submodules of one physical packet:

```text
curvature:                  -1
deleted-star ranks:          3,3,3,3
both selected cofactors:     active
target-2 ruling sites:       3 and 2
```

This is sharper than comparing two unrelated supports.  The local OO
ledger cannot distinguish the nonzero and zero Fitting components even at
one fixed rational point.

The full packet is still source-empty because the odd component (7) is
present.  Thus (10) is a counterguard to a local forcing claim, not a source
counterexample.

## 4. Segre cancellation gives zero minors, not the missing unit

The recombination theorem in
[`recombination-cube-segre-cancellation.md`](recombination-cube-segre-cancellation.md)
says that, on an exact mixed source packet, the aggregate cancellation-mate
array is

\[
                      R_\epsilon=-\prod_i c_{i,\epsilon_i}.   \tag{11}
\]

Thus every two-by-two flattening minor is identically zero.  This is a
strong coefficient constraint, but its sign is opposite to the hoped-for
local Fitting argument: it produces a rank-one Segre rectangle, not a
nonzero determinant.

The two-word component (10) is the smallest literal instance of precisely
that zero-minor geometry inside the curved RR packet.  It shares all local
curvature, goodness, activity, and ruling data with the odd triangle.  So
those ledgers cannot turn (11) into a nonzero minor.

What can still be nonzero is the **cycle-cover character** obtained after
different Segre rows are glued by common matching classes.  Equation (7)
is the smallest example: the individual two-term rows are rank-one data,
but their three-row signed holonomy is odd and has determinant (2K).

## 5. Exact remaining theorem

Start with all literal mixed full-output rows and localize the active cell
monomials.  Quotient any already certified signed binomial character and
peel every one-class row.  On the remaining finite source-labelled module,
decompose the matching-class incidence graph into strongly connected
components.

For a simple cyclic SCC, (5) is its top Fitting minor.  For a general SCC,
the corresponding maximal minors sum the cycle-cover characters.  The
uniform curved-overlap theorem now needs precisely one of the following:

1. every SCC reachable from the selected diagonal/off-diagonal class peels
   to a private monomial;
2. some reachable SCC has nonzero character/Fitting determinant; or
3. a zero-Fitting SCC admits a source switch that strictly lowers a global
   well-founded matching order.

Curvature, goodness, and activity provide the local chart and guarantee
that the physical rows exist.  They do not establish any of 1--3.  A proof
of that global alternative, or a common-source proper saturated component,
is the remaining theorem-level gate.

## 6. Verification and scope

The standard-library checker
[`verify_oo_curved_signed_cycle_fitting_lemma.py`](../computations/verify_oo_curved_signed_cycle_fitting_lemma.py)
pins the global-boundary packet, verifies (2) for cycle lengths 2 through 9,
reconstructs the three-word determinant (7), and reconstructs the parallel
zero determinant (10).  It also pins the dense-Segre cancellation theorem
and verifies that all 112 abstract four-cube flattening minors vanish.  It
confirms that both Fitting components occur inside the same curved,
doubly-good, doubly-active, aligned packet.

This proves the cycle/Fitting lemma and refutes local parity forcing.  It
does not prove that every arbitrary active curved packet has a nonzero SCC,
and it does not construct a Krenn counterexample.
