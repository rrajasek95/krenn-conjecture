# Higher-split Robin exchange and the first uniform diagnostic

## 1. Scope

Put

\[
 h=t-r-1,\qquad 7\le h\le r-2,
 \qquad p=r-1,\qquad k=p-h.
\]

There are \(|E|=p+h+2\) exceptional labels.  On the all-distinct stratum,
the vanishing of all isolated-star pivots gives, for every \(h\)-set
\(R\subset E\), a nonzero polynomial

\[
 \deg q_R\le h-3,
 \qquad
 q_R'(-a)+Y_a(R)q_R(-a)=0\quad(a\in R),                    \tag{1}
\]

where

\[
 Y_a(R)=A_a+\sum_{c\in R\setminus\{a\}}\psi(a,c),
 \qquad
 \psi(a,c)={1\over a+c}-{2\over c-a}.                     \tag{2}
\]

This note records an exact exchange lemma valid for every \(h\), and an
exact finite-field test of the proposed uniform Robin-pencil classification.
The latter is diagnostic only: no characteristic-zero classification is
claimed here.

## 2. The cubic gauge

For an anchor \(a\), set

\[
                         g_a(z)=(z-a)(z+a)^2.                \tag{3}
\]

At every admissible anchor \(c\),

\[
                    {g_a'(-c)\over g_a(-c)}=-\psi(c,a).     \tag{4}
\]

All denominators in (4) are nonzero because the anchors are distinct and no
two are opposites.

**Lemma 2.1 (deletion gauge).**  Let \(R=S\mathbin\sqcup\{a\}\), and suppose
\(q_R\) satisfies (1).  Then the rational function

\[
                              f_a={q_R\over g_a}             \tag{5}
\]

satisfies

\[
                 f_a'(-c)+Y_c(S)f_a(-c)=0\qquad(c\in S).    \tag{6}
\]

Indeed, logarithmic differentiation of (5), followed by (1) and (4),
subtracts precisely the contribution \(\psi(c,a)\) from \(Y_c(R)\).  This
argument can be written without dividing by \(q_R(-c)\): multiplying (6) by
\(g_a(-c)^2\) gives the same linear identity.

**Lemma 2.2 (one-anchor exchange lift).**  Let \(S\) have \(h-1\) elements,
and let \(a,b\notin S\).  Write \(q_a=q_{S\cup\{a\}}\) and
\(q_b=q_{S\cup\{b\}}\).  Then

\[
                         P_a=g_bq_a,
 \qquad                  P_b=g_aq_b                         \tag{7}
\]

are nonzero polynomials of degree at most \(h\), and both satisfy the same
full-core equations

\[
 P'(-c)+Y_c(S\cup\{a,b\})P(-c)=0
       \qquad(c\in S\cup\{a,b\}).                           \tag{8}
\]

For \(c\in S\), equation (4) adds the missing contribution of the other
anchor.  At \(a\), the equation for \(P_a\) follows in the same way from the
equation for \(q_a\), while the equation at \(b\) is automatic because
\(g_b(-b)=g_b'(-b)=0\).  The proof for \(P_b\) is symmetric.

There is also a useful fixed-\((h+1)\)-core consequence.  If
\(T\subset E\) has size \(h+1\), then

\[
                         P_b=g_bq_{T\setminus\{b\}}
                         \quad(b\in T)                       \tag{9}
\]

all belong to one Robin kernel on \(T\).  Their span has dimension at least
two.  Otherwise one nonzero polynomial of degree at most \(h\) would be
divisible by every pairwise coprime cubic \(g_b\), \(b\in T\), which is
impossible.  Cancelling the leading coefficient in two independent members
therefore gives a nonzero common-kernel polynomial of degree at most \(h-1\).

The loss in that last bound is real in the present argument.  A residual for
an \((h+1)\)-core would need degree at most \(h-2\).  Obtaining it requires a
third independent lift, or a proof that the top-two coefficient map on the
lift span has rank at most one.  Lemma 2.2 alone supplies neither fact.

## 3. The uniform Robin-pencil conjecture

For distinct nonzero nodes \(t_1,\ldots,t_n\), with no opposite pair, let
\(D_i\) and \(E_i\) denote derivative and evaluation at \(t_i\).  Consider

\[
 {\cal A}_i(x)=D_i+\bigl(U_i+\psi_i(x)\bigr)E_i,
 \qquad
 \psi_i(x)={1\over x-t_i}-{2\over x+t_i}.                  \tag{10}
\]

The natural classification conjecture is

\[
 \det({\cal A}_i(x))_{i=1}^n\equiv0
 \quad\Longleftrightarrow\quad
 \exists\,0\ne h\in\mathbb C[z]_{\le n-4}:
 h'(t_i)+U_i h(t_i)=0\quad\hbox{for every }i.               \tag{11}
\]

The reverse implication is immediate and uniform: \(q_x=g_xh\) has degree
at most \(n-1\), and (4) makes every row in (10) annihilate it.  Necessity is
the open direction.  In nodal coordinates, if \(D\) is the differentiation
matrix and \(Z=\operatorname {diag}(t_i)\), the cleared pencil is

\[
 R_U(x)=(x^2I-Z^2)(D+\operatorname {diag}U)-xI+3Z.          \tag{12}
\]

Thus (11) says that every identically singular pencil (12) has a right
minimal vector of the cubic factor form \(g_xh\).  A general singular
quadratic matrix polynomial need not have this property; any proof must use
the nodal differentiation commutator.

## 4. A weighted-linear generalization already fails at five nodes

The four-node endpoint certificate used in the sixth-split closure is linear
in the translations, with weights

\[
                         \sigma_i=\prod_{j\ne i}(t_i+t_j).   \tag{13}
\]

There is no five-node analogue of the form
\(\sum_i\sigma_iU_i=\text{node-only constant}\).  Indeed, take the genuine
factor family in (11) with \(h(z)=z-c\).  It has

\[
                              U_i={1\over c-t_i}.             \tag{14}
\]

The proposed left side becomes

\[
                    L(c)=\sum_i{\sigma_i\over c-t_i}.        \tag{15}
\]

At \(c=t_i\), its residue is \(\sigma_i\ne0\).  Hence \(L(c)\) is not
constant in \(c\), and it cannot vanish or equal any expression depending
only on the nodes throughout the singular factor family.  Thus endpoint
descent beyond four anchors must retain the factor polynomial (equivalently,
the low Robin minors); a single translation-linear relation cannot suffice.

## 5. Exact \(n=6\) finite-field certificate

Take \(n=6\), the nodes \(1,2,3,4,5,6\) over \(\mathbb F_{13}\), and let
\(U_1,\ldots,U_6\) be indeterminates.  These nodes are nonzero, distinct, and
contain no opposite pair.  Define two ideals in
\(\mathbb F_{13}[U_1,\ldots,U_6]\):

1. \(I_{\rm pencil}\), generated by all thirteen coefficients in \(x\) of
   \(\det R_U(x)\);
2. \(I_{\rm quad}\), generated by the twenty \(3\times3\) minors of
   \((D+\operatorname {diag}U)|_{\mathbb F_{13}[z]_{\le2}}\).

The companion checker computes both ideals exactly and proves

\[
                              I_{\rm pencil}=I_{\rm quad}.   \tag{16}
\]

It does this by reducing every generator of each ideal by a Groebner basis of
the other.  Both reduced bases have twenty cubic elements.  Consequently, at
this exact node tuple, every identically singular six-node pencil has a
nonzero quadratic \(h\) and is of the predicted factor type.  This is a
strict test of (11), but specialization in finite characteristic does not
prove (11) for arbitrary complex nodes.

## 6. Current frontier

The exchange lemma is uniform in \(h\) and retains all zero/nonzero
hypotheses explicitly.  It converts one-element swaps into a common Robin
kernel, but currently misses the desired next residual degree by one.  The
finite-field calculation finds no extra minimal-index component at \(n=6\).
The remaining proof obligation is therefore precise: show that the lift span
in (9) has enough top-coefficient cancellation, or prove necessity in (11)
from the rank-one nodal commutator.  Either result would give a reusable
fixed-core consequence for the higher all-distinct split layers.

## 7. Exact audit

[verify_higher_split_robin_exchange_n6_f13.py](../computations/verify_higher_split_robin_exchange_n6_f13.py)
checks (4), both gauge transformations in Lemmas 2.1--2.2, the automatic
double-zero endpoint, the obstruction (15), the cleared pencil (12), and the
two ideal containments in (16).  It labels the characteristic-zero
classification as open.
