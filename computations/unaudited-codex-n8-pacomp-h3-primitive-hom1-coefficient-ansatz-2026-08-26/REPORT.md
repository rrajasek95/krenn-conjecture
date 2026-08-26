# PAComp primitive `Hom^1` coefficient ansatz

Status: **exact rational no-go for the maximal pinned source-labelled ansatz.**

After quotienting the joint detector-dark subspace, every pinned primitive, allowed reindexing, admissible composite, and standard interchange vanishes. The only genuine top source shadows left are `Gamma_B=(1,1,0)` and `Gamma_C=(1,0,1)` in coordinates `(eta_top,t_B,t_C)`; the four formally granted switches are zero. Thus the most general clean top ansatz has matrix

```text
[0 0 0 0 1 1]        [2]
[0 0 0 0 1 0] x  =   [0].
[0 0 0 0 0 1]        [0]
```

The exact left-kernel witness `(1,-1,-1)` kills every column and reads `2` on the target. This incorporates the endpoint near-misses: cancelling their protected `t_B,t_C` faces forces their coefficients to zero.

In the retained quotient, all four face-complete rows are zero while the `Lambda` target is `+1` and the `Pi` target is `-1`; the witness `1` certifies both inconsistencies. These certificates apply independently to each of the four `AB/AC x q23/q45` instances, so the 56-variable system fails before its eight coherence equations and five proper-face checks are needed.

A positive control adds one new top signature `(2,0,0)` and one retained signature `1`; coefficients `1,1,-1` then solve the quotient equations. Hence the obstruction is source availability, not a sign or normalization error. The result does not exclude unregistered primitive `Hom^1` records or promote PAComp, uniform descent, or the conjecture.
