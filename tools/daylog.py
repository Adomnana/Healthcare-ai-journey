#!/usr/bin/env python3
"""Log today's study day, update progress files, commit and push to GitHub.

Usage (run from anywhere inside the repo):
    python tools/daylog.py                      # log today's day, asks for a one-line note
    python tools/daylog.py -n "Built the CLI"   # note on the command line
    python tools/daylog.py --day 12             # log a specific day (catching up)
    python tools/daylog.py --no-push            # commit only, don't push
    python tools/daylog.py status               # show progress without changing anything
    python tools/daylog.py today                # show today's lesson, tasks and resources (--day N for another day)

What it updates:
    progress.json            machine-readable state
    PROGRESS.md              checklist of all 84 days
    journal/week-XX.md       your notes, one file per week
    README.md                progress bar between <!-- progress:start --> and <!-- progress:end -->
"""
import argparse
import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from curriculum import START_DATE, build_days  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "progress.json"
DAYS = build_days()
TOTAL = len(DAYS)


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"done": {}}


def save_state(state: dict) -> None:
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def todays_number() -> int:
    n = (date.today() - START_DATE).days + 1
    return max(1, min(TOTAL, n))


def streak(state: dict) -> int:
    dates = sorted({date.fromisoformat(v["date"]) for v in state["done"].values()})
    if not dates:
        return 0
    count, cur = 1, dates[-1]
    if (date.today() - cur).days > 1:
        return 0
    for d in reversed(dates[:-1]):
        if (cur - d).days == 1:
            count, cur = count + 1, d
        elif (cur - d).days == 0:
            continue
        else:
            break
    return count


def bar(state: dict) -> str:
    done = len(state["done"])
    pct = round(100 * done / TOTAL)
    filled = round(20 * done / TOTAL)
    return (f"**Progress:** `{'#' * filled}{'-' * (20 - filled)}` {pct}% "
            f"({done}/{TOTAL} days) | current streak: {streak(state)} day(s)")


def write_progress_md(state: dict) -> None:
    out = ["# Progress", "", bar(state), ""]
    week = 0
    for d in DAYS:
        if d["week"] != week:
            week = d["week"]
            out += ["", f"## Week {week}: {d['theme']}", f"*{d['project']}*", ""]
        mark = "x" if str(d["n"]) in state["done"] else " "
        note = state["done"].get(str(d["n"]), {}).get("note", "")
        suffix = f" - {note}" if note else ""
        out.append(f"- [{mark}] Day {d['n']} ({d['track']}): {d['title']}{suffix}")
    (ROOT / "PROGRESS.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def update_readme_bar(state: dict) -> None:
    readme = ROOT / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    a, b = "<!-- progress:start -->", "<!-- progress:end -->"
    if a in text and b in text:
        head, rest = text.split(a, 1)
        _, tail = rest.split(b, 1)
        readme.write_text(f"{head}{a}\n{bar(state)}\n{b}{tail}", encoding="utf-8")


def append_journal(d: dict, when: str, note: str) -> None:
    folder = ROOT / "journal"
    folder.mkdir(exist_ok=True)
    f = folder / f"week-{d['week']:02d}.md"
    if not f.exists():
        f.write_text(f"# Week {d['week']}: {d['theme']}\n\n*{d['project']}*\n\n", encoding="utf-8")
    with f.open("a", encoding="utf-8") as fh:
        fh.write(f"## Day {d['n']} - {d['title']} ({when})\n- {note or '(no note)'}\n\n")


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def commit_and_push(message: str, push: bool) -> None:
    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        print("Not a git repo yet. Run `git init` and add your GitHub remote, then re-run.")
        return
    git("add", "-A")
    c = git("commit", "-m", message)
    if c.returncode != 0:
        print("Nothing new to commit." if "nothing to commit" in c.stdout else c.stdout + c.stderr)
        return
    print(f"Committed: {message}")
    if push:
        p = git("push")
        if p.returncode == 0:
            print("Pushed to GitHub.")
        else:
            print("Push failed (check your remote / login). Your work is committed locally.")
            print(p.stderr.strip())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", nargs="?", default="log", choices=["log", "status", "today"])
    ap.add_argument("--day", type=int, help="Day number to log (default: today's)")
    ap.add_argument("-n", "--note", help="One-line note about what you did")
    ap.add_argument("--no-push", action="store_true")
    args = ap.parse_args()

    state = load_state()
    if args.command == "status":
        print(bar(state))
        nxt = next((d for d in DAYS if str(d["n"]) not in state["done"]), None)
        if nxt:
            print(f"Next up: Day {nxt['n']} ({nxt['track']}): {nxt['title']}")
        return

    n = args.day or todays_number()
    if not 1 <= n <= TOTAL:
        sys.exit(f"Day must be between 1 and {TOTAL}.")
    d = DAYS[n - 1]
    if args.command == "today":
        print(f"Day {n} | {d['track']}: {d['title']}")
        print(f"Week {d['week']}: {d['theme']}  ({d['project']})\n")
        print(f"WARM-UP:   https://exercism.org/tracks/python or https://www.kaggle.com/learn/python\n")
        print(f"DO:        {d['do']}\n")
        print(f"SHIP:      {d['out']}\n")
        print(f"RESOURCES: {d['res']}\n")
        if d["video"]:
            print(f"WATCH:     {d['video']}")
        return
    if str(n) in state["done"]:
        print(f"Day {n} is already logged; updating its note.")
    note = args.note
    if note is None:
        note = input(f"Day {n}: {d['title']}\nOne line: what did you do / ship? > ").strip()

    when = date.today().isoformat()
    state["done"][str(n)] = {"date": when, "note": note}
    save_state(state)
    append_journal(d, when, note)
    write_progress_md(state)
    update_readme_bar(state)
    print(bar(state))
    commit_and_push(f"Day {n}: {d['title']}", push=not args.no_push)


if __name__ == "__main__":
    main()
