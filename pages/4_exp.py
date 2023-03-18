import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime as dt
import snowflake.connector as sf
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import matplotlib.pyplot as plt
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

distinct_year_query = "select d_year from date_dim where d_year between 2000 and 2023;"
distinct_year = pd.read_sql_query(distinct_year_query, engine)['d_year'].unique().tolist()
year = st.selectbox('Year', distinct_year)

gender = st.selectbox('Gender', ['M', 'F'])
marital_status =st.selectbox('Marital Status', ['S', 'U','D','M','W']) 
distinct_education_status_query = "select distinct cd_education_status from customer_demographics;"
distinct_education_status = pd.read_sql_query(distinct_education_status_query, engine)['cd_education_status'].tolist()

# create a dropdown for the education status parameter with the distinct education status values
education_status = st.selectbox('Education Status', distinct_education_status)

query = """select  i_item_id, 
        avg(cs_quantity) agg1,
        avg(cs_list_price) agg2,
        avg(cs_coupon_amt) agg3,
        avg(cs_sales_price) agg4 
 from catalog_sales, customer_demographics, date_dim, item, promotion
 where cs_sold_date_sk = d_date_sk and
       cs_item_sk = i_item_sk and
       cs_bill_cdemo_sk = cd_demo_sk and
       cs_promo_sk = p_promo_sk and
       cd_gender = '{}' and 
       cd_marital_status = '{}' and
       cd_education_status = '{}' and
       (p_channel_email = 'N' or p_channel_event = 'N') and
       d_year = {} group by i_item_id order by i_item_id limit 10""".format(gender,marital_status,education_status,year)

df = pd.read_sql_query(query, engine)
df.rename(columns=str.lower, inplace=True)
##st.dataframe(df)

# rename the columns to lowercase
df.rename(columns=str.lower, inplace=True)

# sort the dataframe by agg2 in descending order
df= df.sort_values('agg2', ascending=True)

# create a bar chart
fig, ax = plt.subplots()
ax.barh(df['i_item_id'], df['agg2'],label='List')
ax.barh(df['i_item_id'], df['agg4'],label='Sale')
ax.set_title('AVG List and Sale Price by Product')
ax.set_ylabel('Product')
ax.set_xlabel('AVG List and Sale')
ax.legend()

# display the chart in Streamlit
st.pyplot(fig)



query="""select  *
from (select avg(ss_list_price) B1_LP
            ,count(ss_list_price) B1_CNT
            ,count(distinct ss_list_price) B1_CNTD
      from store_sales
      where ss_quantity between 0 and 5
        and (ss_list_price between 8 and 8+10 
             or ss_coupon_amt between 459 and 459+1000
             or ss_wholesale_cost between 57 and 57+20)) B1,
     (select avg(ss_list_price) B2_LP
            ,count(ss_list_price) B2_CNT
            ,count(distinct ss_list_price) B2_CNTD
      from store_sales
      where ss_quantity between 6 and 10
        and (ss_list_price between 90 and 90+10
          or ss_coupon_amt between 2323 and 2323+1000
          or ss_wholesale_cost between 31 and 31+20)) B2,
     (select avg(ss_list_price) B3_LP
            ,count(ss_list_price) B3_CNT
            ,count(distinct ss_list_price) B3_CNTD
      from store_sales
      where ss_quantity between 11 and 15
        and (ss_list_price between 142 and 142+10
          or ss_coupon_amt between 12214 and 12214+1000
          or ss_wholesale_cost between 79 and 79+20)) B3,
     (select avg(ss_list_price) B4_LP
            ,count(ss_list_price) B4_CNT
            ,count(distinct ss_list_price) B4_CNTD
      from store_sales
      where ss_quantity between 16 and 20
        and (ss_list_price between 135 and 135+10
          or ss_coupon_amt between 6071 and 6071+1000
          or ss_wholesale_cost between 38 and 38+20)) B4,
     (select avg(ss_list_price) B5_LP
            ,count(ss_list_price) B5_CNT
            ,count(distinct ss_list_price) B5_CNTD
      from store_sales
      where ss_quantity between 21 and 25
        and (ss_list_price between 122 and 122+10
          or ss_coupon_amt between 836 and 836+1000
          or ss_wholesale_cost between 17 and 17+20)) B5,
     (select avg(ss_list_price) B6_LP
            ,count(ss_list_price) B6_CNT
            ,count(distinct ss_list_price) B6_CNTD
      from store_sales
      where ss_quantity between 26 and 30
        and (ss_list_price between 154 and 154+10
          or ss_coupon_amt between 7326 and 7326+1000
          or ss_wholesale_cost between 7 and 7+20)) B6
 limit 100;"""

df = pd.read_sql_query(query, engine)
df.rename(columns=str.lower, inplace=True)
st.dataframe(df)

# rename the columns to lowercase
df.rename(columns=str.lower, inplace=True)


