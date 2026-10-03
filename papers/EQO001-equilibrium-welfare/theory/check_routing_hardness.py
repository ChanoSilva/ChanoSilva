#!/usr/bin/env python3
"""Check of the MAX-CUT reduction for Question 7.1 of EQO001 v0.3 (routing).

Construction (theory/routing_hardness.tex, Theorem thm:routinghard): graph G=(V,E_G)
with integer weights w, integer k>=1.  Commodities: W (weighted, lambda=e_W, demand
D=M=2|E_G|), one commodity per node i (demand 1, routes S_i/P_i) and a switch z
(demand 1, routes Z1/Z0).  Designated flow f*: W on O, every node on P_i, z on Z1.
Claim: e_W in Lambda(f*)  <=>  maxcut_w(G) < k, and Lambda(f*)=Lambda_1(f*) iff the same.

What is checked, per instance (G,k):
  (X1) exact (Fraction) : f* is a Wardrop equilibrium, every unused path strictly
       costlier;  e_W in Lambda_1(f*) (KKT of min C_W on the product of simplices);
       C_W(f*) = C* ; if maxcut>=k, the explicit witness has C_W(f*)-C_W(wit) =
       maxcut-k+1/2 exactly.
  (X2) strong monotonicity of F on K (explicit model): min eigenvalue of the
       Jacobian on the tangent space > 0.
  (A)  INDEPENDENT minimisation of C_W over K: enumerate the pure profiles of the
       lambda=0 commodities (C_W is affine in their flows; Lemma lem:concave) and
       solve the convex QP in W's path flows by projected gradient with a
       Frank-Wolfe duality gap as certified lower bound.  Uses neither the closed
       form nor separability.  Decide membership with margin 1e-6 (the reduction
       has margin 1/2) and compare with brute-force MAX-CUT.
  (A') the per-vertex QP values agree with the closed form h(x,z).
  (U)  for every other commodity h, min_K C_h >= C_h(f*) (same generic method):
       e_h in Lambda(f*), hence Lambda_1 = orthant.
  (B)  on the smallest instances, a second fully generic method: enumeration of
       all faces of K (all supports of all commodities), stationary point of C_W on
       each face with a nonsingular KKT system (a global minimiser lies in such a
       face), min over feasible candidates.  Does not use Lemma lem:concave.
  (D)  DAG realisation (P_k = all s_k-t_k paths of a levelled DAG): path
       enumeration by DFS, structural claims, exact Wardrop / Lambda_1 checks, and
       method (A) with all paths, on small graphs.
Output: theory/check_routing_hardness_output.txt.  Seed 20261003.
"""
import itertools
import math
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np
from scipy.linalg import null_space

SEED = 20261003
TOL_DEC = 1e-6
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_routing_hardness_output.txt")


# ----------------------------------------------------------------------------- graphs
def maxcut(n, wedges):
    best, bestx = 0, [0] * n
    for mask in range(2 ** n):
        x = [(mask >> i) & 1 for i in range(n)]
        c = sum(w for i, j, w in wedges if x[i] != x[j])
        if c > best:
            best, bestx = c, x
    return best, bestx


# ----------------------------------------------------------------------------- networks
class Net:
    def __init__(self):
        self.a, self.b, self.name, self.arcs, self.idx = [], [], [], [], {}

    def add(self, name, a, b, u=None, v=None):
        self.idx[name] = len(self.a)
        self.a.append(Fr(a)); self.b.append(Fr(b)); self.name.append(name); self.arcs.append((u, v))
        return self.idx[name]


