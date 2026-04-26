"""
Program: David_Brown_Employee_HR_Analytics.py
Author: David Brown
Date: May 3, 2026
Purpose: to create an employee and HR analytics dashboard
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


"""
Final Project:
Employee Performance & HR Analytics Dashboard
"""


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


st.set_page_config(page_title="Employee HR Analytics Dashboard", layout="wide")

st.title("Employee Performance & HR Analytics Dashboard")

st.write(
    "This dashboard reviews employee attrition, salary patterns, and performance ratings."
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

    st.subheader("Data Cleaning Summary")

    clean_col1, clean_col2, clean_col3, clean_col4 = st.columns(4)

    clean_col1.metric("Duplicates Removed", duplicates_removed)
    clean_col2.metric("Missing Values", missing_values)
    clean_col3.metric("Rows After Cleaning", clean_df.shape[0])
    clean_col4.metric("Columns", clean_df.shape[1])

    """
    This section adds the department filter.
    The filter changes the data used in the metrics and charts.
    """

    st.sidebar.header("Dashboard Filters")

    department_options = ["All Departments"] + sorted(clean_df["Department"].unique())

    selected_department = st.sidebar.selectbox(
        "Select Department",
        department_options
    )

    if selected_department != "All Departments":
        filtered_df = clean_df[clean_df["Department"] == selected_department]
    else:
        filtered_df = clean_df

    # Rebuild dashboard object with filtered data
    dashboard = HRDashboard(filtered_df)

    st.subheader("Dashboard Summary Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Employees", dashboard.total_employees())
    col2.metric("Attrition Rate", f"{dashboard.attrition_rate():.2f}%")
    col3.metric("Avg. Monthly Income", f"${dashboard.average_salary():,.2f}")
    col4.metric("Avg. Performance", f"{dashboard.average_performance():.2f}")
    col5.metric("Avg. Age", f"{dashboard.average_age():.1f}")

    st.subheader("Required HR Visualizations")

    st.write("These charts show attrition, salary, and performance trends in the HR dataset.")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.pyplot(dashboard.chart_attrition_by_department(), use_container_width=True)

    with chart_col2:
        st.pyplot(dashboard.chart_salary_distribution(), use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        st.pyplot(dashboard.chart_performance_distribution(), use_container_width=True)

    with chart_col4:
        st.info("The required charts include attrition, salary, and performance rating distribution.")

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

    st.subheader("Filtered Dataset Preview")
    st.dataframe(filtered_df.head())

    st.subheader("Filtered Dataset Size")
    st.write(f"Rows: {filtered_df.shape[0]}")
    st.write(f"Columns: {filtered_df.shape[1]}")

    with st.expander("Show Column Names"):
        st.write(list(filtered_df.columns))

    with st.expander("Show Missing Values by Column"):
        st.write(filtered_df.isnull().sum())

except FileNotFoundError:
    st.error(
        "Dataset file was not found. Make sure the CSV file is in the same folder as this Python file."
    )
