# ---------------------------------------------------
# IMPORT LIBRARIES
# ---------------------------------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Aston Villa vs Liverpool Tactical Analysis",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("⚽ Aston Villa vs Liverpool Tactical Match Analysis")

st.markdown("""
### Premier League 2025/2026 — Aston Villa vs Liverpool

This dashboard explores:
- Expected Goals (xG)
- Shot Quality
- Tactical Patterns
- Player Threat
- Set-Piece Efficiency
""")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
data = {
    "team": [
        "Aston Villa","Aston Villa","Aston Villa","Aston Villa","Aston Villa",
        "Aston Villa","Aston Villa","Aston Villa","Aston Villa","Aston Villa",
        "Aston Villa","Aston Villa","Aston Villa","Aston Villa",
        "Liverpool","Liverpool","Liverpool","Liverpool","Liverpool",
        "Liverpool","Liverpool","Liverpool","Liverpool","Liverpool",
        "Liverpool","Liverpool","Liverpool","Liverpool","Liverpool","Liverpool"
    ],

    "player": [
        "Emiliano Buendía","John McGinn","Lucas Digne","Matthew Cash",
        "Morgan Rogers","Ollie Watkins","Ollie Watkins","Ollie Watkins",
        "Ollie Watkins","Ollie Watkins","Ollie Watkins","Pau Torres",
        "Ross Barkley","Youri Tielemans",

        "Alexis Mac Allister","Cody Gakpo","Cody Gakpo","Curtis Jones",
        "Curtis Jones","Dominik Szoboszlai","Federico Chiesa",
        "Florian Wirtz","Joseph Gomez","Joseph Gomez",
        "Rio Ngumoha","Rio Ngumoha","Rio Ngumoha",
        "Ryan Gravenberch","Virgil van Dijk","Virgil van Dijk"
    ],

    "X": [
        0.863,0.812,0.726,0.796,0.884,
        0.837,0.874,0.895,0.911,0.943,
        0.965,0.926,0.756,0.809,
        0.965,0.906,0.919,0.875,0.896,
        0.695,0.977,0.806,0.719,0.859,
        0.747,0.800,0.961,0.791,0.926,0.927
    ],

    "Y": [
        0.718,0.314,0.386,0.708,0.715,
        0.542,0.643,0.429,0.530,0.399,
        0.510,0.477,0.580,0.597,
        0.579,0.491,0.503,0.523,0.354,
        0.389,0.597,0.703,0.293,0.325,
        0.650,0.714,0.677,0.654,0.575,0.483
    ],

    "xG": [
        0.046744,0.037566,0.043899,0.018321,0.035547,
        0.110304,0.074377,0.365319,0.488731,0.397041,
        0.726361,0.501773,0.035787,0.057965,
        0.201080,0.426245,0.045561,0.027047,0.048372,
        0.012809,0.087209,0.023044,0.013280,0.042511,
        0.014703,0.022785,0.068070,0.021425,0.191202,0.316694
    ],

    "situation": [
        "OpenPlay","OpenPlay","DirectFreekick","SetPiece","FromCorner",
        "OpenPlay","OpenPlay","OpenPlay","OpenPlay","OpenPlay",
        "FromCorner","FromCorner","OpenPlay","OpenPlay",

        "FromCorner","OpenPlay","FromCorner","FromCorner",
        "OpenPlay","OpenPlay","FromCorner","FromCorner",
        "OpenPlay","OpenPlay","OpenPlay","OpenPlay",
        "OpenPlay","OpenPlay","SetPiece","FromCorner"
    ],

    "result": [
        "ShotOnPost","Goal","BlockedShot","BlockedShot","Goal",
        "SavedShot","MissedShots","Goal","SavedShot","SavedShot",
        "Goal","SavedShot","BlockedShot","SavedShot",

        "MissedShots","MissedShots","MissedShots","MissedShots",
        "BlockedShot","SavedShot","SavedShot","BlockedShot",
        "MissedShots","MissedShots","MissedShots","ShotOnPost",
        "BlockedShot","SavedShot","Goal","Goal"
    ]
}

df = pd.DataFrame(data)

# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------
st.sidebar.title("Dashboard Filters")

team_filter = st.sidebar.selectbox(
    "Select Team",
    ["All Teams", "Aston Villa", "Liverpool"]
)

situation_filter = st.sidebar.selectbox(
    "Select Situation",
    ["All", "OpenPlay", "FromCorner", "SetPiece", "DirectFreekick"]
)

df_filtered = df.copy()

