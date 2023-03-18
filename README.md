# TDCS Dataset 

Assignment 3

Part 1:

Objectives:
Connect Snowflake SQLAlchemy to Streamlit. 
Extract insights from the queries from here
Convert queries to run dynamically
Publish the insights on Streamlit.

References:
https://docs.snowflake.com/en/user-guide/sqlalchemy
https://github.com/snowflakedb/snowflake-sqlalchemy
https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-ds_v2.5.0.pdf
https://github.com/Snowflake-Labs/snowpark-python-demos/tree/main/tpcds-customer-lifetime-value

Team:
Clarison James Dsilva
Alekya Kastury

Queries: 
Computes the average quantity, list price, discount, sales price for promotional items sold through the catalog channel where the promotion was not offered by mail or in an event for given gender, marital status and educational status.

 Find customers and their detailed customer data who have returned items, which they bought on the web, for an amount that is 20% higher than the average amount a customer returns in a given state in a given time period across all items. Order the output by customer data.

For all items sold in stores located in six states during a given year, find the average quantity, average list price, average list sales price, average coupon amount for a given gender, marital status, education and customer demographic

Get all items that were sold in stores in a specific month and year and which were returned in the next six months of the same year and re-purchased by the returning customer afterward through the catalog sales channel in the following three years. For those these items, compute the total quantity sold through the store, the quantity returned and the quantity purchased through the catalog. Group this information by item and store.

Display all customers with specific buy potentials and whose dependent count to vehicle count ratio is larger than 1.2, who in three consecutive years made purchases with between 15 and 20 items in the beginning or the end of each month in stores located in 8 counties.

Dataflow:

![alt text](https://github.com/Clarison/ADM_Customer_Transactions/blob/main/ss5.JPG)



Outputs:

![alt text](https://github.com/Clarison/ADM_Customer_Transactions/blob/main/MicrosoftTeams-image%20(1).png)

![alt text](https://github.com/Clarison/ADM_Customer_Transactions/blob/main/MicrosoftTeams-image.png)

![alt text](https://github.com/Clarison/ADM_Customer_Transactions/blob/main/ss3.JPG)

![alt text](https://github.com/Clarison/ADM_Customer_Transactions/blob/main/ss4.JPG)


https://clarison-adm-customer-transac-hufty-bikes-customer-trans-kuc2yv.streamlit.app/TPCDS_dataset

https://clarison-adm-customer-transac-hufty-bikes-customer-trans-kuc2yv.streamlit.app/TPCDS_dataset_2


