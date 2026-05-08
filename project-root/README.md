    1 # Full-Stack Data Web Application                                         
    2
    3 An end-to-end data project that ingests data from a public API, perform
      s exploratory analysis on a real-world dataset, and surfaces both throu
      gh a deployed Django web application with an interactive analytics dash
      board.
    4
    5 The repository is organized as three connected sub-projects that togeth
      er demonstrate the full lifecycle of a data product — **ingest → analyz
      e → serve**.
    6
    7 ---
    8
    9 ## Table of Contents
   10 - [Overview](#overview)
   11 - [Architecture](#architecture)
   12 - [Tech Stack](#tech-stack)
   13 - [Sub-Projects](#sub-projects)
   14   - [1. Automated Data Pipeline](#1-automated-data-pipeline)
   15   - [2. Real-World Data Storytelling](#2-real-world-data-storytelling)
   16   - [3. Django Web Application](#3-django-web-application)
   17 - [Getting Started](#getting-started)
   18 - [Screenshots](#screenshots)
   19 - [Demo](#demo)
   20 - [Project Structure](#project-structure)
   21 - [Authors](#authors)
   22 - [License](#license)
   23
   24 ---
   25
   26 ## Overview
   27
   28 This project explores the world of basketball through both data analysi
      s and software engineering. It combines:
   29
   30 - A **Python data pipeline** that fetches basketball-related repositori
      es from the GitHub REST API, with retry logic, structured logging, and
      CLI configuration.
   31 - A **Jupyter-based exploratory analysis** of NBA advanced statistics (
      2000–2009) that answers research questions about player efficiency, pos
      ition, and scoring.
   32 - A **Django web application** that serves the cleaned data through CRU
      D views, paginated lists, and an interactive Chart.js analytics dashboa
      rd backed by Pandas aggregations.
   33
   34 The goal is to show, in one repository, how raw API data can be transfo
      rmed into a deployed, user-facing product.
   35
   36 ---
   37
   38 ## Architecture
   39
   40 ```
   41 ┌────────────────────┐      ┌────────────────────────┐      ┌──────────
      ───────────┐
   42 │   GitHub REST API  │ ───▶ │  Automated Data        │ ───▶ │  CSV / SQ
      Lite Store │
   43 │   (basketball repos)│      │  Pipeline (Python)    │      │
                 │
   44 └────────────────────┘      └────────────────────────┘      └──────────
      ┬──────────┘
   45  
      │
   46                             ┌──────────────────────────┐
      │
   47                             │  Real-World Storytelling │
      │
   48                             │  (Jupyter / Pandas EDA)  │
      │
   49                             └──────────────────────────┘
      │
   50  
      ▼
   51                                                          ┌─────────────
      ────────────┐
   52                                                          │  Django Web
      Application │
   53                                                          │  + Chart.js
      Dashboard   │
   54                                                          │  + Bootstrap
       5 UI       │
   55                                                          └─────────────
      ────────────┘
   56 ```
   57
   58 ---
   59
   60 ## Tech Stack
   61
   62 **Backend:** Python 3, Django 5, Gunicorn, WhiteNoise
   63 **Data:** Pandas, NumPy, Matplotlib, Seaborn, Jupyter
   64 **Frontend:** Bootstrap 5, Chart.js, HTML/CSS
   65 **Storage:** SQLite, CSV
   66 **APIs:** GitHub REST API
   67 **Deployment:** Heroku-ready (Procfile, runtime.txt, environment-driven
       config via `python-decouple`)
   68
   69 ---
   70
   71 ## Sub-Projects
   72
   73 ### 1. Automated Data Pipeline
   74 Path: [`automated-data-pipeline/`](./automated-data-pipeline)
   75
   76 A Python pipeline that pages through the GitHub REST API to collect bas
      ketball-related repositories.
   77
   78 **Highlights**
   79 - Modular design: `api_client.py`, `storage.py`, `pipeline.py`
   80 - Configurable runs with CLI arguments
   81 - Robust error handling with retries and structured logging
   82 - Outputs to CSV / SQLite for downstream consumption
   83
   84 ### 2. Real-World Data Storytelling
   85 Path: [`real-world-storytelling/`](./real-world-storytelling)
   86
   87 An exploratory data analysis of NBA advanced statistics from 2000–2009
      ([Kaggle source](https://www.kaggle.com/datasets/bilgehanyaylali/nba-ad
      vanced-stats-2000-2009/data)).
   88
   89 **Research Questions**
   90 1. Who was the most efficient scorer of the era?
   91 2. Which positions are the most efficient?
   92 3. What does the distribution of efficiency look like across the league
      ?
   93 4. Is there a relationship between scoring volume and efficiency?
   94
   95 **Deliverables**
   96 - Cleaned and aggregated dataset (1,890 rows, 4+ numeric and 2 categori
      cal columns)
   97 - `analysis.ipynb` notebook with full EDA, visualizations, and narrativ
      e
   98 - Reusable helpers in `src/functions.py` and `src/nba_analysis.py`
   99
  100 ### 3. Django Web Application
  101 Path: [`django-web-application/`](./django-web-application)
  102
  103 A deployable Django app that turns the pipeline output into an interact
      ive user experience.
  104
  105 **Features**
  106 - Homepage with dataset overview and navigation
  107 - Paginated list view of basketball repositories with full CRUD
  108 - Detail view per repository
  109 - **Analytics dashboard** with Pandas-driven aggregations and Chart.js
      visualizations (stars, language distribution, summary statistics)
  110 - Bootstrap 5 styling and responsive layout
  111 - Deployment-ready configuration: `Procfile`, `runtime.txt`, `whitenois
      e`, `gunicorn`, `python-decouple`, `dj-database-url`
  112 - Passes `manage.py check --deploy` security checks
  113
  114 ---
  115
  116 ## Getting Started
  117
  118 ### Prerequisites
  119 - Python 3.10+
  120 - `pip` and `virtualenv`
  121
  122 ### Clone
  123 ```bash
  124 git clone https://github.com/<your-username>/<repo-name>.git
  125 cd <repo-name>/project-root
  126 ```
  127
  128 ### Run the Data Pipeline
  129 ```bash
  130 cd automated-data-pipeline
  131 pip install -r requirements.txt   # if present
  132 python src/pipeline.py
  133 ```
  134
  135 ### Open the Analysis Notebook
  136 ```bash
  137 cd real-world-storytelling
  138 pip install -r requirements.txt
  139 jupyter notebook analysis.ipynb
  140 ```
  141
  142 ### Run the Web Application
  143 ```bash
  144 cd django-web-application
  145 pip install -r requirements.txt
  146 python myapp/manage.py migrate
  147 python myapp/manage.py fetch_data
  148 python myapp/manage.py seed_data
  149 python myapp/manage.py runserver
  150 ```
  151 Then open `http://127.0.0.1:8000/` in your browser.
  152
  153 ---
  154
  155 ## Screenshots
  156
  157 | Homepage | List View |
  158 | :---: | :---: |
  159 | ![Homepage](django-web-application/screenshots/homepage.png) | ![List
       View](django-web-application/screenshots/listview.png) |
  160
  161 | Analytics Dashboard | Deploy Security Check |
  162 | :---: | :---: |
  163 | ![Analytics Dashboard](django-web-application/screenshots/analyticsda
      shboard.png) | ![Security Check](django-web-application/screenshots/sec
      uritycheck.png) |
  164
  165 ---
  166
  167 ## Demo
  168
  169 Project walkthrough: [YouTube Demo](https://youtu.be/9kQBsbywEdc)
  170
  171 ---
  172
  173 ## Project Structure
  174
  175 ```
  176 project-root/
  177 ├── automated-data-pipeline/      # GitHub API ingestion pipeline
  178 │   ├── src/
  179 │   │   ├── api_client.py
  180 │   │   ├── pipeline.py
  181 │   │   └── storage.py
  182 │   ├── data/
  183 │   └── log/
  184 ├── real-world-storytelling/      # NBA stats EDA
  185 │   ├── analysis.ipynb
  186 │   ├── src/
  187 │   │   ├── functions.py
  188 │   │   └── nba_analysis.py
  189 │   └── data/
  190 └── django-web-application/       # Full-stack web app
  191     ├── myapp/
  192     │   ├── core/                 # views, models, templates, static
  193     │   ├── mysite/               # Django project settings
  194     │   └── manage.py
  195     ├── config/
  196     ├── screenshots/
  197     ├── Procfile
  198     ├── runtime.txt
  199     └── requirements.txt
  200 ```
  201
  202 ---
  203
  204 ## Authors
  205
  206 Built collaboratively for **CIS4930 (Introduction to Python)** at the U
      niversity of Florida.
  207
  208 | Name | GitHub | Primary Contributions |
  209 | --- | --- | --- |
  210 | **Luke Salem** | [@lukehsalem](https://github.com/lukehsalem) | Analy
      tics dashboard, Pandas aggregations, Chart.js integration, Models ORM,
      advanced error handling, retries, and CLI arguments for the data pipeli

⏺ Write(README.md)
  ⎿  User rejected write to README.md
       1 # Full-Stack Data Web Application
       2
       3 An end-to-end data project that ingests data from a public API,
         performs exploratory analysis on a real-world dataset, and surfa
         ces both through a deployed Django web application with an inter
         active analytics dashboard.
       4
       5 The repository is organized as three connected sub-projects that
          together demonstrate the full lifecycle of a data product — **i
         ngest → analyze → serve**.
       6
       7 ---
       8
       9 ## Table of Contents
      10 - [Overview](#overview)
     … +210 lines

❯ i just want you to paste it here so i can put it in a prpoper file and push   
  it mysefl                                                                     
                                                                                
⏺ Here's a professional README for your project:                                
                                                                        
  ---                        

  # Full-Stack Data Web Application                                             
                                                                                
  An end-to-end data project that ingests data from a public API, performs      
  exploratory analysis on a real-world dataset, and surfaces both through a     
  deployed Django web application with an interactive analytics dashboard.      
                  
  The repository is organized as three connected sub-projects that together     
  demonstrate the full lifecycle of a data product — **ingest → analyze → 
  serve**.                                                                      
                  
  ---

  ## Table of Contents                                                          
  - [Overview](#overview)
  - [Architecture](#architecture)                                               
  - [Tech Stack](#tech-stack)
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

  This project explores the world of basketball through both data analysis and
  software engineering. It combines:

  - A **Python data pipeline** that fetches basketball-related repositories from
   the GitHub REST API, with retry logic, structured logging, and CLI
  configuration.
  - A **Jupyter-based exploratory analysis** of NBA advanced statistics
  (2000–2009) that answers research questions about player efficiency, position,
   and scoring.
  - A **Django web application** that serves the cleaned data through CRUD
  views, paginated lists, and an interactive Chart.js analytics dashboard backed
   by Pandas aggregations.

  The goal is to show, in one repository, how raw API data can be transformed
  into a deployed, user-facing product.

  ---

  ## Architecture

  ┌─────────────────────┐      ┌────────────────────────┐
  ┌─────────────────────┐
  │   GitHub REST API   │ ───▶ │  Automated Data        │ ───▶ │  CSV / SQLite
  Store │                                                                       
  │   (basketball repos)│      │  Pipeline (Python)     │      │
       │                                                                        
  └─────────────────────┘      └────────────────────────┘
  └──────────┬──────────┘                                                       
                                                                          │
                               ┌──────────────────────────┐               │
                               │  Real-World Storytelling │               │     
                               │  (Jupyter / Pandas EDA)  │               │
                               └──────────────────────────┘               │     
                                                                          ▼
                                                                                
  ┌─────────────────────────┐                                                   
                                                            │  Django Web
  Application │                                                                 
                                                            │  + Chart.js
  Dashboard   │
                                                            │  + Bootstrap 5 UI
        │                                                                       
  
  └─────────────────────────┘                                                   
                  
  ---

  ## Tech Stack

  **Backend:** Python 3, Django 5, Gunicorn, WhiteNoise                         
  **Data:** Pandas, NumPy, Matplotlib, Seaborn, Jupyter
  **Frontend:** Bootstrap 5, Chart.js, HTML/CSS                                 
  **Storage:** SQLite, CSV                                                      
  **APIs:** GitHub REST API                                                     
  **Deployment:** Heroku-ready (Procfile, runtime.txt, environment-driven config
   via `python-decouple`)                                                       
                                                                                
  ---                                                                           
                  
  ## Sub-Projects

  ### 1. Automated Data Pipeline                                                
  Path: [`automated-data-pipeline/`](./automated-data-pipeline)
                                                                                
  A Python pipeline that pages through the GitHub REST API to collect           
  basketball-related repositories.
                                                                                
  **Highlights**                                                                
  - Modular design: `api_client.py`, `storage.py`, `pipeline.py`
  - Configurable runs with CLI arguments                                        
  - Robust error handling with retries and structured logging                   
  - Outputs to CSV / SQLite for downstream consumption
                                                                                
  ### 2. Real-World Data Storytelling
  Path: [`real-world-storytelling/`](./real-world-storytelling)                 
                                                                                
  An exploratory data analysis of NBA advanced statistics from 2000–2009        
  ([Kaggle source](https://www.kaggle.com/datasets/bilgehanyaylali/nba-advanced-
  stats-2000-2009/data)).                                                       
                  
  **Research Questions**
  1. Who was the most efficient scorer of the era?
  2. Which positions are the most efficient?
  3. What does the distribution of efficiency look like across the league?      
  4. Is there a relationship between scoring volume and efficiency?
                                                                                
  **Deliverables**
  - Cleaned and aggregated dataset (1,890 rows, 4+ numeric and 2 categorical
  columns)                                                                      
  - `analysis.ipynb` notebook with full EDA, visualizations, and narrative
  - Reusable helpers in `src/functions.py` and `src/nba_analysis.py`            
                                                                                
  ### 3. Django Web Application
  Path: [`django-web-application/`](./django-web-application)                   
                  
  A deployable Django app that turns the pipeline output into an interactive    
  user experience.
                                                                                
  **Features**    
  - Homepage with dataset overview and navigation
  - Paginated list view of basketball repositories with full CRUD
  - Detail view per repository                                                  
  - **Analytics dashboard** with Pandas-driven aggregations and Chart.js
  visualizations (stars, language distribution, summary statistics)             
  - Bootstrap 5 styling and responsive layout
  - Deployment-ready configuration: `Procfile`, `runtime.txt`, `whitenoise`,    
  `gunicorn`, `python-decouple`, `dj-database-url`                              
  - Passes `manage.py check --deploy` security checks                           
                                                                                
  ---             

  ## Getting Started

  ### Prerequisites
  - Python 3.10+
  - `pip` and `virtualenv`
                                                                                
  ### Clone
  ```bash                                                                       
  git clone https://github.com/lukehsalem/Full-Stack-Data-Web-Application.git
  cd <repo-name>/project-root

  Run the Data Pipeline                                                         
   
  cd automated-data-pipeline                                                    
  pip install -r requirements.txt   # if present
  python src/pipeline.py

  Open the Analysis Notebook

  cd real-world-storytelling
  pip install -r requirements.txt                                               
  jupyter notebook analysis.ipynb
                                                                                
  Run the Web Application

  cd django-web-application
  pip install -r requirements.txt
  python myapp/manage.py migrate                                                
  python myapp/manage.py fetch_data
  python myapp/manage.py seed_data                                              
  python myapp/manage.py runserver
  Then open http://127.0.0.1:8000/ in your browser.
                                                                                
  ---
  Screenshots                                                                   
                  
  ┌────────────────────────────────────┬────────────────────────────────────┐
  │              Homepage              │             List View              │
  ├────────────────────────────────────┼────────────────────────────────────┤
  │ django-web-application/screenshots │ django-web-application/screenshots │
  │           /homepage.png            │           /listview.png            │
  └────────────────────────────────────┴────────────────────────────────────┘   
   
  ┌──────────────────────────────────────┬──────────────────────────────────┐   
  │         Analytics Dashboard          │      Deploy Security Check       │
  ├──────────────────────────────────────┼──────────────────────────────────┤   
  │ django-web-application/screenshots/a │ django-web-application/screensho │
  │        nalyticsdashboard.png         │       ts/securitycheck.png       │   
  └──────────────────────────────────────┴──────────────────────────────────┘   
   
  ---                                                                           
  Demo            

  Project walkthrough: YouTube Demo (https://youtu.be/9kQBsbywEdc)

  ---
  Project Structure

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
                  
  ---
  Authors
         
  Built collaboratively for CIS4930 (Introduction to Python) at the University
  of Florida.                                                                   
   
  Name: Luke Salem                                                              
  GitHub: @lukehsalem (https://github.com/lukehsalem)
  Primary Contributions: Analytics dashboard, Pandas aggregations, Chart.js
    integration, Models ORM, advanced error handling, retries, and CLI arguments

    for the data pipeline                                                       
  ────────────────────────────────────────
  Name: Matthew Chen                                                            
  GitHub: @mchenrep (https://github.com/mchenrep)
  Primary Contributions: Framework setup, repository structure, URL routing, ORM
                  
    models, fetch_data.py, seed_data.py, data loading and transformation
  ────────────────────────────────────────
    api_client.py, storage.py, alternative analysis notebook, file structure
  ────────────────────────────────────────
  Name: Tony Guillen
  GitHub: @tonyguil1 (https://github.com/tonyguil1)
  Primary Contributions: HTML templates, Bootstrap 5 UI, CSS, charts, data
    visualization, API response transformation

  ---
  License

  This project was created for academic purposes. Feel free to explore, fork,
  and learn from it.

  ---

  Copy the block above into a `README.md` at the root of your repo. A few quick
  notes:

  - The screenshot paths assume you keep them under
  `django-web-application/screenshots/`. If you put the README inside
  `project-root/`, the paths work as-is. If you push it to the very top of your
  repo, prepend `project-root/` to the image paths.
  templates, static
      │   ├── mysite/               # Django project
  settings
      │   └── manage.py
      ├── config/
      ├── screenshots/
      ├── Procfile
      ├── runtime.txt
      └── requirements.txt

  ---
  Authors

  Built collaboratively for CIS4930 (Introduction to
  Python) at the University of Florida.

  Name: Luke Salem
  GitHub: @lukehsalem (https://github.com/lukehsalem)
  Primary Contributions: Analytics dashboard, Pandas
    aggregations, Chart.js integration, Models ORM,
    advanced error handling, retries, and CLI arguments

    for the data pipeline
  ────────────────────────────────────────
  Name: Matthew Chen
  GitHub: @mchenrep (https://github.com/mchenrep)
  Primary Contributions: Framework setup, repository
    structure, URL routing, ORM models, fetch_data.py,
    seed_data.py, data loading and transformation
  ────────────────────────────────────────
  Name: Eric Pengili
  GitHub: @sicc-ranchezz
    (https://github.com/sicc-ranchezz)
  Primary Contributions: Security and deployment
    readiness, settings, api_client.py, storage.py,
    alternative analysis notebook, file structure
  ────────────────────────────────────────
  Name: Tony Guillen
  GitHub: @tonyguil1 (https://github.com/tonyguil1)
  Primary Contributions: HTML templates, Bootstrap 5
  UI,
    CSS, charts, data visualization, API response
    transformation

  ---
  License

  This project was created for academic purposes. Feel
  free to explore, fork, and learn from it.

  ---

  Copy the block above into a `README.md` at the root
  of your repo. A few quick notes:

  - The screenshot paths assume you keep them under
  `django-web-application/screenshots/`. If you put the
   README inside `project-root/`, the paths work as-is.
      ├── runtime.txt
      └── requirements.txt

  ---
  Authors

  Built collaboratively for CIS4930 (Introduction to Python) at the University of Florida.

  ┌───────────┬────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
  │   Name    │                   GitHub                   │                                    Primary Contributions                                     │
  ├───────────┼────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Luke      │ @lukehsalem                                │ Analytics dashboard, Pandas aggregations, Chart.js integration, Models ORM, advanced error   │
  │ Salem     │ (https://github.com/lukehsalem)            │ handling, retries, and CLI arguments for the data pipeline                                   │
  ├───────────┼────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Matthew   │ @mchenrep (https://github.com/mchenrep)    │ Framework setup, repository structure, URL routing, ORM models, fetch_data.py, seed_data.py, │
  │ Chen      │                                            │  data loading and transformation                                                             │
  ├───────────┼────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Eric      │ @sicc-ranchezz                             │ Security and deployment readiness, settings, api_client.py, storage.py, alternative analysis │
  │ Pengili   │ (https://github.com/sicc-ranchezz)         │  notebook, file structure                                                                    │
  ├───────────┼────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Tony      │ @tonyguil1 (https://github.com/tonyguil1)  │ HTML templates, Bootstrap 5 UI, CSS, charts, data visualization, API response transformation │
  │ Guillen   │                                            │                                                                                              │
  └───────────┴────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘

  ---
  License

  This project was created for academic purposes. Feel free to explore, fork, and learn from it.

  ---