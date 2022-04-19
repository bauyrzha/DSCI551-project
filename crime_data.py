import streamlit as st
import pandas as pd
import numpy as np
st.title('Crime in LA')

DATE_COLUMN = 'date/time'
#DATA_URL = ('https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD')
DATA_URL = 'df_crime_modify.csv.gz'
@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load all rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

#option = st.selectbox(
#    'Which ZipCode do you choose?',
#     ('ALL', data['zipcode']))

#'You selected: ', option
number = st.text_input('Insert a number of ZipCode')
st.write('The current number is ', number)
try:
    listo = data['zipcode'].to_list()
    if  int(number) in listo:
        data=data[data['zipcode'] == int(number)]
        if st.checkbox('Show crimes for all zipcodes'):
            data = load_data()
        if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(data)
        st.subheader('Number of crimes by hour')
        hist_values = np.histogram(
            data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
        st.bar_chart(hist_values)
        hour_to_filter = st.slider('hour', 0, 23, 20)  # min: 0h, max: 23h, default: 20h
        filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
        st.subheader(f'Map of all crimes at %s:00' % hour_to_filter)
        st.map(filtered_data)
    else:
        st.write('Inserted number of ZipCode is not found')
except:
    st.write('Enter please 5 main digits of ZipCode')
