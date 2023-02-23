import pandas as pd
import pandas_profiling
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import great_expectations as ge

from streamlit_pandas_profiling import st_profile_report

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

df = ge.read_excel(
        "pages/file.xlsx",
	engine="openpyxl" ,
        sheet_name="CustomerDemographic"
    )

df1 = ge.read_excel(
        "pages/file.xlsx",
        engine="openpyxl",
        sheet_name="Transactions",
	  header=1	
    )

df.expect_column_values_to_be_between("age", 0, 100)

validation_result = df.validate()

if validation_result["success"]:
    st.write("Data Validation Passed!")
else:
    st.error("Data Validation Failed but we fixed it :")
    mask = (df["age"] <= 100)
    df = df.loc[mask, :]
    st.warning("DataFrame after dropping columns where Age > 100:")
    


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
segment = st.sidebar.multiselect(
    "Select the Wealth Segment:",
    options=df["wealth_segment"].unique(),
    default=df["wealth_segment"].unique()
)

industry = st.sidebar.multiselect(
    "Select the Customer Job Industry:",
    options=df["job_industry_category"].unique(),
    default=df["job_industry_category"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

deceased = st.sidebar.multiselect(
    "Deceased:",
    options=df["deceased_indicator"].unique(),
    default=df["deceased_indicator"].unique()
)

df_selection = df.query(
    "wealth_segment == @segment & job_industry_category ==@industry & gender == @gender & deceased_indicator == @deceased"
)



st.title(":bar_chart: Customer Dashboard")
st.markdown("##")

# TOP KPI's
total_customers = int(df_selection["customer_id"].count())
average_tenure = round(df_selection["tenure"].mean(), 1)
average_sale_by_customer = round(df_selection["past_3_years_bike_related_purchases"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Customers:")
    st.subheader(f"{total_customers:,}")
with middle_column:
    st.subheader("Average Tenure:")
    st.subheader(f"{average_tenure}")
with right_column:
    st.subheader("Average Purchases Past Three Years:")
    st.subheader(f"{average_sale_by_customer}")

st.markdown("""---""")


# Customers BY Job Industry Category [BAR CHART]
sales_by_industry = (
    df_selection.groupby(by=["job_industry_category"]).count()[["customer_id"]].sort_values(by="customer_id")
)
fig_product_sales = px.bar(
    sales_by_industry,
    x="customer_id",
    y=sales_by_industry.index,
    orientation="h",
    title="<b>Customers by Industry Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_industry),
    template="plotly_white",
)




# Customers BY total purchases by wealth segments [BAR CHART]
sales_by_segments = (
    df_selection.groupby(by=["wealth_segment"]).sum()[["past_3_years_bike_related_purchases"]].sort_values(by="past_3_years_bike_related_purchases")
)
fig_product_segments = px.bar(
    sales_by_segments,
    x="past_3_years_bike_related_purchases",
    y=sales_by_segments.index,
    orientation="h",
    title="<b>Number of purchases by Wealth Segments</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_segments),
    template="plotly_white",
)


# Customers by owns car [BAR CHART]

owns_a_car = (
    df_selection.groupby(by=["owns_car"]).count()[["customer_id"]].sort_values(by="customer_id")
)
fig_car = px.bar(
    owns_a_car,
    x="customer_id",
    y=owns_a_car.index,
    orientation="h",
    title="<b>Number of Car Owners</b>",
    color_discrete_sequence=["#0083B8"] * len(owns_a_car),
    template="plotly_white"
)



left_column, mid_column, right_column = st.columns(3)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
mid_column.plotly_chart(fig_product_segments, use_container_width=True)
right_column.plotly_chart(fig_car, use_container_width=True)


#histogram by age

fig_age = px.histogram(df_selection,
	x="age",
	title="<b>Distribution by age</b>",
	color_discrete_sequence=["#0083B8"] ,
	template="plotly_white"
)



#histogram by tenure

fig_tenure = px.histogram(df_selection,
	x="tenure",
	title="<b>Distribution by tenure</b>",
	color_discrete_sequence=["#0083B8"] ,
	template="plotly_white"
)



#histogram by purchases

fig_purchases = px.histogram(df_selection,
	x="past_3_years_bike_related_purchases",
	title="<b>Distribution by number of Purchases</b>",
	color_discrete_sequence=["#0083B8"] ,
	template="plotly_white"
)



left_column, mid_column, right_column = st.columns(3)
left_column.plotly_chart(fig_age, use_container_width=True)
mid_column.plotly_chart(fig_tenure, use_container_width=True)
right_column.plotly_chart(fig_purchases, use_container_width=True)



pr = df_selection.profile_report()

st_profile_report(pr)