def build(n, wedges, k, dag=False):
    """Instance of the reduction.  Returns (net, comms, info)."""
    med = []
    for (i, j, w) in wedges:
        med += [(i, j, w), (j, i, w)]
    M = len(med); D = M
    wmax = max(w for _, _, w in wedges)
    alpha = [16 * w for _, _, w in med]
    bo = 16 * wmax
    aD = Fr(2 * k - 1, 2 * D)
    B = 2 + 2 * (D + 1) * sum(alpha)
    Hc = bo + 1
    Bz = B + (2 * (M - 1) * Hc if dag else 0)
    net = Net()
    info = dict(med=med, M=M, D=D, alpha=alpha, bo=bo, aD=aD, B=B, Bz=Bz, Hc=Hc, n=n)
    if not dag:
        net.add('dz', aD, 0); net.add('o', 0, bo)
        for m in range(M):
            net.add(f'p{m}', 0, bo - alpha[m]); net.add(f'e1_{m}', alpha[m], 0)
            net.add(f'e2_{m}', alpha[m], 0); net.add(f'ez_{m}', 2 * alpha[m], 0)
        for i in range(n):
            net.add(f's{i}', 1, B); net.add(f'r{i}', 1, 0)
        net.add('q1', 1, 0); net.add('q0', 1, Bz)
        I = net.idx
        comms = [dict(name='W', d=Fr(D), star=0,
                      paths=[[I['dz'], I['o']]] + [[I['dz'], I[f'p{m}'], I[f'e1_{m}'], I[f'e2_{m}'], I[f'ez_{m}']]
                                                   for m in range(M)])]
        for i in range(n):
            S = [I[f's{i}']] + [I[f'e1_{m}'] for m, (t, h, _) in enumerate(med) if t == i]
            P = [I[f'r{i}']] + [I[f'e2_{m}'] for m, (t, h, _) in enumerate(med) if h == i]
            comms.append(dict(name=f'n{i}', d=Fr(1), star=1, paths=[S, P]))
        comms.append(dict(name='z', d=Fr(1), star=0,
                          paths=[[I['q1']] + [I[f'ez_{m}'] for m in range(M)], [I['q0'], I['dz']]]))
        return net, comms, info
    # ---- levelled DAG
    def E(name, a, b):
        return net.add(name, a, b, ('tail', name), ('head', name))

    def C(name, u, v, b=0):
        return net.add('c:' + name, 0, b, u, v)
    E('dz', aD, 0); E('o', 0, bo)
    C('sW>dz', 'sW', ('tail', 'dz')); C('dz>o', ('head', 'dz'), ('tail', 'o')); C('o>tW', ('head', 'o'), 'tW')
    for m in range(M):
        E(f'p{m}', 0, bo - alpha[m]); E(f'e1_{m}', alpha[m], 0); E(f'e2_{m}', alpha[m], 0); E(f'ez_{m}', 2 * alpha[m], 0)
        C(f'dz>p{m}', ('head', 'dz'), ('tail', f'p{m}')); C(f'p{m}>e1', ('head', f'p{m}'), ('tail', f'e1_{m}'))
        C(f'e1>e2_{m}', ('head', f'e1_{m}'), ('tail', f'e2_{m}'))
        C(f'e2>ez_{m}', ('head', f'e2_{m}'), ('tail', f'ez_{m}')); C(f'ez{m}>tW', ('head', f'ez_{m}'), 'tW')

    def chain(tag, src, snk, first, links):
        C(f'{tag}:src', src, ('tail', first))
        prev = first
        for r, e in enumerate(links):
            C(f'{tag}:{r}', ('head', prev), ('tail', e), 0 if r == 0 else Hc)
            prev = e
        C(f'{tag}:snk', ('head', prev), snk)
    for i in range(n):
        E(f's{i}', 1, B); E(f'r{i}', 1, 0)
        chain(f'S{i}', ('src', i), ('snk', i), f's{i}', [f'e1_{m}' for m, (t, h, _) in enumerate(med) if t == i])
        chain(f'P{i}', ('src', i), ('snk', i), f'r{i}', [f'e2_{m}' for m, (t, h, _) in enumerate(med) if h == i])
    E('q1', 1, 0); E('q0', 1, Bz)
    chain('Z1', 'sz', 'tz', 'q1', [f'ez_{m}' for m in range(M)])
    C('Z0:src', 'sz', ('tail', 'q0')); C('Z0:dz', ('head', 'q0'), ('tail', 'dz')); C('Z0:snk', ('head', 'dz'), 'tz')
    adj = {}
    for e, (u, v) in enumerate(net.arcs):
        adj.setdefault(u, []).append((v, e))

    def paths(s, t):
        out, stack = [], [(s, [])]
        while stack:
            u, p = stack.pop()
            if u == t:
                out.append(p); continue
            for v, e in adj.get(u, []):
                stack.append((v, p + [e]))
        return out
    I = net.idx
    PW = paths('sW', 'tW')
    PW.sort(key=lambda p: (I['o'] not in p, len(p)))
    comms = [dict(name='W', d=Fr(D), star=0, paths=PW)]
    for i in range(n):
        Pi = paths(('src', i), ('snk', i))
        Pi.sort(key=lambda p: I[f'r{i}'] in p)  # S first, P second
        comms.append(dict(name=f'n{i}', d=Fr(1), star=len(Pi) - 1, paths=Pi))
    Pz = paths('sz', 'tz')
    Pz.sort(key=lambda p: (I['q1'] not in p, len(p)))
    comms.append(dict(name='z', d=Fr(1), star=0, paths=Pz))
    return net, comms, info


