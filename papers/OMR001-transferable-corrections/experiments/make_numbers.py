#!/usr/bin/env python3
"""Turn results/results.json into LaTeX macros (manuscript/numbers.tex) and table bodies."""
import json
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
mac("MetaSeconds", f"{meta['seconds']:.0f}"); mac("MetaPython", meta["python"])
mac("MetaNumpy", meta["numpy"]); mac("MetaScipy", meta["scipy"]); mac("MetaMpl", meta["matplotlib"])
mac("Cd", cfg["d"]); mac("CS", cfg["S"]); mac("Cns", cfg["n_s"]); mac("Cn", cfg["n"]); mac("Cm", cfg["m_default"])
mac("Cne", cfg["n"] - cfg["m_default"]); mac("CsnrDep", f"{cfg['snr_dep']:g}")
mac("CnConfigs", summ["n_configs_rev"]); mac("CnOps", len(cfg["operators"]))
mac("CsnrGrid", snrlist(cfg["snr_grid"])); mac("CdepGrid", snrlist(cfg["dep_grid"]))
mac("CmGrid", snrlist(cfg["m_grid"])); mac("CalphaGrid", snrlist(cfg["alpha_grid"]))
mac("CuseThr", pct(cfg["useful_threshold"], signed=False))
mac("SplitCost", pct(cfg["n"] / (cfg["n"] - cfg["m_default"]) - 1, signed=False))
mac("RefRiskE", f4(cfg["d"] / (cfg["n"] - cfg["m_default"]))); mac("RefRiskN", f4(cfg["d"] / cfg["n"]))

# constants of Theorem B
with open(os.path.join(out_dir, "table_constants.tex"), "w") as fh:
    for c in consts:
        fh.write(f"{c['alpha']:g} & {c['z']:.3f} & {c['phi_z']:.4f} & {c['kappa']:.4f} & {c['u_star']:.3f} & "
                 f"{c['ratio_kappa_over_phi']:.3f} & {c['regret_const']:.3f} \\\\\n")
for c in consts:
    w = word(str(c["alpha"]))
    mac(f"Kappa{w}", f"{c['kappa']:.4f}"); mac(f"Phiz{w}", f"{c['phi_z']:.4f}")
    mac(f"Ratio{w}", f"{c['ratio_kappa_over_phi']:.2f}")

# structure sweep tables (EB operator)
with open(os.path.join(out_dir, "table_structure.tex"), "w") as fh:
    for r in structure:
        e = r["ops"]["eb"]
        cells = [f"{r['snr']:g}", f"{r['lam_oracle']:.2f}", f4(r["risk_Rn"][0]),
                 f4(e["always_full"]["risk"][0]) + (r"$^{\mathrm U}$" if e["always_full"]["useful"] else "")]
        for a in ("0.5", "0.2", "0.1", "0.01"):
            q = e["rev"][a]
            cells.append(f4(q["risk"][0]) + (r"$^{\mathrm U}$" if q["useful"] else ""))
        q = e["rev"]["0.1"]
        cells.append(f4(q["risk_refit"][0]) + (r"$^{\mathrm U}$" if q["useful_refit"] else ""))
        cells.append(f4(e["sure"]["risk"][0]) + (r"$^{\mathrm U}$" if e["sure"]["useful"] else ""))
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
        cells = [f"{r['dep_over_tau']:g}", f4(r["risk_Rn"][0]), f4(e["always_full"]["risk"][0])]
        for a in ("0.5", "0.2", "0.1", "0.01"):
            cells.append(f4(e["rev"][a]["risk"][0]))
        q = e["rev"]["0.1"]
        cells += [f4(q["risk_refit"][0]), f4(e["sure"]["risk"][0])]
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
mac("SafeAll", yesno(summ["safe_phi_all"] and summ["safe_alpha_all"] and summ["safe_tight_all"]))
mac("SafeHarmAll", yesno(summ["safe_harm_freq_all"]))
mac("MaxExcessOverPhi", f"{summ['max_excess_over_bound_phi']:.2f}")
mac("MaxRegretOverBound", f"{summ['max_regret_over_bound']:.2f}")
mac("MaxIdentityZ", f"{summ['max_identity_abs_z']:.2f}")
mac("NIdentityCLT", summ["n_identity_clt"]); mac("NIdentityPoisson", summ["n_identity_poisson"])
mac("NIdentityFail", summ["n_identity_fail"])
for a in A:
    w = word(a)
    mac(f"UsefulRev{w}", snrlist(summ["useful_structure_eb"][a]))
    mac(f"UsefulRefit{w}", snrlist(summ["useful_structure_refit_eb"][a]))
    mac(f"HarmMax{w}", pct(summ["max_harm_freq_rev_eb"][a], signed=False))
    mac(f"AccHarmMax{w}", pct(summ["max_accept_given_harmful_eb"][a], signed=False))
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
        mac(f"D{tag}Rev{ww}BoundPhi", f"{q['bound_phi']:.4f}")
        mac(f"D{tag}Rev{ww}BoundAlpha", f"{q['bound_alpha']:.4f}")
        mac(f"D{tag}Rev{ww}BoundTight", f"{q['bound_tight']:.4f}")
    mac(f"D{tag}SureRatio", f"{e['sure']['risk'][0]/r['risk_Rn'][0]:.2f}")
    mac(f"D{tag}RefitTenRatio", f"{e['rev']['0.1']['risk_refit'][0]/r['risk_Rn'][0]:.2f}")
# m sweep named points (alpha = 0.1)
for r in msweep:
    q = r["ops"]["eb"]["rev"]["0.1"]
    tag = {3: "Three", 6: "Six", 12: "Twelve", 24: "TwentyFour"}[r["m"]] + ("Zero" if r["dep_over_tau"] == 0 else "Eight")
    mac(f"M{tag}RevGain", pct(q["gain_vs_Rn"]["gain"]))
    mac(f"M{tag}Excess", f"{q['excess_vs_Re'][0]:+.4f}")
    mac(f"M{tag}BoundPhi", f"{q['bound_phi']:.4f}")

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
print(f"wrote {len(L)} macros and 7 table bodies to {out_dir}")
