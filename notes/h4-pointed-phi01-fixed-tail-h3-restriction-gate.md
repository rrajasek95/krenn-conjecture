# The pointed `h=4` word edge is the fixed-tail prolongation of `Phi_KS,r0/P_f`

## Verdict

The obvious centered-occurrence multiplication does not construct the
missing pointed edge `phi01`.  It selects the correct coefficient exactly,
but its physical boundary still has two endpoint-role-odd cut faces.  Even
after granting both of those fillers, the selected six-term `db01` packet is
independent:

```text
rank before/after selected db01       183 -> 184
centered dual on selected db01        174.
```

There is nevertheless a sharp reduction of the open problem.  Restriction
along the common squarefree tail edge `67` is an exact chain retraction.  It
sends any normalized, pointed, target-corrected `h=4` `phi01` to the unique
normalized `h=3` response-KS-to-cap comparison

\[
 \Phi_1(\epsilon_s)=r_0,
 \qquad
 \Phi_0(c_f)=-E.                                      \tag{1}
\]

Conversely, multiplying (1) by the `67` tail coefficient produces the
relative fixed-tail `phi01`; its only new absolute face is the literal
`dq67` Leibniz/Hasse face.  Thus the new operation-changing datum in `phi01`
is not a second all-order theorem.  It is one labelled fixed-tail instance
of the already open `h=3` theorem `Phi_KS,r0/P_f`.

This reduction does **not** prove that comparison exists.  It collapses the
two local interfaces to one open theorem.

Exact checker:
[`verify_h4_pointed_phi01_fixed_tail_h3_restriction_gate.py`](../computations/verify_h4_pointed_phi01_fixed_tail_h3_restriction_gate.py).

## 1. Orbit-relative site transport is not enough for current `PAComp`

Let `S` be the fixed decorated source object and let `gS` be its relabeling
by the tail-block permutation `g=(2 4)(3 5)`.  The action-groupoid bar has
boundary

\[
                         (gS,m_1)-(S,m_0).             \tag{2}
\]

It is a legitimate orbit-relative comparison, but (2) is not a chain in the
fixed source fibre.  There are exactly two evident ways to bring it back.

1. Apply the honest inverse transport from `gS` to `S`.  It sends the moved
   endpoint back to `m0`, so the boundary of (2) becomes zero.  No fixed
   `m1-m0` edge is produced.
2. Forget the source-object label and call the moved endpoint `m1` in the
   same fibre.  The boundary becomes `m1-m0`, but this is precisely the raw
   fold.  On the two fixed coefficient coordinates its effect is

   ```text
   fixed-source H0 before fold       2
   fixed-source H0 after fold        1.
   ```

The second choice is not a presentation-safe quasi-isomorphism.  Therefore
orbit-relative transport does not imply the current form of `PAComp(h)`,
which asks for an objectwise boundary/terminal or active cap in the actual
complete pointed source, retaining its word, fine, repeated, and operation
rows.

Relabeling invariance of the *property of already being an active cap* does
not repair this gap: it transports a cap after one has been obtained, while
(2) supplies no objectwise boundary from which to obtain it.  An alternative
global proof could use the orbit-relative bar only after proving a new
conservative equivariant-descent theorem from the action groupoid to an
objectwise terminal/active cap.  No such theorem is currently present, and
the fixed-fibre `H0` calculation shows that it cannot be replaced by raw
coinvariants.

## 2. The exact fixed-tail restriction

Write `q67` for the common squarefree coefficient and `dq67` for its first
principal-parts face.  On the fixed-tail tensor product define

\[
 \rho_{67}(q_{67}z)=z,
 \qquad
 \rho_{67}(dq_{67}z)=0.                              \tag{3}
\]

In the `h=3` ordered basis

```text
(epsilon_s, r0, c_f, E)
```

the differential is `d epsilon_s=-c_f`, `d r0=E`.  In the `h=4` basis

```text
q67*(epsilon_s,r0,c_f,E), dq67*(epsilon_s,r0,c_f,E),
```

the total differential has block form

\[
 d_4=
 \begin{pmatrix}
  d_3&0\\
  1&-d_3
 \end{pmatrix}.                                      \tag{4}
\]

The checker verifies exactly

\[
 d_4^2=0,
 \qquad
 \rho_{67}d_4=d_3\rho_{67},
 \qquad
 \rho_{67}I_{67}=1.                                 \tag{5}
\]

Insertion itself has the single explicit defect

\[
             d_4I_{67}-I_{67}d_3=dq_{67}\otimes 1.   \tag{6}
\]

