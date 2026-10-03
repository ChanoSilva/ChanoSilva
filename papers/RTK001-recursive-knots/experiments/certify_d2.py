#!/usr/bin/env python3
"""Computer-assisted proof of the depth-two case of (H_c), c = 1/2, for the default family (2,3).

What is certified (see d2_certified_derivation.md and d2_certified.tex):
  For every r_1 in (0, 1/2] and every r_2 in (0, r_1/2] -- hence for every f <= 1/2, every admissible
  r_2 <= f thick(K_1) (thick(K_1) <= r_1 by Prop. prop:upper), every phase phi_1, phi_2 and every initial
  normal of the Bishop frame of K_1 --
        r_2 * kappa_max(K_2) <= r_2 * RHS(eq:kaprec) <= B_cert < 2,
  so minRad(K_2) > r_2/2 and, by Theorem thm:Hc(c), thick(K_2) >= r_2/2.

Route.  Proposition prop:curvrec bounds kappa_max(K_2) by four numbers of the BASE K_1 only -- v_min, kappa_max,
nu = sup|v'|/v^2, mu = sup|Pi_perp d(kappa)/d sigma| -- and by m = q/p - alpha/2pi, which lies in [1, 2) a priori
(|alpha| <= pi); the bound is increasing in m, so m = 2 is used and the Bishop frame of K_1 is not needed at all.
K_1 is an explicit trigonometric polynomial (period-2pi parameter s, t = 2s):
      x + i y = e^{2is} + (r_1/2i)(e^{5is} - e^{-is}),   z = r_1 cos 3s,
so v, kappa, nu, mu are explicit functions of (s, r_1).  They are enclosed on boxes (s-interval x r_1-interval)
by interval arithmetic:
  * cos(ks), sin(ks) on each s-box: mpmath.iv (rigorous, 80 bits), endpoints rounded outward to binary64;
  * +, -, *, /, sqrt: numpy binary64 (IEEE-754, correctly rounded) followed by one-ulp outward rounding
    (np.nextafter) of every endpoint -- a valid enclosure because round-to-nearest errs by < 1 ulp;
  * the boxes cover [0, 2pi] x [r_lo, r_hi] (s-box endpoints are themselves rigorous enclosures of 2pi j/N).
The final inequality is evaluated in the same interval arithmetic with the monotonicity of eq:kaprec in each input.

Bonus (not needed for the bound): an enclosure of the holonomy alpha_2 of K_1 through the total torsion
(Bishop = Frenet rotated by -int tau dsigma; K_1 has kappa > 0), giving a certified m_2.

Also: a plain floating-point evaluation on a fine point grid (NOT a proof) to show how tight the enclosures are.
Output: certify_d2.json (all numbers for the text) and stdout (saved as certify_d2_output.txt).
Deterministic, no randomness.  About 20-40 s CPU.
"""
import json
import os
import platform
import time
from fractions import Fraction

import mpmath as mp
import numpy as np
from mpmath import iv

iv.prec = 80
HERE = os.path.dirname(os.path.abspath(__file__))
DN = lambda x: np.nextafter(x, -np.inf)   # noqa: E731
UP = lambda x: np.nextafter(x, np.inf)    # noqa: E731


