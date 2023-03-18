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




st.write("For all items sold in stores located in six states during a given year, find the average quantity, average list price,average list sales price, average coupon amount for a given gender, marital status, education and customer demographic")
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




st.write("Get all items that were sold in stores in a specific month and year and which were returned in the next six months of the same year and re-purchased by the returning customer afterwards through the catalog sales channel in the following three years. For those these items, compute the total quantity sold through the store, the quantity returned and the quantity purchased through the catalog. Group this information by item and store.")


# get user input for month and year
month = st.number_input('Enter a month (1-12)', min_value=1, max_value=12)
year = st.number_input('Enter a year', min_value=1999, max_value=2023)



# SQL query with parameters
query = f"""SELECT   
     i_item_id
    ,i_item_desc
    ,s_store_id
    ,s_store_name
    ,SUM(ss_quantity)        AS store_sales_quantity
    ,SUM(sr_return_quantity) AS store_returns_quantity
    ,SUM(cs_quantity)        AS catalog_sales_quantity
FROM
    store_sales
   ,store_returns
   ,catalog_sales
   ,date_dim             d1
   ,date_dim             d2
   ,date_dim             d3
   ,store
   ,item
WHERE
     d1.d_moy               = {month}
 AND d1.d_year              = {year}
 AND d1.d_date_sk           = ss_sold_date_sk
 AND i_item_sk              = ss_item_sk
 AND s_store_sk             = ss_store_sk
 AND ss_customer_sk         = sr_customer_sk
 AND ss_item_sk             = sr_item_sk
 AND ss_ticket_number       = sr_ticket_number
 AND sr_returned_date_sk    = d2.d_date_sk
 AND d2.d_moy               BETWEEN {month} AND {month} + 3
 AND d2.d_year              = {year}
 AND sr_customer_sk         = cs_bill_customer_sk
 AND sr_item_sk             = cs_item_sk
 AND cs_sold_date_sk        = d3.d_date_sk     
 AND d3.d_year              IN ({year},{year+1},{year+2})
GROUP BY
    i_item_id
   ,i_item_desc
   ,s_store_id
   ,s_store_name
HAVING
SUM(sr_return_quantity) > 1
ORDER BY
    SUM(sr_return_quantity) DESC
LIMIT 10;"""


# execute query and display results
df = pd.read_sql_query(query, engine)
df.rename(columns=str.lower, inplace=True)


# create a bar chart
fig, ax = plt.subplots()
ax.bar(df['i_item_id'], df['store_sales_quantity'],label='sales')
ax.bar(df['i_item_id'], df['store_returns_quantity'], bottom=df['store_sales_quantity'],label='returns')
ax.bar(df['i_item_id'], df['catalog_sales_quantity'],bottom=df['store_sales_quantity']+df['store_returns_quantity'],label='repurchase')
ax.set_title('Purchase Return by Product')
ax.set_xlabel('Product')
ax.set_ylabel('Purchase Return')
ax.legend()



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


# Connect to the database and get the list of distinct counties from the store table
distinct_counties = pd.read_sql_query('SELECT DISTINCT s_county FROM store', engine)['s_county'].tolist()

# Create a sidebar with a county parameter input widget
counties = st.multiselect('Select counties', distinct_counties)

# Define the SQL query with the county parameter placeholder
sql_query = """
SELECT c_last_name, c_first_name, c_salutation, c_preferred_cust_flag, ss_ticket_number, cnt 
FROM (
    SELECT ss_ticket_number, ss_customer_sk, COUNT(*) cnt
    FROM store_sales, date_dim, store, household_demographics
    WHERE store_sales.ss_sold_date_sk = date_dim.d_date_sk
        AND store_sales.ss_store_sk = store.s_store_sk  
        AND store_sales.ss_hdemo_sk = household_demographics.hd_demo_sk
        AND (date_dim.d_dom BETWEEN 1 AND 3 OR date_dim.d_dom BETWEEN 25 AND 28)
        AND (household_demographics.hd_buy_potential = '>10000' OR household_demographics.hd_buy_potential = 'Unknown')
        AND household_demographics.hd_vehicle_count > 0
        AND (
            CASE WHEN household_demographics.hd_vehicle_count > 0 
                THEN household_demographics.hd_dep_count / household_demographics.hd_vehicle_count 
                ELSE NULL 
            END
        ) > 1.2
        AND date_dim.d_year IN (1999, 2000, 2001)
        AND store.s_county IN %(counties)s -- parameterized WHERE clause with IN operator
    GROUP BY ss_ticket_number, ss_customer_sk
) dn, customer
WHERE ss_customer_sk = c_customer_sk
    AND cnt BETWEEN 15 AND 20
ORDER BY c_last_name, c_first_name, c_salutation, c_preferred_cust_flag DESC, ss_ticket_number;
"""

# Execute the query with the county parameter and display the resulting DataFrame
params = {'counties': tuple(counties)}
df = pd.read_sql_query(sql_query, engine, params=params)
st.dataframe(df)

