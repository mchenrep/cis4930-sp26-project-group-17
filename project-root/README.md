# Full-Stack Data Web Application

An end-to-end data project that ingests data from a public API, performs exploratory analysis on a real-world dataset, and surfaces both through a deployed Django web application with an interactive analytics dashboard.

The repository is organized as three connected sub-projects that together demonstrate the full lifecycle of a data product — **ingest → analyze → serve**.

---

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Sub-Projects](#sub-projects)
  - [1. Automated Data Pipeline](#1-automated-data-pipeline)
  - [2. Real-World Data Storytelling](#2-real-world-data-storytelling)
  - [3. Django Web Application](#3-django-web-application)
- [Getting Started](#getting-started)
- [Screenshots](#screenshots)
- [Demo](#demo)
- [Project Structure](#project-structure)
- [Authors](#authors)
- [License](#license)

---

## Overview

This project explores the world of basketball through both data analysis and software engineering. It combines:

- A **Python data pipeline** that fetches basketball-related repositories from the GitHub REST API, with retry logic, structured logging, and CLI configuration.
- A **Jupyter-based exploratory analysis** of NBA advanced statistics (2000–2009) that answers research questions about player efficiency, position, and scoring.
- A **Django web application** that serves the cleaned data through CRUD views, paginated lists, and an interactive Chart.js analytics dashboard backed by Pandas aggregations.

The goal is to show, in one repository, how raw API data can be transformed into a deployed, user-facing product.

---

## Architecture

```
GitHub REST API  ──▶  Automated Data Pipeline (Python)  ──▶  CSV / SQLite Store
                                                                    │
                              ┌─────────────────────────────────────┤
                              ▼                                     ▼
                  Real-World Storytelling              Django Web Application
                  (Jupyter / Pandas EDA)               + Chart.js Dashboard
                                                       + Bootstrap 5 UI
```

---

## Tech Stack

- **Backend:** Python 3, Django 5, Gunicorn, WhiteNoise
- **Data:** Pandas, NumPy, Matplotlib, Seaborn, Jupyter
- **Frontend:** Bootstrap 5, Chart.js, HTML/CSS
- **Storage:** SQLite, CSV
- **APIs:** GitHub REST API
- **Deployment:** Heroku-ready (Procfile, runtime.txt, environment-driven config via `python-decouple`)

---

## Sub-Projects

### 1. Automated Data Pipeline
Path: [`automated-data-pipeline/`](./automated-data-pipeline)

A Python pipeline that pages through the GitHub REST API to collect basketball-related repositories.

**Highlights**
- Modular design: `api_client.py`, `storage.py`, `pipeline.py`
- Configurable runs with CLI arguments
- Robust error handling with retries and structured logging
- Outputs to CSV / SQLite for downstream consumption

### 2. Real-World Data Storytelling
Path: [`real-world-storytelling/`](./real-world-storytelling)

An exploratory data analysis of NBA advanced statistics from 2000–2009 ([Kaggle source](https://www.kaggle.com/datasets/bilgehanyaylali/nba-advanced-stats-2000-2009/data)).

**Research Questions**
1. Who was the most efficient scorer of the era?
2. Which positions are the most efficient?
3. What does the distribution of efficiency look like across the league?
4. Is there a relationship between scoring volume and efficiency?

**Deliverables**
- Cleaned and aggregated dataset (1,890 rows, 4+ numeric and 2 categorical columns)
- `analysis.ipynb` notebook with full EDA, visualizations, and narrative
- Reusable helpers in `src/functions.py` and `src/nba_analysis.py`

### 3. Django Web Application
Path: [`django-web-application/`](./django-web-application)

A deployable Django app that turns the pipeline output into an interactive user experience.

**Features**
- Homepage with dataset overview and navigation
- Paginated list view of basketball repositories with full CRUD
- Detail view per repository
- **Analytics dashboard** with Pandas-driven aggregations and Chart.js visualizations (stars, language distribution, summary statistics)
- Bootstrap 5 styling and responsive layout
- Deployment-ready configuration: `Procfile`, `runtime.txt`, `whitenoise`, `gunicorn`, `python-decouple`, `dj-database-url`
- Passes `manage.py check --deploy` security checks

---

## Getting Started

### Prerequisites
- Python 3.10+
- `pip` and `virtualenv`

### Clone
```bash
git clone https://github.com/lukehsalem/Full-Stack-Data-Web-Application.git
cd Full-Stack-Data-Web-Application/project-root
```

### Run the Data Pipeline
```bash
cd automated-data-pipeline
pip install -r requirements.txt
python src/pipeline.py
```

### Open the Analysis Notebook
```bash
cd real-world-storytelling
pip install -r requirements.txt
jupyter notebook analysis.ipynb
```

### Run the Web Application
```bash
cd django-web-application
pip install -r requirements.txt
python myapp/manage.py migrate
python myapp/manage.py fetch_data
python myapp/manage.py seed_data
python myapp/manage.py runserver
```
Then open `http://127.0.0.1:8000/` in your browser.

---

## Screenshots

| Homepage | List View |
| :---: | :---: |
| ![Homepage](django-web-application/screenshots/homepage.png) | ![List View](django-web-application/screenshots/listview.png) |

| Analytics Dashboard | Deploy Security Check |
| :---: | :---: |
| ![Analytics Dashboard](django-web-application/screenshots/analyticsdashboard.png) | ![Security Check](django-web-application/screenshots/securitycheck.png) |

---

## Demo

Project walkthrough: [YouTube Demo](https://youtu.be/9kQBsbywEdc)

---

## Project Structure

```
project-root/
├── automated-data-pipeline/      # GitHub API ingestion pipeline
│   ├── src/
│   │   ├── api_client.py
│   │   ├── pipeline.py
│   │   └── storage.py
│   ├── data/
│   └── log/
├── real-world-storytelling/      # NBA stats EDA
│   ├── analysis.ipynb
│   ├── src/
│   │   ├── functions.py
│   │   └── nba_analysis.py
│   └── data/
└── django-web-application/       # Full-stack web app
    ├── myapp/
    │   ├── core/                 # views, models, templates, static
    │   ├── mysite/               # Django project settings
    │   └── manage.py
    ├── config/
    ├── screenshots/
    ├── Procfile
    ├── runtime.txt
    └── requirements.txt
```

---

## Authors

Built collaboratively for **CIS4930 (Introduction to Python)** at Florida State University.

| Name | GitHub | Primary Contributions |
| --- | --- | --- |
| **Luke Salem** | [@lukehsalem](https://github.com/lukehsalem) | Analytics dashboard, Pandas aggregations, Chart.js integration, Models ORM, advanced error handling, retries, and CLI arguments for the data pipeline |
| **Matthew Chen** | [@mchenrep](https://github.com/mchenrep) | Framework setup, repository structure, URL routing, ORM models, `fetch_data.py`, `seed_data.py`, data loading and transformation |
| **Eric Pengili** | [@sicc-ranchezz](https://github.com/sicc-ranchezz) | Security and deployment readiness, settings, `api_client.py`, `storage.py`, alternative analysis notebook, file structure |
| **Tony Guillen** | [@tonyguil1](https://github.com/tonyguil1) | HTML templates, Bootstrap 5 UI, CSS, charts, data visualization, API response transformation |

---

## License

This project was created for academic purposes. Feel free to explore, fork, and learn from it.