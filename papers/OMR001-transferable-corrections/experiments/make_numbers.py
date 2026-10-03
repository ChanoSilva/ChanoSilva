#!/usr/bin/env python3
"""Turn results/results.json into LaTeX macros (manuscript/numbers.tex) and table bodies."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
res = json.load(open(os.path.join(ROOT, "results", "results.json")))
out_dir = os.path.join(ROOT, "manuscript")
os.makedirs(out_dir, exist_ok=True)

meta, cfg, summ = res["meta"], res["config"], res["summary"]
structure, departure, msweep, consts = (res["structure_sweep"], res["departure_sweep"],
                                        res["m_sweep"], res["constants"])
A = [str(a) for a in cfg["alpha_grid"]]
L = []


def mac(name, val):
    L.append(rf"\newcommand{{\{name}}}{{{val}}}")


def pct(g, signed=True):
    return (f"{100*g:+.1f}" if signed else f"{100*g:.1f}") + r"\%"


def pct_up(g):
    """Maxima quoted as 'never exceeds': round UP at two decimals (referee round 2, m7)."""
    return f"{math.ceil(10000 * g - 1e-6) / 100:.2f}" + r"\%"


def up(x, nd=2, signed=False):
    """Maxima quoted as upper bounds ('largest ratio', 'at most'): round UP (referee round 3, m5; as r2-m7)."""
    v = math.ceil(x * 10 ** nd - 1e-9) / 10 ** nd
    return f"{v:+.{nd}f}" if signed else f"{v:.{nd}f}"


def f4(x):
    return f"{x:.4f}"


def snrlist(xs):
    return ", ".join(f"{x:g}" for x in xs) if xs else "none"


def yesno(b):
    return "yes" if b else "no"


def word(a):
    return {"0.5": "Half", "0.2": "Twenty", "0.1": "Ten", "0.05": "Five", "0.01": "One"}[a]


# meta and configuration
mac("MetaSeed", meta["seed"]); mac("MetaR", f"{cfg['R']:,}".replace(",", r"\,"))
mac("MetaSeconds", f"{meta['seconds']:.0f}"); mac("MetaPython", meta["python"])   # wall-clock seconds
mac("MetaCPUSeconds", f"{meta.get('seconds_cpu', float('nan')):.0f}")
mac("MetaNumpy", meta["numpy"]); mac("MetaScipy", meta["scipy"]); mac("MetaMpl", meta["matplotlib"])
mac("Cd", cfg["d"]); mac("CS", cfg["S"]); mac("Cns", cfg["n_s"]); mac("Cn", cfg["n"]); mac("Cm", cfg["m_default"])
mac("Cne", cfg["n"] - cfg["m_default"]); mac("CsnrDep", f"{cfg['snr_dep']:g}")
mac("CnConfigs", summ["n_configs_rev"]); mac("CnOps", len(cfg["operators"]))
mac("CsnrGrid", snrlist(cfg["snr_grid"])); mac("CdepGrid", snrlist(cfg["dep_grid"]))
mac("CmGrid", snrlist(cfg["m_grid"])); mac("CalphaGrid", snrlist(cfg["alpha_grid"]))
mac("CuseThr", pct(cfg["useful_threshold"], signed=False))
mac("SplitCost", pct(cfg["n"] / (cfg["n"] - cfg["m_default"]) - 1, signed=False))      # m/n_e: fraction of the FULL-data risk d sigma^2/n
mac("SplitCostR", pct(cfg["m_default"] / cfg["n"], signed=False))                        # m/n: fraction of the risk of R = Xbar_e
mac("PhiOne", f"{math.exp(-0.5) / math.sqrt(2 * math.pi):.4f}")                           # sup_x x phi(x) = phi(1)
BORDER = 0.02   # 'borderline' useful: lower CI end within two percentage points of the threshold (referee m9)


def umark(g, useful):
    """Superscript for criterion U: U = met with margin, u = met but borderline."""
    if not useful:
        return ""
    return r"$^{\mathrm u}$" if g["lo"] < cfg["useful_threshold"] + BORDER else r"$^{\mathrm U}$"


def hmark(g):
    """Superscript H: harmful with respect to Xbar_n (upper 95% CI end of the gain below zero)."""
    return r"$^{\mathrm H}$" if g["hi"] < 0 else ""

mac("RefRiskE", f4(cfg["d"] / (cfg["n"] - cfg["m_default"]))); mac("RefRiskN", f4(cfg["d"] / cfg["n"]))

# constants of Theorem 4.2, Corollary 4.3 and Proposition 4.5
with open(os.path.join(out_dir, "table_constants.tex"), "w") as fh:
    for c in consts:
        fh.write(f"{c['alpha']:g} & {c['z']:.3f} & {c['phi_z']:.4f} & {c['kappa']:.4f} & {c['u_star']:.3f} & "
                 f"{c['ratio_kappa_over_phi']:.3f} & {c['kappa2']:.4f} & {c['ratio_kappa2_over_phi1']:.3f} & "
                 f"{c['regret_const']:.3f} \\\\\n")
for c in consts:
    w = word(str(c["alpha"]))
    mac(f"Kappa{w}", f"{c['kappa']:.4f}"); mac(f"Phiz{w}", f"{c['phi_z']:.4f}")
    mac(f"Ratio{w}", f"{c['ratio_kappa_over_phi']:.2f}"); mac(f"KappaTwo{w}", f"{c['kappa2']:.4f}")
    mac(f"InvRatio{w}", f"{1 / c['ratio_kappa_over_phi']:.1f}")         # phi(z)/kappa(alpha)
mac("InvRatioMin", f"{min(1 / c['ratio_kappa_over_phi'] for c in consts):.1f}")
mac("InvRatioMax", f"{max(1 / c['ratio_kappa_over_phi'] for c in consts):.0f}")
mac("UStarMax", f"{max(c['u_star'] for c in consts):.2f}")
mac("UTwoStarMax", f"{max(c['u2_star'] for c in consts):.2f}")
# worst case over operators at the design (Proposition 4.5(b), Corollary 4.3; analytic)
for wc in summ["worst_case"]:
    w = word(str(wc["alpha"]))
    mac(f"WorstLower{w}", f"{wc['lower']:.4f}"); mac(f"WorstUpper{w}", f"{wc['upper_exact']:.4f}")
    mac(f"CapPhi{w}", f"{wc['cap_phi']:.4f}"); mac(f"CapPhiOverCap{w}", f"{wc['cap_phi'] / wc['cap']:.1f}")

# structure sweep tables (EB operator)
with open(os.path.join(out_dir, "table_structure.tex"), "w") as fh:
    for r in structure:
        e = r["ops"]["eb"]
        cells = [f"{r['snr']:g}", f"{r['lam_oracle']:.2f}", f4(r["risk_Rn"][0]),
                 f4(e["always_full"]["risk"][0]) + umark(e["always_full"]["gain_vs_Rn"], e["always_full"]["useful"])]
        for a in ("0.5", "0.2", "0.1", "0.01"):
            q = e["rev"][a]
            cells.append(f4(q["risk"][0]) + umark(q["gain_vs_Rn"], q["useful"]))
        q = e["rev"]["0.1"]
        cells.append(f4(q["risk_refit"][0]) + umark(q["gain_refit_vs_Rn"], q["useful_refit"]))
        cells.append(f4(e["sure"]["risk"][0]) + umark(e["sure"]["gain_vs_Rn"], e["sure"]["useful"]))
        fh.write(" & ".join(cells) + " \\\\\n")
with open(os.path.join(out_dir, "table_structure_check.tex"), "w") as fh:
    for r in structure:
        e = r["ops"]["eb"]; q = e["rev"]["0.1"]
        fh.write(f"{r['snr']:g} & {f4(r['risk_Re'][0])} & {f4(e['always']['risk'][0])} & "
                 f"{100*e['always']['harm_freq']:.1f} & {f4(q['risk'][0])} & {100*q['harm_freq']:.1f} & "
                 f"{q['excess_vs_Re'][0]:+.4f} & {q['bound_tight']:.4f} & {q['bound_phi']:.4f} & {q['bound_alpha']:.4f} \\\\\n")

# departure sweep tables
with open(os.path.join(out_dir, "table_departure.tex"), "w") as fh:
    for r in departure:
        e = r["ops"]["eb"]
        cells = [f"{r['dep_over_tau']:g}", f4(r["risk_Rn"][0]),
                 f4(e["always_full"]["risk"][0]) + hmark(e["always_full"]["gain_vs_Rn"])]
        for a in ("0.5", "0.2", "0.1", "0.01"):
            cells.append(f4(e["rev"][a]["risk"][0]) + hmark(e["rev"][a]["gain_vs_Rn"]))
        q = e["rev"]["0.1"]
        cells += [f4(q["risk_refit"][0]) + hmark(q["gain_refit_vs_Rn"]), f4(e["sure"]["risk"][0]) + hmark(e["sure"]["gain_vs_Rn"])]
        fh.write(" & ".join(cells) + " \\\\\n")
with open(os.path.join(out_dir, "table_departure_check.tex"), "w") as fh:
    for r in departure:
        e = r["ops"]["eb"]; q = e["rev"]["0.1"]
        fh.write(f"{r['dep_over_tau']:g} & {f4(r['risk_Re'][0])} & {f4(e['always']['risk'][0])} & "
                 f"{100*e['always']['harm_freq']:.1f} & {100*q['harm_freq']:.1f} & {100*q['accept_given_harmful']:.1f} & "
                 f"{q['excess_vs_Re'][0]:+.4f} $\\pm$ {q['excess_vs_Re'][1]:.4f} & {q['bound_tight']:.4f} & "
                 f"{q['bound_phi']:.4f} & {q['bound_alpha']:.4f} \\\\\n")

# held-out size table
with open(os.path.join(out_dir, "table_m.tex"), "w") as fh:
    for r in msweep:
        e = r["ops"]["eb"]; q = e["rev"]["0.1"]
        fh.write(f"{r['m']} & {r['n_e']} & {r['dep_over_tau']:g} & {f4(r['risk_Re'][0])} & {f4(r['risk_Rn'][0])} & "
                 f"{f4(e['always_full']['risk'][0])} & {f4(q['risk'][0])} & {pct(q['gain_vs_Rn']['gain'])} & "
                 f"{q['excess_vs_Re'][0]:+.4f} & {q['bound_phi']:.4f} & {f4(q['risk_refit'][0])} & {f4(e['sure']['risk'][0])} \\\\\n")

# other operators
opname = {"eb": "EB shrinkage", "pool": "full pooling", "fixed": r"fixed $\lambda=\tfrac12$"}
with open(os.path.join(out_dir, "table_operators.tex"), "w") as fh:
    for r in structure:
        if r["snr"] not in (0.0, 1.0, 4.0, 16.0):
            continue
        for name in cfg["operators"]:
            e = r["ops"][name]; q = e["rev"]["0.1"]
            fh.write(f"{r['snr']:g} & {opname[name]} & {f4(e['always']['risk'][0])} & {100*e['always']['harm_freq']:.1f} & "
                     f"{f4(q['risk'][0])} & {100*q['harm_freq']:.1f} & {q['excess_vs_Re'][0]:+.4f} & "
                     f"{q['bound_phi']:.4f} & {q['bound_alpha']:.4f} \\\\\n")

# summary macros
mac("SafeAll", yesno(summ["safe_phi_all"] and summ["safe_alpha_all"] and summ["safe_tight_all"]
                     and summ["safe_kappa_all"]))
mac("MaxExcessOverKappa", f"{summ['max_excess_over_bound_kappa']:.2f}")
mac("MaxBoundKappaOverUniform", f"{summ['max_bound_kappa_over_uniform']:.1f}")
mac("SafeHarmAll", yesno(summ["safe_harm_freq_all"]))
mac("MaxExcessOverPhi", f"{summ['max_excess_over_bound_phi']:.2f}")
mac("SafeUniformAll", yesno(summ["safe_uniform_all"]))
mac("MaxExcessOverUniform", f"{summ['max_excess_over_bound_uniform']:.2f}")
mac("SafeUniformPhiAll", yesno(summ["safe_uniform_phi_all"]))
_q0 = departure[0]["ops"]["eb"]["rev"]
for a in A:
    mac(f"UniformCap{word(a)}", f"{_q0[a]['bound_uniform']:.4f}")
_re, _rn = cfg["d"] / (cfg["n"] - cfg["m_default"]), cfg["d"] / cfg["n"]
mac("UniformCapTenOverRe", f"{_q0['0.1']['bound_uniform'] / _re:.2f}")
mac("UniformCapTenRatioRn", f"{(_re + _q0['0.1']['bound_uniform']) / _rn:.2f}")
mac("UniformCapHalfRatioRn", f"{(_re + _q0['0.5']['bound_uniform']) / _rn:.2f}")
# m sweep: tau^2 held fixed
mac("MTauTwo", f"{msweep[0]['tau2']:.4f}")
mac("MTauTwoFrac", f"1/{round(cfg['sigma'] ** 2 / msweep[0]['tau2'])}")
mac("MSnrOwnMin", f"{min(r['snr_vs_own_ne'] for r in msweep):.2f}")
mac("MSnrOwnMax", f"{max(r['snr_vs_own_ne'] for r in msweep):.2f}")
# borderline list for Table 2 (EB operator): entries whose lower CI end is within BORDER of the threshold
_bl = []
for r in structure:
    e = r["ops"]["eb"]
    for lab, g, u in ([("always", e["always_full"]["gain_vs_Rn"], e["always_full"]["useful"]),
                       ("SURE", e["sure"]["gain_vs_Rn"], e["sure"]["useful"]),
                       (r"refit $0.1$", e["rev"]["0.1"]["gain_refit_vs_Rn"], e["rev"]["0.1"]["useful_refit"])] +
                      [(rf"$\alpha={a}$", e["rev"][a]["gain_vs_Rn"], e["rev"][a]["useful"]) for a in ("0.5", "0.2", "0.1", "0.01")]):
        if u and g["lo"] < cfg["useful_threshold"] + BORDER:
            _bl.append(f"{lab} at $\snr={r['snr']:g}$ (gain {pct(g['gain'])}, lower end {pct(g['lo'])})")
mac("NBorderline", len(_bl)); mac("BorderlineList", "; ".join(_bl) if _bl else "none")
mac("BorderPts", f"{100 * BORDER:g}")
mac("MaxRegretOverBound", f"{summ['max_regret_over_bound']:.2f}")
mac("MaxIdentityZ", f"{summ['max_identity_abs_z']:.2f}")
mac("NIdentityCLT", summ["n_identity_clt"]); mac("NIdentityPoisson", summ["n_identity_poisson"])
mac("NIdentityFail", summ["n_identity_fail"])
for a in A:
    w = word(a)
    mac(f"UsefulRev{w}", snrlist(summ["useful_structure_eb"][a]))
    mac(f"UsefulRefit{w}", snrlist(summ["useful_structure_refit_eb"][a]))
    mac(f"HarmMax{w}", pct_up(summ["max_harm_freq_rev_eb"][a]))
    mac(f"AccHarmMax{w}", pct_up(summ["max_accept_given_harmful_eb"][a]))
    mac(f"UsefulRevMax{w}", f"{max(summ['useful_structure_eb'][a]):g}" if summ["useful_structure_eb"][a] else "none")
mac("UsefulAlways", snrlist(summ["useful_structure_always_full_eb"]))
mac("UsefulSure", snrlist(summ["useful_structure_sure_eb"]))
mac("HarmfulAlwaysDep", snrlist(summ["harmful_vs_Rn_always_full_eb_departure"]))
mac("HarmfulSureDep", snrlist(summ["harmful_vs_Rn_sure_eb_departure"]))
mac("HarmfulRefitTenDep", snrlist(summ["harmful_vs_Rn_refit_eb_departure"]["0.1"]))
mac("HarmfulRevTenDep", snrlist(summ["harmful_vs_Rn_rev_eb_departure"]["0.1"]))
w = summ["worst_departure"]
mac("WorstDep", f"{w['dep_over_tau']:g}"); mac("WorstAlways", f4(w["always_risk"]))
mac("WorstRatioAlways", f"{w['always_risk']/w['risk_Re']:.1f}")
mac("WorstRe", f4(w["risk_Re"])); mac("WorstRn", f4(w["risk_Rn"]))
for a in A:
    ww = word(a)
    mac(f"WorstRev{ww}", f4(w["rev"][a])); mac(f"WorstExcess{ww}", f"{w['excess'][a]:.4f}")
    mac(f"WorstBoundPhi{ww}", f"{w['bound_phi'][a]:.4f}"); mac(f"WorstBoundAlpha{ww}", f"{w['bound_alpha'][a]:.4f}")

# named points in the text
def S(snr):
    return next(r for r in structure if r["snr"] == snr)


def D(dep):
    return next(r for r in departure if r["dep_over_tau"] == dep)


for snr, tag in ((0.0, "Zero"), (1.0, "One"), (4.0, "Four"), (16.0, "Sixteen")):
    r = S(snr); e = r["ops"]["eb"]
    mac(f"S{tag}Rn", f4(r["risk_Rn"][0])); mac(f"S{tag}Re", f4(r["risk_Re"][0]))
    mac(f"S{tag}AlwaysGain", pct(e["always_full"]["gain_vs_Rn"]["gain"]))
    mac(f"S{tag}AlwaysHarm", pct(e["always_full"]["harm_freq"], signed=False))
    mac(f"S{tag}AlwaysEHarm", pct(e["always"]["harm_freq"], signed=False))
    for a in A:
        ww = word(a)
        mac(f"S{tag}Rev{ww}Gain", pct(e["rev"][a]["gain_vs_Rn"]["gain"]))
        mac(f"S{tag}Rev{ww}GainE", pct(e["rev"][a]["gain_vs_Re"]["gain"]))
        mac(f"S{tag}Rev{ww}Harm", pct(e["rev"][a]["harm_freq"], signed=False))
        mac(f"S{tag}Rev{ww}Acc", pct(e["rev"][a]["accept_freq"], signed=False))
    mac(f"S{tag}RefitTenGain", pct(e["rev"]["0.1"]["gain_refit_vs_Rn"]["gain"]))
    mac(f"S{tag}RefitTenGainLo", pct(e["rev"]["0.1"]["gain_refit_vs_Rn"]["lo"]))
    mac(f"S{tag}SureGain", pct(e["sure"]["gain_vs_Rn"]["gain"]))
    mac(f"S{tag}PoolAlways", f4(r["ops"]["pool"]["always"]["risk"][0]))
    mac(f"S{tag}PoolRevTen", f4(r["ops"]["pool"]["rev"]["0.1"]["risk"][0]))
for dep, tag in ((0.0, "Zero"), (4.0, "Four"), (8.0, "Eight"), (16.0, "Sixteen")):
    r = D(dep); e = r["ops"]["eb"]
    mac(f"D{tag}Rn", f4(r["risk_Rn"][0])); mac(f"D{tag}Re", f4(r["risk_Re"][0]))
    mac(f"D{tag}AlwaysRatio", f"{e['always_full']['risk'][0]/r['risk_Rn'][0]:.2f}")
    mac(f"D{tag}AlwaysEHarm", pct(e["always"]["harm_freq"], signed=False))
    for a in A:
        ww = word(a)
        q = e["rev"][a]
        mac(f"D{tag}Rev{ww}Ratio", f"{q['risk'][0]/r['risk_Rn'][0]:.2f}")
        mac(f"D{tag}Rev{ww}Harm", pct(q["harm_freq"], signed=False))
        mac(f"D{tag}Rev{ww}Excess", f"{q['excess_vs_Re'][0]:+.4f}")
        mac(f"D{tag}Rev{ww}ExcessSE", f"{q['excess_vs_Re'][1]:.4f}")
        mac(f"D{tag}Rev{ww}BoundPhi", f"{q['bound_phi']:.4f}")
        mac(f"D{tag}Rev{ww}BoundKappa", f"{q['bound_kappa']:.4f}")
        mac(f"D{tag}Rev{ww}BoundAlpha", f"{q['bound_alpha']:.4f}")
        mac(f"D{tag}Rev{ww}BoundTight", f"{q['bound_tight']:.4f}")
    mac(f"D{tag}SureRatio", f"{e['sure']['risk'][0]/r['risk_Rn'][0]:.2f}")
    mac(f"D{tag}UniformCapTen", f"{e['rev']['0.1']['bound_uniform']:.4f}")
    mac(f"D{tag}RefitTenRatio", f"{e['rev']['0.1']['risk_refit'][0]/r['risk_Rn'][0]:.2f}")
# departure sweep: range of risk(rev)/risk(Xbar_n) for alpha <= 0.1 and maximum for alpha = 0.5 (referee round 2, m6)
_rat = [(e["rev"][a]["risk"][0] / r["risk_Rn"][0], a, r["dep_over_tau"])
        for r in departure for e in [r["ops"]["eb"]] for a in ("0.1", "0.05", "0.01")]
mac("DepRevLowMin", f"{min(_rat)[0]:.2f}"); mac("DepRevLowMax", f"{max(_rat)[0]:.2f}")
_h = max((r["ops"]["eb"]["rev"]["0.5"]["risk"][0] / r["risk_Rn"][0], r["dep_over_tau"]) for r in departure)
mac("DepRevHalfMax", f"{_h[0]:.2f}"); mac("DepRevHalfMaxAt", f"{_h[1]:g}")
mac("MThreeSplit", f"{100 * min(cfg['m_grid']) / cfg['n']:g}" + r"\%")    # split fraction m/n at the smallest m
# m sweep named points (alpha = 0.1)
for r in msweep:
    q = r["ops"]["eb"]["rev"]["0.1"]
    tag = {3: "Three", 6: "Six", 12: "Twelve", 24: "TwentyFour"}[r["m"]] + ("Zero" if r["dep_over_tau"] == 0 else "Eight")
    mac(f"M{tag}RevGain", pct(q["gain_vs_Rn"]["gain"]))
    mac(f"M{tag}Excess", f"{q['excess_vs_Re'][0]:+.4f}")
    mac(f"M{tag}BoundPhi", f"{q['bound_phi']:.4f}")
    mac(f"M{tag}BoundKappa", f"{q['bound_kappa']:.4f}")

def max_se(rows):
    v = []
    for r in rows:
        e = r["ops"]["eb"]
        v += [r["risk_Rn"][1], r["risk_Re"][1], e["always_full"]["risk"][1], e["always"]["risk"][1], e["sure"]["risk"][1]]
        v += [e["rev"][a]["risk"][1] for a in A] + [e["rev"]["0.1"]["risk_refit"][1]]
    return max(v)


mac("MaxSEStructure", f"{max_se(structure):.4f}"); mac("MaxSEDeparture", f"{max_se(departure):.4f}")
mac("MaxSEm", f"{max_se(msweep):.4f}")
for snr, tag in ((0.0, "Zero"), (1.0, "One"), (4.0, "Four"), (16.0, "Sixteen")):
    mac(f"S{tag}AlwaysEHelp", pct(1 - S(snr)["ops"]["eb"]["always"]["harm_freq"], signed=False))

rc = summ["identity_recheck"]
mac("CondCheckMaxZ", f"{rc['conditional_max_abs_z']:.2f}")
wr = rc["worst_rare_config"]
if wr:
    mac("RecheckSeeds", wr["recheck_seeds"]); mac("RecheckCount", wr["recheck_count"])
    mac("RecheckExpected", f"{wr['recheck_expected']:.0f}"); mac("RecheckZ", f"{wr['recheck_z']:+.2f}")
    mac("RecheckMainCount", wr["count"]); mac("RecheckMainExpected", f"{wr['expected']:.0f}")
    mac("RecheckConfig", f"{opname[wr['operator']]}, $\\alpha={wr['alpha']:g}$, $m={wr['m']}$, departure ${wr['dep_over_tau']:g}\\tau$")

# ------------------------------------------------------------------------------------------------
# v0.4: transported refit and cross-fitting (Theorem thm:refit, Corollary cor:crossfit).
# Simulation numbers come from results/results.json (same draws as above); the constants, caps and
# Monte Carlo checks come from results/refit_check.json, written by theory/check_refit.py and frozen
# with its SHA-256 in results/refit_check.json.sha256 (checked here).
# ------------------------------------------------------------------------------------------------
import hashlib  # noqa: E402

_rf_path = os.path.join(ROOT, "results", "refit_check.json")
_rf_hash = hashlib.sha256(open(_rf_path, "rb").read()).hexdigest()
_rf_rec = open(_rf_path + ".sha256").read().split()[0]
assert _rf_hash == _rf_rec, "results/refit_check.json does not match its recorded SHA-256"
rf = json.load(open(_rf_path))
mac("RfSHA", _rf_hash[:16]); mac("RfSeconds", f"{rf['meta']['seconds']:.0f}"); mac("RfCPU", f"{rf['meta']['seconds_cpu']:.0f}")
mac("RfReps", f"{rf['meta']['replicates']:,}".replace(",", r"\,"))
RC = {(c["alpha"], c["m"]): c for c in rf["constants"]}
m0 = cfg["m_default"]
mac("RfEtaDefault", f"{m0 / cfg['n']:g}")
mac("RfPsiZeroTen", f"{RC[(0.1, m0)]['psi0']:.4f}")
mac("RfSplitCostAbs", f"{RC[(0.1, m0)]['split']:.4f}")
for a in cfg["alpha_grid"]:
    c = RC[(a, m0)]; w = word(str(a))
    mac(f"RfCap{w}", f"{c['cap_exact']:.4f}"); mac(f"RfLower{w}", f"{c['lower']:.4f}")
    mac(f"RfFourAlphaSplit{w}", f"{4 * a * c['split']:.4f}")
    mac(f"RfSplitLo{w}", f"{c['split_lo']:.4f}"); mac(f"RfSplitHi{w}", f"{c['split_hi']:.4f}")
mac("RfClosedMin", f"{rf['closed_over_exact'][0]:.2f}"); mac("RfClosedMax", up(rf['closed_over_exact'][1], 1))
_v1 = [c["v1_limit"] / c["split"] for c in rf["constants"]]
mac("RfVOneTen", f"{RC[(0.1, m0)]['v1_limit'] / RC[(0.1, m0)]['split']:.2f}")
mac("RfVOneMin", f"{min(_v1):.2f}"); mac("RfVOneMax", up(max(_v1)))
# v0.5 (round 3, m1): the split estimator's worst case is now EXACT, split + (sigma^2/m) E[M_0(alpha; xi)]
# (Proposition prop:sharp(c)); Table tab:worstrefit compares it with the refit's exact worst case.
MT = {3: "Three", 6: "Six", 12: "Twelve", 24: "TwentyFour"}
for c in rf["constants"]:
    t = word(str(c["alpha"])) + MT[c["m"]]
    mac(f"RfSplitEx{t}", f4(c["split_exact"])); mac(f"RfSplitExR{t}", f4(c["split_exact_over_R"]))
    mac(f"RfCapEx{t}", f4(c["cap_exact"]))
    mac(f"RfOraRf{t}", f"{c['oracle_refit']:+.4f}"); mac(f"RfOraSp{t}", f"{c['oracle_split']:+.4f}")
mac("WorstExactTen", f4(RC[(0.1, m0)]["split_exact_over_R"]))
_cls = {}
with open(os.path.join(out_dir, "table_worst_refit.tex"), "w") as fh:
    for a in cfg["alpha_grid"]:
        cells = [f"{a:g}"]
        for m in cfg["m_grid"]:
            c = RC[(a, m)]
            v = f"{c['cap_exact']:.4f}"
            if c["cap_exact"] < c["split_exact"]:
                v, k = r"\textbf{" + v + "}", "better"
            else:
                v, k = r"\textit{" + v + "}", "worse"
            _cls.setdefault(k, []).append((a, m))
            # the exact split value must lie in the bracket of Proposition prop:sharp(b)
            assert c["split_lo"] - 1e-6 <= c["split_exact"] <= c["split_hi"] + 1e-6, (a, m)
            cells += [v, f"{c['split_exact']:.4f}"]
        fh.write(" & ".join(cells) + " \\\\\n")
with open(os.path.join(out_dir, "table_worst_split.tex"), "w") as fh:
    fh.write(" & ".join(r"\multicolumn{2}{c}{" + f"{RC[(0.1, m)]['split']:.4f}" + "}" for m in cfg["m_grid"]) + "\n")
# oracle correction C = theta (round 3, M1): exact excess over Xbar_n, refit vs split (bold: refit better)
_ora_harm, _ora_split_better = [], []
with open(os.path.join(out_dir, "table_oracle.tex"), "w") as fh:
    for a in cfg["alpha_grid"]:
        cells = [f"{a:g}"]
        for m in cfg["m_grid"]:
            c = RC[(a, m)]
            v = f"{c['oracle_refit']:+.4f}"
            if c["oracle_refit"] > 0:
                _ora_harm.append((a, m)); v += r"$^{\mathrm H}$"
            if c["oracle_split"] < c["oracle_refit"]:
                _ora_split_better.append((a, m)); v = r"\textit{" + v + "}"
            else:
                v = r"\textbf{" + v + "}"
            cells += [v, f"{c['oracle_split']:+.4f}"]
        fh.write(" & ".join(cells) + " \\\\\n")
mac("RfOraRfTenTwentyFourPct", pct(RC[(0.1, 24)]["oracle_refit"] / (cfg["d"] * cfg["sigma"] ** 2 / cfg["n"]), signed=False))
# reduction check (round 3, m2) and adversarial families without held-out noise (m4)
red = rf["reduction"]
mac("RfRedCapRelDiff", f"{red['max_cap_rel_diff']:.0e}".replace("e-0", r"\times10^{-").replace("e-", r"\times10^{-") + "}")
assert red["min_abs_c_at_2d_argmax"] > 0.9999 and red["max_cap_rel_diff"] < 1e-5
_ef = rf["adversarial"]["exact_families"]
_wx = [r["over_cap"] for r in _ef if r["family"] == "worst(M_rho)"]
_px = [r["over_cap"] for r in _ef if r["family"] == "Prop4.5b"]
_rx = [r["over_lower"] for r in _ef if r["family"] == "reflect t=2.0"]
mac("RfAdvWorstExMin", f"{min(_wx):.4f}"); mac("RfAdvWorstExMax", up(max(_wx), 4))
mac("RfAdvPropExMin", f"{min(_px):.2f}"); mac("RfAdvPropExMax", up(max(_px), 3))
assert max(abs(x - 1) for x in _rx) < 1e-5 and max(r["over_cap"] for r in _ef) <= 1 + 1e-6
mac("RfAdvRbNcMax", up(rf["adversarial"]["rb_max_over_cap_noncollinear"]))
mac("RfAdvIdExpected", f"{rf['adversarial']['identity_expected_above3']:.1f}")
_ptail = math.erfc(3 / math.sqrt(2))                       # P(|Z| > 3)
mac("RfIdExpected", f"{rf['design']['identity_n_z'] * _ptail:.2f}")
# the refit's Poisson failure is the acceptance-count test of Section 6 on the same replicates (round 3, m3)
_fa = rf["design"]["identity_fail_at"]
_wr = summ["identity_recheck"]["worst_rare_config"]
assert len(_fa) == 1 and _fa[0]["op"] == _wr["operator"] and _fa[0]["alpha"] == _wr["alpha"] \
    and _fa[0]["m"] == _wr["m"] and _fa[0]["dep"] == _wr["dep_over_tau"], "refit identity failure is not the Section 6 one"
# alpha = 0.5 in 36 other designs (round 3, m6)
_gen = rf["general_alpha_half"]
mac("RfGenN", len(_gen)); mac("RfGenWorse", sum(r["ratio"] > 1 for r in _gen))
mac("RfGenRatioMin", f"{min(r['ratio'] for r in _gen):.3f}"); mac("RfGenRatioMax", up(max(r["ratio"] for r in _gen)))
assert all(r["ratio"] > 1 for r in _gen), "text says the refit is worse at alpha = 0.5 in every design tried"


def _cls_text(pairs):
    if not pairs:
        return "no pair"
    by_a = {}
    for a, m in pairs:
        by_a.setdefault(a, []).append(m)
    parts = []
    for a, ms in by_a.items():
        ms_txt = "every $m$" if len(ms) == len(cfg["m_grid"]) else "$m\\in\\{" + ",".join(str(x) for x in ms) + "\\}$"
        parts.append(f"$\\alpha={a:g}$ ({ms_txt})")
    return ", ".join(parts)


mac("RfBetterText", _cls_text(_cls.get("better", [])))
mac("RfWorseText", _cls_text(_cls.get("worse", [])))
mac("RfUnclearText", _cls_text(_cls.get("unclear", [])))
assert all(k == "worse" for (a, m), k in [((a, m), k) for k, v in _cls.items() for (a, m) in v] if a == 0.5), \
    "text claims that the refit is worse than the split at alpha = 0.5 for every m"
# Monte Carlo checks (design, cross-fit, adversarial)
dz = rf["design"]
mac("RfDesignN", dz["n"])
for k, tag in (("b2", "B"), ("b2c", "Bc"), ("cap", "Cap"), ("capc", "Capc")):
    mac(f"RfDesignHold{tag}", dz["hold"][k]); mac(f"RfDesignMax{tag}", f"{dz['max_ratio'][k]:.2f}")
mac("RfIdNz", dz["identity_n_z"]); mac("RfIdMaxZ", f"{dz['identity_max_z']:.2f}")
mac("RfIdNPois", dz["identity_n_poisson"]); mac("RfIdFail", dz["identity_fail"])
mac("RfSimHoldB", dz["simrefit_hold"]["b2"]); mac("RfSimHoldCap", dz["simrefit_hold"]["cap"])
mac("RfSimMaxB", f"{dz['simrefit_max_ratio']['b2']:.2f}"); mac("RfSimMaxCap", f"{dz['simrefit_max_ratio']['cap']:.2f}")
mac("RfReproDiff", f"{max(dz['repro_max_diff'], dz['replica_max_diff']):.0e}")
cf = rf["crossfit"]
mac("RfCfN", cf["n"]); mac("RfCfMs", ", ".join(str(x) for x in cf["m_values"]))
mac("RfCfHoldB", cf["hold"]["b2"]); mac("RfCfHoldCap", cf["hold"]["cap"]); mac("RfCfJensen", cf["jensen_hold"])
mac("RfCfMaxB", f"{cf['max_ratio']['b2']:.2f}"); mac("RfCfMaxCap", f"{cf['max_ratio']['cap']:.2f}")
_cf0 = [r for r in cf["eb10"] if r["m"] == m0 and r["dep"] == 0.0]
_rn = cfg["d"] * cfg["sigma"] ** 2 / cfg["n"]
mac("RfCfSZeroGain", pct(-_cf0[0]["ex"][0] / _rn)); mac("RfCfSSixteenGain", pct(-[r for r in _cf0 if r["snr"] == 16.0][0]["ex"][0] / _rn))
_cfd = [r for r in cf["eb10"] if r["m"] == m0 and r["snr"] == cfg["snr_dep"]]
mac("RfCfDepMax", f"{max(r['ex'][0] for r in _cfd):+.4f}"); mac("RfCfK", cfg["n"] // m0)
ad = rf["adversarial"]
mac("RfAdvN", ad["n"])
for k, tag in (("b2", "B"), ("cap", "Cap"), ("capc", "Capc")):
    mac(f"RfAdvHold{tag}", ad["hold"][k]); mac(f"RfAdvMax{tag}", f"{ad['max_ratio'][k]:.2f}")
mac("RfAdvIdN", ad["identity_n"]); mac("RfAdvIdMaxZ", f"{ad['identity_max_z']:.2f}"); mac("RfAdvIdAbove", ad["identity_n_above3"])
mac("RfAdvWorstMin", f"{min(ad['worst_over_cap']):.2f}"); mac("RfAdvWorstMax", f"{max(ad['worst_over_cap']):.2f}")
mac("RfAdvReflMin", f"{min(ad['reflect_over_lower']):.2f}"); mac("RfAdvReflMax", f"{max(ad['reflect_over_lower']):.2f}")
ac = rf["adversarial_crossfit"]
mac("RfAcfN", ac["n"]); mac("RfAcfHoldB", ac["hold"]["b2"]); mac("RfAcfHoldCap", ac["hold"]["cap"])
mac("RfAcfMaxSplit", f"{ac['max_over_split']:.1f}"); mac("RfAcfMaxSplitM", ac["max_over_split_at"]["m"])
mac("RfAcfMaxSplitAlpha", f"{ac['max_over_split_at']['alpha']:g}")
_w10 = [r["ex"] / r["split"] for r in ac["worst"] if r["alpha"] == 0.1]
mac("RfAcfTenMin", f"{min(_w10):.2f}"); mac("RfAcfTenMax", f"{max(_w10):.2f}")
# transported refit inside the simulation (results.json, same draws as every other estimator)
for a in A:
    ww = word(a)
    mac(f"UsefulTr{ww}", snrlist(summ["useful_structure_transported_eb"][a]))
    mac(f"HarmfulTr{ww}Dep", snrlist(summ["harmful_vs_Rn_transported_eb_departure"][a]))
mac("HarmfulRevHalfDep", snrlist(summ["harmful_vs_Rn_rev_eb_departure"]["0.5"]))
for snr, tag in ((0.0, "Zero"), (1.0, "One"), (4.0, "Four"), (16.0, "Sixteen")):
    q = S(snr)["ops"]["eb"]["rev"]
    for a in ("0.5", "0.1"):
        mac(f"S{tag}Tr{word(a)}Gain", pct(q[a]["gain_transported_vs_Rn"]["gain"]))
_trd = [(r["ops"]["eb"]["rev"]["0.1"]["risk_transported"][0] / r["risk_Rn"][0], r["dep_over_tau"]) for r in departure]
mac("DepTrTenMax", f"{max(_trd)[0]:.2f}"); mac("DepTrTenMaxAt", f"{max(_trd)[1]:g}")
_trh = [(r["ops"]["eb"]["rev"]["0.5"]["risk_transported"][0] / r["risk_Rn"][0], r["dep_over_tau"]) for r in departure]
mac("DepTrHalfMax", f"{max(_trh)[0]:.2f}"); mac("DepTrHalfMaxAt", f"{max(_trh)[1]:g}")
mac("TrHarmMaxTen", pct_up(max(r["ops"]["eb"]["rev"]["0.1"]["harm_freq_transported"] for r in structure + departure)))

with open(os.path.join(out_dir, "numbers.tex"), "w") as fh:
    fh.write("% generated by experiments/make_numbers.py -- do not edit\n" + "\n".join(L) + "\n")

# table bodies must not end with a row terminator: main.tex writes \input{...}\\ itself
# (a file ending in \\ leaves TeX unable to see the following \bottomrule)
for fn in os.listdir(out_dir):
    if fn.startswith("table_") and fn.endswith(".tex"):
        fp = os.path.join(out_dir, fn)
        body = open(fp).read().rstrip()
        if body.endswith("\\\\"):
            body = body[:-2].rstrip()
        open(fp, "w").write(body + "\n")
print(f"wrote {len(L)} macros and 9 table bodies to {out_dir}")
