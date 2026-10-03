#!/usr/bin/env python3
"""Integrator's check (round 3) of the routing reduction (Theorem 5.12, Remark 5.13, Corollary 5.14).
Not an independent verification: written by the author who integrated the result, from theory/routing_hardness.tex only.
Imports nothing from theory/ or experiments/ (round 4: copied into experiments/ unchanged apart from this docstring).
(1) explicit path sets: generic edge-level C_W vs closed form (eq:CW) at random points;
    multistart SLSQP minimisation of C_W over K in path flows (no concavity lemma):
    no point below the predicted minimum, and the predicted minimum attained;
    projected-gradient Wardrop solver from random starts converges to f*;
    remark rem:interior: witness beats f* for lambda_eps by >= 1/4.
(2) DAG of cor:routingdag: path enumeration, structure, and LPs
    max_f [c_{P_i}(f)-c_{S_i}(f)] and max_f [c_{Z1}(f)-min other switch path] over
    all feasible flows (must be < 0), plus the max flow on an e2 arc (D+2 bound).
Seed 4242.
"""
import itertools, time, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import minimize, linprog

rng = np.random.default_rng(4242)
t0 = time.process_time()


def maxcut(n, E):
    return max(sum(w for i, j, w in E if ((m >> i) & 1) != ((m >> j) & 1)) for m in range(2 ** n))


def instance(n, E, k):
    A = [(i, j, w) for i, j, w in E] + [(j, i, w) for i, j, w in E]
    M = len(A); D = M
    al = [16 * w for _, _, w in A]; bo = 16 * max(w for *_, w in E)
    aD = (2 * k - 1) / (2 * D); B = 2 + 2 * (D + 1) * sum(al)
    edges = {}  # name -> (a,b)
    edges['dz'] = (aD, 0); edges['o'] = (0, bo)
    for m in range(M):
        edges[f'p{m}'] = (0, bo - al[m]); edges[f'e1{m}'] = (al[m], 0)
        edges[f'e2{m}'] = (al[m], 0); edges[f'ez{m}'] = (2 * al[m], 0)
    for i in range(n):
        edges[f's{i}'] = (1, B); edges[f'r{i}'] = (1, 0)
    edges['q1'] = (1, 0); edges['q0'] = (1, B)
    names = list(edges); ix = {e: q for q, e in enumerate(names)}
    a = np.array([edges[e][0] for e in names], float); b = np.array([edges[e][1] for e in names], float)
    comms = []  # (demand, [paths as index lists], star)
    comms.append((D, [[ix['dz'], ix['o']]] + [[ix['dz'], ix[f'p{m}'], ix[f'e1{m}'], ix[f'e2{m}'], ix[f'ez{m}']] for m in range(M)], 0))
    for i in range(n):
        S = [ix[f's{i}']] + [ix[f'e1{m}'] for m, (t, h, _) in enumerate(A) if t == i]
        P = [ix[f'r{i}']] + [ix[f'e2{m}'] for m, (t, h, _) in enumerate(A) if h == i]
        comms.append((1, [S, P], 1))
    comms.append((1, [[ix['q1']] + [ix[f'ez{m}'] for m in range(M)], [ix['q0'], ix['dz']]], 0))
    return dict(A=A, M=M, D=D, al=al, bo=bo, aD=aD, B=B, a=a, b=b, comms=comms, ne=len(names), n=n, k=k)


def incid(I):
    cols = []; owner = []
    for c, (d, paths, s) in enumerate(I['comms']):
        for p in paths:
            v = np.zeros(I['ne']); v[p] = 1; cols.append(v); owner.append(c)
    return np.array(cols).T, np.array(owner)


def costs(I, f, Delta, owner):
    fe = Delta @ f
    C = []
    for c in range(len(I['comms'])):
        gc = Delta[:, owner == c] @ f[owner == c]
        C.append(float(((I['a'] * fe + I['b']) * gc).sum()))
    return np.array(C), fe


