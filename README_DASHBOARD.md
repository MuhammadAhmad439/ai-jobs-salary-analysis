# AI Jobs & Salaries Dashboard

An interactive Streamlit dashboard for exploring AI-related salary records.

## Run locally

1. Install Python.
2. Put `app.py`, `requirements.txt`, and the dataset CSV in the same folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

5. If the CSV is not in the same folder or you prefer another file, upload it using the dashboard sidebar.

## Features

- Filters for work year, experience level, work mode, company size, and company location
- KPI metrics for record count, average salary, median salary, and highest salary
- Salary distribution and salary comparisons
- Year-wise salary trend
- Filtered data table and CSV download
