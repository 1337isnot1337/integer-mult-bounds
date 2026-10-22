# Sixteen states are minimal for this dyadic rectangular completion

This is a scoped algebraic lower bound, not a lower bound for all H callers.
Let D=Z[1/2], and retain J=I-R^t R/4 with R R^t=56 I_8.
Consider A=[J,R^t U] and B=[J;V R], where U is 8-by-h and V is h-by-8.
Assume each state coupling is obtained from the primitive eight-state coupling
by adjoining uncoupled state coordinates and an invertible basis over D.
Both U and V then have rank eight after reduction modulo three: invertible
dyadic changes remain invertible over F_3, and 56 is nonzero modulo three.

The right-inverse identity AB=I forces U V=-3 I_8. To see this, use
J^2-I=3 R^t R and cancel the injective R^t and surjective R over Q.
Modulo three, U V=0. Thus image(V) lies in kernel(U). These spaces have
dimensions 8 and h-8, respectively, and h must be at least 16.

The bound is attained algebraically by U=[I,2I], V=[I;-2I]. Their product
is -3I; both have rank eight modulo three and integer unimodular completions:
[[I,2I],[0,I]] and [[I,0],[-2I,I]]. The emitted rectangular native words
realize these two different changes at their actual common helper charts.
They are not claimed to be raw inverse-transpose words.

Allowing rational basis inverses changes this result: h=8, U=I and V=-3I
satisfies the right-inverse identity, but V has rank zero modulo three and
its inverse needs division by three. That is outside the dyadic invertible
basis hypothesis. The theorem also does not cover changed J, nonprimitive
native couplings, operator-valued state maps, or other recursive callers.

Sixteen-state minimality does not solve the width-eight/width-nine mismatch,
state restoration, independent Gaussian output credit or the global moment.
No kappa improvement follows from it alone.
