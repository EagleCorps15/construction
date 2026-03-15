import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Advanced Construction Risk", layout="wide")

st.title("🏗️ Advanced Construction Scheduling Risk Analytics ")
st.write("NRAS Simulation with Risk Contribution & Critical Activity Detection")

# -----------------------------
# USER INPUT PANEL
# -----------------------------
st.sidebar.header("Project Configuration")

num_floors = st.sidebar.slider("Number of Floors", 1, 60, 0)
simulations = st.sidebar.slider("Simulation Runs", 100, 300, 500)
planned_duration = st.sidebar.number_input("Planned Duration (Days)", 100, 500, 180)

st.sidebar.subheader("Phase Duration Inputs (Days)")

def phase_input(name, default):
    opt = st.sidebar.number_input(f"{name} Optimistic", value=default-2)
    ml = st.sidebar.number_input(f"{name} Most Likely", value=default)
    pess = st.sidebar.number_input(f"{name} Pessimistic", value=default+3)
    return (opt, ml, pess)

phases = {
    "Site Preparation": phase_input("Site Preparation", 5),
    "Foundation": phase_input("Foundation", 20),
    "Structure": phase_input("Structure", 18),
    "MEP": phase_input("MEP Installation", 12),
    "Interior": phase_input("Interior Finishing",30),
    "Floor Work": phase_input("Per Floor Construction", 2)
}

# -----------------------------
# SIMULATION ENGINE
# -----------------------------
def triangular(opt, ml, pess, size):
    return np.random.triangular(opt, ml, pess, size) # size parametr is for number of iteration

def run_simulation():
    total_results = []
    contribution_tracker = {phase: [] for phase in phases}

    for _ in range(simulations):

        phase_times = {}

        for phase in phases:
            if phase == "Floor Work":
                phase_times[phase] = triangular(*phases[phase], num_floors).sum()
            else:
                phase_times[phase] = triangular(*phases[phase], 1)[0]

        total_time = sum(phase_times.values())
        total_results.append(total_time)

        for phase in phase_times:
            contribution_tracker[phase].append(phase_times[phase])

    return np.array(total_results), contribution_tracker

# -----------------------------
# RUN BUTTON
# -----------------------------
if st.button("Run Advanced Simulation"):

    results, contribution = run_simulation()

    # -----------------------------
    # KPI METRICS
    # -----------------------------
    avg = np.mean(results)
    p50 = np.percentile(results, 50)
    p80 = np.percentile(results, 80)
    p90 = np.percentile(results, 90)
    delay_prob = np.sum(results > planned_duration) / simulations

    st.subheader("📊 Executive Risk Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Expected Duration", f"{avg:.1f} Days")
    col2.metric("P50 Confidence", f"{p50:.1f}")
    col3.metric("P80 Confidence", f"{p80:.1f}")
    col4.metric("P90 Confidence", f"{p90:.1f}")
    col5.metric("Delay Probability", f"{delay_prob*100:.1f}%")

    # -----------------------------
    # COMPLETION DISTRIBUTION
    # -----------------------------
    st.subheader("Project Completion Distribution")

    fig = px.histogram(results, nbins=40, title="Completion Time Probability Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # RISK CONTRIBUTION ANALYSIS
    # -----------------------------
    st.subheader("Risk Contribution Analysis")

    contribution_avg = {
        phase: np.mean(contribution[phase])
        for phase in contribution
    }

    contrib_df = pd.DataFrame(
        list(contribution_avg.items()),
        columns=["Phase", "Average Duration"]
    ).sort_values("Average Duration", ascending=False)

    fig2 = px.bar(contrib_df, x="Phase", y="Average Duration", title="Phase Risk Contribution (Tornado Style)")
    st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # CRITICAL ACTIVITY DETECTION
    # -----------------------------
    st.subheader("Critical Activity Identification")

    std_dev = {
        phase: np.std(contribution[phase])
        for phase in contribution
    }

    std_df = pd.DataFrame(
        list(std_dev.items()),
        columns=["Phase", "Risk Variability"]
    ).sort_values("Risk Variability", ascending=True)

    st.dataframe(std_df)

    st.info(f"⚠️ Most Risk Sensitive Phase: {std_df.iloc[0]['Phase']}")

    # -----------------------------
    # MULTI PROJECT COMPARISON (SCENARIO STORAGE)
    # -----------------------------
    st.subheader("Scenario Storage")

    scenario_name = st.text_input("Save Scenario Name")

    if "scenarios" not in st.session_state:
        st.session_state.scenarios = {}

    if st.button("Save Scenario"):
        st.session_state.scenarios[scenario_name] = avg
        st.success("Scenario Saved")

    if st.session_state.scenarios:
        scenario_df = pd.DataFrame(
            st.session_state.scenarios.items(),
            columns=["Scenario", "Expected Duration"]
        )
        st.bar_chart(scenario_df.set_index("Scenario"))

    # -----------------------------
    # EXPORT DATA
    # -----------------------------
    df = pd.DataFrame(results, columns=["Completion Time"])
    csv = df.to_csv(index=False).encode()

    st.download_button("Download Simulation Data", csv, "risk_results.csv", "text/csv")
