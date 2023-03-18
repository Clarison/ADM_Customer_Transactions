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

st.write("""Compute the total discounted amount for a particular manufacturer in a particular 90 day period for catalog
sales whose discounts exceeded the average discount by at least 30%.""")

# get user input for year

distinct_date_query1 = "select d_date from date_dim;"
distinct_date1 = pd.read_sql_query(distinct_date_query1, engine)['d_year'].unique().tolist()
date1 = st.selectbox('Year', distinct_date1)

manufacture_id_query1 = "select i_manufact_id from item;"
distinct_manufacture_id = pd.read_sql_query(manufacture_id_query1, engine)['i_manufact_id'].unique().tolist()
manufacture_id = st.selectbox('Year', distinct_manufacture_id) 

query1="""select  sum(cs_ext_discount_amt)  as excess_discount_amount
from 
   catalog_sales 
   ,item 
   ,date_dim
where
i_manufact_id = {}
and i_item_sk = cs_item_sk 
and d_date between '{}' and 
        date_add(cast('{}' as date), 90 )
and d_date_sk = cs_sold_date_sk 
and cs_ext_discount_amt  
     > ( 
         select 
            1.3 * avg(cs_ext_discount_amt) 
         from 
            catalog_sales 
           ,date_dim
         where 
              cs_item_sk = i_item_sk 
          and d_date between '{}' and
                             date_add(cast('{}' as date), 90 )
          and d_date_sk = cs_sold_date_sk 
      ) 
 limit 100;""".format(date1,manufacture_id)

df1 = pd.read_sql_query(query1, engine)
df1.rename(columns=str.lower, inplace=True)
st.dataframe(df1)


