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


st.write("query 26")
df = pd.read_sql_query("select  i_item_id, avg(cs_quantity) agg1,avg(cs_list_price) agg2,avg(cs_coupon_amt) agg3,avg(cs_sales_price) agg4 from catalog_sales,customer_demographics, date_dim, item, promotion where cs_sold_date_sk = d_date_sk and cs_item_sk = i_item_sk and cs_bill_cdemo_sk = cd_demo_sk and cs_promo_sk = p_promo_sk and cd_gender = 'M' and cd_marital_status = 'S' and cd_education_status = 'College' and (p_channel_email = 'N' or p_channel_event = 'N') and d_year = 2000 group by i_item_id order by i_item_id limit 100;", engine)
df.rename(columns=str.lower, inplace=True)
st.dataframe(df)


st.write("query 27")
df = pd.read_sql_query("""select  i_item_id,
        s_state, grouping(s_state) g_state,
        avg(ss_quantity) agg1,
        avg(ss_list_price) agg2,
        avg(ss_coupon_amt) agg3,
        avg(ss_sales_price) agg4
 from store_sales, customer_demographics, date_dim, store, item
 where ss_sold_date_sk = d_date_sk and
       ss_item_sk = i_item_sk and
       ss_store_sk = s_store_sk and
       ss_cdemo_sk = cd_demo_sk and
       cd_gender = 'M' and
       cd_marital_status = 'S' and
       cd_education_status = 'College' and
       d_year = 2002 and
       s_state = 'TN'
 group by rollup(i_item_id, s_state)
 order by i_item_id
         ,s_state
  limit 100;""", engine)
df.rename(columns=str.lower, inplace=True)
st.dataframe(df)




df2 = pd.read_sql_query("SELECT  top 20 * FROM customer", engine)
st.dataframe(df2)