# ----------------------------------------------------------------------------- exact helpers
def star_flows(comms):
    return [[c['d'] if p == c['star'] else Fr(0) for p in range(len(c['paths']))] for c in comms]


def edge_flows(net, comms, flows):
    fe = [Fr(0)] * len(net.a)
    ge = [[Fr(0)] * len(net.a) for _ in comms]
    for ci, c in enumerate(comms):
        for p, path in enumerate(c['paths']):
            if flows[ci][p]:
                for e in path:
                    fe[e] += flows[ci][p]; ge[ci][e] += flows[ci][p]
    return fe, ge


def C_of(net, comms, flows, h):
    fe, ge = edge_flows(net, comms, flows)
    return sum((net.a[e] * fe[e] + net.b[e]) * ge[h][e] for e in range(len(net.a)))


def wardrop_exact(net, comms, flows):
    fe, _ = edge_flows(net, comms, flows)
    ok, margin = True, None
    for ci, c in enumerate(comms):
        cost = [sum(net.a[e] * fe[e] + net.b[e] for e in p) for p in c['paths']]
        used = [cost[p] for p in range(len(cost)) if flows[ci][p] > 0]
        unused = [cost[p] for p in range(len(cost)) if flows[ci][p] == 0]
        if max(used) > min(cost):
            ok = False
        if unused:
            mg = min(unused) - max(used)
            margin = mg if margin is None else min(margin, mg)
    return ok, margin


def lone_unit_exact(net, comms, flows, h):
    """KKT of min C_h at flows (e_h in Lambda_1)."""
    fe, ge = edge_flows(net, comms, flows)
    for ci, c in enumerate(comms):
        g = [sum(net.a[e] * ge[h][e] + (net.a[e] * fe[e] + net.b[e] if ci == h else 0) for e in p) for p in c['paths']]
        used = [g[p] for p in range(len(g)) if flows[ci][p] > 0]
        if max(used) != min(used) or min(used) > min(g):
            return False
    return True


# ----------------------------------------------------------------------------- method (A)
def proj_simplex_rows(Y, s):
    U = -np.sort(-Y, axis=1)
    css = np.cumsum(U, axis=1) - s
    ind = np.arange(1, Y.shape[1] + 1)
    cond = U - css / ind > 0
    rho = cond.shape[1] - 1 - np.argmax(cond[:, ::-1], axis=1)
    theta = css[np.arange(Y.shape[0]), rho] / (rho + 1)
    return np.maximum(Y - theta[:, None], 0.0)


