import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime as dt
import snowflake.connector as sf
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

#trying chemy

engine = create_engine(URL(
    account = 'wh80921.us-east-2.aws',
    user = 'clarison',
    password = '23301631cD*',
    database = 'SNOWFLAKE_SAMPLE_DATA',
    schema = 'TPCDS_SF10TCL',
    warehouse = 'compute_wh'
))


# The code below is for the title and logo for this page.
st.set_page_config(page_title="TPCDS dataset", page_icon="🚲")


st.title("TPCDS dataset")

st.write("")


st.write("""Query 26: Computes the average quantity, list price, discount, sales price for promotional items sold through the catalog
channel where the promotion was not offered by mail or in an event for given gender, marital status and
educational status.""")

df_item=pd.read_sql_query("select d_year from date_dim where d_year between 2000 and 2023",engine)

st.sidebar.header("Please Filter Here:")
year = st.sidebar.multiselect(
    "Select the Year:",
    options=df_item["d_year"].unique().tolist(),
    default=df_item["d_year"].unique())

st.write('You selected:', year)


df = pd.read_sql_query("""select  i_item_id, 
        avg(cs_quantity) agg1,
        avg(cs_list_price) agg2,
        avg(cs_coupon_amt) agg3,
        avg(cs_sales_price) agg4 
 from catalog_sales, customer_demographics, date_dim, item, promotion
 where cs_sold_date_sk = d_date_sk and
       cs_item_sk = i_item_sk and
       cs_bill_cdemo_sk = cd_demo_sk and
       cs_promo_sk = p_promo_sk and
       cd_gender = 'M' and 
       cd_marital_status = 'S' and
       cd_education_status = 'College' and
       (p_channel_email = 'N' or p_channel_event = 'N') and
       d_year = 2000 group by i_item_id order by i_item_id limit 100""", engine)
df.rename(columns=str.lower, inplace=True)
st.dataframe(df)

fig, ax = plt.subplots()
ax.bar(df['i_item_id'], df['agg2'],label='List')
ax.bar(df['i_item_id'], df['agg4'],label='Sale')
ax.set_title('Email promotion and Sales')
ax.set_xlabel('Email promotion')
ax.set_ylabel('AVG List and Sale')
ax.legend()

# rotate the y-axis label
ax.tick_params(axis='y', labelrotation=0)

# display the chart in Streamlit
st.pyplot(fig)
