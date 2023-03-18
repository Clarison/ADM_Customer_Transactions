#Streamlit UI
st.title('Customer Life time Value Prediction')

st.text('')
csv_file = st.file_uploader(label='Upload CSV file with user data', type = 'csv')