# ---------------------------------------------------------------------------------------------------------------
# minimal interval arithmetic on numpy arrays, outward rounding by one ulp after every operation
# ---------------------------------------------------------------------------------------------------------------
class Iv:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = np.asarray(lo, dtype=float)
        self.hi = self.lo if hi is None else np.asarray(hi, dtype=float)

    def __add__(self, o):
        o = _iv(o)
        return Iv(DN(self.lo + o.lo), UP(self.hi + o.hi))

    __radd__ = __add__

    def __sub__(self, o):
        o = _iv(o)
        return Iv(DN(self.lo - o.hi), UP(self.hi - o.lo))

    def __rsub__(self, o):
        return _iv(o) - self

    def __neg__(self):
        return Iv(-self.hi, -self.lo)          # exact

    def __mul__(self, o):
        o = _iv(o)
        p = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Iv(DN(np.minimum.reduce(p)), UP(np.maximum.reduce(p)))

    __rmul__ = __mul__

    def recip(self):
        if not np.all((self.lo > 0) | (self.hi < 0)):
            raise ZeroDivisionError("interval contains 0")
        return Iv(DN(1.0 / self.hi), UP(1.0 / self.lo))

    def __truediv__(self, o):
        return self * _iv(o).recip()

    def __rtruediv__(self, o):
        return _iv(o) * self.recip()

    def sq(self):
        a, b = np.abs(self.lo), np.abs(self.hi)
        mx = np.maximum(a, b)
        mn = np.where((self.lo <= 0) & (self.hi >= 0), 0.0, np.minimum(a, b))
        return Iv(np.maximum(DN(mn * mn), 0.0), UP(mx * mx))

    def sqrt(self):
        return Iv(np.maximum(DN(np.sqrt(np.maximum(self.lo, 0.0))), 0.0), UP(np.sqrt(self.hi)))

    def mag(self):                              # upper bound of |x|
        return np.maximum(np.abs(self.lo), np.abs(self.hi))


def _iv(x):
    if isinstance(x, Iv):
        return x
    x = float(x)                                # only exactly representable constants are passed (integers, 1/2)
    return Iv(x, x)


def vdot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vcross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def vnorm2(a):
    return a[0].sq() + a[1].sq() + a[2].sq()     # sum of squares: lower bound >= 0


def vnorm(a):
    return vnorm2(a).sqrt()


def vscale(c, a):
    return [c * x for x in a]


def vsub(a, b):
    return [x - y for x, y in zip(a, b)]


def mp2f(x):                                    # outward float enclosure of an mpmath interval
    return float(DN(float(x.a))), float(UP(float(x.b)))


# ---------------------------------------------------------------------------------------------------------------
# K_1 and its derivatives on boxes
# ---------------------------------------------------------------------------------------------------------------
KS = (1, 2, 3, 5)


def trig_boxes(Ns, smax_frac):
    """s-boxes [smax*j/Ns, smax*(j+1)/Ns], smax = 2*pi*smax_frac (smax_frac = 1 or 1/3); rigorous cos/sin(k s)."""
    lo = {k: (np.empty(Ns), np.empty(Ns)) for k in KS}
    hi = {k: (np.empty(Ns), np.empty(Ns)) for k in KS}
    fr = Fraction(smax_frac)
    smax = 2 * iv.pi * fr.numerator / fr.denominator
    for j in range(Ns):
        sb = iv.mpf([j, j + 1]) * smax / Ns
        for k in KS:
            c, s = iv.cos(k * sb), iv.sin(k * sb)
            lo[k][0][j], hi[k][0][j] = mp2f(c)
            lo[k][1][j], hi[k][1][j] = mp2f(s)
    return {k: (Iv(lo[k][0][None, :], hi[k][0][None, :]), Iv(lo[k][1][None, :], hi[k][1][None, :])) for k in KS}


def rot_i(X, Y, j):
    """multiply X + iY by i^j (exact)."""
    j %= 4
    return [(X, Y), (-Y, X), (-X, -Y), (Y, -X)][j]


def k1_derivs(E, r, jmax=3):
    """D_j = d^j K_1/ds^j, j = 1..jmax, as lists of 3 Iv (broadcast: r has shape (nr,1), E entries (1,Ns))."""
    C1, S1 = E[1]
    C2, S2 = E[2]
    C3, S3 = E[3]
    C5, S5 = E[5]
    out = {}
    for j in range(1, jmax + 1):
        ax, ay = rot_i(C2, S2, j)
        bx, by = rot_i(C5, S5, j)
        cx, cy = rot_i(C1, -S1, j)
        sgn = -1.0 if j % 2 else 1.0                   # (-1)^j
        Wx = float(5 ** j) * bx - sgn * cx
        Wy = float(5 ** j) * by - sgn * cy
        x = float(2 ** j) * ax + r * (0.5 * Wy)          # (-i/2) W = (W_y/2, -W_x/2)
        y = float(2 ** j) * ay - r * (0.5 * Wx)
        cz = [C3, -S3, -C3, S3][j % 4]
        z = r * (float(3 ** j) * cz)
        out[j] = [x, y, z]
    return out


