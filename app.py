import streamlit as st
import pandas as pd

from main import main


st.set_page_config(
    page_title="Web Scraper",
    page_icon="🔎",
    layout="wide"
)


st.title("🔎 Web Scraping Application")
st.write(
    "Scrape, clean, validate and remove duplicate records "
    "from books and quotes sources."
)


if st.button("🚀 Start Scraping", type="primary"):

    try:

        with st.spinner("Scraping data... Please wait."):

            records, summary = main()

        st.success("Scraping completed successfully! 🎉")

        # -------------------------
        # SUMMARY
        # -------------------------

        st.subheader("📊 Scraping Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Books Scraped",
                summary["books"]["scraped"]
            )

        with col2:
            st.metric(
                "Quotes Scraped",
                summary["quotes"]["scraped"]
            )

        with col3:
            st.metric(
                "Duplicates Removed",
                summary["duplicates"]
            )

        with col4:
            st.metric(
                "Final Records",
                summary["final_records"]
            )

        st.write(
            f"⏱️ Duration: "
            f"{summary['duration_seconds']} seconds"
        )

        # -------------------------
        # DATA
        # -------------------------

        st.subheader("📋 Final Dataset")

        df = pd.DataFrame(records)

        st.dataframe(
            df,
            use_container_width=True
        )

        # -------------------------
        # DOWNLOAD CSV
        # -------------------------

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="final_dataset.csv",
            mime="text/csv"
        )

        # -------------------------
        # SUMMARY JSON
        # -------------------------

        import json

        json_data = json.dumps(
            summary,
            indent=4
        )

        st.download_button(
            label="📥 Download Summary JSON",
            data=json_data,
            file_name="summary_report.json",
            mime="application/json"
        )

    except Exception as error:

        st.error(
            f"Something went wrong: {error}"
        )