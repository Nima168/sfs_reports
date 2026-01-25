# SFS Reports Dashboard 📊

A Streamlit dashboard for analyzing and visualizing SFS Execution Reports.
It provides detailed execution analysis, duplicate tracking, and interactive visualizations to help monitor SFS operations efficiently.

## Features ✨

Clean and interactive data tables for execution reports.

Duplicate transaction analysis with summary statistics.

Altair charts for quick visual insights.

Custom dark/light theme support and modern dashboard styling.

Responsive layout using Streamlit columns and sections.

## Installation ⚡

- Clone the repository:

git clone https://github.com/yourusername/sfs_report.git
cd sfs_report


- Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows


- Install dependencies:

pip install -r requirements.txt

## Usage 🚀

- Run the Streamlit app:

streamlit run app.py


- Open the browser at http://localhost:8501 to view the dashboard.

## File Structure 🗂️
sfs_report/
│
├─ app.py                  # Main Streamlit dashboard
├─ data/                   # Execution report CSV files
├─ utils.py                # Helper functions
├─ requirements.txt
└─ README.md

## Dependencies 📦

- Python 3.10+

- Streamlit

- Pandas

- NumPy

- Altair

### License ⚖️

This project is licensed under the MIT License.

[SFS Reports Dashboard](https://sfsreports-dashboard.streamlit.app/)