def base_quantities(D, torsion=False):
    """Pointwise enclosures of v, kappa, nu_pt = |v'|/v^2, mu_pt = |Pi_perp dkappa/dt|/v, torsion*v."""
    D1, D2, D3 = D[1], D[2], D[3]
    v2 = vnorm2(D1)
    v = v2.sqrt()
    v3 = v2 * v
    g12 = vdot(D1, D2)                       # = v v'
    g13 = vdot(D1, D3)
    X = vcross(D1, D2)
    nX2 = vnorm2(X)
    kap = nX2.sqrt() / v3                    # |D1 x D2| / v^3
    nu = g12 / v3                            # v'/v^2
    P2 = vsub(D2, vscale(g12 / v2, D1))      # Pi_perp D2  (= v^2 kappa-vector)
    P3 = vsub(D3, vscale(g13 / v2, D1))      # Pi_perp D3
    Y = vsub(P3, vscale(3.0 * g12 / v2, P2))  # = v^2 Pi_perp dkappa/dt
    mu = vnorm(Y) / v3
    out = dict(v=v, kap=kap, nu=nu, mu=mu)
    if torsion:
        out["tv"] = vdot(X, D3) / nX2 * v      # torsion * speed  (= -theta' of Bishop vs Frenet)
    return out


# ---------------------------------------------------------------------------------------------------------------
# the bound of eq:kaprec, multiplied by r_2
# ---------------------------------------------------------------------------------------------------------------
SQ2 = iv.sqrt(2)
G_SQ2_HI = mp2f(SQ2 * (SQ2 ** 2 + 2) / (SQ2 ** 2 + 1) ** iv.mpf(1.5))[1]     # g(sqrt 2) = 4 sqrt2/(3 sqrt3)
SQ2_LO = mp2f(SQ2)[0]


def g_iv(z):
    z2 = z.sq()
    return z * (z2 + 2.0) / ((z2 + 1.0) * (z2 + 1.0).sqrt())


def kaprec_times_r(K, V, Nu, Mu, r2, m):
    """Upper bound of r2*[K G(z')/(1-eps) + 1/(r2(1+z'^2)) + lam(Nu(1+eps)+r2 Mu)/(1-eps)^3], eps = r2 K,
    lam = r2 m/V, z' = V(1-eps)/(r2 m).  K, Nu, Mu, r2, m are upper bounds, V a lower bound (floats); the
    expression is non-decreasing in K, Nu, Mu, r2, m and non-increasing in V (see the derivation, Sec. 2)."""
    K, V, Nu, Mu, r2, m = (Iv(float(a)) for a in (K, V, Nu, Mu, r2, m))
    eps = r2 * K
    om = 1.0 - eps
    if not om.lo > 0:
        return dict(ok=False)
    lam = r2 * m / V
    zl = float((V * om / (r2 * m)).lo)                # lower bound of zeta'
    G = G_SQ2_HI if zl <= SQ2_LO else float(g_iv(Iv(zl)).hi)   # G non-increasing; g decreasing on [sqrt2, inf)
    Gi = Iv(G)
    t1 = r2 * K * Gi / om
    t2 = 1.0 / (1.0 + Iv(zl).sq())
    t3 = r2 * lam * (Nu * (1.0 + eps) + r2 * Mu) / (om * om * om)
    tot = t1 + t2 + t3
    return dict(ok=True, eps_hi=float(eps.hi), lam_hi=float(lam.hi), zeta_lo=zl, G_hi=G,
                term1=float(t1.hi), term2=float(t2.hi), term3=float(t3.hi), total=float(tot.hi))


def r_interval(x):
    """outward binary64 enclosure of the real number x given as a decimal string."""
    return mp2f(iv.mpf(x))


