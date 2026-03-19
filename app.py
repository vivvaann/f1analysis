import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="F1 Analytics", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp { background-color: #0b0f1a; color: white; }
.title { font-size: 42px; font-weight: 700; color: #e10600; }
.sidebar-title { font-size: 20px; font-weight: 600; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# ---------- DATA ----------
df = pd.read_csv("f1_complete_dataset_2015_2025.csv")

# ---------- SIDEBAR ----------
st.sidebar.markdown('<div class="sidebar-title">F1 Analytics Dashboard</div>', unsafe_allow_html=True)

page = st.sidebar.radio("Navigate", [
    "Home", "Driver Comparison", "Points Trend",
    "Wins Analysis", "Points Table"
])

teams = st.sidebar.multiselect("Filter by Team", sorted(df["team"].unique()))
if teams:
    df = df[df["team"].isin(teams)]

# ---------- COMMON ----------
def plot(fig):
    fig.update_layout(
        plot_bgcolor="#0b0f1a",
        paper_bgcolor="#0b0f1a",
        font=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ---------- HOME ----------
if page == "Home":
    st.markdown('<div class="title">F1 Analytics (2015-2025) by Vivaan</div>', unsafe_allow_html=True)

    st.write("This dashboard analyzes Formula 1 drivers from 2015 to 2025 using race performance data.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Drivers", df["driver"].nunique())
    c2.metric("Teams", df["team"].nunique())
    c3.metric("Records", len(df))
    c4.metric("Points Scored", int(df["points"].sum()))

    st.subheader("Top Performances")

    top = df.sort_values("points", ascending=False).head(5)[
        ["driver", "team", "year", "points", "wins", "podiums"]
    ]

    top["points"] = top["points"].round(1)
    top = top.reset_index(drop=True)

    st.table(top)

# ---------- DRIVER COMPARISON ----------
elif page == "Driver Comparison":
    st.title("Driver Comparison")
    st.write("Compare drivers across seasons based on performance metrics.")

    selected = st.multiselect("Select Drivers", sorted(df["driver"].unique()))

    if selected:
        data = df[df["driver"].isin(selected)]
        data = data.groupby(["driver", "year"], as_index=False)["points"].sum()

        plot(px.line(data, x="year", y="points", color="driver"))

        summary = data.groupby("driver")["points"].sum().sort_values(ascending=False).reset_index(drop=True)
        st.table(summary)

# ---------- POINTS TREND ----------
elif page == "Points Trend":
    st.title("Points Trend")
    st.write("Analyze how a driver's points change over time.")

    driver = st.selectbox("Select Driver", sorted(df["driver"].unique()))
    data = df[df["driver"] == driver].groupby("year", as_index=False)["points"].sum()

    st.metric("Total Points", int(data["points"].sum()))

    plot(px.line(data, x="year", y="points"))

# ---------- WINS ----------
elif page == "Wins Analysis":
    st.title("Wins Analysis")
    st.write("Shows only drivers who won races in a selected year.")

    year = st.selectbox("Select Year", sorted(df["year"].unique()))
    data = df[(df["year"] == year) & (df["wins"] > 0)]

    plot(px.bar(data, x="wins", y="driver", orientation="h"))

# ---------- POINTS TABLE ----------
elif page == "Points Table":
    st.title("Points Table")
    st.write("Driver standings based on total points in a selected year.")

    year = st.selectbox("Select Year", sorted(df["year"].unique()))
    data = df[df["year"] == year].sort_values("points", ascending=False)

    data = data.reset_index(drop=True)

    st.table(data[[
        "driver", "team", "points", "wins", "podiums", "races_raced"
    ]])