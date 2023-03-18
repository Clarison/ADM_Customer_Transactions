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

st.write("""List counties where the percentage growth in web sales is consistently higher compared to the percentage
growth in store sales in the first three consecutive quarters for a given year.""")

# get user input for year

distinct_year_query1 = "select d_year from date_dim where d_year between 1999 and 2023;"
distinct_year1 = pd.read_sql_query(distinct_year_query1, engine)['d_year'].unique().tolist()
year1 = st.selectbox('Year', distinct_year1)

query1="""with ss as
 (select ca_county,d_qoy, d_year,sum(ss_ext_sales_price) as store_sales
 from store_sales,date_dim,customer_address
 where ss_sold_date_sk = d_date_sk
  and ss_addr_sk=ca_address_sk
 group by ca_county,d_qoy, d_year),
 ws as
 (select ca_county,d_qoy, d_year,sum(ws_ext_sales_price) as web_sales
 from web_sales,date_dim,customer_address
 where ws_sold_date_sk = d_date_sk
  and ws_bill_addr_sk=ca_address_sk
 group by ca_county,d_qoy, d_year)
 select 
        ss1.ca_county
       ,ss1.d_year
       ,ws2.web_sales/ws1.web_sales web_q1_q2_increase
       ,ss2.store_sales/ss1.store_sales store_q1_q2_increase
       ,ws3.web_sales/ws2.web_sales web_q2_q3_increase
       ,ss3.store_sales/ss2.store_sales store_q2_q3_increase
 from
        ss ss1
       ,ss ss2
       ,ss ss3
       ,ws ws1
       ,ws ws2
       ,ws ws3
 where
    ss1.d_qoy = 1
    and ss1.d_year = '{}'
    and ss1.ca_county = ss2.ca_county
    and ss2.d_qoy = 2
    and ss2.d_year = '{}'
 and ss2.ca_county = ss3.ca_county
    and ss3.d_qoy = 3
    and ss3.d_year = '{}'
    and ss1.ca_county = ws1.ca_county
    and ws1.d_qoy = 1
    and ws1.d_year = '{}'
    and ws1.ca_county = ws2.ca_county
    and ws2.d_qoy = 2
    and ws2.d_year = '{}'
    and ws1.ca_county = ws3.ca_county
    and ws3.d_qoy = 3
    and ws3.d_year ='{}'
    and case when ws1.web_sales > 0 then ws2.web_sales/ws1.web_sales else null end 
       > case when ss1.store_sales > 0 then ss2.store_sales/ss1.store_sales else null end
    and case when ws2.web_sales > 0 then ws3.web_sales/ws2.web_sales else null end
       > case when ss2.store_sales > 0 then ss3.store_sales/ss2.store_sales else null end
 order by ss1.ca_county;""".format(year1)

df1 = pd.read_sql_query(query1, engine)
df1.rename(columns=str.lower, inplace=True)
st.dataframe(df1)


