# Healthcare AI Journey

A 12-week, project-based path through **Python + Healthcare AI + AI Automation**, learned side by side. Every week ends with something built and pushed to GitHub.

<!-- progress:start -->
**Progress:** `--------------------` 1% (1/84 days) | current streak: 1 day(s)
<!-- progress:end -->

## How it works

- **Daily rhythm:** 15-min Python warm-up, then the day's task. Weekdays ~1.5 h, Saturday ~3 h build block, Sunday ~1 h review.
- **Weekly rhythm:** Mon-Thu learn by doing small exercises, Fri-Sat build the project, Sun review and push.
- **Two tracks, one codebase:** Healthcare AI days and Automation days alternate, and Python is practised every day. The two meet in the capstones.
- **Practical first:** you read theory only when the next build needs it.

## The 3 months

| Month | Weeks | What you build |
|---|---|---|
| 1: Foundations by building | 1-4 | **P0** Vitals Logger CLI, **P1** Health Data Explorer (Streamlit), **P2** Daily Health Digest (automated, runs on GitHub Actions) |
| 2: Models, LLMs, retrieval | 5-8 | **P3** Disease Risk Predictor + model card, **P4** Clinical Note Extractor (synthetic notes), **P5** Guideline Q&A with citations (RAG) |
| 3: Capstones + launch | 9-12 | **Capstone A** Chronic Disease Risk Screening Assistant (Ghana focus), **Capstone B** Clinic Admin Automation Pipeline, portfolio + write-up |

Day-by-day detail lives in `tools/curriculum.py`, in `study_calendar.ics`, and as checkboxes in `PROGRESS.md`.

## Repo layout

```
healthcare-ai-journey/
├── README.md
├── PROGRESS.md            auto-generated checklist
├── progress.json          auto-generated state
├── study_calendar.ics     import into your calendar app
├── journal/               week-01.md ... (auto-appended notes)
├── exercises/             daily drills and small scripts
├── projects/
│   ├── 00-vitals-logger/
│   ├── 01-health-data-explorer/
│   ├── 02-daily-health-digest/
│   ├── 03-risk-predictor/
│   ├── 04-clinical-note-extractor/
│   ├── 05-guideline-qa-rag/
│   ├── capstone-a-risk-screening-assistant/
│   └── capstone-b-clinic-automation/
└── tools/                 curriculum.py, make_calendar.py, daylog.py
```

## Daily GitHub workflow (about 1 minute)

After each study session:

```bash
python tools/daylog.py -n "Built the add/list commands"
```

This marks the day done, appends your note to `journal/week-XX.md`, refreshes `PROGRESS.md` and the bar above, then commits (`Day 7: Vitals Logger CLI: core`) and pushes. Useful options: `--day 12` (catch up on a missed day), `--no-push`, and `python tools/daylog.py status`.

Commit your project code as you go with normal `git add` / `git commit`; `daylog.py` also sweeps up anything uncommitted.

## Calendar

1. Optional: change `START_DATE` in `tools/curriculum.py` (must be a Monday), then run `python tools/make_calendar.py`.
2. Import `study_calendar.ics` into Google Calendar (desktop web: Settings, Import & export), Apple Calendar or Outlook.
3. Each event has the day's task, what to ship, and a 15-minute reminder. Times are Accra time (UTC+0).

## Ground rules

1. **No real patient data, ever.** Use public datasets (UCI Heart Disease, Pima diabetes, WHO GHO open data) or synthetic data.
2. **Secrets never go in Git.** API keys live in `.env`; `.env` is in `.gitignore`.
3. **Nothing here is medical advice.** Every demo says so, and every model gets a model card with its limits.
4. **Ship small.** A finished, documented small project beats a perfect unfinished one.
5. If you fall behind, don't restart: skip to the current week's build days and catch up on exercises later.

## Free resources to lean on

Kaggle Learn (Python, Pandas, Data Visualization, Intro to ML), Exercism Python track, the official docs for pandas, scikit-learn, Streamlit and FastAPI, your LLM provider's API docs, and the n8n docs.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install pandas scikit-learn matplotlib seaborn streamlit pytest
```
Install the rest (FastAPI, pydantic, an LLM SDK, chromadb, etc.) in the week that needs it. The tooling in `tools/` uses only the Python standard library.
