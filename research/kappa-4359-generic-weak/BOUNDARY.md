# Why the nonmaximal-paid condition is needed for the global leaf bound

Positive mixed surplus and weak rank separation alone do not imply the
global logarithmic leaf bound for the literal compiler used here. This
section gives an exact counterexample to that stronger assertion.

The example is a synthetic complete-role contract. It is not a claimed
native circuit, an integer-multiplication lower bound, or an impossibility
result for other uniformization constructions. The actual repacked native
tariff has many paid ranks below its minimum productive rank and is outside
this excluded boundary.

## The contract and its positive mixed surplus

Take productive roles `a` of rank two and `b` of rank three. Use two
chronological paid rank-two calls: one on `a`, then one on the uncredited
owned center. Thus

```math
q=2,\qquad m=3,\qquad
S_t=2^t+3^t,\qquad P_t=2\cdot2^t.
```

The complete owner contract satisfies the new weak interface. The original
strict constructor rejects it. Its rank-one surplus is one, and at
`t=1/2` its mixed surplus is strictly positive:

```math
S_{1/2}-P_{1/2}=\sqrt3-\sqrt2>0.
```

Every paid rank equals `q`. Consequently both the actual tilted mean and
its rational upper bound equal `q`:

```math
P_{t+1}/P_t=P_2/P_1=2.
```

This contract fails the positive theorem's requirement that at least one
paid rank be strictly below `q`.

## Exact source and exit counts at every power of two

Set `n=2^k`, where `k>=2`. The literal compiler uses

```math
G=\left\lfloor\log_2(n/3)\right\rfloor=k-2.
```

At paid depth `d`, the dilation is `2^d`, and a target lattice point has
degree `G-d`. If that point has `b` rank-three factors, its column is

```math
2^G(3/2)^b.
```

The ambient condition requires `(3/2)^b<=4/3`. Since `3/2>4/3`, necessarily
`b=0`. Every ordered class therefore has exactly one all-two lattice
point, with multiplicity one and column `2^G=n/4`.

There are `2^d` ordered paid paths at depth `d`. The root class has one
unfunded rank-two target, of rank `n/2`. In every later class, the incoming
paid job exactly funds that target. Every class has one independent
rank-three source, of rank `3n/4`. Summing the class counts gives:

| Item | Rank | Exact multiplicity |
| --- | ---: | ---: |
| Root rank-two source | `n/2` | `1` |
| Rank-three sources | `3n/4` | `2^(k-1)-1` |
| Terminal paid exits | `n/2` | `2^(k-1)` |

The total source count is `B=2^(k-1)`. All paid calls retain their actual
physical owners. In particular, a parent's owned center becomes a real
child input after the first generation. No owned output receives credit.

## The complete leaf recurrence grows at least as Fibonacci

Let `f_k=L(2^k)`, where `L` is the normalized leaf count of this particular
compiler. The base leaves give `f_0=1` and `f_1=2`.

The root source requires its rank-`n/2` complement. Each rank-`3n/4`
source requires its rank-`n/4` complement. The exits also require
rank-`n/2` children. Dividing their complete bill by `B` gives, for every
`k>=2`,

```math
f_k=(1+2^{1-k})f_{k-1}+(1-2^{1-k})f_{k-2}.
```

These counts survive integer batching: the compiler clears each ordered
child denominator and multiplies both leaves and productive width by the
same exact replication factor. The normalized recurrence is unchanged.

All coefficients are positive. The recurrence gives `f_k>f_(k-1)`, and
therefore

```math
f_k=f_{k-1}+f_{k-2}+2^{1-k}(f_{k-1}-f_{k-2})
    \geq f_{k-1}+f_{k-2}.
```

Let `phi=(1+sqrt(5))/2`. Since `f_0=1=phi^0`, `f_1=2>phi`, and
`phi^2=phi+1`, induction gives

```math
L(2^k)=f_k\geq\phi^k.
```

Also `phi^2=phi+1>2`, so `phi>sqrt(2)`. For every fixed real `gamma`,

```math
\frac{L(2^k)}{(2^k)^{1/2}(\log(2^k))^\gamma}
\geq\frac{(\phi/\sqrt2)^k}{(k\log2)^\gamma}
\longrightarrow\infty.
```

Thus no finite constant `A` and fixed logarithmic exponent `gamma` can
give the asserted global `A*n^(1/2)*max(1,ln(n))^gamma` bound for this
literal compiler. This conclusion concerns the global leaf bound; it
does not rule out a useful specially chosen rank or a different compiler.

## Executable evidence and reproduction

`boundary_check.py` authenticates the frozen original compiler and the
separate `WeakRule` implementation before importing them. It instantiates
the full role contract above and checks the exact source and exit formulas
at the seven ranks `4,8,16,32,64,128,256`. It compares every complete leaf
bill with the independently derived recurrence and checks each actual
integer batch and the uncredited owned allocation.

The first values are `L(4)=7/2`, `L(8)=47/8`, and `L(16)=619/64`. The
all-rank growth conclusion follows from the proof above; finite samples
are not used to infer it.

```sh
python3 -B research/kappa-4359-generic-weak/boundary_check.py --source-root /path/to/pr4359 --check
```

Use `--out /tmp/generic-weak-boundary.json` to write a fresh deterministic
receipt. The source root is the separate PR #4359 checkout at
`da637c87c89482bc4c86be36bd0071b3d400dbed`. No predecessor file or frozen
earlier certificate is modified.

The literal compiler is from zxv's PR #4359; its mixed flow builds on
Jacob Alan Sussman's Theorem 1G in PR #4268. Original notices remain
applicable. New material is Apache-2.0.
