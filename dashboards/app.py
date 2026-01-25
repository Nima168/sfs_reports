#######################
# Import libraries
import sys
from pathlib import Path
import pandas as pd
import numpy as np

import streamlit as st
import plotly.express as px  # for interactive charts
import altair as alt
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Fix imports ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from sfs_lib.utils import clean_execution_report, duplicate_tcs, get_duplicate_summary  # custom logic

#######################
# Page configuration
st.set_page_config(
    page_title="SFS Reports Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

st.title("📊 SFS Execution Report Dashboard")


#######################
# --- Load data ---
DATA_PATH = PROJECT_ROOT / "data" / "Execution_Report.csv"
df = pd.read_csv(DATA_PATH)
df_clean=clean_execution_report(df)

df_dup_tc = duplicate_tcs(df_clean)

# --- Duplicate summary ---
dup_dict, summary_df = get_duplicate_summary(df_clean)


df_clean_1=df_dup_tc.sort_values(['Execution Date','End Time']).groupby("Process Name", as_index=False).tail(1)
df_clean_1.head() #Test cases selected with latest data

df_without_dup=df_clean[~df_clean["Process Name"].isin(df_dup_tc["Process Name"])]
# print(f'No. of test cases executed only once= {df_without_dup.shape[0]}')
# print(f'No. of test cases executed more than once= {df_clean_1.shape[0]}')
df_final=pd.concat([df_without_dup, df_clean_1],axis=0)
# print(f'Total no. of test cases executed = {df_final.shape[0]}')
status_counts=df_final['Status'].value_counts()

df_without_dup=df_clean[~df_clean["Process Name"].isin(df_dup_tc["Process Name"])]
# print(f'No. of test cases executed only once= {df_without_dup.shape[0]}')

df_final['Elapsed Time'] = pd.to_timedelta(df_final['Elapsed Time'])
total_time = df_final['Elapsed Time'].sum()

days = total_time.days
hours = total_time.components.hours
minutes = total_time.components.minutes
seconds = total_time.components.seconds

formatted = f"{days}D {hours}H {minutes}M {seconds}S"


# Create Tabs
tab1, tab2, tab3 = st.tabs([
    "📌 Brief Summary",
    "📑 Detailed Summary",
    "🤖 Agent Call"
])

# --------------------------------------------------
# TAB 1: Brief Summary
# --------------------------------------------------
with tab1:
    st.subheader("📊 Brief Execution Summary")

    # ---------------- KPI SECTION ----------------
    total_tc = df_final.shape[0]
    passed_tc = int(status_counts.get('passed', 0))
    failed_tc = int(status_counts.get('failed', 0))
    pass_pct = round((passed_tc / total_tc) * 100, 2) if total_tc else 0

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Test Cases", total_tc)
    col2.metric("Passed", passed_tc)
    col3.metric("Failed", failed_tc)
    col4.metric("Pass %", f"{pass_pct}%")
    col5.metric("Total Time", formatted)

    st.caption(
        f"✅ **Test cases passed in first execution:** {df_without_dup.shape[0]}"
    )

    st.divider()

    # ---------------- EXECUTION HEALTH FLAGS ----------------
    if pass_pct >= 95:
        st.success("✔ Execution health is GOOD (Pass rate ≥ 95%)")
    elif pass_pct >= 85:
        st.warning("⚠ Execution health is MODERATE (85% – 95%)")
    else:
        st.error("❌ Execution health is POOR (Pass rate < 85%)")

    if df_without_dup.shape[0] > 0:
        st.info(f"🔁 {df_without_dup.shape[0]} test cases were executed more than once")

    st.divider()

    # ---------------- STATUS DISTRIBUTION ----------------
    st.write("### 📈 Test Cases Execution Report")

    # --- Filter test cases by duplicate count ---
    st.subheader("Filter Test Cases by Execution Count")
    dup_selected = st.slider(
        "Select number of executions",
        min_value=int(df_clean['Process Name'].value_counts().min()),
        max_value=int(df_clean['Process Name'].value_counts().max()),
        value=int(df_clean['Process Name'].value_counts().min())
    )

    if dup_selected in dup_dict:
        st.dataframe(dup_dict[dup_selected])
    else:
        st.info(f"No test cases executed {dup_selected} times.")

    # ---------------- OPTIONAL DETAILS ----------------
    with st.expander("🔍 View Status Breakdown Table"):
        dup_dict, summary_df = get_duplicate_summary(df_dup_tc)

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        st.caption("📌 Shows number of time test cases were executed")

    st.divider()

    # ---------------- NAVIGATION HINT ----------------
    st.markdown(
        "➡️ **Go to _Detailed Summary_ tab for failure analysis and execution timelines**  \n"
        "➡️ **Go to _Agent Call_ tab for logs and execution traces**"
    )

# --------------------------------------------------
# TAB 2: Detailed Summary
# --------------------------------------------------
with tab2:
    st.subheader("🔍 Detailed Execution Analysis")

    # ---------------- STATUS PIE CHART ----------------
    st.write("### Test Case Execution Distribution")
    # Prepare data
    status_counts = df_final['Status'].value_counts()
    status_df = status_counts.reset_index()
    status_df.columns = ["Status", "Count"]

    # Donut chart
    fig_donut = px.pie(
        status_df,
        names="Status",
        values="Count",
        color="Status",
        color_discrete_map={"Passed": "green", "Failed": "red"},
        hole=0.5,  # creates the donut hole
        title="Passed vs Failed"
    )

    fig_donut.update_traces(
        textinfo="percent+label",  # show both percent and label
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}"
    )

    fig_donut.update_layout(height=350, margin=dict(t=50, b=50))

    st.plotly_chart(fig_donut, use_container_width=True)
    st.divider()

    # ---------------- FILTERS ----------------
    st.write("### ⚙️ Filter / Explore Test Cases")

    # Status filter
    status_options = ['passed', 'failed']
    selected_status = st.multiselect(
        "Select Status to analyze",
        options=status_options,
        default=status_options
    )

    # Top N slider
    top_n = st.slider("Show Top N slowest test cases", min_value=5, max_value=300, value=15, step=20)

    # Filter dataframe
    df_final["Elapsed Time"] = pd.to_timedelta(df_final["Elapsed Time"])
    df_final['Elapsed sec'] = df_final['Elapsed Time'].dt.total_seconds()
    df_filtered = df_final[df_final['Status'].isin(selected_status)]
    df_sorted = df_filtered.sort_values("Elapsed sec", ascending=False).head(top_n).reset_index(drop=True)

    # Format elapsed time nicely
    def format_timedelta(td):
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        parts = []
        if hours > 0:
            parts.append(f"{hours} hr")
        if minutes > 0:
            parts.append(f"{minutes} m")
        parts.append(f"{seconds} sec")
        return " ".join(parts)

    df_sorted['Elapsed Time (H:M:S)'] = df_sorted['Elapsed Time'].apply(format_timedelta)

    col2, col3 = st.columns(2)

    # ---------------- BAR CHART ----------------
    with col2:
        st.write(f"### ⏱ Time Taken per Test Case (Top {top_n})")
        bar_fig = px.bar(
            df_sorted,
            x='Process Name',
            y='Elapsed sec',
            text='Elapsed Time (H:M:S)',
            labels={'Process Name':'Test Cases', 'Elapsed sec':'Time (seconds)'},
            title=f"Time Taken per Test Case (Max → Min)",
            color='Elapsed sec',
            color_continuous_scale='Viridis',
            hover_data={'Elapsed Time (H:M:S)': True, 'Status': True}
        )
        bar_fig.update_traces(textposition='outside')
        bar_fig.update_layout(
            xaxis_tickangle=-45,
            height=450,
            margin=dict(t=60, b=120)
        )
        st.plotly_chart(bar_fig, use_container_width=True)

    # ---------------- TABLE ----------------
    with col3:
        st.write(f"### 📋 Execution Time Table (Top {top_n})")
        table_fig = go.Figure(
            data=[go.Table(
                header=dict(
                    values=["Process Name", "Status", "Elapsed Time"],
                    fill_color='paleturquoise',
                    align='left'
                ),
                cells=dict(
                    values=[
                        df_sorted['Process Name'],
                        df_sorted['Status'],
                        df_sorted['Elapsed Time (H:M:S)']
                    ],
                    fill_color='lavender',
                    align='left'
                )
            )]
        )
        table_fig.update_layout(height=450)
        st.plotly_chart(table_fig, use_container_width=True)


# --------------------------------------------------
# TAB 3: Agent Call
# --------------------------------------------------
with tab3:
    st.subheader("Agent Call / Action Center")

    st.write("### Trigger Agent / Automation")

    agent_name = st.selectbox(
        "Select Agent",
        ["Failure Analysis Agent", "Duplicate Cleanup Agent", "Performance Agent"]
    )

    user_input = st.text_area(
        "Provide instructions or context for the agent",
        placeholder="Analyze failed test cases and suggest root causes..."
    )

    if st.button("🚀 Run Agent"):
        with st.spinner("Agent is running..."):
            # Call your LLM / API / function here
            st.success(f"{agent_name} executed successfully!")

        st.write("### Agent Output")
        st.code("Agent response will appear here")