def certify_point(rstr, f, E, Ns_full, smax_frac):
    """r_1 = rstr (decimal), f: certify r_2 in (0, f r_1]."""
    rlo, rhi = r_interval(rstr)
    r = Iv(np.array([[rlo]]), np.array([[rhi]]))
    D = k1_derivs(E, r, 3)
    Q = base_quantities(D, torsion=(smax_frac == 1))
    V = float(Q["v"].lo.min())
    K = float(Q["kap"].hi.max())
    Nu = float(Q["nu"].mag().max())
    Mu = float(Q["mu"].hi.max())
    r2 = float(UP(f * rhi))
    out = dict(r1=rstr, f=f, r2_max=r2, Ns=Ns_full, s_domain=f"[0, 2pi*{smax_frac}]", v_min_lo=V, kappa_max_hi=K,
               nu_hi=Nu, mu_hi=Mu)
    out["bound_m2"] = kaprec_times_r(K, V, Nu, Mu, r2, 2.0)
    # holonomy of K_1 from the total torsion (needs the full period)
    if smax_frac == 1:
        tv = Q["tv"]
        slo = sum(Fraction(float(x)) for x in tv.lo.ravel())
        shi = sum(Fraction(float(x)) for x in tv.hi.ravel())
        width = 2 * iv.pi / Ns_full
        I_lo = iv.mpf(slo.numerator) / slo.denominator * width
        I_hi = iv.mpf(shi.numerator) / shi.denominator * width
        tot = iv.mpf([I_lo.a, I_hi.b])                       # encloses int_0^{2pi} tau v ds
        alpha = -tot                                         # alpha = -total torsion (mod 2pi)
        k = int(round((float(alpha.a) + float(alpha.b)) / 2 / (2 * np.pi)))
        alpha = alpha - 2 * k * iv.pi                        # reduce to (-pi, pi]
        m2 = iv.mpf(1.5) - alpha / (2 * iv.pi)
        out["total_torsion"] = list(mp2f(tot))
        out["alpha2"] = list(mp2f(alpha))
        out["m2"] = list(mp2f(m2))
    return out


def float_check(r1, f, n=200000):
    """Plain floating-point point evaluation (NOT rigorous) on a fine grid, for comparison."""
    s = np.linspace(0, 2 * np.pi, n, endpoint=False)
    E = {k: (Iv(np.cos(k * s)[None, :]), Iv(np.sin(k * s)[None, :])) for k in KS}
    Q = base_quantities(k1_derivs(E, Iv(np.array([[r1]])), 3), torsion=True)
    mid = lambda q: 0.5 * (q.lo + q.hi)      # noqa: E731
    tv = mid(Q["tv"]).ravel()
    return dict(v_min=float(mid(Q["v"]).min()), kappa_max=float(mid(Q["kap"]).max()),
                nu=float(np.abs(mid(Q["nu"])).max()), mu=float(mid(Q["mu"]).max()),
                total_torsion=float(tv.mean() * 2 * np.pi))


def certify_continuum(E, Ns, nr, rmax=0.5, chunk=32):
    """r_1 boxes [rmax*i/nr, rmax*(i+1)/nr] (exact binary endpoints for nr a power of 2), r_2 = r_1hi/2."""
    worst = None
    rows = []
    for i0 in range(0, nr, chunk):
        idx = np.arange(i0, min(nr, i0 + chunk))
        rlo = rmax * idx / nr
        rhi = rmax * (idx + 1) / nr
        r = Iv(rlo[:, None], rhi[:, None])
        Q = base_quantities(k1_derivs(E, r, 3))
        V = Q["v"].lo.min(axis=1)
        K = Q["kap"].hi.max(axis=1)
        Nu = Q["nu"].mag().max(axis=1)
        Mu = Q["mu"].hi.max(axis=1)
        for a, b, Va, Ka, Na, Ma in zip(rlo, rhi, V, K, Nu, Mu):
            res = kaprec_times_r(Ka, Va, Na, Ma, float(b) / 2, 2.0)
            row = dict(r1_lo=float(a), r1_hi=float(b), v_min_lo=float(Va), kappa_max_hi=float(Ka), nu_hi=float(Na),
                       mu_hi=float(Ma), total=res["total"] if res["ok"] else None)
            rows.append(row)
            if worst is None or (row["total"] is None) or row["total"] > worst["total"]:
                worst = row
    return worst, rows


