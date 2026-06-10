# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🎓 Student Performance Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)
PRIMARY = "#6366F1"
SECONDARY = "#06B6D4"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"

BG = "#0F172A"
CARD = "#1E293B"
TEXT = "#F8FAFC"
# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main{
    background-color:#0F172A;
}

.kpi-card{
    background: linear-gradient(135deg,#6366F1,#06B6D4);
    padding:20px;
    border-radius:15px;
    color:white;
    box-shadow:0 0 25px rgba(99,102,241,.4);
}

</style>
""", unsafe_allow_html=True)
# ---------------- LOAD DATA ----------------
# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("csv00")   # agar file ka naam csv00.csv hai to yahan csv00.csv likhein
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

df = load_data()

# Agar data load na ho to app yahin ruk jaye
if df.empty:
    st.stop()

# Debug (temporary - baad mein hata sakte hain)
# ---------------- FEATURE ENGINEERING ----------------
df["average_score"] = (
    df["math score"] +
    df["reading score"] +
    df["writing score"]
) / 3

df["performance"] = pd.cut(
    df["average_score"],
    bins=[0, 60, 80, 100],
    labels=["Poor", "Good", "Excellent"]
)

# ---------------- HEADER ----------------
st.markdown("""
<div style="
padding:30px;
border-radius:20px;
background:linear-gradient(135deg,#1E3A8A,#06B6D4);
text-align:center;
color:white;
box-shadow:0 8px 20px rgba(0,0,0,0.3);
margin-bottom:25px;
">
<h1>🎓 Student Performance Analytics Dashboard</h1>
<h4>Advanced Student Performance Insights & Analytics</h4>
<p>Interactive Dashboard for Academic Performance Evaluation</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135755.png",
    width=120
)

st.sidebar.title("🔍 Filters")

gender = st.sidebar.multiselect(
    "Gender",
    df["gender"].unique(),
    default=df["gender"].unique()
)

lunch = st.sidebar.multiselect(
    "Lunch Type",
    df["lunch"].unique(),
    default=df["lunch"].unique()
)

prep = st.sidebar.multiselect(
    "Preparation Course",
    df["test preparation course"].unique(),
    default=df["test preparation course"].unique()
)

education = st.sidebar.multiselect(
    "Parent Education",
    df["parental level of education"].unique(),
    default=df["parental level of education"].unique()
)

score_range = st.sidebar.slider(
    "Average Score Range",
    0,
    100,
    (0, 100)
)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df["gender"].isin(gender))
    & (df["lunch"].isin(lunch))
    & (df["test preparation course"].isin(prep))
    & (df["parental level of education"].isin(education))
    & (df["average_score"].between(score_range[0], score_range[1]))
]
st.markdown("## 🤖 AI Generated Insights")

avg_math = filtered_df["math score"].mean()
avg_reading = filtered_df["reading score"].mean()
avg_writing = filtered_df["writing score"].mean()

best_subject = max(
    {
        "Math": avg_math,
        "Reading": avg_reading,
        "Writing": avg_writing
    },
    key=lambda x: {
        "Math": avg_math,
        "Reading": avg_reading,
        "Writing": avg_writing
    }[x]
)


# ---------------- KPIs ----------------
st.markdown("## 📊 Executive Summary")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("👨‍🎓 Students", len(filtered_df))
col2.metric("➕ Avg Math", round(filtered_df["math score"].mean(),1))
col3.metric("📖 Avg Reading", round(filtered_df["reading score"].mean(),1))
col4.metric("✍ Avg Writing", round(filtered_df["writing score"].mean(),1))
col5.metric("🏆 Avg Overall", round(filtered_df["average_score"].mean(),1))

st.divider()

# ---------------- CHARTS ROW 1 ----------------
# ---------------- CHARTS ROW 1 ----------------
c1, c2 = st.columns(2)

