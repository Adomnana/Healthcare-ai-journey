#!/usr/bin/env python3
"""Generate study_calendar.ics (one event per day) from curriculum.py.

Usage:
    python tools/make_calendar.py                 # uses START_DATE in curriculum.py
    python tools/make_calendar.py --start 2026-10-19

Times are in Africa/Accra (UTC+0, no daylight saving), so they are written as UTC.
Import the .ics into Google/Apple/Outlook Calendar. Re-importing after edits
updates the same events (stable UIDs) in most calendar apps.
"""
import argparse
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from curriculum import START_DATE, SLOTS, WARMUP, build_days

ROOT = Path(__file__).resolve().parent.parent


def esc(text: str) -> str:
    return (text.replace("\\", "\\\\").replace(";", "\\;")
                .replace(",", "\\,").replace("\n", "\\n"))


def fold(line: str) -> str:
    """RFC 5545 line folding at 75 octets."""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    parts, current = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        limit = 75 if not parts else 74
        if len(current) + len(b) > limit:
            parts.append(current)
            current = b
        else:
            current += b
    parts.append(current)
    return "\r\n ".join(p.decode("utf-8") for p in parts)


def build_ics(start: date) -> str:
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0",
        "PRODID:-//healthcare-ai-journey//study plan//EN",
        "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
        "X-WR-CALNAME:Healthcare AI + Automation: 12-week plan",
        "X-WR-TIMEZONE:Africa/Accra",
    ]
    for d in build_days():
        day = start + timedelta(days=d["n"] - 1)
        s, e = SLOTS[day.weekday()]
        dtstart = datetime.strptime(f"{day.isoformat()} {s}", "%Y-%m-%d %H:%M")
        dtend = datetime.strptime(f"{day.isoformat()} {e}", "%Y-%m-%d %H:%M")
        summary = f"Day {d['n']} | {d['track']}: {d['title']}"
        desc = (f"Week {d['week']}: {d['theme']}\n"
                f"Project: {d['project']}\n\n"
                f"{WARMUP}\n\n"
                f"DO: {d['do']}\n\n"
                f"SHIP: {d['out']}\n\n"
                f"When done, log it: python tools/daylog.py")
        lines += [
            "BEGIN:VEVENT",
            f"UID:hai-journey-day{d['n']:02d}@healthcare-ai-journey",
            f"DTSTAMP:{now}",
            f"DTSTART:{dtstart.strftime('%Y%m%dT%H%M%SZ')}",
            f"DTEND:{dtend.strftime('%Y%m%dT%H%M%SZ')}",
            f"SUMMARY:{esc(summary)}",
            f"DESCRIPTION:{esc(desc)}",
            f"CATEGORIES:{esc(d['track'])}",
            "BEGIN:VALARM", "TRIGGER:-PT15M", "ACTION:DISPLAY",
            f"DESCRIPTION:{esc(summary)}", "END:VALARM",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(l) for l in lines) + "\r\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", help="Day 1 date (YYYY-MM-DD), should be a Monday")
    ap.add_argument("--out", default=str(ROOT / "study_calendar.ics"))
    args = ap.parse_args()
    start = date.fromisoformat(args.start) if args.start else START_DATE
    if start.weekday() != 0:
        print("Note: start date is not a Monday; Sunday/Saturday time slots will shift.")
    Path(args.out).write_text(build_ics(start), encoding="utf-8", newline="")
    print(f"Wrote {args.out} (Day 1 = {start}, Day 84 = {start + timedelta(days=83)})")


if __name__ == "__main__":
    main()
