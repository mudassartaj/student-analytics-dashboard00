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

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.kpi-card {
    background: linear-gradient(135deg,#4F46E5,#06B6D4);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

h1,h2,h3 {
    color: white;
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

highest_corr = filtered_df[
    ["math score", "reading score", "writing score"]
].corr()

reading_writing_corr = highest_corr.loc["reading score", "writing score"]

male_avg = filtered_df[
    filtered_df["gender"] == "male"
]["average_score"].mean()

female_avg = filtered_df[
    filtered_df["gender"] == "female"
]["average_score"].mean()

prep_completed = filtered_df[
    filtered_df["test preparation course"] == "completed"
]["average_score"].mean()

prep_none = filtered_df[
    filtered_df["test preparation course"] == "none"
]["average_score"].mean()

st.info(f"""
### 📊 Smart Insights

✅ **{best_subject}** has the highest average score among all subjects.

✅ Reading and Writing scores have a **strong positive correlation ({reading_writing_corr:.2f})**.

✅ Female students average score: **{female_avg:.1f}**

✅ Male students average score: **{male_avg:.1f}**

✅ Students who completed the test preparation course scored **{prep_completed:.1f}** on average.

✅ Students without preparation scored **{prep_none:.1f}** on average.

✅ Test preparation improves performance by approximately **{prep_completed - prep_none:.1f} marks**.

✅ Overall class average score is **{filtered_df["average_score"].mean():.1f}**.

""")
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
c1, c2 = st.columns(2)

with c1:
    fig = px.bar(
        filtered_df.groupby("gender")["math score"]
        .mean()
        .reset_index(),
        x="gender",
        y="math score",
        color="gender",
        title="Average Math Score by Gender"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.pie(
        filtered_df,
        names="gender",
        title="Gender Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- CHARTS ROW 2 ----------------
c1, c2 = st.columns(2)

with c1:
    fig = px.histogram(
        filtered_df,
        x="math score",
        nbins=20,
        title="Math Score Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.box(
        filtered_df,
        x="gender",
        y="writing score",
        color="gender",
        title="Writing Score Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- CHARTS ROW 3 ----------------
c1, c2 = st.columns(2)

with c1:
    fig = px.scatter(
        filtered_df,
        x="math score",
        y="reading score",
        color="gender",
        size="writing score",
        hover_data=["average_score"],
        title="Math vs Reading Score"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    performance_count = (
        filtered_df["performance"]
        .value_counts()
        .reset_index()
    )

    fig = px.bar(
        performance_count,
        x="performance",
        y="count",
        color="performance",
        title="Performance Categories"
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
