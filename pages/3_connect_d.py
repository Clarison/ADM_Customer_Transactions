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


st.write("query 26")
df = pd.read_sql_query("""select  i_item_id, avg(cs_quantity) agg1,avg(cs_list_price) agg2,avg(cs_coupon_amt) agg3,avg(cs_sales_price) agg4 
                       from catalog_sales,customer_demographics, date_dim, item, promotion where cs_sold_date_sk = d_date_sk and cs_item_sk = i_item_sk 
                       and cs_bill_cdemo_sk = cd_demo_sk and cs_promo_sk = p_promo_sk and cd_gender = 'M' and cd_marital_status = 'S' 
                       and cd_education_status = 'College' and (p_channel_email = 'N' or p_channel_event = 'N') and d_year = 2000
                       group by i_item_id order by i_item_id limit 100;""", engine)
df.rename(columns=str.lower, inplace=True)
st.dataframe(df)


# define the parameters
gender = st.selectbox('Gender', ['M', 'F'])
marital_status =st.selectbox('Marital Status', ['S', 'U','D','M','W']) 

# create a dropdown for the year parameter with values from 1990 to 2023
years = list(range(1990, 2024))
year = st.selectbox('Year', years)


# get the distinct education status values from the database
distinct_education_status_query = "select distinct cd_education_status from customer_demographics;"
distinct_education_status = pd.read_sql_query(distinct_education_status_query, engine)['cd_education_status'].tolist()

# create a dropdown for the education status parameter with the distinct education status values
education_status = st.selectbox('Education Status', distinct_education_status)

# get the distinct state values from the database
distinct_states_query = "select distinct s_state from store;"
distinct_states = pd.read_sql_query(distinct_states_query, engine)['s_state'].tolist()

# create a dropdown for the state parameter with the distinct state values
state = st.selectbox('State', distinct_states)

# define the SQL query with the parameters
query = """
    select i_item_id,
        s_state,
        avg(ss_quantity) agg1,
        avg(ss_list_price) agg2,
        avg(ss_coupon_amt) agg3,
        avg(ss_sales_price) agg4
    from store_sales, customer_demographics, date_dim, store, item
    where ss_sold_date_sk = d_date_sk
        and ss_item_sk = i_item_sk
        and ss_store_sk = s_store_sk
        and ss_cdemo_sk = cd_demo_sk
        and cd_gender = '{}'
        and cd_marital_status = '{}'
        and cd_education_status = '{}'
        and d_year = {}
        and s_state = '{}'
    group by i_item_id, s_state
    order by agg1 desc
    limit 10;
""".format(gender, marital_status, education_status, year, state)

# execute the query and fetch the results
df = pd.read_sql_query(query, engine)

# rename the columns to lowercase
df.rename(columns=str.lower, inplace=True)



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



st.write("query 28")

df = pd.read_sql_query("""select  *
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
 limit 100;""", engine)
df.rename(columns=str.lower, inplace=True)
st.dataframe(df)


st.write("query 29")

df = pd.read_sql_query("""select   
     i_item_id
    ,i_item_desc
    ,s_store_id
    ,s_store_name
    ,sum(ss_quantity)        as store_sales_quantity
    ,sum(sr_return_quantity) as store_returns_quantity
    ,sum(cs_quantity)        as catalog_sales_quantity
 from
    store_sales
   ,store_returns
   ,catalog_sales
   ,date_dim             d1
   ,date_dim             d2
   ,date_dim             d3
   ,store
   ,item
 where
     d1.d_moy               = 9 
 and d1.d_year              = 1999
 and d1.d_date_sk           = ss_sold_date_sk
 and i_item_sk              = ss_item_sk
 and s_store_sk             = ss_store_sk
 and ss_customer_sk         = sr_customer_sk
 and ss_item_sk             = sr_item_sk
 and ss_ticket_number       = sr_ticket_number
 and sr_returned_date_sk    = d2.d_date_sk
 and d2.d_moy               between 9 and  9 + 3 
 and d2.d_year              = 1999
 and sr_customer_sk         = cs_bill_customer_sk
 and sr_item_sk             = cs_item_sk
 and cs_sold_date_sk        = d3.d_date_sk     
 and d3.d_year              in (1999,1999+1,1999+2)
 group by
    i_item_id
   ,i_item_desc
   ,s_store_id
   ,s_store_name
having
sum(sr_return_quantity) > 1
order by
    sum(sr_return_quantity) desc
  limit 10;""", engine)
df.rename(columns=str.lower, inplace=True)
st.dataframe(df)

# create a bar chart
fig, ax = plt.subplots()
ax.bar(df['i_item_id'], df['store_sales_quantity'],label='sales')
ax.bar(df['i_item_id'], df['store_returns_quantity'], bottom=df['store_sales_quantity'],label='returns')
ax.bar(df['i_item_id'], df['catalog_sales_quantity'],bottom=df['store_sales_quantity']+df['store_returns_quantity'],label='repurchase')
ax.set_title('Purchase Return by Product')
ax.set_xlabel('Product')
ax.set_ylabel('Purchase Return')
ax.legend()

# rotate the y-axis label
ax.tick_params(axis='y', labelrotation=0)

# display the chart in Streamlit
st.pyplot(fig)

st.write("query 34")

df = pd.read_sql_query("""select c_last_name
       ,c_first_name
       ,c_salutation
       ,c_preferred_cust_flag
       ,ss_ticket_number
       ,cnt from
   (select ss_ticket_number
          ,ss_customer_sk
          ,count(*) cnt
    from store_sales,date_dim,store,household_demographics
    where store_sales.ss_sold_date_sk = date_dim.d_date_sk
    and store_sales.ss_store_sk = store.s_store_sk  
    and store_sales.ss_hdemo_sk = household_demographics.hd_demo_sk
    and (date_dim.d_dom between 1 and 3 or date_dim.d_dom between 25 and 28)
    and (household_demographics.hd_buy_potential = '>10000' or
         household_demographics.hd_buy_potential = 'Unknown')
    and household_demographics.hd_vehicle_count > 0
    and (case when household_demographics.hd_vehicle_count > 0 
	then household_demographics.hd_dep_count/ household_demographics.hd_vehicle_count 
	else null 
	end)  > 1.2
    and date_dim.d_year in (1999,1999+1,1999+2)
    and store.s_county in ('Williamson County','Williamson County','Williamson County','Williamson County',
                           'Williamson County','Williamson County','Williamson County','Williamson County')
    group by ss_ticket_number,ss_customer_sk) dn,customer
    where ss_customer_sk = c_customer_sk
      and cnt between 15 and 20
    order by c_last_name,c_first_name,c_salutation,c_preferred_cust_flag desc, ss_ticket_number;""", engine)
df.rename(columns=str.lower, inplace=True)
st.dataframe(df)


