import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/cbrown-clu/class_data/refs/heads/main/data/DS_job_roles_UK.csv"
df = pd.read_csv(url)

df.columns = df.columns.str.strip()
df = df.dropna(subset=['Job Title', 'Location', 'Salary', 'Skills'])

df['Salary'] = (
    df['Salary']
    .astype(str)
    .str.replace(r"[^\d.]", "", regex=True)
    .str.replace(r"\.+$", "", regex=True)
    .replace('', pd.NA)
    .astype(float)
)
df = df.dropna(subset=['Salary'])

st.title("UK Data Science Job Roles Dashboard")

st.sidebar.header("Filter Table")

location_filter = st.sidebar.selectbox("Choose Location", ['All'] + sorted(df['Location'].unique()))

salary_min, salary_max = int(df['Salary'].min()), int(df['Salary'].max())
salary_range = st.sidebar.slider("Salary Range (£)", salary_min, salary_max, (salary_min, salary_max))

filtered_df = df.copy()
if location_filter != 'All':
    filtered_df = filtered_df[filtered_df['Location'] == location_filter]
filtered_df = filtered_df[(filtered_df['Salary'] >= salary_range[0]) & (filtered_df['Salary'] <= salary_range[1])]

st.subheader("Filtered Job Listings Table")
st.write(f"Showing {len(filtered_df)} job(s)")
st.dataframe(
    filtered_df[['Job Title', 'Location', 'Salary', 'Skills']],
    use_container_width=True
)

st.subheader("Salary Distribution for Top 10 Job Titles")
top_titles = df['Job Title'].value_counts().head(10).index
plot_df = df[df['Job Title'].isin(top_titles)]

keyword = st.text_input("Optional keyword filter (applies to top job titles)")
if keyword:
    plot_df = plot_df[plot_df['Job Title'].str.contains(keyword, case=False)]

fig, ax = plt.subplots(figsize=(10, 6))
plot_df.boxplot(column='Salary', by='Job Title', ax=ax)
ax.set_title("Salary by Job Title (Top 10)")
ax.set_ylabel("Salary (£)")
ax.set_xlabel("Job Title")
plt.suptitle("")
plt.xticks(rotation=45)
st.pyplot(fig)
