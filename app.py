import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="HR Attrition Dashboard", layout="wide")
st.title("HR Attrition Dashboard")

st.markdown("""
This dashboard provides interactive, in-depth analysis of employee attrition for HR directors and stakeholders.
Use the filters in the sidebar to drill down on specific segments.
""")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("EA.csv")

df = load_data()

st.header("Dataset Preview")
st.write("Below is a preview of the uploaded employee dataset, including attrition labels:")
st.dataframe(df.head())

# Sidebar Filters
st.sidebar.header("Filters")
if 'Department' in df.columns:
    departments = df['Department'].dropna().unique()
    selected_departments = st.sidebar.multiselect("Department", departments, default=departments)
else:
    selected_departments = []

if 'Gender' in df.columns:
    genders = df['Gender'].dropna().unique()
    selected_genders = st.sidebar.multiselect("Gender", genders, default=genders)
else:
    selected_genders = []

age_min, age_max = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))

# Apply Filters
filtered_df = df.copy()
if selected_departments:
    filtered_df = filtered_df[filtered_df['Department'].isin(selected_departments)]
if selected_genders:
    filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]
filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]

st.header("Filtered Dataset")
st.write("This is the data after applying filters:")
st.dataframe(filtered_df)

# 1. Overall Attrition Rate
st.subheader("1. Overall Attrition Rate")
st.write("Shows proportion of employees who have left vs. stayed.")
fig1 = px.pie(filtered_df, names='Attrition', title='Overall Attrition Rate')
st.plotly_chart(fig1, use_container_width=True)

# 2. Attrition by Department
if 'Department' in filtered_df.columns:
    st.subheader("2. Attrition by Department")
    st.write("Departments with higher attrition can be identified here.")
    fig2 = px.histogram(filtered_df, x='Department', color='Attrition', barmode='group')
    st.plotly_chart(fig2, use_container_width=True)

# 3. Attrition by Age
st.subheader("3. Attrition by Age")
st.write("Visualizes attrition distribution across age groups.")
fig3 = px.histogram(filtered_df, x='Age', color='Attrition', nbins=20)
st.plotly_chart(fig3, use_container_width=True)

# 4. Attrition by Gender
if 'Gender' in filtered_df.columns:
    st.subheader("4. Attrition by Gender")
    st.write("Shows attrition breakdown between genders.")
    fig4 = px.histogram(filtered_df, x='Gender', color='Attrition')
    st.plotly_chart(fig4, use_container_width=True)

# 5. Education Level
if 'Education' in filtered_df.columns:
    st.subheader("5. Attrition by Education Level")
    st.write("Highlights education levels of those leaving.")
    fig5 = px.histogram(filtered_df, x='Education', color='Attrition')
    st.plotly_chart(fig5, use_container_width=True)

# 6. Years at Company
if 'YearsAtCompany' in filtered_df.columns:
    st.subheader("6. Years at Company vs Attrition")
    st.write("Shows tenure patterns among employees.")
    fig6 = px.histogram(filtered_df, x='YearsAtCompany', color='Attrition')
    st.plotly_chart(fig6, use_container_width=True)

# 7. Monthly Income vs Attrition
if 'MonthlyIncome' in filtered_df.columns:
    st.subheader("7. Monthly Income by Attrition Status")
    st.write("Compares income levels for attrition.")
    fig7 = px.box(filtered_df, x='Attrition', y='MonthlyIncome')
    st.plotly_chart(fig7, use_container_width=True)

# 8. Age vs Attrition Boxplot
st.subheader("8. Age Distribution by Attrition")
st.write("Shows age spread for leaving vs staying.")
fig8 = px.box(filtered_df, x='Attrition', y='Age')
st.plotly_chart(fig8, use_container_width=True)

# 9. Heatmap of Correlations
st.subheader("9. Correlation Heatmap")
st.write("Identifies relationships between numeric variables.")
numeric_cols = filtered_df.select_dtypes(include='number').columns
if len(numeric_cols) > 1:
    corr = filtered_df[numeric_cols].corr()
    fig9, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    st.pyplot(fig9)

