# A Data-Driven Decision Support System for Public Expenditure Analysis and Budget Optimization in the DR Congo

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Description

This project provides an interactive decision support tool for the financing
of public institutions in the Democratic Republic of Congo (DRC).
It relies on the extraction, integration and analysis of heterogeneous data
from multiple sources, and exposes results through a Streamlit interface.*

> **Repository (code & data):**
> https://github.com/BoazNzazi/Systeme_Aide_Decision_Gestion_Depenses_Publiques

---

## Table of Contents / Table des matières

1. [Project Structure](#project-structure)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Data](#data)
5. [Running the Application](#running-the-application)
6. [Application Modules](#application-modules)
7. [Reproducibility](#reproducibility)
8. [Dependencies](#dependencies)
9. [Authors](#authors)
10. [Citation](#citation)

---

## Project Structure

```
Systeme_Aide_Decision_Gestion_Depenses_Publiques/
│
├── Main.py                              # Entry point — Streamlit application
├── FINAL_WITH_ALL_INDICATEURS.xlsx      # Consolidated dataset (all indicators)
├── requirements                         # Pinned Python dependencies
├── .gitignore
│
├── sections/                            # Application modules (one per tab)
│   ├── accueil.py                       # Home / Welcome page
│   ├── data.py                          # Data exploration & preview
│   ├── visualisation.py                 # Charts and dashboards
│   ├── analyse.py                       # Statistical analysis
│   ├── nlp.py                           # Natural Language Processing module
│   └── apropos.py                       # About / project information
│
├── env/                                 # (Virtual environment — not tracked)
└── monenviron/                          # (Virtual environment — not tracked)
```

---

## Prerequisites

| Tool        | Recommended version | Notes                          |
|-------------|---------------------|--------------------------------|
| Python      | 3.9 or higher       | 3.10 / 3.11 also tested        |
| pip         | 23+                 | `python -m pip install --upgrade pip` |
| Git         | any recent version  | to clone the repository        |

---

## Installation

### Step 1 — Clone the repository

```bash
git clone https://github.com/BoazNzazi/Systeme_Aide_Decision_Gestion_Depenses_Publiques.git
cd Systeme_Aide_Decision_Gestion_Depenses_Publiques
```

### Step 2 — Create and activate a virtual environment (recommended)

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

### Step 3 — Install dependencies

```bash
pip install -r requirements
```

---

## Data

The dataset used by the application is:

| File                                  | Format | Description                                        |
|---------------------------------------|--------|----------------------------------------------------|
| `FINAL_WITH_ALL_INDICATEURS.xlsx`     | Excel  | Consolidated dataset containing all indicators     |
|                                       |        | related to public expenditure in the DRC           |

The file is loaded automatically by `Main.py` at startup:

```python
df = pd.read_excel('FINAL_WITH_ALL_INDICATEURS.xlsx')
```

Make sure the file is present in the **root directory** of the project before
launching the application.

---

## Running the Application

From the root of the project (with the virtual environment activated):

```bash
streamlit run Main.py
```

The application will open automatically in your default web browser at:

```
http://localhost:8501
```

---

## Application Modules

The application is structured around six navigation sections accessible
from the sidebar:

| Section         | File                    | Description                                                   |
|-----------------|-------------------------|---------------------------------------------------------------|
| **Accueil**     | `sections/accueil.py`   | Welcome page, project overview                               |
| **Data**        | `sections/data.py`      | Raw data exploration, filtering, and preview                 |
| **Visualisation** | `sections/visualisation.py` | Interactive charts, dashboards, and spatial maps        |
| **Analyse**     | `sections/analyse.py`   | Statistical analysis, correlations, and indicators           |
| **NLP**         | `sections/nlp.py`       | Natural language processing applied to public finance data   |
| **À Propos**    | `sections/apropos.py`   | Project information, methodology, and team                   |

---

## Reproducibility

This repository is made available to ensure the **full reproducibility** of
the results presented in the associated research paper.

To reproduce all results:

1. Clone the repository (see [Installation](#installation)).
2. Install the exact dependency versions listed in `requirements`
   (all versions are pinned).
3. Launch the application with `streamlit run Main.py`.
4. Navigate through each section to reproduce figures, tables,
   and analyses described in the paper.

### Exact environment snapshot

All dependencies are pinned in the `requirements` file. Key libraries:

```
streamlit==1.38.0
pandas==2.2.2
numpy==2.1.1
matplotlib==3.9.2
seaborn==0.13.2
openpyxl==3.1.5
altair==5.4.1
pyarrow==17.0.0
```

A complete list is provided in the `requirements` file at the root of the
repository.

### Python version used

```
Python 3.9+  (tested on 3.9, 3.10, 3.11)
```

---

## Dependencies

All dependencies with their exact versions are listed in the `requirements` file.
Install them with:

```bash
pip install -r requirements
```

Main libraries used:

- **Streamlit** — interactive web application framework
- **Pandas** — data manipulation and analysis
- **NumPy** — numerical computing
- **Matplotlib / Seaborn** — static visualizations
- **Altair** — declarative interactive visualizations
- **OpenPyXL / XlsxWriter** — Excel file reading and writing
- **PyArrow** — columnar data processing

---

## Authors

**Boaz Nzazi** - Msc In computer Engineering
GitHub: [@BoazNzazi](https://github.com/BoazNzazi)
**Selain Kasereka** - PhD in Mathematical Sciences and Computer Science
GitHub: [@sedjokas](https://github.com/sedjokas)
**Vinh Ho Tuong** - PhD In computer Engineering
Site: https://sites.google.com/view/hotuongvinh/home

---

## Citation

If you use this code or dataset in your research, please cite:

```bibtex
@misc{nzazi2025adatadr,
  author       = {Nzazi, Boaz and Kasereka, Selain and HO Tuong, Vinh},
  title        = {A Data-Driven Decision Support System for Public Expenditure Analysis and Budget Optimization in the DR Congo},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/BoazNzazi/
                  Systeme_Aide_Decision_Gestion_Depenses_Publiques}},
  note         = {Accessed: 28 March 2026}
}
```

---

## License

This project is distributed for research and reproducibility purposes.
Please contact the author for any reuse beyond academic citation.

---

*Last updated: 27 March 2026*