def main():
    t0, c0 = time.time(), time.process_time()
    print("=== certify_d2.py: depth-two case of (H_c), c = 1/2, default family (2,3) ===")
    print(f"python {platform.python_version()}, numpy {np.__version__}, mpmath {mp.__version__}; iv.prec = {iv.prec}")
    # sanity of the 3-fold symmetry used below: K_1(s + 2pi/3) = R_z(4pi/3) K_1(s) (exact identity; checked in float)
    s = np.linspace(0, 2 * np.pi, 97)
    K1 = lambda s, r: np.stack([np.cos(2 * s) * (1 + r * np.sin(3 * s)), np.sin(2 * s) * (1 + r * np.sin(3 * s)),  # noqa
                                r * np.cos(3 * s)], 1)
    a = 4 * np.pi / 3
    R = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    print("symmetry residual max |K_1(s+2pi/3) - R K_1(s)| =", float(np.abs(K1(s + 2 * np.pi / 3, 0.5) - K1(s, 0.5) @ R.T).max()))

    res = dict(meta=dict(python=platform.python_version(), numpy=np.__version__, mpmath=mp.__version__, iv_prec=iv.prec))

    # ---- (A) the concrete family: r_1 = f, all r_2 in (0, f r_1], full period ----
    Ns_full = 4096
    t1 = time.process_time()
    E_full = trig_boxes(Ns_full, 1)
    print(f"\n(A) s-boxes on [0,2pi]: {Ns_full}, trig enclosures in {time.process_time() - t1:.1f} s CPU")
    res["A"] = {}
    for rstr, f in (("0.5", 0.5), ("0.35", 0.35), ("0.25", 0.25)):
        out = certify_point(rstr, f, E_full, Ns_full, 1)
        fc = float_check(float(rstr), f)
        out["float_check"] = fc
        res["A"][rstr] = out
        b = out["bound_m2"]
        print(f"r_1 = {rstr}: certified  v_min >= {out['v_min_lo']:.5f}  kappa_max <= {out['kappa_max_hi']:.5f}  "
              f"nu <= {out['nu_hi']:.5f}  mu <= {out['mu_hi']:.5f}")
        print(f"            float grid  v_min  = {fc['v_min']:.5f}  kappa_max  = {fc['kappa_max']:.5f}  "
              f"nu  = {fc['nu']:.5f}  mu  = {fc['mu']:.5f}   (not rigorous, for comparison)")
        print(f"            total torsion in {out['total_torsion']}, alpha_2 in {out['alpha2']}, m_2 in {out['m2']} "
              f"(float: total torsion {fc['total_torsion']:.6f})")
        print(f"            r_2 <= f r_1 = {out['r2_max']:.6g}: eps <= {b['eps_hi']:.4f}, zeta' >= {b['zeta_lo']:.4f}, "
              f"terms {b['term1']:.4f} + {b['term2']:.4f} + {b['term3']:.4f}")
        print(f"            => r_2 kappa_max(K_2) <= {b['total']:.4f} (m <= 2 a priori);  < 2: {b['total'] < 2}")
    # same with the 3-fold symmetry (s in [0, 2pi/3]) -- must agree up to the box size
    E_third = trig_boxes(Ns_full // 3 + 1, Fraction(1, 3))
    chk = certify_point("0.5", 0.5, E_third, Ns_full // 3 + 1, Fraction(1, 3))
    print(f"    check on [0,2pi/3] ({Ns_full // 3 + 1} boxes), r_1 = 0.5: v_min >= {chk['v_min_lo']:.5f}, kappa <= "
          f"{chk['kappa_max_hi']:.5f}, nu <= {chk['nu_hi']:.5f}, mu <= {chk['mu_hi']:.5f}, bound {chk['bound_m2']['total']:.4f}")
    res["A_third_check"] = {k: v for k, v in chk.items() if k != "float_check"}

    # ---- (B) every r_1 in (0, 1/2], every r_2 in (0, r_1/2]: boxes in (s, r_1), s in [0, 2pi/3] by symmetry ----
    Ns_B, nr_B = 2048, 512
    t1 = time.process_time()
    E_B = trig_boxes(Ns_B, Fraction(1, 3))
    worst, rows = certify_continuum(E_B, Ns_B, nr_B)
    tB = time.process_time() - t1
    print(f"\n(B) r_1 in (0, 1/2]: {nr_B} r_1-boxes x {Ns_B} s-boxes on [0, 2pi/3] ({tB:.1f} s CPU)")
    print(f"    worst box r_1 in [{worst['r1_lo']}, {worst['r1_hi']}]: v_min >= {worst['v_min_lo']:.4f}, kappa <= "
          f"{worst['kappa_max_hi']:.4f}, nu <= {worst['nu_hi']:.4f}, mu <= {worst['mu_hi']:.4f}  ->  "
          f"r_2 kappa_max(K_2) <= {worst['total']:.4f} < 2: {worst['total'] < 2}")
    sel = [rows[i] for i in (0, nr_B // 4 - 1, nr_B // 2 - 1, 3 * nr_B // 4 - 1, nr_B - 1)]
    for rw in sel:
        print(f"    r_1 in [{rw['r1_lo']:.6f}, {rw['r1_hi']:.6f}]: bound {rw['total']:.4f}")
    res["B"] = dict(Ns=Ns_B, nr=nr_B, s_domain="[0, 2pi/3]", worst=worst, all_below_2=all(rw["total"] < 2 for rw in rows),
                    max_total=max(rw["total"] for rw in rows), samples=sel)
    # bonus: the part 'minRad(K_d) > r_d' of Conjecture conj at d = 2, along the family r_1 = f, r_2 <= f r_1 = f^2:
    # on the box r_1 = f in [a, b] use r_2 = b^2 (non-decreasing in r_2) -> largest f_c with r_2 kappa_max(K_2) < 1 for all f <= f_c
    fc = 0.0
    for rw in rows:
        bb = rw["r1_hi"]
        rr = kaprec_times_r(rw["kappa_max_hi"], rw["v_min_lo"], rw["nu_hi"], rw["mu_hi"], float(UP(bb * bb)), 2.0)
        rw["total_family"] = rr["total"]
        if rr["total"] < 1:
            fc = bb
        else:
            break
    res["B"]["f_c_minrad_gt_r"] = fc
    print(f"    family r_1 = f, r_2 <= f^2: r_2 kappa_max(K_2) < 1 (i.e. minRad(K_2) > r_2) certified for every f <= {fc}")
    # and the same with r_2 <= r_1/2 (every f <= 1/2 with r_1 <= f): largest r_1 with bound < 1
    rc = 0.0
    for rw in rows:
        if rw["total"] < 1:
            rc = rw["r1_hi"]
        else:
            break
    res["B"]["r1_c_minrad_gt_r_any_r2_le_r1_half"] = rc
    print(f"    any r_2 <= r_1/2: minRad(K_2) > r_2 certified for every r_1 <= {rc}")

    # ---- (C) for reference: the a priori d = 2 analogue (Remark rem:H3status) with the certified data ----
    a = res["A"]["0.5"]
    lhs = 6 / np.sqrt(13) * a["nu_hi"] + 1 / np.sqrt(13) * a["mu_hi"]
    res["C"] = dict(apriori_lhs_with_cert_data=float(lhs), apriori_rhs=0.6845)
    print(f"\n(C) a priori analogue of eq:tol at d = 2 with the certified data: {lhs:.3f} (needs <= 0.685) -- still fails;"
          f" the certificate uses eq:kaprec with the actual data instead.")

    res["meta"].update(seconds_wall=time.time() - t0, seconds_cpu=time.process_time() - c0)
    with open(os.path.join(os.path.dirname(HERE), "results", "certify_d2.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=str)
    print(f"\nwall {res['meta']['seconds_wall']:.1f} s, CPU {res['meta']['seconds_cpu']:.1f} s; wrote certify_d2.json")


if __name__ == "__main__":
    main()