Hence insertion is a chain map in the relative quotient by the spectator
face, and (6) is exactly the face supplied by the absolute cubical
Leibniz/Hasse totalization.  There is no hidden scalar normalization or new
overlap class in this step.

## 3. Why restriction gives exactly `Phi_KS,r0/P_f`

Project the restricted edge to its operation-changing summand.  The source
is the root-labelled response KS complex and the target is the labelled
`AugP2/K_Eq` cap complex.  Word roots may carry the response word to the cap
word, but they preserve the response operation parent; thus the projection
cannot be supplied by word transport alone.

Write

\[
 \Phi_1(\epsilon_s)=a r_0,
 \qquad
 \Phi_0(c_f)=bE.
\]

The chain-map equation is `a+b=0`.  Its solution space is one-dimensional,
and monicity plus the normalized cap target gives `(a,b)=(1,-1)`.  Since
`rho67` is the identity on the `q67` block, any monic physical `phi01` has

\[
       \pi_{\mathrm{mix}}\rho_{67}(\phi_{01})
       =\Phi_{KS,r0/P_f}.                             \tag{7}
\]

Conversely, `q67*Phi` together with (6) gives the relative fixed-tail edge.
The other presentation/Hasse terms are canonical faces already exposed by
the three-window totalization.  Consequently the implications are

```text
physical pointed phi01  =>  labelled Phi_KS,r0/P_f instance;
Phi_KS,r0/P_f + spectator Hasse face  =>  relative fixed-tail phi01.
```

This is equivalence of the one *new operation-changing source datum*.  It is
not a claim that the complete absolute all-`h` spectator naturality theorem
has already been proved.

## 4. The first face is preserved term by term

The selected `h=3` first face is

\[
 p_0s_1\!\!\sum_{23|45,24|35,25|34}
 (dq_e q_{e'}+q_e dq_{e'}).                          \tag{8}
\]

Its six terms are

```text
p0*s1*dq23*q45       p0*s1*q23*dq45
p0*s1*dq24*q35       p0*s1*q24*dq35
p0*s1*dq25*q34       p0*s1*q25*dq34.
```

The fixed-tail packet is obtained by multiplying every term in (8) by
`q67`.  Equation (3) maps these six terms bijectively back to (8); its matrix
is the `6 x 6` identity.  The three extra spectator terms

```text
dq67*p0*s1*q23*q45,
dq67*p0*s1*q24*q35,
dq67*p0*s1*q25*q34
```

are precisely (6) and are killed by `rho67`.  Therefore the reduction does
not merely match the top generator: it preserves the first unavoidable
selected-`db01` face term by term.

## 5. Conditional cap readouts

For a selected cap corner, use row order

```text
B, Eq, target, M, ainc, q, P_f, ores, W, ridge, eta, sigma.
```

Every one of the six conditional `db01*r0` faces has readout

```text
(1, 1, 1, -1, -1, 0, 1, 0, 0, 0, 0, 0),             (9)
```

with `q=M-ainc=0`.  The aggregate over all six terms is

```text
(6, 6, 6, -6, -6, 0, 6, 0, 0, 0, 0, 0).             (10)
```

Restriction by `rho67` preserves (9) and (10).  These are exact readouts of
the existing cap-internal `r0` packet, but they are conditional as readouts
of `phi01`, because the mixed physical arrow is still open.

The pointed conormal must not be conflated with the primitive cap.  In the
small quotient with rows `(P_f,Q,ores)`,

\[
                  P_f=(1,0,0),
              \qquad p=(0,-1,-1),                    \tag{11}
\]

and the pair has rank two.  Thus a source-valid `Phi_KS,r0/P_f` schema must
carry the pointed comparison in addition to the `r0` target normalization;
coefficient selection alone does not infer it.

## Scope and shortest remaining theorem

This is an exact rational calculation on the single `h=4` overlap packet
with common edge `67`.  It retains the six selected PP terms, the spectator
Leibniz face, response/cap operation idempotents, pointed conormal, and all
listed augmented cap rows.

The shortest remaining positive theorem is now shared by the local and
first uniformity interfaces:

> Construct one source-labelled, pointed, normalized, protected-row
> comparison schema `Phi_KS,r0/P_f`, natural in the marked one-root object
> and compatible with the literal selected-`db01` face.

At `h=3` it closes the local response-to-cap bridge.  Its fixed-tail
prolongation closes the missing `h=4` `phi01` edge modulo the explicit
spectator Hasse totalization.  This does not by itself establish full
`PAComp(h)` for every `h`, but it removes `phi01` as an independent theorem.