def batch_qp(H, Lin, s, tol=1e-10, maxit=20000):
    """min 1/2 x'Hx + Lin_r x over {x>=0, sum x = s}, row-wise; returns value, FW gap."""
    nb, P = Lin.shape
    L = max(float(np.linalg.eigvalsh(H).max()), 1e-12)
    X = np.full((nb, P), s / P); Y = X.copy(); tk = np.ones(nb)
    for it in range(maxit):
        G = Y @ H + Lin
        Xn = proj_simplex_rows(Y - G / L, s)
        tn = (1 + np.sqrt(1 + 4 * tk ** 2)) / 2
        restart = np.sum((Y - Xn) * (Xn - X), axis=1) > 0
        mom = np.where(restart, 0.0, (tk - 1) / tn)
        tn = np.where(restart, 1.0, tn)
        Y = Xn + mom[:, None] * (Xn - X)
        X, tk = Xn, tn
        if it % 25 == 24:
            G = X @ H + Lin
            gap = np.sum(G * X, axis=1) - s * G.min(axis=1)
            if gap.max() < tol:
                break
    G = X @ H + Lin
    val = 0.5 * np.sum((X @ H) * X, axis=1) + np.sum(Lin * X, axis=1)
    gap = np.sum(G * X, axis=1) - s * G.min(axis=1)
    return val, np.maximum(gap, 0.0), X


def min_C_generic(net, comms, h, keep_profiles=False):
    """min over K of C_h: pure profiles of the other commodities x convex QP in h's flows."""
    Eh = sorted(set(e for p in comms[h]['paths'] for e in p))
    pos = {e: r for r, e in enumerate(Eh)}
    a = np.array([float(net.a[e]) for e in Eh]); b = np.array([float(net.b[e]) for e in Eh])
    A = np.zeros((len(Eh), len(comms[h]['paths'])))
    for q, p in enumerate(comms[h]['paths']):
        for e in p:
            A[pos[e], q] += 1
    choices, owners = [], []
    for ci, c in enumerate(comms):
        if ci == h:
            continue
        fps = {}
        for q, p in enumerate(c['paths']):
            fp = tuple(sorted(pos[e] for e in p if e in pos))
            fps.setdefault(fp, q)
        if len(fps) == 1 and () in fps:
            continue
        choices.append([(fp, q, float(c['d'])) for fp, q in fps.items()]); owners.append(ci)
    profs = list(itertools.product(*choices)) if choices else [()]
    R = np.zeros((len(profs), len(Eh)))
    for r, pr in enumerate(profs):
        for fp, _, d in pr:
            for e in fp:
                R[r, e] += d
    H = 2 * A.T @ np.diag(a) @ A
    Lin = (R * a + b) @ A
    val, gap, _ = batch_qp(H, Lin, float(comms[h]['d']))
    r = int(np.argmin(val))
    res = dict(upper=float(val.min()), lower=float((val - gap).min()), maxgap=float(gap.max()),
               nprof=len(profs), argprof={owners[t]: profs[r][t][1] for t in range(len(owners))})
    if keep_profiles:
        res.update(profs=profs, owners=owners, val=val, gap=gap)
    return res


