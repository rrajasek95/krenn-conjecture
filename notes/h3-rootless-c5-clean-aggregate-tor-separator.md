# The clean normalized C5 has automatic zero aggregate Tor

## Universal weighted identity

Let

\[
 b:S^{15}\longrightarrow S^{243},\qquad
 d_{v,a}\longmapsto e_a^{(v)}q^{[2]},
\]

and keep the selected word \(m=12112\).  Write a denominator kernel vector
as

\[
 k=\sum_v y_vd_{v,m_v}+\sum_{a\ne m_v}z_{v,a}d_{v,a},
 \qquad b(k)=0,
\]

so its selected projection is \(y=\tau(k)\).  The literal \(m\)-word
coordinate satisfies

\[
 [e_m]b(d_{v,m_v})=h_v,qquad
 [e_m]b(d_{v,a})=0\quad(a\ne m_v),                    \tag{1}
\]

where \(h_v\) is the complete three-matching hafnian on
\(D\setminus\{v\}\).  Applying (1) to \(b(k)=0\) gives the universal
weighted relation

\[
                         \boxed{\sum_v h_vy_v=0}.      \tag{2}
\]

This holds after every base change and for polynomial kernel coefficients;
it is one source coordinate, not a numerical rank observation.

## Decisive clean-C5 consequence

On the target-preserving normalized C5 chart, every face has

\[
                              h_v=1+R_v.               \tag{3}
\]

The exact clean collision slice is \(R_v=0\) for all five faces.  Therefore

\[
                         h_1=\cdots=h_5=1,
\]

and (2) becomes

\[
                         \boxed{\epsilon(y)=\sum_vy_v=0}                \tag{4}
\]

for every \(y\in\operatorname{im}\tau\).  Thus the aggregate ideal from
`0e117b8` is automatically

\[
                         \epsilon(\operatorname{im}\tau)=(0).           \tag{5}
\]

The conditional unit-aggregate theorem in `0e117b8` remains correct, but
its positive branch cannot occur on the exact clean C5 slice.

Equivalently, the aggregate selected denominator column

\[
                         \sum_v b(d_{v,m_v})            \tag{6}
\]

has \(m\)-word coordinate \(\sum_vh_v=5\), while every combination of the
ten unselected columns has that coordinate zero.  Over a nonzero
characteristic-zero clean-C5 ring, (6) is not in the unselected image.
This one coordinate rules out every low-degree Koszul, Euler, or Schur
multiplier proposed for that membership.

## Why the old Tor packets do not contradict this

The frozen direct-free and tilted packets have transgression ranks four and
three and each contains a selected projection of nonzero aggregate.  In both
packets

\[
                              h_1=\cdots=h_5=0.
\]

Relation (2) is therefore vacuous there.  Those packets are not full-source
points and, more specifically, are not on the clean normalized slice where
the face values are one.

## Proof consequence

The clean rootless path is forced into the dual side of the aggregate
attachment-or-dual theorem.  Its primitive face-sum covector is automatic;
positive denominator Tor cannot build the missing physical base.

This does **not** yet construct the Component-III terminal annihilator.
The reduced face covector must still be promoted across the endpoint bars,
which force the aggregate \(\Omega\) component, and then through the
multidegree-preserving \(\Omega_v\to r_v\) comparison while killing
physical `W`, target, ordinary residue, and every correction row.  The
result therefore sharpens the remaining task to physical separator
promotion rather than aggregate membership.

## Scope and verification

This is an exact universal source-coordinate theorem and an exact result on
the clean \(R_v=0\) normalized C5 slice.  It does not decide the scalar-zero
\(h_v=0\) branch or construct the physical terminal comparison.

Run:

```text
python3 computations/verify_h3_rootless_c5_clean_aggregate_tor_separator.py
python3 -O computations/verify_h3_rootless_c5_clean_aggregate_tor_separator.py
python3 -I -S computations/verify_h3_rootless_c5_clean_aggregate_tor_separator.py
```

Frozen ledger SHA-256:

```text
2929c94187b0e1ab9a925fd82a0754cba6e877f34a0906f778e2346c59b22eaa
```
