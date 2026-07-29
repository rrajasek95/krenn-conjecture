# Independent audit of the path/triangle exposed-grid obstruction

## Verdict

The path and triangle exclusions in
[`rank-budget-path-triangle-exposed-grid-obstruction.md`](rank-budget-path-triangle-exposed-grid-obstruction.md)
are correct under the stated rank-budget-equality hypotheses.  This audit
reconstructs the quotient grid directly from the nine response identities,
checks every zero/nonzero branch in the crossed-target argument, and proves
the two contradictions in a different endpoint notation.  No
perfect-matching summand is isolated and the argument does not use
\(q^{[3]}=0\) after the response equations have been quotiented.

The wedge-plus-disjoint grid is genuinely satisfiable as a *quotient-grid
system*.  Thus this method alone cannot exclude that incidence geometry.
This is not a construction of a full common-power response model: the
unquotiented response equations and \(q^{[3]}=0\) may still exclude the
wedge.

## 1. Reconstruction from the response equations

Let \(U\) be the six sites, let

\[
 F=q^{[2]}=\sum_{P\in\binom U2}F_P,
 \qquad
 F_P\in\bigotimes_{u\notin P}W_u,
\]

where \(F_P\) is the part whose two unoccupied sites are \(P\).  In matrix
form the nine response equations are

\[
             (p_r s_sF)_{0\le r,s\le2}
        =\sum_{c=0}^2E_{cc}\otimes
          \bigotimes_{u\in U}e_c^{(u)}.                 \tag{1}
\]

At rank-budget equality, the four-cover argument gives

\[
 W_u=\operatorname{span}\{e_c^{(u)}:u\notin B_c\},
 \qquad |B_c|=2.                                      \tag{2}
\]

Fix \(P=\{u,v\}\), quotient the \(u\)- and \(v\)-factors by
\(W_u,W_v\), and write bars for quotient classes.  If \(Q\ne P\), then
\(F_Q\) occupies at least one of \(u,v\) with an endpoint of \(q\), hence
with a vector in the corresponding \(W\)-space.  Its image is zero.
Therefore (1), with no termwise matching assumption, becomes

\[
 \left(\bar p_{r,u}\otimes\bar s_{s,v}
       +\bar s_{s,u}\otimes\bar p_{r,v}\right)_{r,s}
       \otimes F_P
 =\sum_{c:B_c=P}E_{cc}\otimes
   \bar e_c^{(u)}\otimes\bar e_c^{(v)}\otimes E_c(P). \tag{3}
\]

If two colors had the same \(B_c=P\), the right side of (3) would have
flattening rank at least two: its left factors are independent already in
the matrix coordinates \(E_{cc}\), and its right factors \(E_c(P)\) are
independent because the target axes are independent at every remaining
site.  The left side has rank at most one across the displayed bar.  Thus
the three \(B_c\)'s are distinct.  When \(P=B_c\), uniqueness of a nonzero
simple tensor gives

\[
 N_P=\eta_cE_{cc}\otimes
      \bar e_c^{(u)}\otimes\bar e_c^{(v)},
 \qquad \eta_c\ne0,                                   \tag{4}
\]

where \((N_P)_{rs}\) is the parenthesized tensor in (3).

Put \(I(u)=\{c:u\in B_c\}\).  By (2), the quotient vectors
\(\{\bar e_c^{(u)}:c\in I(u)\}\) are independent.  Choose dual
functionals \(L_{u,c}\), and define

\[
 a_{u,c}=(L_{u,c}\bar p_{0,u},L_{u,c}\bar p_{1,u},
          L_{u,c}\bar p_{2,u})^t,
 \quad
 b_{u,c}=(L_{u,c}\bar s_{0,u},L_{u,c}\bar s_{1,u},
          L_{u,c}\bar s_{2,u})^t.                    \tag{5}
\]

For \(X=(a,b)\), \(Y=(a',b')\), set