# ----------------------------------------------------------------------------- method (B)
def min_C_faces(net, comms, h):
    """Enumerate all faces of K; stationary point of C_h on faces with nonsingular KKT."""
    allp, com = [], []
    for ci, c in enumerate(comms):
        for p in c['paths']:
            allp.append(p); com.append(ci)
    P = len(allp); nE = len(net.a); m = len(comms)
    A = np.zeros((nE, P))
    for q, p in enumerate(allp):
        for e in p:
            A[e, q] += 1
    a = np.array([float(x) for x in net.a]); b = np.array([float(x) for x in net.b])
    sel = np.array([1.0 if com[q] == h else 0.0 for q in range(P)])
    Mm = A.T @ np.diag(a) @ A @ np.diag(sel)
    Qs = Mm + Mm.T
    cv = sel * (A.T @ b)
    d = np.array([float(c['d']) for c in comms])
    offs = np.cumsum([0] + [len(c['paths']) for c in comms])
    supp = []
    for ci, c in enumerate(comms):
        idx = list(range(offs[ci], offs[ci + 1]))
        supp.append([s for r in range(1, len(idx) + 1) for s in itertools.combinations(idx, r)])
    best, nfaces, nsing = math.inf, 0, 0
    for combo in itertools.product(*supp):
        S = [q for s in combo for q in s]
        nS = len(S); nfaces += 1
        K = np.zeros((nS + m, nS + m))
        K[:nS, :nS] = Qs[np.ix_(S, S)]
        for r, q in enumerate(S):
            K[nS + com[q], r] = 1.0; K[r, nS + com[q]] = 1.0
        rhs = np.concatenate([-cv[S], d])
        if np.linalg.cond(K) > 1e10:
            nsing += 1; continue
        sol = np.linalg.solve(K, rhs)
        fS = sol[:nS]
        if fS.min() < -1e-10:
            continue
        f = np.zeros(P); f[S] = np.maximum(fS, 0)
        val = f @ Mm @ f + cv @ f
        best = min(best, val)
    return best, nfaces, nsing


# ----------------------------------------------------------------------------- closed form
def closed_h(info, x, z):
    D, aD, bo = info['D'], info['aD'], info['bo']
    v = aD * D * (D + 1 - z) + bo * D
    for m, (i, j, w) in enumerate(info['med']):
        c = x[j] - x[i] - 2 * z
        if c > 0:
            v -= Fr(info['alpha'][m], 16) * c * c
    return v


def witness(net, comms, info, cutx, dag=False):
    """Flow from a cut: node i on S iff cutx[i]=1, z on Z0, t_m=1/8 on gaining mediators."""
    I = net.idx
    flows = [[Fr(0)] * len(c['paths']) for c in comms]
    for i in range(info['n']):
        c = comms[1 + i]
        q = [r for r, p in enumerate(c['paths']) if (I[f's{i}'] in p) == (cutx[i] == 1)][0]
        flows[1 + i][q] = Fr(1)
    cz = comms[-1]
    qz = [r for r, p in enumerate(cz['paths']) if I['q0'] in p and len(set(p) & {I['dz']}) and
          not any(net.name[e].startswith('p') for e in p)][0]
    flows[-1][qz] = Fr(1)
    W = comms[0]; tot = Fr(0)
    for m, (i, j, w) in enumerate(info['med']):
        if cutx[i] == 0 and cutx[j] == 1:
            need = {I[f'p{m}'], I[f'e1_{m}'], I[f'e2_{m}'], I[f'ez_{m}']}
            q = [r for r, p in enumerate(W['paths']) if need <= set(p) and
                 not any(net.b[e] == info['Hc'] and net.a[e] == 0 and net.name[e].startswith('c:') for e in p)][0]
            flows[0][q] = Fr(1, 8); tot += Fr(1, 8)
    flows[0][W['star']] = W['d'] - tot
    return flows


