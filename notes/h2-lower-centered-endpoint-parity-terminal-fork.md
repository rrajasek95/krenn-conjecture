# The lower centered packet has a sharp endpoint-parity fork

## Outcome

Each marked proper face of the \(h=3\) centered occurrence class lands in
the order-two occurrence module on four sites. That module has twelve
ordered endpoint occurrences. If \(S\) reverses the ordered endpoints and

\[
                         c_f=12e_f-\mathbf 1,
\]

then

\[
 \boxed{
 c_f^-={1-S\over2}c_f=6(e_f-e_{Sf}),
 \qquad
 c_f^+={1+S\over2}c_f=6(e_f+e_{Sf})-\mathbf 1.}        \tag{1}
\]

This gives a real terminal fork, but not an automatic closure.

- If a **physically typed** odd projection is nonzero, at least one of its
  two ordered orientation coordinates is nonzero and the existing
  oriented active-clean/terminal alternative applies.
- If the odd projection is dark, the residual is \(c_f^+\). Complete
  response/common \(H_0\) alone does not kill it. The endpoint-even
  augmentation-zero quotient has dimension five, and an explicit primitive
  symmetric covector kills \(H_0\) and every odd class while reading \(12\)
  on \(c_f^+\).
- Coefficientwise the even residual has a short positive solution. For the
  degree-four endpoint adjacency \(B\),

  \[
   \Pi_{\rm even}={B(B+2I)\over24},
   \qquad
   c_f^+=-{1\over24}(B+6I)(B-4I)c_f^+.                \tag{2}
  \]

  Hence one occurrence-local physical lift of \(B-4I\), with its quadratic
  Hasse/product-rule face, would close the odd-dark branch.

The current complete response and group-bar inventory does not construct
that occurrence-local lift. Endpoint parity therefore reduces the two lower
debts to one precise source type; it does not remove them.

Companion checker:
[verify_h2_lower_centered_endpoint_parity_terminal_fork.py](../computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py).

## 1. Exact parity decomposition

An order-two occurrence is an ordered pair \((p,s)\) on four sites; its one
residual edge is forced. Endpoint reversal has six two-element orbits, so

\[
 \dim V^+=6,
 \qquad
 \dim V^-=6.
\]

The constant response line lies in \(V^+\). Its complement there has
dimension five. Formula (1) follows by applying \((1\pm S)/2\) to
\(12e_f-\mathbf 1\).

The odd class has selected orientation coordinates

\[
                             (6,-6).                  \tag{3}
\]

Therefore a nonzero image of \(c_f^-\) in a physical ordered-orientation
quotient forces at least one nonzero orientation. This is exactly the
linear implication used by the oriented active-clean fork.

There are two necessary qualifications.

First, \(c_f^-\) is not one endpoint-adjacency eigenline. It has nonzero
projections to both odd eigenvalues \(+2\) and \(-2\). Thus it cannot be
identified with one pre-existing odd carrier merely by its parity.

Second, the active-clean theorem requires that the nonzero ordered
coefficient be the literal projection of a complete augmented source class.
The current lower occurrence module is a coefficient presentation. No
pinned comparison transports its word, endpoint decoration, protected rows,
and physical \(q\) to that relative quotient. Hence

\[
 \boxed{
 c_f^-\ne0\text{ coefficientwise}
 \quad\not\Rightarrow\quad
 \text{physical active-clean exit}}
\]

without the typed projection hypothesis.

## 2. Odd-dark does not make the even class common \(H_0\)

Assume the odd component vanishes in the candidate quotient. Then
\([c_f]=[c_f^+]\). Choose one other unordered endpoint pair
\(\{g,Sg\}\), and define the primitive symmetric covector
\(\lambda_f^+\) to be \(+1\) on \(f,Sf\), \(-1\) on \(g,Sg\), and zero
elsewhere. It satisfies

\[
 \lambda_f^+(\mathbf 1)=0,
 \qquad
 \lambda_f^+(V^-)=0,
 \qquad
 \lambda_f^+(c_f^+)=12.                               \tag{4}
\]

