# Software Quality Engineering (SQE) Labs

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Pytest](https://img.shields.io/badge/Pytest-9.1.1-0A9EDC?style=for-the-badge&logo=pytest)
![JIRA](https://img.shields.io/badge/JIRA-Software-0052CC?style=for-the-badge&logo=jira)
![Coverage](https://img.shields.io/badge/Coverage-90%25-success?style=for-the-badge)
![GitHub](https://img.shields.io/badge/GitHub-faizanali022-181717?style=for-the-badge&logo=github)

**Student Name:** Faizan Ali  
**Course:** Software Quality Engineering  
**Institution:** Mirpur University of Sciences and Technology  

---

## 📖 Overview
This repository contains the practical implementations and deliverables for the Software Quality Engineering (SQE) course. It covers a wide range of software testing methodologies, from theoretical quality attribute assessments (ISO/IEC 25010) and test management documentation (STLC) to automated Python testing, code coverage analysis, and combinatorial testing.

---

## 📂 Repository Structure

```text
sqe-labs-faizanali022/
│
├── week2/                     # ISO 25010 Quality Attribute Assessment
│   ├── quality_analysis.py    # Python script for radar chart & weighted scores
│   └── quality_radar_*.png    # Generated quality profile chart
│
├── week3/                     # STLC & Test Documentation Setup
│   ├── (RTM).xlsx             # Requirement Traceability Matrix
│   └── (TestPlan).pdf         # IEEE 829 Test Plan
│
└── week7/                     # Code Coverage & Pairwise Testing
    ├── auth.py                # Authentication module under test
    ├── tests/                 # Pytest test suites (TC-001 to TC-027)
    ├── pairwise_check.py      # AllPairs combinatorial testing script
    └── htmlcov/               # HTML Coverage report