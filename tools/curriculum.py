"""
12-week (84-day) project-based curriculum: Python + Healthcare AI + AI Automation.

Edit START_DATE if you start on a different day. Everything else
(calendar, progress log, README bar) is generated from this file.

Daily rhythm: 15-min Python warm-up, then the day's task.
Tracks: PYTHON, HEALTH AI, AUTOMATION, BUILD, REVIEW.
"""
import re
from datetime import date
from urllib.parse import quote_plus

START_DATE = date(2026, 10, 8)  # Day 1 (any weekday works)

# Event times (Africa/Accra = UTC+0), by kind of day and whether it falls on a weekend.
# kind: learn (PYTHON/HEALTH AI/AUTOMATION), build (BUILD), review (REVIEW)
SLOTS = {
    ("learn", False): ("19:00", "20:30"), ("learn", True): ("10:00", "11:30"),
    ("build", False): ("19:00", "21:00"), ("build", True): ("10:00", "13:00"),
    ("review", False): ("19:00", "20:00"), ("review", True): ("17:00", "18:00"),
}


def slot_for(track, day):
    kind = "build" if track == "BUILD" else "review" if track == "REVIEW" else "learn"
    return SLOTS[(kind, day.weekday() >= 5)]


WARMUP = ("Start with a 15-min Python warm-up: https://exercism.org/tracks/python "
          "or https://www.kaggle.com/learn/python")

