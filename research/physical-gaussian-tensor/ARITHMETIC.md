# Exact arithmetic adaptations

Jose Manuel (`jmbarrancoml`), with substantial OpenAI Codex assistance.
I retain the word, FFT, phase and Gaussian sources through the authenticated
archives in `inputs/`. I describe the new arithmetic below. I have not yet
completed the whole tensor replay or its conditional proof.

## Byte products

In `tensor_word.py` I use eight fixed shift/add phases to multiply two byte
controls. The product is at most65025. During a schoolbook digit update,

```
old_byte + first_byte * second_byte + carry <= 255 + 65025 + 255 = 65535.
```

I write the low byte and retain a carry at most255. I keep arbitrary-width
operands and accumulated digits on physical tapes. I zero-extend the final
partial operand byte and normalize the result after the final row.

After processing the first `i` bytes of the first operand, I retain its exact
partial product with the complete second operand. For the next row I shift
the starting position by one byte. The existing highest occupied byte lies
within this row's second-operand span. After those updates I therefore reach
the right marker and append one carry byte. I walk back exactly eight times
the encoded second-operand byte count, reaching the next row's start.

I use the retained amortized ripple countdown for that walk. For operand
bit lengths `a,b`, I spend `O((a+1)(b+1))` time and `O(a+b+1)` space, including
input copies, normalization and cleanup. I need a fixed number of tapes.

`ByteWordProduct` fixes the leaf cutoff at1024 bits. Above that cutoff I call
the retained recursive entry, continuation and output serializer. I check
both operand widths before taking the zero shortcut. The fixed leaf change
preserves that recursion's asymptotic bound.

In `tensor_counts.py` I use the same digit calculation for arbitrary-width
setup products. I copy both operands, so an aliased square still has two
independent read cursors. I specialize `Count.product` only for the duration
of `TensorPreparation.run` and restore the exact original class method on
exit, including exceptions. I retain the coefficient formulas and exact
rational operations. I do not decode a complete operand into a host integer.

## Binary digit-pair square roots

In `tensor_twiddles.py` I scan the operand from its most significant end in
pairs, with a single initial bit for odd lengths. Suppose I have processed
the prefix `x` and retained `q=floor(sqrt(x))`, `r=x-q*q`. Then
`0<=r<2q+1`. Appending a digit `d` in `0..3` gives

```
4x+d = (2q)^2 + (4r+d).
```

The next root is either `2q` or `2q+1`: `4x+d < (2q+2)^2`. I select the
second case exactly when `4r+d >= 4q+1`, subtracting `4q+1` from the remainder.
That proves the invariant by induction and the exact integer square root at
the final digit. I keep `q` and `r` on encoded tapes; only the two-bit digit
and the parity of the operand length enter finite control.

For an `n`-bit input I make `O(n)` iterations, each with `O(n)` scans. I spend
`O(n²)` time and `O(n)` space on a fixed tape inventory. I restore the borrowed
input head after stepping back from its left marker.

## Inward roots of unity at fixed small orders

For any admitted precision `P>=16`, set

```
B = 2^P
U = 2^(2P-1)
m = floor(sqrt(2^(4P-3)))
h = floor(sqrt(U))
c = floor(sqrt(U+m))
s = floor(sqrt(U-m-1)).
```

Write `z=sqrt(2^(4P-3))`. Irrationality gives `m<z<m+1`. The exact squared
numerators of `cos(pi/8)` and `sin(pi/8)` on the `B` grid are `U+z` and `U-z`.
Each lies between consecutive integers. Since no integer square lies strictly
between consecutive integers, I obtain

```
c = floor(B*cos(pi/8))
s = floor(B*sin(pi/8))
h = floor(B/sqrt(2)).
```

I need the minus one in the sine radicand: the upper endpoint `U-m` could
itself be an integer square. I apply signs after flooring nonnegative
magnitudes, preserve exact axis values and select orders2,4,8 from order16.
Each component has no larger magnitude than its exact counterpart and an
error below `2^-P`. Each complex value therefore has norm at most one and
error below `sqrt(2)*2^-P < 2*2^-P`.

These estimates meet the retained Twiddles and positive PhaseBasis contracts.
I retain the original run methods, including signed emission, norm checks,
protected returns and cleanup. I bind their `TwiddlePlan` constructor to the
authored `SmallOrderPlan`. For orders above16 that plan delegates to the
original setup and value methods. I retain no table across calls.

The small-order setup uses a fixed number of encoded square roots and scans,
so I charge `O(P²)` time and `O(P)` space. I make no change to the general-order
setup allowance. The new producer need not reproduce a Taylor enclosure's
bytes, though the checked complete p48 chirp did reproduce them on this
fixture.

## Local evidence and limits

I checked all65536 byte-control pairs,52 physical word products through2049
bits, recursive parents and an actual FFT-word call. I also checked311 setup
products, including aliasing and class-method restoration after an exception.
For digit-pair roots I checked540 cases through1024-bit square boundaries
against host integer square roots. I checked32 complete signed phase tables
and four positive phase bases at precisions16,48,54,113 against separate
rational radical enclosures.

The full64-coordinate p48 chirp passed its separate dense Fourier enclosure
and reproduced hash
`0d77ae678a513059c5e6153b4ba85fc273dabcbfbf58155ca69e514c609f5297`.
On this host I measured52.461 seconds with both adaptations,475.041 seconds
with only the byte leaf, and519.754 seconds with the earlier fixed1024-bit
leaf. I used the disclosed exact p48 metadata specialization and retained
finite q2 children. These timings do not establish production-scale behavior
or a new multiplication exponent. I have not obtained independent human
review or formal verification.
