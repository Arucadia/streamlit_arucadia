import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

COLOR_MAP = {
    "Need Further Observation": "#FFD501",
    "Don't Promote": "#FC4755",
    "Recommend for Promotion": "#23D000"
}


def map_promotion_recency(x):
    if x == 0:
        return "Promoted This Year"
    elif x == 1:
        return "1 Year Ago"
    elif 2 <= x <= 3:
        return "2–3 Years Ago"
    elif 4 <= x <= 5:
        return "4–5 Years Ago"
    elif x > 5:
        return "Over 5 Years Ago"
    else:
        return None

def hr_dashboard():

    BASE_DIR = Path(__file__).parent
    st.title("Employee Promotion Readiness Dashboard")

    df = pd.read_csv(BASE_DIR / "Dataset" / "hr_final.csv")
    seg = pd.read_csv(BASE_DIR / "Dataset" / "hr_segment.csv")


    df = df.merge(
        seg[["EmployeeID", "RFM_Segment", "F_Score", "M_Score"]],
        on="EmployeeID",
        how="left"
    )

    # SIDEBAR FILTER
    st.sidebar.header("Filters")

    dept = st.sidebar.multiselect(
        "Department",
        options=df["Department"].unique(),
        default=df["Department"].unique()
    )

    age_range = st.sidebar.slider(
        "Age Range",
        int(df["Age"].min()),
        int(df["Age"].max()),
        (25, 55)
    )

    df_f = df[
        (df["Department"].isin(dept)) &
        (df["Age"].between(age_range[0], age_range[1]))
    ]

    # KPI – READY FOR PROMOTION
    total_emp = len(df_f)
    ready_emp = (df_f["RFM_Segment"] == "Recommend for Promotion").sum()
    ready_pct = (ready_emp / total_emp) * 100 if total_emp > 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total Employee", total_emp)
    c2.metric("Ready for Promotion", f"{ready_pct:.1f}%")
    c3.metric("AVG Performance", round(df_f["PerformanceRating"].mean(), 2))
    c4.metric("AVG Monthly Income", f"{df_f['MonthlyIncome'].mean():,.0f}")
    c5.metric("AVG Age", round(df_f["Age"].mean(), 1))

    st.divider()

    # YEARS AT COMPANY (AREA)
    left, right = st.columns(2)

    with left:
        tenure = (
            df_f["YearsAtCompany"]
            .value_counts()
            .sort_index()
            .reset_index(name="Count")
            .rename(columns={"index": "YearsAtCompany"})
        )

        fig_area = px.area(
            tenure,
            x="YearsAtCompany",
            y="Count",
            title="Years of Employee Works Here"
        )
        st.plotly_chart(fig_area, use_container_width=True)

    # DONUT – RFM SEGMENT
    with right:
        rfm_dist = (
            df_f["RFM_Segment"]
            .value_counts()
            .reset_index(name="Count")
            .rename(columns={"index": "RFM_Segment"})
        )

        fig_donut = px.pie(
            rfm_dist,
            names="RFM_Segment",
            values="Count",
            hole=0.5,
            title="RFM Segment Distribution",
            color="RFM_Segment",
            color_discrete_map=COLOR_MAP
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # PROMOTION RECENCY BAR
    df_f["Promotion_Recency"] = df_f["YearsSinceLastPromotion"].apply(map_promotion_recency)

    recency_df = (
        df_f
        .groupby(["Promotion_Recency", "RFM_Segment"])
        .size()
        .reset_index(name="Count")
    )

    order_recency = [
        "Promoted This Year",
        "1 Year Ago",
        "2–3 Years Ago",
        "4–5 Years Ago",
        "Over 5 Years Ago"
    ]

    fig_recency = px.bar(
        recency_df,
        x="Count",
        y="Promotion_Recency",
        color="RFM_Segment",
        orientation="h",
        category_orders={"Promotion_Recency": order_recency},
        title="Promotion Readiness Since Last Promotion",
        color_discrete_map=COLOR_MAP
    )

    st.plotly_chart(fig_recency, use_container_width=True)

    st.divider()

    # SCATTER – INDIVIDUAL LEVEL
    left_s, right_s = st.columns(2)

    with left_s:
        fig_individual = px.scatter(
            df_f,
            x="F_Score",
            y="M_Score",
            color="RFM_Segment",
            title="Performance vs Value (Individual)",
            color_discrete_map=COLOR_MAP,
            hover_data=["EmployeeID", "MonthlyIncome"]
        )
        st.plotly_chart(fig_individual, use_container_width=True)

    # SCATTER – SEGMENT LEVEL
    with right_s:
        scatter_seg = (
            df_f
            .groupby("RFM_Segment")
            .agg(
                F_score_sum=("F_Score", "sum"),
                M_score_sum=("M_Score", "sum"),
                total_income=("MonthlyIncome", "sum")
            )
            .reset_index()
        )

        fig_segment = px.scatter(
            scatter_seg,
            x="F_score_sum",
            y="M_score_sum",
            size="total_income",
            color="RFM_Segment",
            title="Performance vs Value (Segment)",
            color_discrete_map=COLOR_MAP,
            labels={
                "F_score_sum": "Sum of F Score",
                "M_score_sum": "Sum of M Score",
                "total_income": "Total Monthly Income"
            }
        )
        st.plotly_chart(fig_segment, use_container_width=True)

    # DATA PREVIEW
    st.subheader("Employee Data Preview")
    st.dataframe(df_f.head(20))