# ----------------------------------------------------------------------------- per instance
def check_instance(n, wedges, k, mc, cutx, dag=False, faces=False):
    net, comms, info = build(n, wedges, k, dag)
    fs = star_flows(comms)
    r = dict(n=n, E=len(wedges), k=k, mc=mc, dag=dag)
    r['wardrop'], margin = wardrop_exact(net, comms, fs)
    r['strict'] = margin is not None and margin > 0
    r['lone_W'] = lone_unit_exact(net, comms, fs, 0)
    Cstar = C_of(net, comms, fs, 0)
    r['Cstar_ok'] = Cstar == info['aD'] * info['D'] ** 2 + info['bo'] * info['D']
    if mc >= k:
        wf = witness(net, comms, info, cutx, dag)
        r['wit_exact'] = (Cstar - C_of(net, comms, wf, 0)) == Fr(2 * (mc - k) + 1, 2)
    resA = min_C_generic(net, comms, 0, keep_profiles=not dag)
    C0 = float(Cstar)
    if resA['lower'] >= C0 - TOL_DEC:
        r['A'] = 'member'
    elif resA['upper'] < C0 - TOL_DEC:
        r['A'] = 'nonmember'
    else:
        r['A'] = 'undecided'
    r['A_gap'] = resA['maxgap']; r['A_prof'] = resA['nprof']
    r['A_margin'] = abs(resA['upper'] - C0)
    r['expected'] = 'member' if mc < k else 'nonmember'
    if not dag:  # (A') per-vertex closed form
        dmax = 0.0
        for pr, v in zip(resA['profs'], resA['val']):
            x = [0] * n; z = 1
            ch = dict(zip(resA['owners'], [t[1] for t in pr]))
            for t, ci in enumerate(resA['owners']):
                if ci == len(comms) - 1:
                    z = 1 if ch[ci] == 0 else 0
                elif ci >= 1:
                    x[ci - 1] = 1 if ch[ci] == 0 else 0
            dmax = max(dmax, abs(v - float(closed_h(info, x, z))))
        r['closed_diff'] = dmax
        # (X2) strong monotonicity on the tangent space
        allp = [p for c in comms for p in c['paths']]
        A = np.zeros((len(net.a), len(allp)))
        for q, p in enumerate(allp):
            for e in p:
                A[e, q] += 1
        J = A.T @ np.diag([float(x) for x in net.a]) @ A
        Ec = np.zeros((len(comms), len(allp))); q = 0
        for ci, c in enumerate(comms):
            for _ in c['paths']:
                Ec[ci, q] = 1; q += 1
        Z = null_space(Ec)
        r['mu'] = float(np.linalg.eigvalsh(Z.T @ J @ Z).min())
    # (U) other unit vectors in Lambda
    okU, gapU = True, 0.0
    for h in range(1, len(comms)):
        res = min_C_generic(net, comms, h)
        gapU = max(gapU, res['maxgap'])
        if res['lower'] < float(C_of(net, comms, fs, h)) - TOL_DEC:
            okU = False
    r['others_in_Lam'] = okU; r['U_gap'] = gapU
    if faces:
        best, nf, ns = min_C_faces(net, comms, 0)
        r['B'] = 'member' if best >= C0 - TOL_DEC else 'nonmember'
        r['B_faces'] = nf; r['B_diffA'] = abs(best - resA['upper'])
    if dag:
        I = net.idx
        nodes_ok = all(len(comms[1 + i]['paths']) == 2 for i in range(n))
        intended = 0; W_bad = 0
        for p in comms[0]['paths']:
            has_hc = any(net.name[e].startswith('c:') and net.b[e] == info['Hc'] for e in p)
            if not has_hc:
                intended += 1
        W_ok = intended == info['M'] + 1
        z_ok = all((I['q1'] in p and I['q0'] not in p and I['dz'] not in p) or (I['q0'] in p and I['dz'] in p)
                   for p in comms[-1]['paths']) and sum(I['q1'] in p for p in comms[-1]['paths']) == 1
        r['dag_struct'] = nodes_ok and W_ok and z_ok
        r['dag_paths'] = (len(comms[0]['paths']), len(comms[-1]['paths']))
    return r


