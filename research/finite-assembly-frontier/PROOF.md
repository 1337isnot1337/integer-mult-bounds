# A finite witness below every rational assembly ceiling

This is a parameter-selection result for the retained balanced outer engine.
It changes neither supplier. Supplier admission, the weighted finite bootstrap,
and the inherited compiler, common-grid, restored-work, precision and analytic
interfaces remain premises. It does not prove unconditional integer
multiplication complexity or global optimality over other assemblies.

Let the admitted rational bit and complex caps be c and b. Write

    a0 = 384599 / 10^10,   u = min(b,c),   F(x) = x/(1+x).

Assume a0 < u and b < 1/32. The supremum of the retained family, using seeds
strictly below both caps, is F(u). Every rational 0 < k < F(u) has a finite
constructible witness. The endpoint itself is not admitted.

## Constructive choice

Put t=k/(1-k), s=(u+max(a0,t))/2, and beta=(b-s)/(2b). Then

    a0 < s < u,   0 < beta < 1,   s < (1-beta)b = (b+s)/2.

Starting at a0, apply the inherited bootstrap a[j+1]=(1-s)s+s*a[j] until a[j]>t.
Its closed form is a[j]=s-(s-a0)*s^j. Since 0<s<1/32, the loop terminates.
For example, when t>=a0, any integer N with

    2^N > (s-a0)/(s-t)

is a sufficient finite upper bound on the number of iterations. If a0>t,
zero iterations suffice. This uses a finite fixed number of bootstrap levels
for each supplied rational target, not a limit in the complexity construction.

For each step a'=a[j+1], check the original four positive gaps

    s-a',  1-a'-s,  1-a'-s*(1-a[j]),  1-s.

They are positive because a[j]<a'<s<1/32. If C<=2^B is an admitted finite
coefficient charge, let g be their minimum and choose the positive integer

    L = max(1, ceil(36/g^2), ceil(2*(4+B)/g)).

Then L*g^2>=36 and L*g>=2*(4+B), exactly the retained finite cutoff conditions.
The solver checks both inequalities rationally. A smaller target may need
fewer levels and smaller cutoffs; no practical input-size benefit is claimed.

At termination write a=a[j] and d=F(a)-k>0. Set

    eta = min(1/16, d/(6*a)).

For q=a*(1-2*eta), the compact outer margin is

    M = (1-eta)*q/(1+q).

Direct subtraction gives

    F(a)-M = a*eta*(3+a-2*(1+a)*eta) /
             ((1+a)*(1+a-2*a*eta)) < 3*a*eta <= d/2.

Consequently M>k. Both eta and beta are strictly positive.

## All outer inequalities remain strict

The unmodified, source-pinned `vendor/outer.py` checks all 47 inequalities.
The following bounds also prove that the constructor always reaches an
accepted tuple under its stated premises, rather than merely trying one.

For 0<a<1/32 and 0<eta<=1/16, let epsilon=(1-eta)/(1+q). Then

    0 < q < a < 1/32,   10/11 < epsilon < 1,
    c_outer = q+eta/4 < 3/64,
    M = epsilon*q < a,   r = M+eta/2 < 1/16,
    delta = eta/8 > 0.

The internal saving is a because b>a. The leaf saving (1-beta)b exceeds s>a.
Thus q is strictly below both savings, lambda lies strictly between 1-a and
1-q, and the compact leaf and reservation inequalities are positive.
The remaining geometric identities are

    1-epsilon = M+eta,
    1-epsilon-r = eta/2,
    1-epsilon*(1+c_outer) = eta*(1-epsilon/4),
    c_outer-q = eta/4.

The cell gap is greater than 10/11-1/2, the short-record gap is greater than
10/11-1/32, and the artificial-boundary gap is greater than 7. Also r<1/4,
delta<1/8, and all parameter positivity and unit bounds follow above.
The literal scalar gap is 1 and the retained row gap is 23971789/25.
Of the seven final margins, the compact phase margin is M; the balanced
prefix is M+eta, Gaussian arithmetic is M+3*eta/8, and scalar work is
M+7*eta/8. Coordinate movement and bulk exposure equal a>M, while dimension
equals epsilon>M. Therefore all seven exceed k, proving all 47 constraints.

## Ceiling and exact grid maximality

Every finite witness in this family has a<s<u and eta>0, hence M<F(a)<F(u).
Conversely the construction above reaches every rational target below F(u).
The claim is relative to the given supplier caps and this assembly family;
improving a supplier or changing the outer assembly may raise the ceiling.

For a rational grid g>0, write F(u)/g=p/q in lowest terms. The greatest
admissible grid point is

    k = g * floor((p-1)/q),

provided k>0. The formula is strict even if the supremum lies exactly on the
grid. The next grid point is at or above the supremum, so cannot be obtained
inside this family. The implementation rejects the endpoint and larger targets.