if team_filter != "All Teams":
    df_filtered = df_filtered[df_filtered["team"] == team_filter]

if situation_filter != "All":
    df_filtered = df_filtered[df_filtered["situation"] == situation_filter]

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------
st.subheader("📊 Match KPIs")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Shots",
        len(df_filtered)
    )

with col2:
    st.metric(
        "Total xG",
        round(df_filtered["xG"].sum(), 2)
    )

with col3:
    goals = (df_filtered["result"] == "Goal").sum()

    st.metric(
        "Goals",
        goals
    )

# ---------------------------------------------------
# SHOT MAP
# ---------------------------------------------------
st.subheader("🎯 Shot Map (xG Intensity)")

# Convert coordinates
df_filtered["plotX"] = df_filtered["X"] * 100
df_filtered["plotY"] = df_filtered["Y"] * 100

pitch = Pitch(
    pitch_type='opta',
    pitch_color='#1e1e1e',
    line_color='white'
)

fig, ax = pitch.draw(figsize=(8, 5.5))

scatter = pitch.scatter(
    df_filtered["plotX"],
    df_filtered["plotY"],
    s=df_filtered["xG"] * 2200,
    c=df_filtered["xG"],
    cmap="coolwarm",
    edgecolors="black",
    linewidth=1,
    alpha=0.85,
    ax=ax
)

cbar = plt.colorbar(
    scatter,
    ax=ax,
    fraction=0.03,
    pad=0.02
)

cbar.set_label("xG")

ax.set_title(
    "Shot Location Map",
    fontsize=15,
    color="white",
    pad=12
)

st.pyplot(fig)

# ---------------------------------------------------
# PLAYER THREAT ANALYSIS
# ---------------------------------------------------
st.subheader("🔥 Player Threat Analysis")

player_summary = (
    df_filtered.groupby("player")
    .agg(
        shots=("xG", "count"),
        total_xG=("xG", "sum")
    )
    .reset_index()
    .sort_values(by="total_xG", ascending=False)
)

st.dataframe(player_summary)

# ---------------------------------------------------
# PLAYER xG CHART
# ---------------------------------------------------
st.subheader("📈 Player Expected Goals")

fig_xg = px.bar(
    player_summary,
    x="player",
    y="total_xG",
    color="total_xG",
    height=400,
    text_auto=".2f"
)

fig_xg.update_layout(
    template="plotly_dark",
    showlegend=False,
    xaxis_title="Player",
    yaxis_title="Total xG",
    margin=dict(l=20, r=20, t=40, b=20)
)

fig_xg.update_xaxes(tickangle=45)

st.plotly_chart(
    fig_xg,
    use_container_width=True
)

# ---------------------------------------------------
# SHOT OUTCOME DISTRIBUTION
# ---------------------------------------------------
st.subheader("⚽ Shot Outcome Distribution")

result_counts = (
    df_filtered["result"]
    .value_counts()
    .reset_index()
)

result_counts.columns = ["result", "count"]

fig_result = px.bar(
    result_counts,
    x="result",
    y="count",
    color="count",
    height=350,
    text_auto=True
)

fig_result.update_layout(
    template="plotly_dark",
    showlegend=False,
    xaxis_title="Shot Result",
    yaxis_title="Count",
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(
    fig_result,
    use_container_width=True
)

# ---------------------------------------------------
# SITUATION ANALYSIS
# ---------------------------------------------------
st.subheader("🧠 Situation-Based xG Analysis")

situation_summary = (
    df_filtered.groupby("situation")
    .agg(
        total_xG=("xG", "sum"),
        shots=("xG", "count")
    )
    .reset_index()
)

fig_situation = px.bar(
    situation_summary,
    x="situation",
    y="total_xG",
    color="shots",
    height=400,
    text_auto=".2f"
)

fig_situation.update_layout(
    template="plotly_dark",
    xaxis_title="Situation",
    yaxis_title="Total xG",
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(
    fig_situation,
    use_container_width=True
)

# ---------------------------------------------------
# INSIGHTS
# ---------------------------------------------------
st.subheader("📌 Tactical Insights")

st.markdown("""
### Aston Villa
- Generated significantly higher-quality chances
- Ollie Watkins was the primary attacking threat
- Created dangerous opportunities from corners
- Strong central penalty-box penetration

### Liverpool
- Relied heavily on set pieces
- Generated more low-quality shots
- Virgil van Dijk provided aerial threat
- Lower open-play efficiency

### Tactical Conclusion
Aston Villa produced clearer scoring opportunities despite lower shot volume, while Liverpool depended more on set-piece efficiency.
""")