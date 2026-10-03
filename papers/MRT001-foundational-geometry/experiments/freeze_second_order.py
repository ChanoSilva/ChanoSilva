#!/usr/bin/env python3
"""Freeze the output of theory/check_second_order.py into results/ (v0.8, round 5).

theory/check_second_order.py writes its log (with timings) and a JSON into theory/.  This script
never modifies theory/.  It reads that log and JSON (or, with --run, runs the check in a temporary
copy of the directory layout and reads the copy's files), removes the timing information, and writes

  results/check_second_order_output.txt      log without timing lines (reproducible SHA-256)
  results/check_second_order_output.sha256
  results/second_order_results.json          JSON without the 'cpu_seconds' entry
  results/check_second_order_meta.json       SHA-256 of both files, CPU seconds of the run, versions

make_numbers.py verifies both SHA-256 before generating the macros of the second-order results.
"""
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TIMING = re.compile(r" \(\d+(?:\.\d+)?s\)$")


def strip(txt):
    out = []
    for line in txt.splitlines():
        if line.startswith("total CPU time:"):
            continue
        out.append(TIMING.sub("", line))
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="rerun the check in a temporary copy first")
    ap.add_argument("--src", default=os.path.join(ROOT, "theory"), help="directory holding the log and JSON")
    args = ap.parse_args()
    src = args.src
    tmp = None
    if args.run:
        tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(tmp, "theory"))
        os.makedirs(os.path.join(tmp, "experiments"))
        for f in ("check_second_order.py", "check_realizer_law.py"):
            shutil.copy(os.path.join(ROOT, "theory", f), os.path.join(tmp, "theory", f))
        shutil.copy(os.path.join(ROOT, "experiments", "lorentzian_chain.py"), os.path.join(tmp, "experiments"))
        subprocess.run([sys.executable, "check_second_order.py"], cwd=os.path.join(tmp, "theory"), check=True,
                       stdout=subprocess.DEVNULL)
        src = os.path.join(tmp, "theory")
    log = open(os.path.join(src, "check_second_order_output.txt")).read()
    res = json.load(open(os.path.join(src, "second_order_results.json")))
    m = re.search(r"^total CPU time: ([\d.]+) s", log, flags=re.M)
    seconds = float(m.group(1)) if m else res.get("cpu_seconds")
    res.pop("cpu_seconds", None)
    frozen = strip(log)
    jtxt = json.dumps(res, indent=1, sort_keys=True) + "\n"
    rdir = os.path.join(ROOT, "results")
    open(os.path.join(rdir, "check_second_order_output.txt"), "w").write(frozen)
    open(os.path.join(rdir, "second_order_results.json"), "w").write(jtxt)
    sha = hashlib.sha256(frozen.encode()).hexdigest()
    sha_j = hashlib.sha256(jtxt.encode()).hexdigest()
    open(os.path.join(rdir, "check_second_order_output.sha256"), "w").write(f"{sha}  check_second_order_output.txt\n")
    try:
        import mpmath
        import numpy
        vers = {"numpy": numpy.__version__, "mpmath": mpmath.__version__}
    except ImportError:
        vers = {}
    meta = {"script": "theory/check_second_order.py", "frozen_by": "experiments/freeze_second_order.py",
            "source": "rerun in a temporary copy" if args.run else os.path.relpath(src, ROOT),
            "deterministic": True, "seconds": seconds, "cpu": "one core",
            "sha256_frozen_output": sha, "sha256_frozen_json": sha_j,
            "python": platform.python_version(), **vers}
    json.dump(meta, open(os.path.join(rdir, "check_second_order_meta.json"), "w"), indent=1)
    if tmp:
        shutil.rmtree(tmp)
    print(sha, sha_j)


if __name__ == "__main__":
    main()