# ---------- Bar Chart ----------
with c1:
    fig = px.bar(
        filtered_df.groupby("gender")["math score"]
        .mean()
        .reset_index(),
        x="gender",
        y="math score",
        color="gender",
        color_discrete_map={
            "female": "#EC4899",   # Pink
            "male": "#3B82F6"      # Blue
        },
        text_auto=".1f",
        title="📊 Average Math Score by Gender"
    )

    fig.update_traces(
        marker_line_color="white",
        marker_line_width=2,
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(color="white"),
        title_font=dict(size=20),
        xaxis_title="Gender",
        yaxis_title="Average Math Score"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------- Donut Chart ----------
with c2:
    fig = px.pie(
        filtered_df,
        names="gender",
        hole=0.55,   # Donut effect
        color="gender",
        color_discrete_map={
            "female": "#EC4899",   # Pink
            "male": "#3B82F6"      # Blue
        },
        title="👥 Gender Distribution"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(color="white"),
        title_font=dict(size=20)
    )

    st.plotly_chart(fig, use_container_width=True)
# ---------------- CHARTS ROW 2 ----------------
# ---------------- CHARTS ROW 2 ----------------
c1, c2 = st.columns(2)

# ---------- Histogram ----------
with c1:
    fig = px.histogram(
        filtered_df,
        x="math score",
        nbins=25,
        color_discrete_sequence=["#06B6D4"],
        title="📈 Math Score Distribution"
    )

    fig.update_traces(
        marker_line_color="white",
        marker_line_width=1.5
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(color="white"),
        title_font=dict(size=20),
        xaxis_title="Math Score",
        yaxis_title="Number of Students"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------- Box Plot ----------
with c2:
    fig = px.box(
        filtered_df,
        x="gender",
        y="writing score",
        color="gender",
        color_discrete_map={
            "female": "#EC4899",   # Pink
            "male": "#3B82F6"      # Blue
        },
        title="✍️ Writing Score Distribution by Gender"
    )

    fig.update_traces(
        marker=dict(size=6),
        line=dict(width=2)
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(color="white"),
        title_font=dict(size=20),
        xaxis_title="Gender",
        yaxis_title="Writing Score"
    )

    st.plotly_chart(fig, use_container_width=True)
# ---------------- CHARTS ROW 3 ----------------
# ---------------- CHARTS ROW 3 ----------------
c1, c2 = st.columns(2)

# ---------- Scatter Plot ----------
with c1:
    fig = px.scatter(
        filtered_df,
        x="math score",
        y="reading score",
        color="average_score",
        size="writing score",
        hover_data=["average_score"],
        color_continuous_scale="Turbo",
        title="📊 Math vs Reading Performance"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(color="white"),
        title_font=dict(size=20),
        xaxis_title="Math Score",
        yaxis_title="Reading Score",
        coloraxis_colorbar=dict(title="Average")
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------- Performance Categories ----------
with c2:

    performance_count = (
        filtered_df["performance"]
        .value_counts()
        .reset_index()
    )

    performance_count.columns = ["performance", "count"]

    fig = px.bar(
        performance_count,
        x="performance",
        y="count",
        color="performance",
        text="count",
        color_discrete_map={
            "Poor": "#EF4444",        # Red
            "Good": "#F59E0B",        # Orange
            "Excellent": "#10B981"   # Green
        },
        title="🏆 Performance Categories"
    )

    fig.update_traces(
        marker_line_color="white",
        marker_line_width=2,
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(color="white"),
        title_font=dict(size=20),
        xaxis_title="Performance",
        yaxis_title="Number of Students"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- HEATMAP ----------------
st.subheader("🔥 Correlation Heatmap")

corr = filtered_df[
    ["math score","reading score","writing score"]
].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- AREA CHART ----------------
st.subheader("📈 Score Trends")

area_data = filtered_df[
    ["math score","reading score","writing score"]
]

st.area_chart(area_data)

# ---------------- TOP STUDENTS ----------------
st.subheader("🏆 Top 10 Students")

top_students = filtered_df.sort_values(
    by="average_score",
    ascending=False
).head(10)

st.dataframe(top_students, use_container_width=True)

# ---------------- DOWNLOAD BUTTON ----------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "filtered_students.csv",
    "text/csv"
)

# ---------------- FULL DATA ----------------
with st.expander("📋 View Full Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center>Developed with ❤️ using Streamlit & Plotly</center>",
    unsafe_allow_html=True
)
