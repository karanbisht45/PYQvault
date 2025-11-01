import streamlit as st
import backend
import pandas as pd
import matplotlib.pyplot as plt

def show_dashboard():
    st.header("Analytics Dashboard")
    pyqs = backend.get_pyqs()
    if not pyqs:
        st.info("No data yet — upload some PYQs to see analytics.")
        return

    df = pd.DataFrame(pyqs)

    st.subheader("Basic stats")
    st.write(f"Total PYQs: {len(df)}")

    # Show a simple table of recent uploads
    st.subheader("Recent uploads")
    recent = df[["pyq_id", "title", "subject", "year", "university", "upload_date"]].head(10)
    st.dataframe(recent)

    # ---------- Top Subjects ----------
    st.subheader("Top subjects")
    subj = df["subject"].fillna("Unknown").value_counts().head(10)
    fig1, ax1 = plt.subplots()
    subj.plot(kind="bar", ax=ax1)
    ax1.set_xlabel("Subject")
    ax1.set_ylabel("Count")
    ax1.set_title("Top Subjects by Uploads")
    st.pyplot(fig1)

    # ---------- Year-wise Count ----------
    st.subheader("Year-wise count")
    year_counts = df["year"].fillna("Unknown").value_counts().sort_index()
    fig2, ax2 = plt.subplots()
    year_counts.plot(kind="line", marker="o", ax=ax2)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Number of PYQs")
    ax2.set_title("PYQs Uploaded per Year")
    st.pyplot(fig2)

    # ---------- Top Universities ----------
    st.subheader("Top universities")
    uni = df["university"].fillna("Unknown").value_counts().head(10)
    fig3, ax3 = plt.subplots()
    uni.plot(kind="bar", ax=ax3)
    ax3.set_xlabel("University")
    ax3.set_ylabel("Count")
    ax3.set_title("Top Universities by Uploads")
    st.pyplot(fig3)
