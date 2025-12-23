# Note-Taking App Selection Decision Support System (DSS)

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![UUM](https://img.shields.io/badge/Universiti_Utara_Malaysia-162B4E?style=for-the-badge&logoColor=white)](http://www.uum.edu.my/)
[![uv](https://img.shields.io/badge/uv-managed-purple?style=for-the-badge)](https://docs.astral.sh/uv/)

## 📖 Project Overview

This repository contains the source code for the **Final Year Project (FYP)** submitted for the **Bachelor of Science in Decision Mathematics and Data Analytics with Honours (Decision Science)** at **Universiti Utara Malaysia (UUM)**.

The project is a Web-based **Decision Support System (DSS)** designed to assist university students in selecting the most suitable note-taking application based on their personal preferences and constraints. By utilizing a Multi-Criteria Decision Making (MCDM) approach, the system analyzes various quantitative and qualitative factors to recommend the best alternative.

### 🎯 Objective
To solve the "choice overload" problem faced by students when choosing digital tools for academic study by providing a data-driven ranking system.

---

## ⚙️ The Decision Model

The DSS evaluates alternatives based on specific criteria relevant to academic note-taking.

### 1. Criteria (Attributes)
The system evaluates apps based on the following weighted criteria:
* **Ease of Use:** User interface intuition and learning curve.
* **Functionality:** Feature richness (handwriting recognition, recording, templates, etc.).
* **Cross-Device Sync:** Reliability of syncing across iPad, iPhone, Mac, or Windows.
* **Cost:** Pricing model (One-time purchase vs. Subscription).
* **Storage & Security:** Backup options and data protection.

### 2. Alternatives
The following applications are evaluated within the system:
1.  GoodNotes
2.  Notability
3.  Microsoft OneNote
4.  Flexcil
5.  Kilonote

---

## 🛠️ Technology Stack

This project is built using Python and the Streamlit framework, managed by **uv**.

* **Package Manager:** [uv](https://github.com/astral-sh/uv)
* **Frontend & Framework:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Visualization:** [Plotly](https://plotly.com/), [Matplotlib](https://matplotlib.org/)
* **Language:** Python 3.x

---

## 🚀 Installation & Usage

This project uses `uv` for fast package management and environment isolation.

### Prerequisites
* **Git** installed.
* **uv** installed. (If not, install it via `curl -LsSf https://astral.sh/uv/install.sh | sh` or `pip install uv`).

### Step 1: Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

### Step 2: Sync Dependencies
Initialize the environment and install dependencies defined in `pyproject.toml` using `uv`.

```bash
uv sync
```

### Step 3: Run the Application
Use `uv run` to launch the Streamlit app within the managed environment.

```Bash
uv run streamlit run app.py
```
The application will launch in your default web browser at http://localhost:8501.

## 📊 Features
1. Interactive Criteria Weighting: Users can input or adjust the importance of each criterion (e.g., prioritizing "Cost" over "Functionality").
2. Dynamic Ranking: The system calculates scores in real-time using Python (Pandas/NumPy) and updates the rank of alternatives.
3. Visual Analytics:
* Bar Charts (Matplotlib): Comparison of scores per app.
* Radar Charts (Plotly): To visualize the strengths and weaknesses of the top-ranked app.
4. Detailed Comparison Table: A comprehensive view of the data matrix used for decision-making.

## 📂 Project Structure
```Bash
├── main.py                                                                 # Main Streamlit Logic file
├── dashboard.py                                                            # Dashboard algorithm file
├── home.py                                                                 # Home page file (criteria setting and recommendation ranking)
├── datacleanning.py                                                        # Algorithm of cleanning data from Form responses 1.csv
├── pyproject.toml                                                          # Project metadata and dependencies (managed by uv)
├── uv.lock                                                                 # Lock file for exact dependency versions
├── README.md                                                               # Project documentation
├── Note-Taking Application Selection (Responses) - Form responses 1.csv    # Responses csv from Google Form
└── average_matrix_result.csv                                               # File Generate by datacleanning.py after processing raw data from Form responses 1.csv
```
