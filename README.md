# SFS Reports Dashboard

An interactive Streamlit dashboard built to analyze and visualize SFS Execution Reports.
The project focuses on cleaning raw execution data, identifying details on passed and failed test cases, and presenting actionable insights through interactive visualizations.

## Project Overview

The SFS Reports Dashboard is designed to:
- Perform data cleaning and preprocessing on raw execution CSV files
- Perform EDA on passed and failed test cases
- Summarize execution results
-  Provide interactive visual analytics using Streamlit

#### The project follows a clean separation of concerns:

1. Data storage

2. EDA and experimentation

3. Reusable utility functions

4. Production-ready Streamlit dashboard

## Project Structure

```bash
SFS_REPORTS/
│
├── agents/                    # Reserved for future automation / agent logic
│
├── dashboards/
│   └── app.py                 # Main Streamlit application
│
├── data/
│   └── Execution_Report.csv   # Raw execution report
│
├── notebooks/
│   └── sfs_report.ipynb       # EDA and experimentation notebook
│
├── sfs_lib/
│   ├── __init__.py
│   └── utils.py               # Common reusable utility functions
│
├── venv/                      # Virtual environment (not committed)
│
├── README.md                  # Project documentation
└── requirements.txt           # Project dependencies
```


## Workflow & Architecture

**1. Data Storage**

- All raw execution reports are stored in the ***data/*** directory.

- Data is read directly from CSV files using pandas.

**2. Exploratory Data Analysis (EDA)**

- Performed in ***notebooks/sfs_report.ipynb***

- Key activities:

1. Understanding execution status distribution

2. Identifying failed test cases

3. Analyzing execution durations

4. Detecting duplicate and repeated failures

The notebook is used for analysis, experimentation, and validation before integrating logic into the dashboard.

**3. Utility Functions (*sfs_lib/utils.py*)**

- Common, reusable functions are implemented here and shared across: Jupyter Notebook and Streamlit Dashboard

- Key functionalities include:

1.  Cleaning and standardizing CSV data

2.  Extracting failed test cases

3.  Identifying details related to passed and failed test cases

4.  Merging cleaned execution reports

5.  Generating summarized views for visualization


**4. Streamlit Dashboard (*dashboards/app.py*)**

- The Streamlit app is the entry point of the project.

- Uses cleaned and processed data from utility functions.

- Provides:

1. Interactive tables

2. Charts and visual summaries

3. Execution insights for quick decision-making

The dashboard is designed to be user-friendly, interactive, and scalable.

## Data Visualization & Analysis

The following libraries are used for analysis and visualization:

***Library	Purpose***
1. [pandas](https://pandas.pydata.org/docs/): 	    Data loading, cleaning, transformation
2. [matplotlib](https://matplotlib.org/): 	        Static visualizations
3. [seaborn](https://seaborn.pydata.org/):    	    Statistical and distribution plots built on matplotlib
4. [plotly](https://plotly.com/python/):     	      Highly interactive charts, and dashboard-friendly
5. [altair](https://altair-viz.github.io/):         Declarative, grammar-of-graphics style (Vega-Lite)
6. [streamlit](https://docs.streamlit.io/):  	      Web-based interactive dashboard

***Following libraries can also be explored for interactive visualisations***

[bokeh](https://docs.bokeh.org/en/latest/):         Interactive, browser-based visualizations


## How to Run the Project
- Clone the Repository
```bash
git clone <repository-url> 

cd SFS_REPORTS
```

- Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

- Install Dependencies
```bash
pip install -r requirements.txt
```

- Run the Streamlit App
```bash
streamlit run dashboards/app.py
```


## Conclusion

The SFS Reports Dashboard provides a structured and scalable approach to analyzing execution reports, enabling faster insights and better decision-making through interactive visualizations.
