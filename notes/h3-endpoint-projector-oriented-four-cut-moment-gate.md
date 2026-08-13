# The endpoint projector reaches the oriented carrier only through one common base-change

## Outcome

The endpoint occurrence projector and the two oriented four-cut actions fit
together algebraically, but not yet physically.

At response order three there are ninety occurrences and the centered
operator is

\[
                       C=90I-J.                         \tag{1}
\]

For every occurrence coefficient vector \(y\),

\[
 y={1\over90}\left(Cy+\operatorname {aug}(y){\bf1}\right). \tag{2}
\]

Thus the projector reconstructs a family only after its constant
augmentation is supplied.  In the present application that surviving line
is the unweighted \(H_0\) base class.  If a single source-valid lift of (2)
commuted with both ordered four-cut restrictions, then its two projections
would be

\[
 K^\rightarrow H_0=(q-x)H_0,
 \qquad
 K^\leftarrow H_0=(q-r+x)H_0.                          \tag{3}
\]

Consequently a nonzero projection would enter the already isolated
oriented active-clean/terminal alternative, while a dark--dark packet would
give

\[
 (K^\rightarrow+K^\leftarrow)H_0=(2q-r)H_0=0,
 \qquad
 \boxed{c_0=(r-2q)H_0=0}.                              \tag{4}
\]

The sign and coefficient in (4) are exact; no factor two is missing.

This is a conditional composition theorem, not a construction of (3).  The
committed projector is a coefficient projector plus a local projected cap
gate.  It does not yet give the required common restriction--insertion
square, and its first unweighted endpoint/Hasse face does not supply the
weighted carrier \(c_1\).

Companion checker:
[verify_h3_endpoint_projector_oriented_four_cut_moment_gate.py](../computations/verify_h3_endpoint_projector_oriented_four_cut_moment_gate.py).

## 1. What the occurrence projector reconstructs

Let \(e_f\) be the occurrence basis and let \({\bf1}=\sum_f e_f\).  The
marked centered column is

\[
                         c_f=90e_f-{\bf1}.              \tag{5}
\]

All \(c_f\) have augmentation zero and span the rank-89 standard module.
Adding the constant line gives the complete 90-dimensional coefficient
module.  Equation (2) is therefore both necessary and sufficient at the
coefficient level.

There are two consequences.

First, one marked centered cell is not a global oriented action.  Global
reconstruction uses the full family of centered columns and the aggregate
line.  Second, even complete coefficient reconstruction says nothing about
whether the reconstruction commutes with a physical chain differential,
ordered restriction, or multiplication by the curvature factors in (3).
Those are properties of a lifted map, not of \(C\).

The exact missing square has the form

\[
\begin{CD}
 P_{\rm com} @>{\widetilde C}>> P_{\rm com}\\
 @V{\operatorname{res}^\rightarrow\oplus
        \operatorname{res}^\leftarrow}VV
 @VV{\operatorname{res}^\rightarrow\oplus
        \operatorname{res}^\leftarrow}V\\
 P^\rightarrow\oplus P^\leftarrow
 @>>{K^\rightarrow\oplus K^\leftarrow}>
 P^\rightarrow\oplus P^\leftarrow .
\end{CD}                                                  \tag{6}
\]

Here every space is the complete augmented source module, including target,
anchor, terminal, physical \(q\), and protected rows.  The constant
augmentation must map to the *same* \(H_0\) before evaluation.  If (6)
exists, (3)--(4) follow.  If the two restrictions instead use
\(H^\rightarrow=H_0+\delta^\rightarrow\) and
\(H^\leftarrow=H_0+\delta^\leftarrow\), their sum leaves the previously
isolated mismatch

\[
 c_0=K^\rightarrow\delta^\rightarrow
          +K^\leftarrow\delta^\leftarrow,              \tag{7}
\]

not (4).

## 2. Exact word and fine-grade boundary

The endpoint projector is currently physical only up to its primitive cap
gate at \(h=3\).  Its local source data are

```text
word                 01211222
fine grade           Q_(v,N)=t_v q_(v,N)
repeated-site type   P3+K2
occurrence count     90
```

The oriented four-cut theorem is formulated on the complete scalar-unit
top-word carrier at arbitrary \(h\), with ordered response endpoints.  No
pinned theorem identifies its two restricted carriers with the two
projections of the `01211222`, repeated-`P3+K2` cap cell.  Such an
identification must preserve the word, fine and repeated grades as well as
the protected/terminal readouts; polynomial coefficient equality is
insufficient.

In particular, the common-tail symbol \(t_v\) in
\(Q_{v,N}=t_vq_{v,N}\) is a decorated physical cell multiplier.  It is not
the affine parameter \(t\) in

\[
 H_s=\int_0^1t^s(q+tr)^{[h-2]},dt.                    \tag{8}
\]

Conflating those two symbols would turn an ordinary Rees-grade lift into a
moment transgression without a source identity.

## 3. Why a first endpoint/Hasse face does not give \(c_1\)

The next required relation is

\[
                     c_1=(r-2q)H_1=0,
 \qquad H_1=\int_0^1t(q+tr)^{[h-2]},dt.               \tag{9}

An unweighted projector face supplies no affine weight.  This remains true
even if one grants its endpoint values and first endpoint jets.  The exact
polynomial bubble

\[
                 z(t)=t^2(1-t)^2\left(t-\tfrac12\right) \tag{10}
\]

satisfies

\[
 z(0)=z(1)=z'(0)=z'(1)=0,
 \qquad \int_0^1z(t),dt=0,
 \qquad \int_0^1t z(t),dt={1\over840}.                \tag{11}

Hence two horizontal candidates differing by \(z\) have identical
unweighted aggregate and endpoint 1-jets but different first weighted
moments.  This is a finite polynomial shadow of the committed based-loop
torsor.  It does not say that every possible Hasse refinement fails: it says
that a refinement must carry the affine density/weight or prove the bubble
class is a physical boundary.  An ordinary endpoint face alone cannot do
so.

The exact extra datum is therefore a source-valid ordered polynomial
one-form \(E(t)dt\) with

\[
 dE(t)dt=(r-2q)(q+tr)^{[h-2]}dt,                       \tag{12}
\]

together with zero based-loop moment residue.  Its unweighted integral
would realize \(c_0\); its \(t\)-weighted integral would realize \(c_1\).
The current endpoint projector contains neither the affine density in
(12) nor the zero-indeterminacy theorem.

## 4. Sharp proof frontier

The cross-gate route is reduced to one enriched physical map:

1. lift all centered occurrence columns and the constant \(H_0\) line in
   the same augmented source module;
2. make both ordered four-cut restriction/multiplication squares commute;
3. preserve `01211222`, repeated `P3+K2`, protected, anchor, terminal, and
   physical-\(q\) readouts; and
4. refine the lift to the weighted one-form (12), or separately kill its
   first based-loop moment residue.

Items 1--3 give the exact active-clean-or-\(c_0\) alternative.  Item 4 is
genuinely additional and gives \(c_1\).  The endpoint association algebra
does not remove either physical obligation.

## Verification

Run

```text
python3 computations/verify_h3_endpoint_projector_oriented_four_cut_moment_gate.py
python3 -O computations/verify_h3_endpoint_projector_oriented_four_cut_moment_gate.py
python3 -I -S computations/verify_h3_endpoint_projector_oriented_four_cut_moment_gate.py
```

The checker pins the endpoint primitive-cap gate, the oriented common
carrier gate, the based-loop torsor, and the augmented moment criterion.  It
verifies (1)--(4), coefficient reconstruction with the constant line, and
the exact bubble identities (10)--(11).
