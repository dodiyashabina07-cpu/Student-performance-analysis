import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Analysis", page_icon="📊", layout="wide")
st.title("Student Performance Analysis System")
st.write("A simple Data Science project to calculate student results and visualize academic performance.")

def grade_for(percentage):
    if percentage >= 90: return "A+"
    if percentage >= 80: return "A"
    if percentage >= 70: return "B"
    if percentage >= 60: return "C"
    if percentage >= 40: return "D"
    return "F"

if "records" not in st.session_state:
    st.session_state.records = []

st.subheader("Enter Student Details")
with st.form("student_form", clear_on_submit=True):
    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")
    c1, c2, c3 = st.columns(3)
    with c1: python_marks = st.number_input("Python Marks (out of 100)", 0, 100, 0)
    with c2: statistics_marks = st.number_input("Statistics Marks (out of 100)", 0, 100, 0)
    with c3: ds_marks = st.number_input("Data Science Marks (out of 100)", 0, 100, 0)
    submitted = st.form_submit_button("Add Student Record")

if submitted:
    if not name.strip() or not roll.strip():
        st.error("Please enter the student name and roll number.")
    elif any(row["Roll Number"] == roll.strip() for row in st.session_state.records):
        st.warning("That roll number already exists.")
    else:
        total = int(python_marks + statistics_marks + ds_marks)
        percentage = round(total / 3, 2)
        st.session_state.records.append({
            "Student Name": name.strip(),
            "Roll Number": roll.strip(),
            "Python": int(python_marks),
            "Statistics": int(statistics_marks),
            "Data Science": int(ds_marks),
            "Total Marks": total,
            "Percentage": percentage,
            "Grade": grade_for(percentage)
        })
        st.success(f"Record added. Percentage: {percentage}% | Grade: {grade_for(percentage)}")

st.subheader("Student Records")
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    search_text = st.text_input("Search by name or roll number")
    if search_text.strip():
        shown = df[
            df["Student Name"].str.contains(search_text.strip(), case=False, na=False) |
            df["Roll Number"].str.contains(search_text.strip(), case=False, na=False)
        ]
    else:
        shown = df
    st.dataframe(shown, use_container_width=True, hide_index=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("Number of Students", len(df))
    m2.metric("Class Average", f'{df["Percentage"].mean():.2f}%')
    m3.metric("Highest Percentage", f'{df["Percentage"].max():.2f}%')

    st.subheader("Student Percentage Chart")
    fig, ax = plt.subplots()
    ax.bar(df["Student Name"], df["Percentage"])
    ax.set_ylabel("Percentage")
    ax.set_ylim(0, 100)
    ax.set_title("Student-wise Performance")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    st.pyplot(fig)

    st.subheader("Grade Distribution")
    grade_counts = df["Grade"].value_counts().sort_index()
    fig2, ax2 = plt.subplots()
    ax2.bar(grade_counts.index, grade_counts.values)
    ax2.set_xlabel("Grade")
    ax2.set_ylabel("Number of Students")
    fig2.tight_layout()
    st.pyplot(fig2)

    st.download_button(
        "Download Student Data (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="student_performance.csv",
        mime="text/csv"
    )
    if st.button("Clear All Records"):
        st.session_state.records = []
        st.rerun()
else:
    st.info("Add a student record above to display the analysis and charts.")

st.caption("Academic demonstration project. Records remain in the current app session and may reset when the session restarts.")
