
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Performance Analysis System")
st.write(
    "Analyze student marks, calculate grades, "
    "and visualize academic performance."
)


def grade_for(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    return "F"


if "records" not in st.session_state:
    st.session_state.records = []

st.subheader("📝 Enter Student Details")

with st.form("student_form", clear_on_submit=True):
    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")

    c1, c2, c3 = st.columns(3)

    with c1:
        python_marks = st.number_input(
            "Python Marks (out of 100)", 0, 100, 0
        )
    with c2:
        statistics_marks = st.number_input(
            "Statistics Marks (out of 100)", 0, 100, 0
        )
    with c3:
        ds_marks = st.number_input(
            "Data Science Marks (out of 100)", 0, 100, 0
        )

    submitted = st.form_submit_button(
        "➕ Add Student Record",
        use_container_width=True
    )

if submitted:
    name = name.strip()
    roll = roll.strip()

    if not name or not roll:
        st.error("Please enter both student name and roll number.")

    elif any(
        row["Roll Number"].casefold() == roll.casefold()
        for row in st.session_state.records
    ):
        st.warning("This roll number already exists.")

    else:
        total = int(python_marks + statistics_marks + ds_marks)
        percentage = round(total / 3, 2)
        grade = grade_for(percentage)

        st.session_state.records.append({
            "Student Name": name,
            "Roll Number": roll,
            "Python": int(python_marks),
            "Statistics": int(statistics_marks),
            "Data Science": int(ds_marks),
            "Total Marks": total,
            "Percentage": percentage,
            "Grade": grade
        })

        st.success(
            f"Record added successfully! "
            f"Percentage: {percentage}% | Grade: {grade}"
        )

st.divider()
st.subheader("📋 Student Records")

if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)

    search_text = st.text_input(
        "🔍 Search by student name or roll number"
    )

    if search_text.strip():
        mask = (
            df["Student Name"].str.contains(
                search_text.strip(), case=False, na=False
            )
            | df["Roll Number"].str.contains(
                search_text.strip(), case=False, na=False
            )
        )
        shown = df[mask]
    else:
        shown = df

    st.dataframe(
        shown,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📈 Class Dashboard")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Total Students", len(df))
    m2.metric("Class Average", f'{df["Percentage"].mean():.2f}%')
    m3.metric("Highest Percentage", f'{df["Percentage"].max():.2f}%')
    m4.metric("Passing Students", int((df["Percentage"] >= 40).sum()))

    st.subheader("📊 Student Performance Chart")

    fig, ax = plt.subplots()
    ax.bar(
        df["Student Name"] + " (" + df["Roll Number"] + ")",
        df["Percentage"]
    )
    ax.set_ylabel("Percentage")
    ax.set_ylim(0, 100)
    ax.set_title("Student-wise Performance")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("📚 Subject-wise Class Average")

    subjects = ["Python", "Statistics", "Data Science"]
    averages = [df[subject].mean() for subject in subjects]

    fig2, ax2 = plt.subplots()
    ax2.bar(subjects, averages)
    ax2.set_ylabel("Average Marks")
    ax2.set_ylim(0, 100)
    ax2.set_title("Average Marks by Subject")
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    st.subheader("🏆 Grade Distribution")

    grade_order = ["A+", "A", "B", "C", "D", "F"]
    grade_counts = (
        df["Grade"].value_counts()
        .reindex(grade_order, fill_value=0)
    )

    fig3, ax3 = plt.subplots()
    ax3.bar(grade_counts.index, grade_counts.values)
    ax3.set_xlabel("Grade")
    ax3.set_ylabel("Number of Students")
    ax3.set_title("Grade Distribution")
    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

    st.download_button(
        "⬇️ Download Student Data (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="student_performance.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("🗑️ Clear All Records"):
        st.session_state.records = []
        st.rerun()

else:
    st.info(
        "No student records yet. Add a student above "
        "to see the dashboard and charts."
    )

st.caption(
    "Student Performance Analysis System | "
    "Developed using Python, Streamlit, Pandas and Matplotlib. "
    "Records are temporary and may reset when the app session restarts."
    )