# Each week: theme, project focus, 6 day tuples (Mon-Sat), Sunday demo line.
# Day tuple = (track, title, what to do, what to ship/commit)
WEEKS = [
    dict(
        theme="Setup + Python fast-track",
        project="Project 0: Vitals Logger CLI",
        days=[
            ("PYTHON", "Environment + Git workflow",
             "Install Python 3.12 + VS Code, create a venv, clone/reorganise your healthcare-ai-journey repo with the folder layout from the README. Do 10 mini-exercises (functions, loops, conditionals) to test out of the basics you already know.",
             "First commit with the new repo layout + exercises/week01.py"),
            ("PYTHON", "Data structures + files",
             "Lists, dicts, sets, comprehensions. Read/write CSV and JSON. Parse a CSV of SYNTHETIC patient vitals into a list of dicts and compute averages.",
             "exercises/vitals_parse.py"),
            ("HEALTH AI", "Health data 101 + privacy",
             "Skim what EHRs, ICD-10 and FHIR are (30 min). Read the basics of Ghana's Data Protection Act, 2012 (Act 843). Write data-rules.md: never use real patient data, de-identify, keep secrets out of Git. Generate 50 synthetic patients with Python's random module or Faker.",
             "data-rules.md + synthetic_patients.csv"),
            ("AUTOMATION", "Folder organiser script",
             "Use pathlib + argparse to build a script that sorts a messy folder by file type/date. Add a --dry-run flag and logging.",
             "exercises/organiser.py committed"),
            ("BUILD", "Vitals Logger CLI: core",
             "Build a command-line tool: add, list and summarise readings (blood pressure, temperature, glucose) stored in JSON. Flag out-of-range values using simple documented thresholds.",
             "Working add/list/summary commands"),
            ("BUILD", "Vitals Logger CLI: tests + README",
             "Write 5 pytest tests, add a README with usage examples, tidy the code into functions.",
             "Project 0 pushed to GitHub with README"),
        ],
        demo="Vitals Logger CLI works and has tests",
    ),
    dict(
        theme="pandas + SQL for health data",
        project="Project 1: Health Data Explorer (start)",
        days=[
            ("PYTHON", "pandas I",
             "DataFrames, read_csv, head/info/describe, selecting and filtering. Load the UCI Heart Disease dataset and answer 5 questions about it.",
             "notebooks/01_heart_intro.ipynb"),
            ("HEALTH AI", "Cleaning clinical data",
             "Handle missing values, odd codes, outliers, wrong dtypes. Write a data dictionary for the heart dataset and log every cleaning decision with a reason.",
             "data_dictionary.md + cleaned CSV"),
            ("PYTHON", "pandas II + SQL tie-in",
             "groupby, merge, pivot. Load the data into SQLite and rewrite 5 of your pandas queries in SQL (you already know SQL, so use it as a cross-check).",
             "queries.sql + matching pandas code"),
            ("AUTOMATION", "APIs with requests",
             "Pull Ghana indicators from the WHO Global Health Observatory open data API into a CSV. Add error handling, timeouts and retries.",
             "scripts/fetch_who_ghana.py"),
            ("BUILD", "Explorer notebook",
             "Answer 8 questions about the heart data plus Ghana WHO indicators in one clean notebook, with a short written finding under each.",
             "Notebook with 8 questions answered"),
            ("BUILD", "Charts + findings",
             "Make 6 clear charts (matplotlib/seaborn), label axes, write a one-page summary of findings and limits of the data.",
             "Charts + findings.md pushed"),
        ],
        demo="Explorer notebook with 6 charts and findings",
    ),
    dict(
        theme="Dashboards + scheduled scripts",
        project="Project 1: Health Data Explorer (ship)",
        days=[
            ("PYTHON", "Modules, type hints, structure",
             "Refactor last week's notebook code into a src/ package: functions, type hints, docstrings.",
             "src/health_explorer/ package"),
            ("HEALTH AI", "EDA done right",
             "Correlations, class balance, stratified summaries by sex/age. Ask: who is represented in this dataset, and how is that different from patients in Ghana?",
             "Bias/representativeness section in findings.md"),
            ("PYTHON", "Streamlit basics",
             "Widgets, layout, caching. Build a skeleton app that loads your cleaned data and shows a table.",
             "app.py skeleton running locally"),
            ("AUTOMATION", "Email + scheduling",
             "Send an email from Python (smtplib or an email API) using secrets from a .env file. Schedule a script with cron / Task Scheduler. Never commit .env.",
             "scripts/send_report.py + .gitignore with .env"),
            ("BUILD", "Streamlit dashboard",
             "Turn the explorer into a dashboard with filters (age, sex, outcome) and 3 live charts.",
             "Dashboard working locally"),
            ("BUILD", "Deploy + README",
             "Deploy to Streamlit Community Cloud, add screenshots and a how-to-run section to the README.",
             "Live link in README, Project 1 shipped"),
        ],
        demo="Dashboard deployed with a live link",
    ),
    dict(
        theme="Automation I: Daily Health Digest",
        project="Project 2: Daily Health Digest + Month 1 checkpoint",
        days=[
            ("PYTHON", "Errors, logging, pytest",
             "try/except done properly, the logging module, pytest fixtures. Add logging and tests to your fetch script.",
             "tests/ folder with 5+ tests"),
            ("AUTOMATION", "RSS + storage",
             "Fetch health news from public RSS feeds (e.g. WHO), dedupe by URL, store in SQLite.",
             "scripts/fetch_news.py + news.db schema"),
            ("AUTOMATION", "LLM summaries",
             "Call an LLM API (Claude or any provider) to summarise each article in 2 sentences. Keep API keys in env vars, cap costs with a daily item limit.",
             "summarise.py with a prompt you can explain"),
            ("HEALTH AI", "First ML model (preview)",
             "Train/test split, overfitting, accuracy vs other metrics. Fit a logistic regression on the heart data in 20 lines and read the results critically.",
             "notebooks/04_first_model.ipynb"),
            ("BUILD", "Digest pipeline",
             "Wire it together: fetch, dedupe, summarise, build an HTML/plain-text digest, email it to yourself.",
             "End-to-end run succeeds locally"),
            ("BUILD", "GitHub Actions cron",
             "Run the pipeline daily with a GitHub Actions schedule and repo secrets. Add a README with an architecture sketch.",
             "Project 2 live and running daily"),
        ],
        demo="Month 1 checkpoint: 3 projects shipped, repo README updated",
    ),
    dict(
        theme="ML for clinical prediction I",
        project="Project 3: Disease Risk Predictor (build)",
        days=[
            ("PYTHON", "NumPy + sklearn pipelines",
             "NumPy essentials, then sklearn Pipeline and ColumnTransformer so preprocessing is part of the model.",
             "exercises/pipelines.py"),
            ("HEALTH AI", "Baseline models",
             "Logistic regression, random forest and gradient boosting on the Pima diabetes or heart dataset with cross-validation. Compare them in one table.",
             "Model comparison table"),
            ("PYTHON", "Features + data leakage",
             "Feature engineering and a leakage hunt: check whether any column gives away the label or comes from after diagnosis. Document what you find.",
             "leakage_check.md"),
            ("AUTOMATION", "Automated experiments",
             "Script that trains several models from a YAML config and logs results to a CSV, so you can rerun everything with one command.",
             "run_experiments.py + config.yaml"),
            ("BUILD", "Risk Predictor: training",
             "Create the project folder with a clean train.py, evaluation table and saved results.",
             "projects/03-risk-predictor/train.py working"),
            ("BUILD", "Tune + save",
             "Hyperparameter tuning (GridSearchCV or Optuna), save the best model with joblib, push.",
             "model.joblib + metrics.json"),
        ],
        demo="Trained, tuned risk model with reproducible training script",
    ),
    dict(
        theme="Evaluation that matters in healthcare",
        project="Project 3: Disease Risk Predictor (ship)",
        days=[
            ("HEALTH AI", "Clinical metrics",
             "Sensitivity, specificity, ROC-AUC, precision-recall, thresholds. Why accuracy misleads for screening. Pick a threshold for a screening use case and justify it.",
             "metrics_notes.md"),
            ("PYTHON", "Evaluation plots",
             "Matplotlib: ROC curve, calibration curve, confusion matrix. Package them into a reusable evaluate.py.",
             "evaluate.py + 3 saved plots"),
            ("HEALTH AI", "Explainability + fairness",
             "Permutation importance or SHAP. Check performance by subgroup (sex, age bands) and record gaps.",
             "explainability.ipynb"),
            ("AUTOMATION", "Model as an API",
             "Wrap the model in a FastAPI /predict endpoint with pydantic validation. Test with curl and pytest.",
             "api.py + tests"),
            ("BUILD", "Model card + UI",
             "Write the model card (intended use, data, metrics, limits, ethics) and a Streamlit risk-calculator that calls your API.",
             "MODEL_CARD.md + UI working"),
            ("BUILD", "Deploy + polish",
             "Deploy the UI (and API if you can), add a clear 'not medical advice' notice, README with results. Optional: Dockerfile.",
             "Project 3 shipped with live link"),
        ],
        demo="Risk predictor with model card and live demo",
    ),
    dict(
        theme="LLMs for health text",
        project="Project 4: Clinical Note Extractor (synthetic data only)",
        days=[
            ("PYTHON", "Structured data with pydantic",
             "Pydantic models, JSON schema, validating messy input. Practise turning free text into typed objects.",
             "exercises/pydantic_schemas.py"),
            ("HEALTH AI", "Prompting on clinical text",
             "Generate 30 SYNTHETIC clinical notes (LLM or Synthea). Write prompts to summarise and extract symptoms, medications and dosages. Never use real patient notes.",
             "data/synthetic_notes/ + prompts.md"),
            ("AUTOMATION", "Extraction pipeline",
             "LLM output to JSON validated by pydantic to CSV. Add retries when the JSON is invalid.",
             "extract.py producing notes.csv"),
            ("HEALTH AI", "Evaluate the LLM",
             "Hand-label a 20-note gold set. Measure precision/recall per field and keep a failure log of what the model gets wrong.",
             "eval/results.md"),
            ("BUILD", "Extractor app",
             "Streamlit app: paste a note, get a structured summary and extracted fields side by side.",
             "App working locally"),
            ("BUILD", "Guardrails + README",
             "Add disclaimers, a PII-scrub step, refuse-to-diagnose behaviour. README with your eval numbers and known failures.",
             "Project 4 shipped"),
        ],
        demo="Extractor app with measured accuracy and failure log",
    ),
    dict(
        theme="RAG + agents on health guidelines",
        project="Project 5: Guideline Q&A with citations + Month 2 checkpoint",
        days=[
            ("PYTHON", "Documents to chunks",
             "Parse PDFs (pypdf), clean text, chunk it sensibly. Learn what embeddings are by playing with a small example.",
             "ingest/parse_pdf.py"),
            ("AUTOMATION", "Ingestion pipeline",
             "Public guideline PDFs (e.g. WHO guidance or Ghana's standard treatment guidelines) to chunks to embeddings to a vector store (Chroma or FAISS).",
             "ingest pipeline runs end to end"),
            ("HEALTH AI", "RAG with citations",
             "Retrieve the top chunks, answer using only them, and show source page numbers. Make the model say 'I don't know' when the guidelines don't cover the question.",
             "rag.py with citations"),
            ("AUTOMATION", "Evaluate RAG",
             "Write 15 test questions. Check retrieval hits, groundedness and the I-don't-know behaviour. Fix the weakest 3.",
             "eval/rag_eval.md"),
            ("BUILD", "Chat UI",
             "Streamlit chat interface with expandable source snippets under every answer.",
             "Chat app working"),
            ("BUILD", "Polish + month 2 write-up",
             "README, screenshots, limitations section. Write a short post on what you built in month 2.",
             "Project 5 shipped"),
        ],
        demo="Month 2 checkpoint: 6 projects shipped, one blog/LinkedIn draft",
    ),
    dict(
        theme="Capstones: planning + Capstone A start",
        project="Capstone A: Chronic Disease Risk Screening Assistant (Ghana focus)",
        days=[
            ("PYTHON", "Project architecture",
             "Repo layout, config handling, modules, Makefile or task runner. Set up both capstone repos/folders.",
             "projects/capstone-a/ and capstone-b/ skeletons"),
            ("HEALTH AI", "Capstone A spec",
             "One-page spec: problem, users, dataset(s), success metrics, risks, what the tool will NOT do. Risk model + plain-language explanation layer, built on Ghana-relevant context.",
             "docs/spec.md"),
            ("AUTOMATION", "Capstone B spec",
             "Clinic admin automation: intake form to extraction to triage category to notification to dashboard. Model the workflow as a BPMN diagram (you already know BPMN).",
             "docs/workflow.bpmn or .png + spec.md"),
            ("HEALTH AI", "Capstone A data pipeline",
             "Build the cleaning/feature pipeline for Capstone A using your earlier work. Add data checks.",
             "pipeline.py + tests"),
            ("BUILD", "Capstone A model",
             "Train, evaluate and tune using your Project 3 playbook. Record threshold choice and subgroup results.",
             "Trained model + metrics"),
            ("BUILD", "Capstone A API + tests",
             "FastAPI endpoint, input validation, tests, simple CI with GitHub Actions.",
             "Green CI badge in README"),
        ],
        demo="Capstone A has spec, model and API; Capstone B has spec and workflow",
    ),
    dict(
        theme="Capstone A finish + workflow tools",
        project="Capstone A: ship",
        days=[
            ("PYTHON", "Quality pass",
             "Linting (ruff), formatting, test coverage on the capstone code. Fix the 5 worst smells.",
             "Cleaner code, coverage report"),
            ("HEALTH AI", "Explanation layer",
             "Add feature explanations and an LLM-written plain-language summary for a result, with strict guardrails (no diagnosis, advise seeing a clinician).",
             "explain.py + guardrail tests"),
            ("AUTOMATION", "n8n workflow basics",
             "Run n8n locally, build a webhook-triggered workflow that calls your API and sends a notification. Compare it with doing the same in Python.",
             "workflows/n8n_intro.json exported"),
            ("BUILD", "Capstone A UI",
             "Streamlit interface: inputs, result, explanation, clear limits notice.",
             "UI working"),
            ("BUILD", "Capstone A deploy",
             "Deploy, test from your phone, fix what breaks.",
             "Live link"),
            ("BUILD", "Capstone A docs",
             "Model card, README with demo GIF, ethics and limitations section.",
             "Capstone A shipped"),
        ],
        demo="Capstone A live with model card",
    ),
    dict(
        theme="Capstone B build",
        project="Capstone B: Clinic Admin Automation Pipeline",
        days=[
            ("AUTOMATION", "Intake + webhook",
             "A simple intake form (FastAPI form or Google Form) that sends data to your pipeline. Use synthetic submissions only.",
             "intake endpoint + 10 test submissions"),
            ("AUTOMATION", "LLM extraction + urgency",
             "Extract key fields and assign a triage category with a confidence score. Low confidence goes to a human.",
             "triage.py + prompts"),
            ("PYTHON", "Storage layer",
             "SQLite (or Postgres) tables for submissions, extracted fields, decisions, audit log. Write the data access code and tests.",
             "db.py + tests"),
            ("AUTOMATION", "Notifications",
             "Notify the right person by email or Telegram bot depending on category. Add rate limits and failure handling.",
             "notify.py working"),
            ("BUILD", "Human-in-the-loop review",
             "Review screen where a person approves or corrects the AI's triage. Log every correction.",
             "Review UI working"),
            ("BUILD", "Dashboard",
             "Streamlit dashboard: volume per day, categories, AI-vs-human agreement rate.",
             "Dashboard with real metrics"),
        ],
        demo="Capstone B working end to end on synthetic data",
    ),
    dict(
        theme="Polish, publish, plan what's next",
        project="Portfolio launch",
        days=[
            ("PYTHON", "Final code cleanup",
             "Refactor, lint, raise test coverage on both capstones. Delete dead code and unused notebooks.",
             "Clean main branches"),
            ("BUILD", "READMEs that sell",
             "For every project: problem, demo link, screenshot, how to run, results, limitations. Pin your best 4 repos on GitHub.",
             "8 READMEs updated"),
            ("BUILD", "Profile + portfolio",
             "GitHub profile README, update your personal website/CV with project links and one-line results.",
             "Profile and site updated"),
            ("BUILD", "Demo videos",
             "Record 2-3 minute walk-throughs of both capstones: problem, demo, what you'd improve.",
             "Videos linked in READMEs"),
            ("BUILD", "Write it up",
             "Write a post: what you built in 3 months, what failed, what you learned. Publish on LinkedIn or a blog.",
             "Post published"),
            ("REVIEW", "Explain your projects",
             "Practise explaining each project aloud in 2 minutes: problem, approach, result, limits, what's next. Draft your next 3-month plan.",
             "next_steps.md"),
        ],
        demo="Portfolio launched, next 3-month plan drafted",
    ),
]


