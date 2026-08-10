# The twenty three-set cuts carry one source-relative terminal class

## Outcome

Fix exposed physical sites `p,q`, distinct endpoint labels `a != b`, and
six residual sites `W={0,...,5}`.  Fix two distinct residual labels `c,e`.
For every three-set `S subset W`, let

\[
 w_S(x)=\begin{cases}e,&x\in S,\\c,&x\notin S.\end{cases}
\]

Write the literal selected full row as

\[
 F_{ab}(w)=\alpha\,\operatorname {haf}(q^w)
       +[R^w(q^w)^{[2]}],\qquad
 \alpha=A_{pq}(a,b),                                      \tag{1}
\]

where

\[
 R^w_{xy}=p_{a,x}(w_x)s_{b,y}(w_y)
           +p_{a,y}(w_y)s_{b,x}(w_x).                    \tag{2}
\]

On the pure `c^6` slice put `Q=q^{c^6}`, `R=R^{c^6}`, and

\[
 Q_j=R^{[j]}Q^{[3-j]},\qquad
 H_2=\alpha Q_2+3Q_3,\qquad T=Q_3/6.                    \tag{3}
\]

For the canonical cut polynomial `Theta_S` of the response two-jet, define
the literal landing error and response companion

\[
 \varepsilon_S=operatorname {haf}(q^{w_S})
       -\Theta_S(2\alpha R,R,Q),\qquad
 M_S=[R^{w_S}(q^{w_S})^{[2]}].                           \tag{4}
\]

Then the first exact source-relative connecting class is

\[
 \mathcal K_{ab;c,e}:=
       \sum_{|S|=3}(M_S+\alpha\varepsilon_S).           \tag{5}
\]

It satisfies the ordinary polynomial identity

\[
 \boxed{
 \mathcal K_{ab;c,e}-96\alpha T
   =\sum_{|S|=3}F_{ab}(w_S)-8\alpha H_2.}               \tag{6}
\]

Thus the twenty literal all-word rows and the already certified Hamming-two
row do **not** by themselves say that each cut, its companion, or its
landing error is zero.  They identify their aggregate with the terminal
class:

\[
 F_{ab}(w_S)=0\ (|S|=3),\quad H_2=0
 \quad\Longrightarrow\quad
 \boxed{\mathcal K_{ab;c,e}=96\alpha T.}                \tag{7}
\]

Consequently an adjacent-chart Bianchi proof of `T=0` has one sharply
specified task: prove `K=0` (or give a second expression for `K` that is
zero) using source relations which change the selected endpoint fine grade.
This is not supplied by the literal two-tag span: its unique route is
`H_2`, as proved in
[`h3-two-chart-h2-tagged-reinsertion-cokernel.md`](h3-two-chart-h2-tagged-reinsertion-cokernel.md).

## 1. Literal row labels and the cut formula

For `S={i,k,p}` and complement `S^c={u,v,w}`, direct matching expansion is

\[
\begin{aligned}
 \operatorname {haf}(q^{w_S})={}&
 q_{ik}(e,e)\sum_{j\in S^c}q_{pj}(e,c)
                       q_{S^c\setminus\{j\}}(c,c)\\
 &+q_{ip}(e,e)\sum_{j\in S^c}q_{kj}(e,c)
                       q_{S^c\setminus\{j\}}(c,c)\\
 &+q_{kp}(e,e)\sum_{j\in S^c}q_{ij}(e,c)
                       q_{S^c\setminus\{j\}}(c,c)\\
 &+\operatorname {per}\bigl(q_{xy}(e,c)\bigr)_{x\in S,y\in S^c}.
                                                               \tag{8}
\end{aligned}
\]

Endpoint order in (8) is literal: if the smaller physical endpoint lies in
`S^c`, the displayed `q(e,c)` is the correspondingly reversed cell in that
unordered block.  Equation (8) is exactly `Theta_S` with the physical
second and first cells on that word; no symmetric-cell assumption is used.

The source labels in (6) are therefore explicit:

* `F_ab(w_S)` is the `(p,a;q,b)` row at the literal six-letter word
  `w_S=e^S c^{S^c}`;
* `H_2` is the same `(p,a;q,b)` row tagged twice by the selected response
  `(a,b)`, in fine degree `3(e_a^L,e_b^R)`;
* `M_S` is the one-response/two-internal-edge matching part of that same
  literal row.

The canonical marking identity

\[
 \sum_{|S|=3}\Theta_S(2\alpha R,R,Q)
       =8(\alpha Q_2+Q_3)                               \tag{9}
\]

and (1), summed over the twenty words, prove (6):

\[
\begin{aligned}
 \sum_SF_{ab}(w_S)
  &=\mathcal K_{ab;c,e}+8\alpha(\alpha Q_2+Q_3),\\
 \sum_SF_{ab}(w_S)-8\alpha H_2
  &=\mathcal K_{ab;c,e}-16\alpha Q_3.
\end{aligned}
\]

Since `Q_3=6T`, the last term is `96 alpha T`.

## 2. Target handling

The GHZ target of a literal row is

\[
 \operatorname {tgt}F_{ij}(w)
   =\delta_{ij}\,\mathbf 1_{w=i^6}.                    \tag{10}
\]

Every `w_S` contains three `c` labels and three `e` labels.  Hence all
twenty rows in (6) have target zero, even if one repeats the construction
with a diagonal endpoint pair.  The selected `H_2` row also has target zero
because `a != b`.  Thus (6) has no hidden target term.

The diagonal anchors used by an adjacent-chart landing are different.  The
literal pure row has target one, so the source equation available to a
Bianchi combination is

\[
                       F_{ii}(i^6)-1=0,                 \tag{11}
\]

not `F_ii(i^6)=0`.  If a proposed two-chart expression for `K` uses anchor
rows with coefficients `lambda_i`, its scalar target augmentation is
`-sum_i lambda_i` and must be retained.  This is precisely where the known
seven-row guards fail: they omit part of the diagonal target provenance.

## 3. What has and has not been proved

Equation (6) is a source-variable polynomial identity over `Z`; after the
definition `T=Q_3/6`, only the harmless characteristic-zero division by six
is used.  It supplies the requested first source-relative connecting class
with literal rows and complete target bookkeeping.  It does **not** prove
`K=0`, and therefore does not prove `T=0` or Krenn's conjecture.  Rather, it
shows exactly what a positive two-chart Bianchi identity must annihilate.

The dependency-free checker
[`verify_h3_three_set_source_relative_terminal_class.py`](../computations/verify_h3_three_set_source_relative_terminal_class.py)
expands all twenty literal words in independent endpoint-ordered cell
variables, checks (8), verifies the canonical marking identity and (6) as
formal sparse polynomials, and audits the mixed-word and pure-anchor target
values.  It uses runtime failures and runs unchanged under optimized and
isolated Python.
