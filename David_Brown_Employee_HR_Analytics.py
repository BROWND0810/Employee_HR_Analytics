"""
Program: David_Brown_Employee_HR_Analytics_Added_Features.py
Author: David Brown
Date: May 3, 2026
Purpose: to create an employee and HR analytics dashboard with added web app features
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class HRDashboard:
    def __init__(self, data):
        self.data = data

    def clean_data(self):
        # Make a copy so the original data stays safe
        cleaned_data = self.data.copy()

        # Count duplicate rows before cleaning
        duplicates_before = cleaned_data.duplicated().sum()

        # Remove duplicate rows
        cleaned_data = cleaned_data.drop_duplicates()

        # Count missing values
        missing_values = cleaned_data.isnull().sum().sum()

        # Save cleaned data back to the class
        self.data = cleaned_data

        return cleaned_data, duplicates_before, missing_values

    def total_employees(self):
        return len(self.data)

    def attrition_rate(self):
        attrition_count = self.data[self.data["Attrition"] == "Yes"].shape[0]
        total_count = self.data.shape[0]

        if total_count == 0:
            return 0

        rate = (attrition_count / total_count) * 100
        return rate

    def average_salary(self):
        return self.data["MonthlyIncome"].mean()

    def average_performance(self):
        return self.data["PerformanceRating"].mean()

    def average_age(self):
        return self.data["Age"].mean()

    def chart_attrition_by_department(self):
        chart_data = self.data.groupby(["Department", "Attrition"]).size().reset_index(name="Count")

        fig, ax = plt.subplots(figsize=(5, 3))
        sns.barplot(data=chart_data, x="Department", y="Count", hue="Attrition", ax=ax)

        ax.set_title("Attrition by Department")
        ax.set_xlabel("Department")
        ax.set_ylabel("Employee Count")
        ax.tick_params(axis="x", rotation=20)

        plt.tight_layout()
        return fig

    def chart_salary_distribution(self):
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.histplot(self.data["MonthlyIncome"], bins=20, kde=True, ax=ax)

        ax.set_title("Salary Distribution")
        ax.set_xlabel("Monthly Income")
        ax.set_ylabel("Employee Count")

        plt.tight_layout()
        return fig

    def chart_performance_distribution(self):
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.countplot(data=self.data, x="PerformanceRating", ax=ax)

        ax.set_title("Performance Rating Distribution")
        ax.set_xlabel("Performance Rating")
        ax.set_ylabel("Employee Count")

        plt.tight_layout()
        return fig

    def chart_average_salary_by_department(self):
        chart_data = self.data.groupby("Department")["MonthlyIncome"].mean().reset_index()

        fig, ax = plt.subplots(figsize=(5, 3))
        sns.barplot(data=chart_data, x="Department", y="MonthlyIncome", ax=ax)

        ax.set_title("Average Monthly Income by Department")
        ax.set_xlabel("Department")
        ax.set_ylabel("Average Monthly Income")
        ax.tick_params(axis="x", rotation=20)

        plt.tight_layout()
        return fig

    def chart_attrition_by_job_role(self):
        chart_data = self.data[self.data["Attrition"] == "Yes"]
        chart_data = chart_data["JobRole"].value_counts().reset_index()
        chart_data.columns = ["JobRole", "Count"]

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(data=chart_data, x="Count", y="JobRole", ax=ax)

        ax.set_title("Attrition by Job Role")
        ax.set_xlabel("Employee Count")
        ax.set_ylabel("Job Role")

        plt.tight_layout()
        return fig

    def chart_overtime_and_attrition(self):
        chart_data = self.data.groupby(["OverTime", "Attrition"]).size().reset_index(name="Count")

        fig, ax = plt.subplots(figsize=(5, 3))
        sns.barplot(data=chart_data, x="OverTime", y="Count", hue="Attrition", ax=ax)

        ax.set_title("Overtime and Attrition")
        ax.set_xlabel("Overtime")
        ax.set_ylabel("Employee Count")

        plt.tight_layout()
        return fig

    def chart_years_at_company(self):
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.histplot(self.data["YearsAtCompany"], bins=20, kde=True, ax=ax)

        ax.set_title("Years at Company Distribution")
        ax.set_xlabel("Years at Company")
        ax.set_ylabel("Employee Count")

        plt.tight_layout()
        return fig

    def chart_overall_attrition_pie(self):
        attrition_counts = self.data["Attrition"].value_counts()

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(
            attrition_counts,
            labels=attrition_counts.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title("Overall Employee Attrition")
        plt.tight_layout()
        return fig


st.set_page_config(page_title="Employee HR Analytics Dashboard", layout="wide")

# Light dashboard styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f9fc;
    }

    section[data-testid="stSidebar"] {
        background-color: #eef3f8;
    }

    .main-title {
        background-color: white;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #e6e6e6;
        margin-bottom: 20px;
        box-shadow: 0px 1px 4px rgba(0,0,0,0.05);
    }

    .main-title h1 {
        margin-bottom: 8px;
    }

    .main-title p {
        font-size: 17px;
        margin-bottom: 0px;
    }

    .small-note {
        background-color: #eef6ff;
        padding: 12px;
        border-radius: 10px;
        border-left: 5px solid #4a90e2;
        margin-bottom: 18px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #e6e6e6;
        box-shadow: 0px 1px 3px rgba(0,0,0,0.04);
    }

    h2, h3 {
        color: #1f2937;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-title">
        <h1>Employee Performance & HR Analytics Dashboard</h1>
        <p>This dashboard reviews employee attrition, salary patterns, performance ratings, overtime, and department trends.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Load HR Dataset")

file_name = "WA_Fn-UseC_-HR-Employee-Attrition.csv"

try:
    df = pd.read_csv(file_name)

    st.success("Dataset loaded successfully.")

    # Create object from HRDashboard class
    dashboard = HRDashboard(df)

    # Clean the data
    clean_df, duplicates_removed, missing_values = dashboard.clean_data()

    st.sidebar.header("Dashboard Filters")

    department_options = ["All Departments"] + sorted(clean_df["Department"].unique())
    gender_options = ["All Genders"] + sorted(clean_df["Gender"].unique())
    attrition_options = ["All Attrition"] + sorted(clean_df["Attrition"].unique())
    overtime_options = ["All Overtime"] + sorted(clean_df["OverTime"].unique())

    selected_department = st.sidebar.selectbox("Select Department", department_options)
    selected_gender = st.sidebar.selectbox("Select Gender", gender_options)
    selected_attrition = st.sidebar.selectbox("Select Attrition", attrition_options)
    selected_overtime = st.sidebar.selectbox("Select Overtime", overtime_options)

    filtered_df = clean_df.copy()

    if selected_department != "All Departments":
        filtered_df = filtered_df[filtered_df["Department"] == selected_department]

    if selected_gender != "All Genders":
        filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]

    if selected_attrition != "All Attrition":
        filtered_df = filtered_df[filtered_df["Attrition"] == selected_attrition]

    if selected_overtime != "All Overtime":
        filtered_df = filtered_df[filtered_df["OverTime"] == selected_overtime]

    # Rebuild dashboard object with filtered data
    dashboard = HRDashboard(filtered_df)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Overview", "Required Charts", "Extra Insights", "Dataset Preview"]
    )

    with tab1:
        st.subheader("Data Cleaning Summary")

        clean_col1, clean_col2, clean_col3, clean_col4 = st.columns(4)

        clean_col1.metric("Duplicates Removed", duplicates_removed)
        clean_col2.metric("Missing Values", missing_values)
        clean_col3.metric("Rows After Cleaning", clean_df.shape[0])
        clean_col4.metric("Columns", clean_df.shape[1])

        st.subheader("Dashboard Summary Metrics")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Total Employees", dashboard.total_employees())
        col2.metric("Attrition Rate", f"{dashboard.attrition_rate():.2f}%")
        col3.metric("Avg. Monthly Income", f"${dashboard.average_salary():,.2f}")
        col4.metric("Avg. Performance", f"{dashboard.average_performance():.2f}")
        col5.metric("Avg. Age", f"{dashboard.average_age():.1f}")

        st.subheader("Quick Insight")

        if dashboard.attrition_rate() >= 20:
            st.warning(
                "The selected group has a higher attrition rate. This group may need more HR review."
            )
        elif dashboard.attrition_rate() > 0:
            st.info(
                "The selected group has some employee attrition. The dashboard can help review possible patterns."
            )
        else:
            st.success(
                "The selected group has no attrition in the current filtered view."
            )

        st.subheader("Overall Attrition Visual")

        pie_col1, pie_col2 = st.columns([1, 1])

        with pie_col1:
            st.pyplot(dashboard.chart_overall_attrition_pie(), use_container_width=True)

        with pie_col2:
            st.markdown(
                """
                <div class="small-note">
                    This pie chart gives a quick view of employee attrition.
                    It works like a simple visual summary for the selected filters.
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab2:
        st.subheader("Required HR Visualizations")

        st.write("These charts show attrition, salary, and performance trends.")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.pyplot(dashboard.chart_attrition_by_department(), use_container_width=True)

        with chart_col2:
            st.pyplot(dashboard.chart_salary_distribution(), use_container_width=True)

        chart_col3, chart_col4 = st.columns(2)

        with chart_col3:
            st.pyplot(dashboard.chart_performance_distribution(), use_container_width=True)

        with chart_col4:
            st.info(
                "These three visuals meet the required chart section for the project."
            )

    with tab3:
        st.subheader("Additional HR Visualizations")

        st.write("These extra charts help support the report and PowerPoint.")

        extra_col1, extra_col2 = st.columns(2)

        with extra_col1:
            st.pyplot(dashboard.chart_average_salary_by_department(), use_container_width=True)

        with extra_col2:
            st.pyplot(dashboard.chart_overtime_and_attrition(), use_container_width=True)

        extra_col3, extra_col4 = st.columns(2)

        with extra_col3:
            st.pyplot(dashboard.chart_attrition_by_job_role(), use_container_width=True)

        with extra_col4:
            st.pyplot(dashboard.chart_years_at_company(), use_container_width=True)

        st.subheader("HR Review Notes")

        with st.form("hr_notes_form"):
            reviewer_name = st.text_input("Reviewer Name")
            review_note = st.text_area("Enter a short HR observation")
            submitted = st.form_submit_button("Submit Note")

            if submitted:
                st.success("HR note submitted for review.")
                st.write(f"Reviewer: {reviewer_name}")
                st.write(f"Observation: {review_note}")

        st.write(
            "This form connects to the class concept of collecting user input in a web application."
        )

    with tab4:
        st.subheader("Filtered Dataset Preview")
        st.dataframe(filtered_df.head())

        st.subheader("Filtered Dataset Size")
        st.write(f"Rows: {filtered_df.shape[0]}")
        st.write(f"Columns: {filtered_df.shape[1]}")

        csv_data = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Filtered Dataset",
            data=csv_data,
            file_name="filtered_employee_hr_data.csv",
            mime="text/csv"
        )

        with st.expander("Show Column Names"):
            st.write(list(filtered_df.columns))

        with st.expander("Show Missing Values by Column"):
            st.write(filtered_df.isnull().sum())

        st.subheader("Project Links")

        st.write("Streamlit App: https://employeehranalytics.streamlit.app")
        st.write("GitHub Repository: https://github.com/BROWNDO810/Employee_HR_Analytics")
        st.write(
            "Dataset Source: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset"
        )

except FileNotFoundError:
    st.error(
        "Dataset file was not found. Make sure the CSV file is in the same folder as this Python file."
    )