def closed_CW(I, x, z, t):
    s = I['aD'] * I['D'] * (I['D'] + 1 - z) + I['bo'] * I['D']
    for m, (i, j, w) in enumerate(I['A']):
        s += I['al'][m] * (4 * t[m] ** 2 + t[m] * (x[i] - x[j] + 2 * z))
    return s


def to_paths(I, x, z, t):
    f = [I['D'] - sum(t)] + list(t)
    for i in range(I['n']):
        f += [x[i], 1 - x[i]]
    f += [z, 1 - z]
    return np.array(f, float)


def fstar(I):
    out = []
    for d, paths, s in I['comms']:
        out += [d if q == s else 0 for q in range(len(paths))]
    return np.array(out, float)


graphs = []
for n in (3, 4, 5):
    for _ in range(6):
        while True:
            E = [(i, j, int(rng.integers(1, 4)) if rng.random() < .5 else 1)
                 for i, j in itertools.combinations(range(n), 2) if rng.random() < .6]
            deg = [0] * n
            for i, j, _ in E: deg[i] += 1; deg[j] += 1
            if E and min(deg) > 0: break
        graphs.append((n, E))

stats = dict(pairs=0, form=0.0, below=0, attained=0, wardrop=0, interior=0, mism=0)
for n, E in graphs:
    mc = maxcut(n, E)
    for k in sorted({1, mc, mc + 1}):
        if k < 1: continue
        I = instance(n, E, k); Delta, owner = incid(I)
        stats['pairs'] += 1
        # (a) closed form vs generic
        for _ in range(20):
            x = rng.random(n); z = rng.random(); t = rng.random(I['M']) * 0.5
            C, _ = costs(I, to_paths(I, x, z, t), Delta, owner)
            stats['form'] = max(stats['form'], abs(C[0] - closed_CW(I, x, z, t)) / max(1, abs(C[0])))
        Cstar = I['aD'] * I['D'] ** 2 + I['bo'] * I['D']
        pred = Cstar + min(0.0, k - 0.5 - mc)
        # (b) multistart SLSQP over K in path flows
        groups = [np.where(owner == c)[0] for c in range(len(I['comms']))]
        dem = [I['comms'][c][0] for c in range(len(I['comms']))]
        cons = [{'type': 'eq', 'fun': (lambda f, g=g, d=d: f[g].sum() - d)} for g, d in zip(groups, dem)]
        fun = lambda f: costs(I, f, Delta, owner)[0][0]
        best = np.inf
        for s in range(25):
            f0 = np.concatenate([rng.dirichlet(np.ones(len(g))) * d for g, d in zip(groups, dem)])
            # start half the runs at random vertices of the weightless commodities
            if s % 2:
                for g, d in zip(groups[1:], dem[1:]):
                    f0[g] = 0; f0[rng.choice(g)] = d
            r = minimize(fun, f0, method='SLSQP', bounds=[(0, None)] * len(f0), constraints=cons,
                         options=dict(maxiter=500, ftol=1e-12))
            fr = np.maximum(r.x, 0)
            for g, d in zip(groups, dem):
                fr[g] *= d / fr[g].sum()
            best = min(best, fun(fr))
        if best < pred - 1e-7: stats['below'] += 1
        if abs(best - pred) < 1e-6: stats['attained'] += 1
        if ((best < Cstar - 1e-6) != (mc >= k)): stats['mism'] += 1
        # (c) Wardrop by projected gradient (path costs), random starts
        fs = fstar(I); ok = True
        L = np.linalg.norm(Delta.T @ np.diag(I['a']) @ Delta, 2)
        for _ in range(3):
            f = np.concatenate([rng.dirichlet(np.ones(len(g))) * d for g, d in zip(groups, dem)])
            for it in range(4000):
                cp = Delta.T @ (I['a'] * (Delta @ f) + I['b'])
                y = f - cp / L
                for g, d in zip(groups, dem):  # projection onto scaled simplex
                    v = y[g]; u = np.sort(v)[::-1]; cs = np.cumsum(u) - d
                    rho = np.nonzero(u - cs / np.arange(1, len(u) + 1) > 0)[0][-1]
                    f[g] = np.maximum(v - cs[rho] / (rho + 1), 0)
            ok &= np.abs(f - fs).max() < 1e-6
        stats['wardrop'] += ok
        # (d) remark rem:interior
        if mc >= k:
            for xb in itertools.product((0, 1), repeat=n):
                if sum(w for i, j, w in E if xb[i] != xb[j]) == mc: break
            t = [Fr(1, 8) if (xb[i] == 0 and xb[j] == 1) else 0 for i, j, _ in I['A']]
            fw = to_paths(I, xb, 0, [float(v) for v in t])
            Cw, _ = costs(I, fw, Delta, owner); Cs, _ = costs(I, fs, Delta, owner)
            Gam = 2 * I['B'] + 2 * k + 1; eps = 1 / (4 * (n + 1) * Gam)
            lam = np.r_[1.0, eps * np.ones(len(Cw) - 1)]
            stats['interior'] += (lam @ (Cw - Cs) <= -0.25 + 1e-9) and (Cw[1:].max() <= Gam)