# Day-specific starting resources, keyed by day number. Pages move around: if a link
# 404s, search the resource name. Sundays use the review resources below.
REVIEW_RES = "Your journal/week-XX.md and PROGRESS.md; open your GitHub repo page afterwards to confirm the push."
RESOURCES = {
    1: "Exercism Python track (exercism.org/tracks/python); Python tutorial (docs.python.org/3/tutorial); VS Code Python setup (code.visualstudio.com/docs/python/python-tutorial); Pro Git book ch. 1-2 (git-scm.com/book)",
    2: "Python tutorial: Data Structures + Input and Output (docs.python.org/3/tutorial); csv and json module docs; Kaggle Learn Python (kaggle.com/learn/python)",
    3: "Ghana Data Protection Act 2012 (Act 843): Data Protection Commission, dataprotection.org.gh; FHIR overview (hl7.org/fhir/overview.html); ICD-10 browser (icd.who.int/browse10); Faker docs (faker.readthedocs.io)",
    4: "Python docs: pathlib, argparse, logging (docs.python.org/3/library); Automate the Boring Stuff, files chapters (automatetheboringstuff.com)",
    5: "argparse tutorial (docs.python.org/3/howto/argparse.html); json module docs; your Day 1-2 exercise code",
    6: "pytest Get Started (docs.pytest.org); Make a README (makeareadme.com)",
    8: "Kaggle Learn Pandas (kaggle.com/learn/pandas); 10 minutes to pandas (pandas.pydata.org); UCI Heart Disease dataset (archive.ics.uci.edu, search 'Heart Disease')",
    9: "Kaggle Learn Data Cleaning (kaggle.com/learn/data-cleaning); pandas docs: Working with missing data",
    10: "Kaggle Learn Intro to SQL (kaggle.com/learn/intro-to-sql); Python sqlite3 docs; pandas read_sql / to_sql docs",
    11: "WHO Global Health Observatory OData API (search 'WHO GHO OData API'); requests Quickstart (requests.readthedocs.io)",
    12: "Kaggle Learn Data Visualization (kaggle.com/learn/data-visualization); matplotlib quick start (matplotlib.org)",
    13: "seaborn tutorial (seaborn.pydata.org/tutorial.html); matplotlib docs",
    15: "Real Python: modules, packages and type hints (realpython.com); Python docs: typing",
    16: "Paper: 'Datasheets for Datasets' (search the title); WHO guidance 'Ethics and governance of artificial intelligence for health'",
    17: "Streamlit docs: Get started + API reference (docs.streamlit.io)",
    18: "Python docs: smtplib, email; python-dotenv (pypi.org/project/python-dotenv); crontab.guru for cron schedules on Mac",
    19: "Streamlit docs: widgets, layouts, charts (docs.streamlit.io)",
    20: "Streamlit Community Cloud docs: Deploy your app (docs.streamlit.io)",
    22: "pytest docs: fixtures; Python Logging HOWTO (docs.python.org/3/howto/logging.html)",
    23: "feedparser docs (feedparser.readthedocs.io); WHO RSS feeds (search 'WHO RSS feeds'); sqlite3 docs",
    24: "Your LLM provider's API quickstart and prompt engineering guide (Claude: docs.claude.com); GitHub docs: 'Removing sensitive data from a repository'",
    25: "Kaggle Learn Intro to Machine Learning (kaggle.com/learn/intro-to-machine-learning); scikit-learn Getting Started (scikit-learn.org)",
    26: "Python docs: email.message; Jinja2 docs, optional for HTML email (jinja.palletsprojects.com)",
    27: "GitHub Actions Quickstart + 'schedule' event + 'Using secrets' (docs.github.com/actions)",
    29: "NumPy absolute beginners guide (numpy.org/doc/stable/user/absolute_beginners.html); scikit-learn user guide: Pipelines and composite estimators",
    30: "Pima Indians Diabetes dataset (search Kaggle or UCI); scikit-learn Cross-validation docs; Kaggle Learn Intermediate Machine Learning (kaggle.com/learn/intermediate-machine-learning)",
    31: "Kaggle Intermediate ML: Data Leakage lesson; scikit-learn docs: Common pitfalls (data leakage)",
    32: "PyYAML docs (pyyaml.org); argparse; pandas to_csv docs",
    33: "scikit-learn docs: Model selection and evaluation; your Week 5 notebooks",
    34: "scikit-learn GridSearchCV docs; Optuna (optuna.org); joblib persistence docs",
    36: "scikit-learn Metrics docs: ROC, precision-recall; Google ML Crash Course: Classification metrics (developers.google.com/machine-learning/crash-course)",
    37: "scikit-learn ConfusionMatrixDisplay and CalibrationDisplay docs; matplotlib docs",
    38: "SHAP docs (shap.readthedocs.io); scikit-learn: Permutation feature importance; paper 'Model Cards for Model Reporting'",
    39: "FastAPI tutorial (fastapi.tiangolo.com/tutorial); Pydantic docs (docs.pydantic.dev)",
    40: "'Model Cards for Model Reporting' (search the title); Streamlit docs",
    41: "Streamlit Community Cloud docs; optional: Docker Get Started (docs.docker.com/get-started)",
    43: "Pydantic docs: Models and Validation; Python json docs",
    44: "Synthea synthetic patients (synthetichealth.github.io/synthea); your LLM provider's prompt engineering guide (docs.claude.com)",
    45: "Your LLM provider docs: structured output / tool use; tenacity retries (tenacity.readthedocs.io)",
    46: "scikit-learn precision_recall_fscore_support docs; blog post 'Your AI Product Needs Evals' by Hamel Husain (search the title)",
    47: "Streamlit docs: text_area, columns, session_state",
    48: "Microsoft Presidio docs for PII detection (microsoft.github.io/presidio); WHO guidance on ethics and governance of AI for health",
    50: "pypdf docs (pypdf.readthedocs.io); search 'chunking strategies for RAG'; search 'The Illustrated Word2vec' for embeddings intuition",
    51: "Chroma docs (docs.trychroma.com); sentence-transformers (sbert.net) or your LLM provider's embeddings docs; Ghana Standard Treatment Guidelines (Ministry of Health Ghana) and WHO publications (who.int/publications)",
    52: "Your LLM provider's RAG and citations docs (docs.claude.com, search 'citations')",
    53: "Ragas docs, optional (docs.ragas.io); or a simple spreadsheet of 15 questions with pass/fail columns",
    54: "Streamlit docs: st.chat_message and st.chat_input",
    55: "makeareadme.com; your journal entries from weeks 5-8",
    57: "Cookiecutter Data Science (cookiecutter-data-science.drivendata.org); Real Python: Python Application Layouts",
    58: "Google People + AI Guidebook (pair.withgoogle.com/guidebook); search 'ML design doc template'",
    59: "diagrams.net or bpmn.io (tools you already know); n8n docs overview (docs.n8n.io)",
    60: "pandas docs; Great Expectations (greatexpectations.io) or plain assert checks",
    61: "scikit-learn docs; your Project 3 model card and evaluate.py",
    62: "FastAPI docs: Testing; GitHub Actions docs: Building and testing Python (docs.github.com/actions)",
    64: "Ruff docs (docs.astral.sh/ruff); pytest-cov docs",
    65: "Your LLM provider's docs on system prompts and safety; SHAP docs",
    66: "n8n docs: Webhook node and running n8n locally (docs.n8n.io)",
    67: "Streamlit docs",
    68: "Streamlit Community Cloud docs; Hugging Face Spaces or Render docs for hosting an API",
    69: "makeareadme.com; Kap screen recorder for GIFs (getkap.co); Model Cards paper",
    71: "FastAPI docs: Form data; optionally Google Forms with Apps Script webhooks",
    72: "Your LLM provider's structured output docs; your Week 7 extraction code",
    73: "SQLite docs; SQLAlchemy tutorial (docs.sqlalchemy.org)",
    74: "Telegram Bot API (core.telegram.org/bots); Python smtplib docs",
    75: "Streamlit docs: forms and session_state; Google People + AI Guidebook",
    76: "Streamlit charts docs; pandas groupby and resample docs",
    78: "Ruff and pytest-cov docs; your own test failures",
    79: "makeareadme.com; GitHub docs: pinning repos and profile README (docs.github.com)",
    80: "GitHub docs: Managing your profile README; your personal website project",
    81: "Built into Mac: QuickTime Player, File > New Screen Recording; or Loom free tier",
    82: "Your journal/week-XX.md files as raw material; LinkedIn post or any blog platform",
    83: "Mock interview partners (Pramp, or a friend); your READMEs as speaking notes",
}