# 10. Attrition Rate by Department Table
if 'Department' in filtered_df.columns:
    st.subheader("10. Table: Attrition Rate by Department")
    st.write("Numerical view of attrition rates by department.")
    table1 = pd.crosstab(filtered_df['Department'], filtered_df['Attrition'], normalize='index') * 100
    st.dataframe(table1.style.format("{:.2f}"))

# 11. Attrition Rate by Gender Table
if 'Gender' in filtered_df.columns:
    st.subheader("11. Table: Attrition Rate by Gender")
    st.write("Numeric view by gender.")
    table2 = pd.crosstab(filtered_df['Gender'], filtered_df['Attrition'], normalize='index') * 100
    st.dataframe(table2.style.format("{:.2f}"))

# 12. Education vs Income
if 'Education' in filtered_df.columns and 'MonthlyIncome' in filtered_df.columns:
    st.subheader("12. Education vs Monthly Income")
    st.write("Compares income across education levels.")
    fig12 = px.box(filtered_df, x='Education', y='MonthlyIncome', color='Attrition')
    st.plotly_chart(fig12, use_container_width=True)

# 13. Years at Company vs Income
if 'YearsAtCompany' in filtered_df.columns and 'MonthlyIncome' in filtered_df.columns:
    st.subheader("13. Years at Company vs Monthly Income")
    st.write("Shows tenure and income trends.")
    fig13 = px.scatter(filtered_df, x='YearsAtCompany', y='MonthlyIncome', color='Attrition')
    st.plotly_chart(fig13, use_container_width=True)

# 14. Marital Status
if 'MaritalStatus' in filtered_df.columns:
    st.subheader("14. Attrition by Marital Status")
    st.write("Examines attrition across marital statuses.")
    fig14 = px.histogram(filtered_df, x='MaritalStatus', color='Attrition')
    st.plotly_chart(fig14, use_container_width=True)

# 15. Job Role
if 'JobRole' in filtered_df.columns:
    st.subheader("15. Attrition by Job Role")
    st.write("Highlights attrition in various roles.")
    fig15 = px.histogram(filtered_df, x='JobRole', color='Attrition')
    st.plotly_chart(fig15, use_container_width=True)

# 16. Years Since Last Promotion
if 'YearsSinceLastPromotion' in filtered_df.columns:
    st.subheader("16. Years Since Last Promotion vs Attrition")
    st.write("Shows promotion recency and attrition.")
    fig16 = px.box(filtered_df, x='Attrition', y='YearsSinceLastPromotion')
    st.plotly_chart(fig16, use_container_width=True)

# 17. Years with Current Manager
if 'YearsWithCurrManager' in filtered_df.columns:
    st.subheader("17. Years with Current Manager vs Attrition")
    st.write("Manager tenure and attrition relation.")
    fig17 = px.box(filtered_df, x='Attrition', y='YearsWithCurrManager')
    st.plotly_chart(fig17, use_container_width=True)

# 18. Age vs Monthly Income
if 'Age' in filtered_df.columns and 'MonthlyIncome' in filtered_df.columns:
    st.subheader("18. Age vs Monthly Income Scatter")
    st.write("Explore relationship between age and income.")
    fig18 = px.scatter(filtered_df, x='Age', y='MonthlyIncome', color='Attrition')
    st.plotly_chart(fig18, use_container_width=True)

# 19. Interactive Table
st.subheader("19. Interactive Filtered Table")
st.write("Search and sort the data below.")
st.dataframe(filtered_df)

# 20. Download Button
st.subheader("20. Download Filtered Data")
st.write("Download the filtered dataset as CSV.")
st.download_button("Download CSV", filtered_df.to_csv(index=False), file_name='filtered_data.csv')

st.success("Adjust filters in the sidebar to refine your analysis.")