\[
                         H(X,Y)=a(b')^t+a'b^t.         \tag{6}
\]

Applying \(L_{u,d}\otimes L_{v,e}\) to (4) reconstructs the complete
typed grid

\[
 H(X_{u,d},X_{v,e})=
 \begin{cases}
   \eta_cE_{cc},&d=e=c,\\
   0,&\text{otherwise},
 \end{cases}
 \qquad d\in I(u),\ e\in I(v).                       \tag{7}
\]

In particular every endpoint occurring in a target corner is nonzero.
This is the only place where the common-power response system enters the
path/triangle contradiction.

## 2. Complete crossed-target audit

For nonzero \(X=(a,b)\) and \(Z=(c,d)\), the equation \(H(X,Z)=0\) has
exactly three kinds of solution:

1. \(b=d=0\) (both are \(a\)-pure);
2. \(a=c=0\) (both are \(b\)-pure);
3. \(a,b\ne0\) and \(Z=\rho(a,-b)\) for some \(\rho\ne0\).

Indeed, if one half of \(X\) vanishes, the corresponding outer product
forces the same half of \(Z\) to vanish.  If both halves of \(X\) are
nonzero, neither side of

\[
                         a d^t=-c b^t                 \tag{8}
\]

can vanish (otherwise \(Z=0\)).  Equality of nonzero rank-one matrices
then gives the third form.  This explicitly covers the zero-half cases;
the entirely zero point is excluded because it cannot belong to a nonzero
target corner.

Now suppose target edges \(XY\) and \(ZW\) have values
\(\alpha E_{ii}\) and \(\beta E_{jj}\), where
\(i\ne j\) and \(\alpha\beta\ne0\), while the crossed edges \(XZ\) and
\(YW\) have value zero.  Apply the preceding trichotomy to those two zero
edges.  The nine possible branch pairs reduce as follows:

| branch of \(XZ\) | branch of \(YW\) | obstruction |
|---|---|---|
| mixed | mixed | the two target matrices are proportional |
| mixed | \(a\)-pure | the targets have the same row space |
| mixed | \(b\)-pure | the targets have the same column space |
| \(a\)-pure | mixed | the targets have the same row space |
| \(b\)-pure | mixed | the targets have the same column space |
| \(a\)-pure | \(a\)-pure | both target matrices vanish |
| \(b\)-pure | \(b\)-pure | both target matrices vanish |
| \(a\)-pure | \(b\)-pure | possible |
| \(b\)-pure | \(a\)-pure | possible |

Distinct diagonal units are nonproportional and have different row and
column lines.  Hence only the last two branches remain: all four points are
pure, the endpoints on each zero edge have the same type, and the endpoints
on each target edge have opposite types.  This proves the crossed-target
lemma including all zero/nonzero edge cases.

## 3. Path and triangle in endpoint notation

Name the six target edges

\[
            ab\ (\text{color }0),\qquad
            cd\ (\text{color }1),\qquad
            ef\ (\text{color }2).                    \tag{9}
\]

For the path \(AB,BC,CD\), direct expansion of (7) gives the zero edges

\[
                         ac,\ bd,\ be,\ ce,\ df.       \tag{10}
\]

The crossed square on target edges \(ab,cd\) uses \(ac,bd\), and the
crossed square on \(cd,ef\) uses \(ce,df\).  Thus all six endpoints are
pure and, writing \(\sim\) for equal pure type,

\[
                         a\sim c\sim e,
 \qquad                  b\sim d\sim f,               \tag{11}
\]

with the two chains of opposite type.  But (10) also contains the zero edge
\(be\), whose endpoints therefore must have equal type, a contradiction.

For the triangle \(AB,BC,CA\), the target naming (9) can be chosen so that
the nine zero edges are

\[
                  ac,bf,cf,\quad bd,be,ce,\quad ad,df,ae. \tag{12}
\]

Again \(ac,bd\) purify the first two targets and \(ce,df\) purify the last
two.  Equations (11) follow, while the extra zero edge \(be\) contradicts
them.  This independently reproduces both UNSAT conclusions.

## 4. Why the wedge is still open

For the wedge-plus-disjoint pairs \(AB,BC,DE\), the only zero edges in
the exposed grids are \(ac,bd\).  They purify the first two targets, but
the third target is disconnected.  More strongly, the entire quotient
grid has exact pure solutions.  For example, with standard basis vectors
\(e_0,e_1,e_2\), take

\[
\begin{array}{c|cccccc}
 &a&b&c&d&e&f\\ \hline
 a\text{-half}&e_0&0&e_1&0&e_2&0\\
 b\text{-half}&0&e_0&0&e_1&0&e_2.
\end{array}                                           \tag{13}
\]

Then the three target values are \(E_{00},E_{11},E_{22}\), while
\(H(a,c)=H(b,d)=0\).  Reversing both types in the connected component
\(\{a,b,c,d\}\) and independently reversing the component \(\{e,f\}\)
gives four pure solutions.  Consequently the wedge remains genuinely
unclosed by the typed quotient grids.

## 5. Independent checker

[`audit_rank_budget_path_triangle_exposed_grid_obstruction_independent.py`](../computations/audit_rank_budget_path_triangle_exposed_grid_obstruction_independent.py)

* derives every grid cell solely from the omission pairs;
* exhausts the zero-pair trichotomy over both \(\mathbb F_3\) and
  \(\mathbb F_5\), including zero points and pure half-zero cases;
* exhausts the complete crossed-target lemma over \(\mathbb F_3\);
* reaches path and triangle contradictions with a parity union-find rather
  than the primary checker's \(2^6\) assignment enumeration; and
* constructs all four exact rational pure solutions of the wedge quotient
  grid.