nonm = sum(1 for n, E in graphs for k in sorted({1, maxcut(n, E), maxcut(n, E) + 1}) if k >= 1 and maxcut(n, E) >= k)
print(f"[explicit] graphs {len(graphs)}, pairs {stats['pairs']} (non-members {nonm})")
print(f"  max rel |C_W generic - closed form (eq:CW)| at 20 random points/pair: {stats['form']:.2e}")
print(f"  multistart SLSQP (25 starts, no lemma): pairs with a point below predicted min: {stats['below']}; predicted min attained: {stats['attained']}/{stats['pairs']}; membership mismatches: {stats['mism']}")
print(f"  projected-gradient Wardrop from 3 random starts converges to f*: {stats['wardrop']}/{stats['pairs']}")
print(f"  rem:interior witness gap <= -1/4 and C_h(y)<=Gamma: {stats['interior']}/{nonm}")
print(f"  CPU so far {time.process_time()-t0:.1f}s")


# ---------------------------------------------------------------- DAG
def dag(n, E, k):
    I = instance(n, E, k); A, M = I['A'], I['M']; H = I['bo'] + 1; Bp = I['B'] + 2 * (M - 1) * H
    arcs = []  # (u,v,a,b,name)
    def arc(name, a, b): arcs.append((('t', name), ('h', name), a, b, name))
    def con(u, v, b=0, name='c'): arcs.append((u, v, 0, b, name))
    arc('dz', I['aD'], 0); arc('o', 0, I['bo'])
    con('oW', ('t', 'dz')); con(('h', 'dz'), ('t', 'o')); con(('h', 'o'), 'dW')
    for m in range(M):
        arc(f'p{m}', 0, I['bo'] - I['al'][m]); arc(f'e1{m}', I['al'][m], 0); arc(f'e2{m}', I['al'][m], 0); arc(f'ez{m}', 2 * I['al'][m], 0)
        con(('h', 'dz'), ('t', f'p{m}')); con(('h', f'p{m}'), ('t', f'e1{m}')); con(('h', f'e1{m}'), ('t', f'e2{m}'))
        con(('h', f'e2{m}'), ('t', f'ez{m}')); con(('h', f'ez{m}'), 'dW')
    def chain(src, snk, first, links):
        con(src, ('t', first)); prev = first
        for r, e in enumerate(links):
            con(('h', prev), ('t', e), 0 if r == 0 else H, 'chain' if r else 'c'); prev = e
        con(('h', prev), snk)
    for i in range(n):
        arc(f's{i}', 1, I['B']); arc(f'r{i}', 1, 0)
        chain(('o', i), ('d', i), f's{i}', [f'e1{m}' for m, (t, h, _) in enumerate(A) if t == i])
        chain(('o', i), ('d', i), f'r{i}', [f'e2{m}' for m, (t, h, _) in enumerate(A) if h == i])
    arc('q1', 1, 0); arc('q0', 1, Bp)
    chain('oz', 'dz_', 'q1', [f'ez{m}' for m in range(M)])
    con('oz', ('t', 'q0')); con(('h', 'q0'), ('t', 'dz')); con(('h', 'dz'), 'dz_')
    adj = {}
    for q, (u, v, *_) in enumerate(arcs): adj.setdefault(u, []).append((v, q))
    def paths(s, t):
        out, st = [], [(s, [])]
        while st:
            u, p = st.pop()
            if u == t: out.append(p); continue
            for v, q in adj.get(u, []): st.append((v, p + [q]))
        return out
    nm = [a_[4] for a_ in arcs]
    PW = paths('oW', 'dW'); Pn = [paths(('o', i), ('d', i)) for i in range(n)]; Pz = paths('oz', 'dz_')
    return I, arcs, nm, PW, Pn, Pz

