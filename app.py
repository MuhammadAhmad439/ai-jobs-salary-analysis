import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Jobs & Salaries Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("AI Jobs & Salaries Dashboard")
st.caption("Explore salary patterns across experience levels, job titles, locations, work modes, and company sizes.")

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_csv("ai_jobs_salaries_clean.csv")
    data["salary_in_usd"] = pd.to_numeric(data["salary_in_usd"], errors="coerce")
    data["work_year"] = pd.to_numeric(data["work_year"], errors="coerce")
    return data

uploaded_file = st.sidebar.file_uploader("Upload the dataset CSV", type=["csv"])
try:
    df = load_data(uploaded_file)
except FileNotFoundError:
    st.info("Upload your AI jobs salary CSV using the sidebar to start exploring the dashboard.")
    st.stop()

required_columns = {
    "salary_in_usd", "experience_level_label", "job_title", "work_year",
    "work_mode", "company_size", "company_location"
}
missing = required_columns - set(df.columns)
if missing:
    st.error("The dataset is missing required columns: " + ", ".join(sorted(missing)))
    st.stop()

st.sidebar.header("Filters")

years = sorted(df["work_year"].dropna().astype(int).unique().tolist())
selected_years = st.sidebar.multiselect("Work year", years, default=years)

experience_values = sorted(df["experience_level_label"].dropna().unique().tolist())
selected_experience = st.sidebar.multiselect(
    "Experience level", experience_values, default=experience_values
)

work_modes = sorted(df["work_mode"].dropna().unique().tolist())
selected_modes = st.sidebar.multiselect("Work mode", work_modes, default=work_modes)

company_sizes = sorted(df["company_size"].dropna().unique().tolist())
selected_sizes = st.sidebar.multiselect("Company size", company_sizes, default=company_sizes)

locations = sorted(df["company_location"].dropna().unique().tolist())
selected_locations = st.sidebar.multiselect(
    "Company location", locations, default=locations
)

filtered = df[
    df["work_year"].isin(selected_years)
    & df["experience_level_label"].isin(selected_experience)
    & df["work_mode"].isin(selected_modes)
    & df["company_size"].isin(selected_sizes)
    & df["company_location"].isin(selected_locations)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Change one or more filters.")
    st.stop()

total_jobs = len(filtered)
avg_salary = filtered["salary_in_usd"].mean()
median_salary = filtered["salary_in_usd"].median()
max_salary = filtered["salary_in_usd"].max()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Job records", f"{total_jobs:,}")
m2.metric("Average salary", f"${avg_salary:,.0f}" if pd.notna(avg_salary) else "N/A")
m3.metric("Median salary", f"${median_salary:,.0f}" if pd.notna(median_salary) else "N/A")
m4.metric("Highest salary", f"${max_salary:,.0f}" if pd.notna(max_salary) else "N/A")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Average salary by experience")
    exp_salary = (
        filtered.groupby("experience_level_label", as_index=False)
        .agg(Average_Salary=("salary_in_usd", "mean"), Job_Count=("salary_in_usd", "size"))
        .sort_values("Average_Salary", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=exp_salary, x="Average_Salary", y="experience_level_label", ax=ax)
    ax.set_xlabel("Average salary (USD)")
    ax.set_ylabel("Experience level")
    ax.set_title("Average salary by experience level")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Salary distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data=filtered, x="salary_in_usd", bins=40, kde=True, ax=ax)
    ax.set_xlabel("Salary (USD)")
    ax.set_ylabel("Number of records")
    ax.set_title("Salary distribution")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

left, right = st.columns(2)

with left:
    st.subheader("Most common job titles")
    top_jobs = filtered["job_title"].value_counts().head(10).rename_axis("Job title").reset_index(name="Job count")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=top_jobs, x="Job count", y="Job title", ax=ax)
    ax.set_title("Top 10 job titles by record count")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Average salary by work mode")
    mode_salary = (
        filtered.groupby("work_mode", as_index=False)
        .agg(Average_Salary=("salary_in_usd", "mean"), Job_Count=("salary_in_usd", "size"))
        .sort_values("Average_Salary", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=mode_salary, x="work_mode", y="Average_Salary", ax=ax)
    ax.set_xlabel("Work mode")
    ax.set_ylabel("Average salary (USD)")
    ax.set_title("Average salary by work mode")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"${y:,.0f}"))
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

left, right = st.columns(2)

with left:
    st.subheader("Salary trend by year")
    year_salary = (
        filtered.groupby("work_year", as_index=False)
        .agg(Average_Salary=("salary_in_usd", "mean"))
        .sort_values("work_year")
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=year_salary, x="work_year", y="Average_Salary", marker="o", ax=ax)
    ax.set_xlabel("Work year")
    ax.set_ylabel("Average salary (USD)")
    ax.set_title("Average salary by year")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"${y:,.0f}"))
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Average salary by company size")
    size_salary = (
        filtered.groupby("company_size", as_index=False)
        .agg(Average_Salary=("salary_in_usd", "mean"), Job_Count=("salary_in_usd", "size"))
        .sort_values("Average_Salary", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=size_salary, x="company_size", y="Average_Salary", ax=ax)
    ax.set_xlabel("Company size")
    ax.set_ylabel("Average salary (USD)")
    ax.set_title("Average salary by company size")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"${y:,.0f}"))
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()
st.subheader("Filtered data")
st.caption("Use the filters in the sidebar, then explore or download the matching records.")
st.dataframe(filtered, use_container_width=True, hide_index=True)

csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered data as CSV",
    data=csv_data,
    file_name="filtered_ai_jobs_salaries.csv",
    mime="text/csv"
)