# YouTube search queries per day. These open search results (links never go stale);
# pick a recent, well-rated tutorial. Good channels: freeCodeCamp, Corey Schafer,
# Tech With Tim, StatQuest, Kaggle, Real Python.
VIDEO = {
    1: "python virtual environment venv mac vscode tutorial", 2: "python lists dictionaries sets comprehensions tutorial",
    3: "FHIR explained for beginners", 4: "python pathlib organize files automation tutorial",
    5: "python argparse command line tool tutorial", 6: "pytest tutorial for beginners",
    8: "pandas tutorial for beginners", 9: "pandas data cleaning missing values tutorial",
    10: "python sqlite pandas read_sql tutorial", 11: "python requests API tutorial retries",
    12: "matplotlib tutorial for beginners", 13: "seaborn data visualization tutorial",
    15: "python modules packages type hints tutorial", 16: "exploratory data analysis dataset bias tutorial",
    17: "streamlit tutorial for beginners", 18: "python send email smtplib tutorial",
    19: "streamlit dashboard pandas tutorial", 20: "deploy streamlit app community cloud",
    22: "python logging tutorial", 23: "python feedparser rss tutorial",
    24: "LLM API python tutorial summarize text", 25: "scikit-learn logistic regression tutorial",
    26: "python html email automation tutorial", 27: "github actions schedule cron python tutorial",
    29: "scikit-learn pipeline columntransformer tutorial", 30: "cross validation random forest scikit-learn tutorial",
    31: "data leakage machine learning explained", 32: "python yaml config machine learning experiments",
    33: "scikit-learn compare models tutorial", 34: "gridsearchcv optuna hyperparameter tuning tutorial",
    36: "sensitivity specificity roc auc explained", 37: "calibration curve confusion matrix scikit-learn",
    38: "SHAP explained machine learning tutorial", 39: "fastapi tutorial deploy machine learning model",
    40: "model cards machine learning explained", 41: "deploy streamlit app docker tutorial",
    43: "pydantic tutorial python", 44: "LLM extraction clinical notes prompt engineering",
    45: "LLM structured output json pydantic tutorial", 46: "evaluating LLM outputs evals tutorial",
    47: "streamlit text input app tutorial", 48: "PII redaction presidio tutorial",
    50: "python pypdf extract text chunking RAG", 51: "chroma vector database RAG python tutorial",
    52: "RAG with citations tutorial", 53: "evaluate RAG pipeline tutorial",
    54: "streamlit chatbot tutorial", 55: "how to write a great github readme",
    57: "python project structure best practices", 58: "machine learning project design doc problem definition",
    59: "n8n tutorial for beginners", 60: "data validation pandas great expectations tutorial",
    61: "scikit-learn training evaluation pipeline tutorial", 62: "fastapi testing pytest github actions",
    64: "ruff python linter tutorial pytest coverage", 65: "LLM guardrails safety healthcare",
    66: "n8n webhook workflow tutorial", 67: "streamlit layout ui tutorial",
    68: "deploy fastapi render tutorial", 69: "record demo gif mac readme",
    71: "fastapi form data tutorial", 72: "LLM classification confidence threshold human in the loop",
    73: "sqlalchemy sqlite tutorial python", 74: "telegram bot python tutorial notifications",
    75: "human in the loop AI review interface streamlit", 76: "streamlit dashboard charts tutorial",
    78: "python code refactoring cleanup tutorial", 79: "github profile readme pin repositories tutorial",
    80: "github profile readme tutorial", 81: "record screen demo video mac tutorial",
    82: "how to write a technical blog post about your projects", 83: "explain your data science project in an interview",
}