dstat = dict(pairs=0, struct=0, domP=-np.inf, domZ=-np.inf, e2max=0, Dp2=0)
for n, E in graphs[:8]:
    mc = maxcut(n, E)
    for k in sorted({1, mc + 1}):
        I, arcs, nm, PW, Pn, Pz = dag(n, E, k); dstat['pairs'] += 1
        a = np.array([x[2] for x in arcs], float); b = np.array([x[3] for x in arcs], float)
        ok = all(len(P) == 2 for P in Pn)
        ok &= sum(1 for p in PW if not any(nm[q] == 'chain' for q in p)) == I['M'] + 1
        idx_q0 = nm.index('q0'); idx_q1 = nm.index('q1')
        ok &= all((idx_q1 in p) == (len([1 for q in p if nm[q].startswith('ez')]) == I['M'] and idx_q0 not in p) for p in Pz)
        ok &= sum(1 for p in Pz if idx_q1 in p) == 1
        dstat['struct'] += ok
        # LP over all feasible path flows: variables = path flows of all commodities
        allP = [(0, p) for p in PW] + [(1 + i, p) for i in range(n) for p in Pn[i]] + [(n + 1, p) for p in Pz]
        dem = [I['D']] + [1] * n + [1]
        Dl = np.zeros((len(arcs), len(allP)))
        for c, (_, p) in enumerate(allP): Dl[p, c] = 1
        Aeq = np.zeros((n + 2, len(allP)))
        for c, (o, _) in enumerate(allP): Aeq[o, c] = 1
        def lpmax(vec, const):  # max vec.f + const
            r = linprog(-vec, A_eq=Aeq, b_eq=dem, bounds=(0, None), method='highs')
            return -r.fun + const
        # c_P(f) = sum_{e in P}(a_e f_e + b_e) is linear in path flows
        for i in range(n):
            S, P = Pn[i]
            if not any(nm[q] == 's' + str(i) for q in S): S, P = P, S
            vec = (a[P] @ Dl[P]) - (a[S] @ Dl[S]); const = b[P].sum() - b[S].sum()
            dstat['domP'] = max(dstat['domP'], lpmax(vec, const))
        Z1 = [p for p in Pz if idx_q1 in p][0]
        for p in Pz:
            if p is Z1: continue
            vec = (a[Z1] @ Dl[Z1]) - (a[p] @ Dl[p]); const = b[Z1].sum() - b[p].sum()
            dstat['domZ'] = max(dstat['domZ'], lpmax(vec, const))
        for m in range(I['M']):
            e2 = nm.index(f'e2{m}')
            v = lpmax(Dl[e2], 0.0); dstat['e2max'] = max(dstat['e2max'], v - I['D'])
            dstat['Dp2'] += abs(v - (I['D'] + 2)) < 1e-9
print(f"[DAG] pairs {dstat['pairs']}; structure ok {dstat['struct']}/{dstat['pairs']}")
print(f"  LP max over all feasible flows of c_P_i - c_S_i: {dstat['domP']:.3f} (<0 needed); of c_Z1 - c_other: {dstat['domZ']:.3f} (<0 needed)")
print(f"  max over feasible flows of f(e2_m) - D: {dstat['e2max']:.3f}  (theorem's bound uses D+1; {dstat['Dp2']} arcs e2_m reach D+2)")
print(f"total CPU {time.process_time()-t0:.1f}s")
