import urllib.request


import numpy as np
import pandas as pd

import requests
import streamlit as st


from streamlit_lottie import st_lottie


st.set_page_config(page_title="Hufty Bikes Analysis App", layout="wide")
st.title("Analyzing of Hufty Bikes")
st.markdown(
        "Hey there! Welcome to Clarison's Hufty Bikes Analysis App. will add despription here ")


row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

data = pd.read_excel('KPMG_VI_New_raw_data_update_final.xlsx', sheet_name= "NewCustomerList", header =1 )


with row3_1:
    st.subheader("Customer State")
    fig = px.bar(
        data,
        x="State",
        y="Number of Customers",
        title="Number of Customers by State",
        color_discrete_sequence=["#9EE6CF"],
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                

with row3_2:
    st.subheader("Book Age")


row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row4_1:
    st.subheader("How Do You Rate Your Reads?")

with row4_2:
    st.subheader("How do Goodreads Users Rate Your Reads?")


row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)
with row5_1:
    st.subheader("Book Length Distribution")

with row5_2:
    st.subheader("How Quickly Do You Read?")


row6_space1, row6_1, row6_space2, row6_2, row6_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row6_1:
    st.subheader("Gender Breakdown")


with row6_2:
    st.subheader("Gender Distribution Over Time")


st.markdown(
        "For one last bit of analysis, we scraped a few hundred book lists from famous thinkers in technology, media, and government (everyone from Barack and Michelle Obama to Keith Rabois and Naval Ravikant). We took your list of books read and tried to recommend one of their lists to book through based on information we gleaned from your list"
    )
st.markdown("***")
st.markdown(
        "Thanks for going through this mini-analysis with me! I'd love feedback on this, so if you want to reach out you can find me on [twitter](https://twitter.com/tylerjrichards) or my [website](http://www.tylerjrichards.com/)."
    )
        
