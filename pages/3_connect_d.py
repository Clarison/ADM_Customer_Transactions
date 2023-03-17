import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime as dt
import snowflake.connector as sf



# Connect to Snowflake
conn = sf.connect(
    user='clarison',
    password='23301631cD*',
    account='wh80921.us-east-2.aws',
    warehouse='compute_wh',
    database='SNOWFLAKE_SAMPLE_DATA',
    schema='TPCDS_SF10TCL'
)


cur = conn.cursor()
cur.execute('SELECT top 20 * FROM customer')

# Fetch the results into a Pandas DataFrame
results = cur.fetchall()
df = pd.DataFrame(results, columns=[desc[0] for desc in cur.description])



# The code below is for the title and logo for this page.
st.set_page_config(page_title="Cohort Analysis on the Bikes dataset", page_icon="🚲")


st.title("Cohort Analysis → `Bikes` dataset")

st.write("")

df.rename(columns=str.lower, inplace=True)
st.dataframe(df)
