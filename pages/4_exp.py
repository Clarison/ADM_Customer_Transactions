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


st.write("""Computes the average quantity, list price, discount, sales price for promotional items sold through the catalog
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

st.write("""What is the monthly sales figure based on extended price for a specific month in a specific year, for
manufacturers in a specific category in a given time zone. Group sales by manufacturer identifier and sort
output by sales amount, by channel, and give Total sales.
""")

# get user input for year

# get user input for month and year and offset
ca_gmt_offset = st.number_input('Enter the offset', min_value=-10, max_value=-5)

year = st.number_input('Enter a year', min_value=1998, max_value=2023)
month = st.number_input('Enter a month', min_value=1, max_value=12)

d_category = pd.read_sql_query("select i_category from item", engine)['i_category'].unique().tolist()
category = st.selectbox('Category', d_category)

query1="""with ss as (
 select
          i_manufact_id,sum(ss_ext_sales_price) total_sales 
 from
 	store_sales,
 	date_dim,
         customer_address,
         item
 where
         i_manufact_id in (select
  i_manufact_id
from
 item
where i_category in ('{category}'))
 and     ss_item_sk              = i_item_sk
 and     ss_sold_date_sk         = d_date_sk
 and     d_year                  = {year}
 and     d_moy                   = {month}
 and     ss_addr_sk              = ca_address_sk
 and     ca_gmt_offset           = {ca_gmt_offset}
 group by i_manufact_id),
 cs as (
 select
          i_manufact_id,sum(cs_ext_sales_price) total_sales
 from
 	catalog_sales,
 	date_dim,
         customer_address,
         item
 where
         i_manufact_id               in (select
  i_manufact_id
from
 item
where i_category in ('{category}'))
 and     cs_item_sk              = i_item_sk
 and     cs_sold_date_sk         = d_date_sk
 and     d_year                  = {year}
 and     d_moy                   = {month}
 and     cs_bill_addr_sk         = ca_address_sk
 and     ca_gmt_offset           = {ca_gmt_offset}
 group by i_manufact_id),
 ws as (
 select
          i_manufact_id,sum(ws_ext_sales_price) total_sales
 from
 	web_sales,
 	date_dim,
         customer_address,
         item
 where
         i_manufact_id               in (select
  i_manufact_id
from
 item
where i_category in ('{category}'))
 and     ws_item_sk              = i_item_sk
 and     ws_sold_date_sk         = d_date_sk
 and     d_year                  = {year}
 and     d_moy                   = {month}
 and     ws_bill_addr_sk         = ca_address_sk
 and     ca_gmt_offset           = {ca_gmt_offset}
 group by i_manufact_id)
  select  i_manufact_id ,sum(total_sales) total_sales
 from  (select * from ss 
        union all
        select * from cs 
        union all
        select * from ws) tmp1
 group by i_manufact_id
 order by total_sales
 limit 10;"""


df1 = pd.read_sql_query(query1, engine)
df1.rename(columns=str.lower, inplace=True)
st.dataframe(df1)

