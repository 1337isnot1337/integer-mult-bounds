# Local cost and the unfilled physical allowance

These are constructive counts for the **actual eighth collector and named
consumer operations** in the frozen source word. They do not price the whole
word, produce the required input values, or admit a recursive supplier.
[PROOF.md](PROOF.md) distinguishes the original rejected coefficient point
from the all-$B_9$ admitted family. The complete input and predecessor pins
are in [SOURCES.json](SOURCES.json).

## 1. Eighth collector: events 2114 to 2128

Let $N=512$,
$O_0=(257,129,65,33,16,9,5,2)$, and $P_0=(400)$.
The source initializes owned scratch C in $O_0$, gathers D4 through D0,
transports C to $P_0$, adds C into Q0, transports C back to $O_0$,
ungathers D0 through D4, and erases C at zero. The ten D reads leave their
sources unchanged. Q0 is the mutable query.

| Source or component operation | Count |
|---|---:|
| D gathers / ungathers | 5 / 5 full-bank unit ADDs |
| Q0 readout | 1 full-bank unit ADD |
| Native calls | 2, each rank 7 |
| Native rank mass | 14 |
| Native pair applications | $2\cdot7\cdot256=3584$ |
| Native component ADD/SUB evaluations | $8\cdot3584=28672$ |
| Field real ADD/SUB evaluations | $11\cdot1024=11264$ |
| Component ADD/SUB subtotal | 39,936 |
| Native signed-floor half evaluations | $4\cdot3584=14336$ |
| Native Gaussian quarter turns | 3,584 |
| Actual monomial wrappers | 4 |
| Owned Gaussian scratch bank / zero erasure | 1 / 1 |

The native-only child tariff is $2\cdot7^s$ if a rank-r child costs $r^s$.
Wrapper implementation, physical access, zero supply and control are
additional. The component subtotal is not a complete strict-register or
physical tape invoice. A literal native pair can involve nonexact individual
floor halves while its completed output agrees exactly with the ideal map
on the admitted Newton module.

The archive specifies separate forward and reverse recipes. The actual four
wrappers, in execution order, have:

| Event / wrapper | Permutation cycles | Ordinary Gaussian payload SWAPs |
|---|---:|---:|
| 2120 / right | 64 | 448 |
| 2120 / left | 64 | 448 |
| 2122 / right | 128 | 384 |
| 2122 / left | 48 | 464 |
| **Total** | **304** | **1,744** |

A length-l cycle needs l−1 ordinary two-word swaps, so the total is
$4N-304=1744$. This is not the different zero-scratch cycle schedule.
Each wrapper has 128 input-address entries of each phase $1,i,-1,-i$;
the aggregate has 512 of each. Phases are evaluated on the input address
using the source's strict-upper-triangle quadratic convention. The
histogram is an inventory, not an operator-identity test. The actual reverse
wrappers cannot be replaced in this invoice by an assumed paired inverse
of the forward wrappers.

## 2. Named consumer updates and restoration

| Event | Actual source operation | Frame | Local real arithmetic |
|---|---|---|---:|
| 3025 | $G0\mathrel{+}=Q0$ | $P_0$ | 1,024 ADDs |
| 4104 | $G0\mathrel{-}=Q0$ | $F$ | 1,024 SUBs |
| 4241 | $Q0\mathrel{-}=Y90/4$ | $F$ | 1,024 SUBs, plus the division/restoration below |

Here $F=(256,128,64,32,16,8,4,2,1)$.
These are three separated chronological operations, not an adjacent
self-contained return program. The source still needs all intervening
frame paths and required reads. In particular, the X0 delivery at event
3278, X0's sign and final chart, and all other affected outputs are
additional to this table.

The admitted family proves $Y90\in4B_9$ at event 4241. If the physical
contract permits temporarily mutating that donor, each real component can
be divided exactly twice, used in the signed ADD, and doubled twice to
restore it. For the bank this adds **2,048 exact halves and 2,048 restoring
doublings**. A strictly read-only donor needs a separately supplied and
priced divided-copy/cleanup implementation. Divisibility alone grants no
ownership permission.

Together, the collector and these three scalar operations have a
**43,008 component ADD/SUB subtotal**, plus the listed native floor halves,
quarter turns, wrappers, exact donor halves and restoration doublings.
No allocation, control, routing or bit-complexity tariff is hidden in that
subtotal.

## 3. The existing X0 endpoint adapter is reused, not charged twice

X0 is among the 93 banks omitted from PR3446's projection. PR3469 already
binds its initial frame $(386)$ to final frame F with a rank-eight
adapter. It is one of the 52 rank-eight entries in the existing profile
$52\cdot8^s+41\cdot9^s$, whose rank mass is 785.

When assembling a projected normalized completion, that X0 adapter must be
included **once** as part of the credited 93-bank boundary. It is not an
additional rank-eight cost on top of that profile. When interpreting the
original full word, its actual X0 transports already occur in the source;
the endpoint adapter is not appended a second time.

For $0\leq s\leq1$, the existing tariff is sharp only in its stated separate-bank,
nine-axis native model with free affine quadratic-phase monomials.
It does not price common-frame scalar acquisition, the monomial
implementation, ownership, or routing. Nor does it authorize replacing
the original interleaved transports by a single terminal adapter across
arbitrary intervening ADDs.

## 4. Complete allowance and family decision

| Obligation | Status in this result |
|---|---|
| Exact source-event coefficients and compatible recorded frames | Bound and checked |
| Eighth collector's numerical dirty compensation and C zero exit | Proved under the inherited native/module premises |
| Admitted all-$B_9$ family and actual X0 observation | Proved by the scalar-coefficient induction and phase-correct charts |
| Local collector and three-update arithmetic | Constructive component counts above |
| X0's omitted endpoint chart adapter | Credited PR3469 binding; counted once |
| A physical producer of the 52 PR3467 coefficient meanings | Unknown |
| Acquisition of the D/Y sources in the required frames | Additional; no complete physical allowance supplied |
| Physical permissions, temporary ownership, addresses and routing | Unknown |
| Complete scalar/native lowering, zero supply, controller and bit costs | Unknown |
| Actual caller component heights and finite storage widths | Unknown; the exact reference uses unbounded integers |
| Complete recursive supplier budget and outer transfer | Unknown |

The fourfold family lies in the strong entrance $S=(4B_9)^{52}$.
Its required X0 output does not factor through the five first-collector
readouts, but it establishes no benefit from the larger quotient $L/S$.
No positive budget is inferred from a module index or from ignoring
additional required outputs.

The inherited [PR #3423](https://github.com/CrocSwap/integer-mult-bounds/pull/3423)
599/584 stop remains conditional on its original fixed profile and coverage.
This package changes neither those hypotheses nor the selected frontier.
An optimistic budget for a different caller does not supply the missing
allowance for this coefficient interface.

**Decision: finish this interface audit and stop dependent construction.**
A further construction needs an actual producer/consumer contract and a
complete allowance covering the missing rows. Unknown costs are not zero.

Credit ywz65/PR2586 for the word/native recipes; Arham Tahir/PR2665 for
retention; the PR3025/PR3382 signed-floor and Newton lineage for component
semantics; PR3554 for the owned-donor quarter lowering and assigned
handoffs; Hiroki Kumazaki/PR3446 for the port projection; and Nick
Petalas/PR3416/#3462/#3469 for exact covariance, normalized completion
and the existing endpoint adapter. These remain scoped predecessor
results, not newly admitted physical suppliers.
