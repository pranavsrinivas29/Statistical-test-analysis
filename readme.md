# 📊 COVID-19 Statistical Test Dashboard

An interactive Dash-based web application for performing statistical hypothesis tests on COVID-19 data grouped by WHO region. Users can explore **Chi-Square Tests**, **T-Tests**, and **Z-Tests** on metrics like case fatality and recovery rates.

---

## 📁 Project Structure

├── app.py # Dash web application
├── statistical_test.py # Core statistical test logic
├── country_wise_latest.csv # Dataset used in the app
├── README.md # Project documentation


---

## 🚀 Features

- ✅ One-sample and two-sample **T-Tests**
- ✅ **Chi-Square Test** for categorical associations
- ✅ **Z-Test for Proportions**
- ✅ Interactive UI with dropdown-based inputs
- ✅ Auto-hiding of irrelevant input fields based on selected test
- ✅ Clean, browser-based statistical outputs with interpretation

---

## 📦 Requirements

Install dependencies:

```bash
pip install dash pandas scipy statsmodels
```
Tested with:
    - Python 3.11+
    - Dash 2.0+
    - pandas
    - scipy
    - statsmodels

---

## 📊 Dataset
Ensure country_wise_latest.csv is placed in the project directory. Required columns include:
WHO Region: Categorical region label (e.g., "Europe", "Africa")
Recovered / 100 Cases: Numeric column for recovery analysis
Deaths / 100 Cases: Numeric column for fatality rate analysis


---
## 🧪 Supported Statistical Tests

| Test Type              | Description                                                                   |
| ---------------------- | ----------------------------------------------------------------------------- |
| Chi-Square Test        | Tests association between a binary variable (e.g., recovery > 70%) and region |
| Two-Sample T-Test      | Compares mean values of a numeric column between two WHO regions              |
| One-Sample T-Test      | Compares a region’s mean with global average (supports one-/two-tailed)       |
| Z-Test for Proportions | Compares proportions of regions exceeding a metric threshold                  |

---

## 🧠 Example Use Case
Goal: Check if recovery rate >70% significantly differs across WHO regions.
Steps:
    Select Chi-Square Test
    Choose:
    Group column: WHO Region
    Numeric column: Recovered / 100 Cases

    Condition: >
    Threshold: 70

    Click Run Test

    View:

    Test statistic
    p-value
    Null hypothesis decision

---

## 🎨 UI Design
Inputs shown/hidden dynamically based on selected test type
Dropdowns prevent invalid or unsupported input combinations
Clean, formatted result display:

Test statistic
P-value
Decision on null hypothesis

---

## 📚 Code Overview
- statistical_test.py
- Encapsulates core logic with the following methods:
- two_sample_ttest(df, group1, group2)
- one_sample_ttest(df, col, region, flag)
- z_test_proportions(df, region1, region2, threshold, col, sign)
- chi_square_test_binary(df, group_col, metric_col, condition, threshold)

---

## app.py
Implements the frontend logic:
Dash UI with dropdowns, inputs, and callbacks
Dynamic input handling based on selected test
Result panel with computed output and interpretation

---

## ✅ Future Enhancements
📤 Export test results as CSV or PDF
📈 Add bar charts or p-value plots
📁 Enable user-uploaded datasets
🧪 Support more statistical tests (ANOVA, correlation, etc.)

---