def main():
    t0 = time.process_time()
    rng = np.random.default_rng(SEED)
    graphs = []
    for n in (3, 4):
        pairs = list(itertools.combinations(range(n), 2))
        for mask in range(1, 2 ** len(pairs)):
            graphs.append((n, [(i, j, 1) for t, (i, j) in enumerate(pairs) if (mask >> t) & 1], 'all'))
    for n in (5, 6):
        pairs = list(itertools.combinations(range(n), 2))
        for wt in ('unit', 'w123'):
            cnt = 0
            while cnt < (20 if wt == 'unit' else 10):
                sel = [pq for pq in pairs if rng.random() < 0.5]
                if not sel:
                    continue
                ws = [1 if wt == 'unit' else int(rng.integers(1, 4)) for _ in sel]
                graphs.append((n, [(i, j, w) for (i, j), w in zip(sel, ws)], wt)); cnt += 1
    lines = []

    def log(s):
        print(s); lines.append(s)
    log("check_routing_hardness.py -- MAX-CUT reduction for Question 7.1 (routing), EQO001")
    log(f"seed {SEED}; Python {sys.version.split()[0]}, NumPy {np.__version__}")
    log("")
    # ---------------- explicit model, method (A) on all graphs
    rows = []
    for (n, wedges, fam) in graphs:
        mc, cutx = maxcut(n, wedges)
        for k in sorted({1, max(1, mc), mc + 1}):
            rows.append((fam, check_instance(n, wedges, k, mc, cutx)))
    tA = time.process_time() - t0
    R = [r for _, r in rows]
    log("[explicit path sets] graphs: %d (all labelled graphs with >=1 edge on 3 and 4 nodes; "
        "40 random on 5 nodes and 40 on 6, half with weights in {1,2,3}); pairs (G,k): %d"
        % (len(graphs), len(R)))
    log("  members (maxcut<k): %d   non-members (maxcut>=k): %d"
        % (sum(r['expected'] == 'member' for r in R), sum(r['expected'] == 'nonmember' for r in R)))
    log("  (X1) f* Wardrop, exact: %d/%d; unused paths strictly costlier: %d/%d"
        % (sum(r['wardrop'] for r in R), len(R), sum(r['strict'] for r in R), len(R)))
    log("  (X1) e_W in Lambda_1(f*), exact KKT: %d/%d; C_W(f*) = C*: %d/%d"
        % (sum(r['lone_W'] for r in R), len(R), sum(r['Cstar_ok'] for r in R), len(R)))
    W_ = [r for r in R if 'wit_exact' in r]
    log("  (X1) witness from a maximum cut, C_W(f*)-C_W(wit) = maxcut-k+1/2 exactly: %d/%d"
        % (sum(r['wit_exact'] for r in W_), len(W_)))
    log("  (X2) strong monotonicity: min eigenvalue of DF on the tangent space, min over instances = %.4g"
        % min(r['mu'] for r in R))
    mism = [r for r in R if r['A'] != r['expected']]
    log("  (A) e_W in Lambda(f*) by generic minimisation  <=>  maxcut<k : mismatches %d / %d, undecided %d"
        % (len(mism), len(R), sum(r['A'] == 'undecided' for r in R)))
    log("      max Frank-Wolfe gap %.2e; profiles per instance <= %d; min |min C_W - C_W(f*)| over non-members %.4f"
        % (max(r['A_gap'] for r in R), max(r['A_prof'] for r in R),
           min([r['A_margin'] for r in R if r['expected'] == 'nonmember'] or [math.nan])))
    log("  (A') per-vertex QP value vs closed form h(x,z): max |diff| = %.2e" % max(r['closed_diff'] for r in R))
    log("  (U) every other unit vector e_h in Lambda(f*) (so Lambda_1 = orthant): %d/%d (max FW gap %.1e)"
        % (sum(r['others_in_Lam'] for r in R), len(R), max(r['U_gap'] for r in R)))
    log("      hence Lambda(f*) = Lambda_1(f*) iff maxcut<k on all %d pairs: %s"
        % (len(R), all(r['others_in_Lam'] and r['lone_W'] for r in R) and not mism))
    log("  CPU time so far %.1f s" % tA)
    log("")
    # ---------------- method (B): face enumeration on small instances
    small = [(3, [(0, 1, 1)]), (3, [(0, 1, 1), (1, 2, 1)]), (3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)]),
             (4, [(0, 1, 1), (2, 3, 1)]), (4, [(0, 1, 1), (1, 2, 1), (2, 3, 1)]),
             (4, [(0, 1, 1), (0, 2, 1), (0, 3, 1)]), (3, [(0, 1, 2), (1, 2, 1)])]
    RB = []
    for n, wedges in small:
        mc, cutx = maxcut(n, wedges)
        for k in sorted({max(1, mc), mc + 1}):
            RB.append(check_instance(n, wedges, k, mc, cutx, faces=True))
    log("[face enumeration, no use of the concavity lemma] %d pairs on 7 small graphs (P2, P3, K3, 2K2, P4, K1,3, weighted P3)"
        % len(RB))
    log("  faces enumerated per pair <= %d; agreement of (B) with maxcut<k: %d/%d; |min_B - min_A| <= %.2e"
        % (max(r['B_faces'] for r in RB), sum(r['B'] == r['expected'] for r in RB), len(RB),
           max(r['B_diffA'] for r in RB)))
    log("  CPU time so far %.1f s" % (time.process_time() - t0))
    log("")
    # ---------------- DAG realisation
    dagg = [(3, [(0, 1, 1)]), (3, [(0, 1, 1), (1, 2, 1)]), (3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)]),
            (4, [(0, 1, 1), (1, 2, 1), (2, 3, 1)]), (4, [(0, 1, 1), (0, 2, 1), (0, 3, 1)]),
            (4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 3, 1)]), (4, [(0, 1, 1), (2, 3, 1)]),
            (3, [(0, 1, 2), (1, 2, 1), (0, 2, 3)])]
    RD = []
    for n, wedges in dagg:
        mc, cutx = maxcut(n, wedges)
        for k in sorted({max(1, mc), mc + 1}):
            RD.append(check_instance(n, wedges, k, mc, cutx, dag=True))
    log("[DAG realisation, P_k = all s_k-t_k paths] %d pairs on 8 graphs (P2, P3, K3, P4, K1,3, C4, 2K2, weighted K3)"
        % len(RD))
    log("  paths of W / of z per instance: " + ", ".join("%d/%d" % r['dag_paths'] for r in RD[::2]))
    log("  structure (nodes: exactly 2 paths; W: exactly M+1 paths without an H_c connector; z: Z1 and paths through q0,dz): %d/%d"
        % (sum(r['dag_struct'] for r in RD), len(RD)))
    log("  f* Wardrop exact: %d/%d (strict %d/%d); e_W in Lambda_1 exact: %d/%d; witness exact: %d/%d"
        % (sum(r['wardrop'] for r in RD), len(RD), sum(r['strict'] for r in RD), len(RD),
           sum(r['lone_W'] for r in RD), len(RD), sum(r.get('wit_exact', False) for r in RD),
           sum('wit_exact' in r for r in RD)))
    log("  (A) with all paths: e_W in Lambda iff maxcut<k: %d/%d (max FW gap %.1e); other e_h in Lambda: %d/%d"
        % (sum(r['A'] == r['expected'] for r in RD), len(RD), max(r['A_gap'] for r in RD),
           sum(r['others_in_Lam'] for r in RD), len(RD)))
    log("")
    allok = (not mism and all(r['wardrop'] and r['strict'] and r['lone_W'] and r['Cstar_ok'] and r['others_in_Lam']
                              for r in R + RD)
             and all(r['wit_exact'] for r in R + RD if 'wit_exact' in r)
             and all(r['B'] == r['expected'] for r in RB)
             and all(r['A'] == r['expected'] and r['dag_struct'] for r in RD)
             and max(r['closed_diff'] for r in R) < 1e-7 and min(r['mu'] for r in R) > 0)
    log("ALL CHECKS PASS: %s" % allok)
    log("total CPU time %.1f s" % (time.process_time() - t0))
    with open(OUT, 'w') as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == '__main__':
    main()