_URL_RE = re.compile(r"(?<![/\w.@-])((?:[a-z0-9-]+\.)+(?:org|com|io|dev|net|co|ai|int)(?:/[^\s;,)\]]*)?)")


def link_fix(text):
    """Turn bare domains like docs.python.org/3/tutorial into clickable https:// links."""
    return _URL_RE.sub(lambda m: "https://" + m.group(1), text)


def video_url(n):
    q = VIDEO.get(n)
    return "https://www.youtube.com/results?search_query=" + quote_plus(q) if q else ""


def build_days():
    """Flatten WEEKS into 84 day dicts."""
    days = []
    n = 0
    for w_index, week in enumerate(WEEKS, start=1):
        for d_index, (track, title, do, out) in enumerate(week["days"]):
            n += 1
            days.append(dict(n=n, week=w_index, weekday=d_index, track=track,
                             title=title, do=do, out=out, res=link_fix(RESOURCES.get(n, "")), video=video_url(n),
                             theme=week["theme"], project=week["project"]))
        n += 1
        days.append(dict(
            n=n, week=w_index, weekday=6, track="REVIEW",
            title=f"Week {w_index} review + push",
            do=("Write your weekly journal: what worked, what broke, what you'd do differently. "
                "Tick off the week's days and push everything with `python tools/daylog.py`."),
            out=week["demo"], res=REVIEW_RES.replace("week-XX", f"week-{w_index:02d}"), video="",
            theme=week["theme"], project=week["project"]))
    return days


if __name__ == "__main__":
    ds = build_days()
    print(len(ds), "days;", START_DATE.strftime("%A"), "start")
