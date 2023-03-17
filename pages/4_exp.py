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

df = pd.read_sql_query("""with customer_total_return as
 (select wr_returning_customer_sk as ctr_customer_sk
        ,ca_state as ctr_state, 
 sum(wr_return_amt) as ctr_total_return
 from web_returns
     ,date_dim
     ,customer_address
 where wr_returned_date_sk = d_date_sk 
   and d_year =2002
   and wr_returning_addr_sk = ca_address_sk 
 group by wr_returning_customer_sk
         ,ca_state)
  select  c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
       ,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
       ,c_last_review_date,ctr_total_return
 from customer_total_return ctr1
     ,customer_address
     ,customer
 where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
 from customer_total_return ctr2 
  where ctr1.ctr_state = ctr2.ctr_state)
       and ca_address_sk = c_current_addr_sk
       and ca_state = 'GA'
       and ctr1.ctr_customer_sk = c_customer_sk
 order by c_customer_id,c_salutation,c_first_name,c_last_name,c_preferred_cust_flag
                  ,c_birth_day,c_birth_month,c_birth_year,c_birth_country,c_login,c_email_address
                  ,c_last_review_date,ctr_total_return
 limit 100""", engine)
df.rename(columns=str.lower, inplace=True)
st.dataframe(df)


