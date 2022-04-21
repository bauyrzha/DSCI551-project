#import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google.cloud import firestore
from PIL import Image

#Setting up our homepage window of Streamlit app
def main():
    page = st.sidebar.selectbox(
        "Select a Page",
        [
            "Homepage",
            "Crime LA",
            "Food LA",
            "Education LA"
        ]
    )
    
    #First Page
    if page == "Homepage":
        homepage()
    #Crime LA Page
    if page == "Crime LA":
        crime()
    #Food LA Page
    if page == "Food LA":
        food()
    #Education LA Page
    if page == "Education LA":
        education()

def homepage():
    st.write("""
        # Social Inequality Across LA County
        #### ***Topic:*** This project will examine inequalities in regions of Los Angeles based on crime rates, access to food, and access to quality education. 
        ###### The app are made by _**Yerkebulan B., Soumeya K., Zihao H.**_
        #""")
    image = Image.open('homepage.jpg')
    st.image(image, caption='Original Map of Los Angeles Country')

def crime():
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
    def checkbox(data):
        if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(data)
    def hist(data):
        st.subheader('Number of crimes by hour')
        hist_values = np.histogram(
        data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
        st.bar_chart(hist_values)
    def zip_plot(data):
        # use count() and sort()
        data1 = data.groupby(['zipcode'])['dr_no'].count().reset_index(name='Count').sort_values(['Count'], ascending=False)
        # in context of zipcode            
        st.subheader('Number of crimes in context of zipcodes')        
        fig = plt.figure(figsize=(9, 6))
        plt.bar(data1['zipcode'], data1['Count'])
        plt.xlabel("ZipCode")
        plt.ylabel("Number of Crimes")
        st.pyplot(fig)
    def maps(data):
        hour_to_filter = st.slider('hour', 0, 23, 20)  # min: 0h, max: 23h, default: 20h
        filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
        st.subheader(f'Map of all crimes at %s:00' % hour_to_filter)
        st.map(filtered_data)
    def top10_zip(data):
        # use count() and sort()
        data1 = data.groupby(['zipcode'])['dr_no'].count().reset_index(name='Count').sort_values(['Count'], ascending=False)
        if st.checkbox('Show top 10 crimest zipcodes'):
            st.subheader('Top 10 crimest zipcodes')
            st.write(data1.head(10))
    def top10_less_zip(data):
        # use count() and sort()
        data1 = data.groupby(['zipcode'])['dr_no'].count().reset_index(name='Count').sort_values(['Count'], ascending=True)
        if st.checkbox('Show top 10 safest zipcodes'):
            st.subheader('Top 10 the safest zipcodes')
            st.write(data1.head(10))
    def top10_crime(data):
        # use count() and sort()
        data2 = data.groupby(['crm cd desc'])['dr_no'].count().reset_index(name='Count').sort_values(['Count'], ascending=False)
        if st.checkbox('Show top 10 crimes'):
            st.subheader('Top 10 crimes')
            st.write(data2.head(10))
    def top10_rare_crime(data):
        # use count() and sort()
        data2 = data.groupby(['crm cd desc'])['dr_no'].count().reset_index(name='Count').sort_values(['Count'], ascending=True)
        if st.checkbox('Show top 10 rare crimes'):
            st.subheader('Top 10 rare crimes')
            st.write(data2.head(10))
    def victim_sex(data):
        if st.checkbox('Show number of crimes in context of victim sex'):
            # victim sex
            data3 = data[data['vict sex'] != 'H']
            data3 = data3.groupby(['vict sex'])['dr_no'].count().reset_index(name='Count').sort_values(['Count'], ascending=False)
            # in context of victim sex            
            st.subheader('Number of crimes by victim sex')        
            fig = plt.figure(figsize=(9, 6))
            plt.bar(data3['vict sex'], data3['Count'])
            plt.xlabel("victim sex")
            plt.ylabel("Number of Crimes")
            Gender=['M - Male F - Female X - Unknown']
            plt.legend(Gender,loc=1) 
            st.pyplot(fig)
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load all rows of data into the dataframe.
    data = load_data()
    # Notify the reader that the data was successfully loaded.
    data_load_state.text("Done! (using cache)")
    number = st.text_input('Insert a number of ZipCode or type/check "ALL" to see all crimes in LA county')
    try:
        listo = data['zipcode'].to_list()
        if number == 'ALL' or number == '"ALL"' or number == 'all' or number == '"all"' or st.checkbox('ALL'):
            checkbox(data)
            hist(data)
            zip_plot(data)
            maps(data)
            top10_zip(data)
            top10_less_zip(data)
            top10_crime(data)
            top10_rare_crime(data)
            victim_sex(data)
        elif int(number) in listo:
            data=data[data['zipcode'] == int(number)]
            checkbox(data)
            hist(data)
            maps(data)
            top10_crime(data)
            top10_rare_crime(data)
            victim_sex(data)
        else:
            st.write('Inserted number of ZipCode is not found')
    except:
        st.write('Enter please 5 main digits of ZipCode')

def food():
    st.write('Soumeya, write your code under def food() in main.py')
    
def education():
    st.write('Zihao, write your code under def education() in main.py')

        
#driver code
if __name__ == "__main__":
    main()