Thus adjoining the complete response/common-\(H_0\) line and killing the
odd sector still leaves \(c_f^+\). More globally, if
\(c_{\{p,s\}}^+\) denotes the six pair classes, their only coefficient
relation is

\[
                  \sum_{\{p,s\}}c_{\{p,s\}}^+=0.       \tag{5}
\]

The five-dimensional even standard/pair module remains.

The covector (4) is a presentation-level separator. It becomes a physical
terminal/Fredholm functional only if it extends by zero across the complete
protected source map, including the physical-\(q\) domain. No such promotion
is claimed here.

## 3. The quadratic even projector

Let \(B\) move either ordered endpoint through one of the two residual
sites and re-pair the displaced endpoint with the residual mate. It has
degree four and commutes with \(S\). Its spectra are

\[
 \begin{array}{c|c}
  V^+&4,0,-2\\
  V^-&2,-2.
 \end{array}                                           \tag{6}
\]

The \(4\)-eigenspace is exactly the constant line. Hence on \(V^+\),

\[
                         \Pi_{\rm even}={B(B+2I)\over24} \tag{7}
\]

is the constant projector. Since \(c_f^+\) has augmentation zero,
\(\Pi_{\rm even}c_f^+=0\). Factoring \(1-\Pi_{\rm even}\) gives

\[
 1-\Pi_{\rm even}
   =-{1\over24}(B+6I)(B-4I),                           \tag{8}
\]

which proves (2).

The operator \(B-4I\) is the sum of four formal endpoint differences. On
the even module its image has rank five, exactly the whole even centered
quotient. Therefore the coefficient problem in the odd-dark branch is
complete: one equivariant endpoint-difference family plus the quadratic
correction in (8) fills every even centered class.

The source-provenance problem remains. A formal edge difference
\(e_{bg}-e_g\) assumes a source generator localized at the occurrence \(g\).
The committed complete physical source row is constant across its matching
occurrences, and its site/Cartan bars remain constant in that occurrence
coordinate. This is why the physical occurrence-splitter theorem does not
already realize \(B-4I\).

## 4. Literal lower words and reinsertion

For the marked top occurrence

~~~text
f=(0,1;23|45),   top word 01211222,
~~~

the two marked restrictions are

~~~text
delete 23: lower word 0112, reinsert q23:21,
delete 45: lower word 0121, reinsert q45:12.
~~~

Same-edge reinsertion restores the top word and labelled repeated
P3+K2 coefficient. Endpoint reversal preserves each four-site word but
exchanges its ordered endpoint-colour decoration from (0,1) to (1,0).
The coefficient involution \(S\) therefore does not by itself give a
fixed-fine-grade source chain map.

A positive lower-parity theorem must construct one rho-compatible family
whose two proper faces are occurrence-local lifts of \(B-4I\) in these two
lower words, and whose reinsertions land in the common
01211222/repeated-P3+K2 grade. It must also totalize the quadratic
endpoint product-rule face and preserve Eq, target, residue, anchor,
eta/sigma, \(W\), and physical \(q\).

## 5. Effect on the Gamma1 frontier

The shifted raw Gamma1 packet has lower centered coefficient
\(-5/8\) on each marked face. Apply the fork separately to those two
faces.

1. A physically visible odd part gives the existing active-clean/terminal
   branch.
2. In the odd-dark branch, only the even part remains.
3. Equation (2) expresses that even part through the single endpoint
   difference \(B-4I\), plus the common constant projector.

Thus the shortest new source statement is not a general twelve-coordinate
filler. It is a physically typed, endpoint-even quadratic
restriction-insertion cell. Failure leaves the exact even covector (4),
which must then be tested against the complete augmented source map.

## Scope

Proved here are the complete order-two endpoint parity decomposition, the
odd/even dimensions, the primitive symmetric even dual, the endpoint
spectra, the quadratic projector, and the formal endpoint-difference filler
identity.

Not proved are the physical active-clean landing, the occurrence-local
source bar, its full word/fine/repeated-grade lift, or terminal promotion of
the even dual. Therefore this is a sharp conditional terminal fork and a
smaller construction target, not closure of Gamma1.

## Verification

Run

~~~text
python3 computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py
python3 -O computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py
python3 -I -S computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py
~~~
