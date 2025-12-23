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

