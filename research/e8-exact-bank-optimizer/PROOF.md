# Exact optimal bank construction

## Pattern inequality

Let `h >= 2` be an integer, `m = h(h-1)+1`, `D=(h-1)^2`, `0<a<1`, and `epsilon>=0`. A nonempty bank contains `k` residual items of integer ranks at most `h`, with total rank `q<=m` and padding `p=m-q`. It pays one recursive padding child when `p>0`. Define

```
C = m - m^a
y_r = (C + h*epsilon)(r-1)/D - epsilon.
```

Then its complete bank cost satisfies

```
q - m^a + p^a + epsilon*1[p>0] >= sum_items y_r,
```

where `0^a=0`.

If `p=0`, then `k>=h` because `q=m>h(h-1)`. The exact slack is `(k-h)(C+m*epsilon)/D`, which is nonnegative.

If `p>=1`, concavity of `x^a` on `[1,m]` gives

```
p^a >= 1 + (p-1)(m^a-1)/(m-1).
```

Thus the main cost is at least `C*q/(h(h-1))`. Subtracting its main dual term leaves at least `C*(h*k-q)/(h*D)>=0`, since every item rank is at most `h`. The fallback slack is

```
epsilon * (D + m*k - h*q)/D
    >= epsilon * (p-1)/(m-1) >= 0,
```

using `k>=q/h`. This establishes the inequality for every permitted real exponent, with no floating solver or sampled powers.

Equality holds for a full bank containing exactly `h` items, or for `h-1` rank-`h` items with one padding coordinate. For `0<a<1` and nonempty banks, these are the only equality patterns.

## Fixed-inventory optimum

For inventory `n_r`, write `K=sum n_r` and `W=sum (r-1)n_r`. Summing the pattern inequalities gives

```
total bank cost >= (C+h*epsilon)*W/D - epsilon*K.
```

Any exact integer packing made exclusively of the equality patterns attains this bound. Its number of banks is `W/D` and its number of padded banks is `h*W/D-K`. Integer replication scales both the bound and such a packing exactly.

## Necessary and sufficient conditions for width 73

For ranks in `{4,5,7,8,9}`, let `K=sum n_r`, `W=sum (r-1)n_r`. An integer packing attaining the bound exists exactly when

```
W is divisible by 64,
P = 9W/64 - K >= 0,
n_8 >= n_4,
n_8 + 2n_7 >= 3n_4.
```

For an attaining packing, the preceding equality characterization gives `B=W/64` banks, `P=9B-K` one-coordinate padded banks and `F=K-8B` full banks. These counts are necessary; `F>=0` follows from all ranks being at most9.

A full bank has nine items of mass73. Replacing each item's rank `r` by its deficit `9-r` therefore leaves exactly8 deficit units per full bank. The available deficits are5,4,2,1,0. A deficit5 cannot share a bank with another5 or a4, and its remaining3 must be either `2+1` or `1+1+1`. Thus each rank4 item needs at least one rank8 item, and all rank4 items together need at least `3n_4` units from ranks7 and8. This proves necessity of the two capacity inequalities. A padded equality bank is eight rank9 items and cannot absorb another rank.

For sufficiency, put `x=min(n_4,n_7)` rank4 items with one rank7 and one rank8 item each. Put the remaining `n_4-x` rank4 items with three rank8 items each. The two capacity inequalities ensure enough rank8 items: the total used is `3n_4-2x`. Fill each of these banks to nine items with rank9 items after all nonzero deficits have been assigned.

The residual deficit1 count is even. This follows because the original total deficit is `9K-sum r*n_r = 8F`, and the already completed banks remove multiples of8. Pair the remaining deficit1 items into deficit2 blocks. Combine those with the original remaining deficit2 items; their total number is even because the remaining total deficit is divisible by4. Pair them into deficit4 blocks, combine with the original deficit4 items, and pair again into deficit8 blocks. The total is divisible by8, so this last pairing is exact. Each resulting block has at most8 original items and can be filled to nine with rank9 items.

These blocks make exactly `F` full banks. If `L` is the number of non-rank9 items, full banks need `9F-L` rank9 items. The inventory contains

```
n_9 = 9F - L + 8P,
```

because `K=9F+8P`. Since `P>=0`, there are enough rank9 items. Exactly `8P` remain for the padded banks. This constructs an equality witness and proves sufficiency. The empty inventory has the empty packing.

The implementation keeps multiplicities compressed. Each pairing operates on a bounded number of pattern types, so the number of integer operations does not grow with item counts. Integer bit complexity still grows with the bit length of those counts. It uses neither floating arithmetic nor an optimization dependency.

## Minimum replication and architecture constraints

For counts per replica, the two capacity inequalities and the sign of `9W-64K` are invariant under positive replication. If any fails, no replica count reaches this equality bound. This does not mean ordinary nonsaturating bank packing is impossible.

Otherwise the only remaining condition is `64 | T*W`. The least positive replica count is exactly

```
T_min = 64 / gcd(W,64).
```

If the surrounding architecture requires a multiple of `A`, the least admissible count is `lcm(T_min,A)`. The existing PR403 expander requires multiples of8. PR404's packing minimum is4, but its existing architecture minimum is8. The optimizer exposes both numbers and never claims a smaller packing witness validates a changed global architecture.

## Connection to the actual paid moment

Take `a=1-b` and `epsilon=32*m^2*10^-16`. This epsilon is the retained rank-one fallback charge per paid child, not an omitted lower-order term. Multiplying the normalized moment minus one by the positive denominator `stock*m^a` gives

```
sum_paid count*r^a + epsilon*sum_paid count - stock*m^a.
```

For a fixed local ledger and `L` stages, the packing-dependent part is `L*sum_banks(p^a+epsilon*1[p>0]-m^a)`. Adding the fixed residual rank mass converts it to the bank cost just bounded. Hence an attaining packing minimizes the full moment numerator for every `0<b<1`, including fallback. Its certified coarse root cannot be improved by repacking that fixed inventory or by integer replication alone.

This theorem does not prove validity of the multiplication supplier or optimize entrance choices. The full local/phase/routing/invoice checks are separate. The optimizer supplies a bank witness and its exact optimality certificate. Every changed supplier still needs separate local, phase, ownership, invoice and outer verification.
