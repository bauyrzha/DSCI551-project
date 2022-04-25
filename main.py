#import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import firebase_admin
from firebase_admin import credentials, firestore
import pydeck as pdk

#Setting up our homepage window of Streamlit app
def main():
    page = st.sidebar.selectbox(
        "Select a Page",
        [
            "Homepage",
            "Crime in LA",
            "Food in LA",
            "Education in LA",
            "Equity, Opportunity and Risk",
            "Additional Resources"
        ]
    )
    
    #First Page
    if page == "Homepage":
        homepage()
    #Crime LA Page
    if page == "Crime in LA":
        crime()
    #Food LA Page
    if page == "Food in LA":
        food()
    #Education LA Page
    if page == "Education in LA":
        education()
    #Equity and opportunity
    if page == "Equity, Opportunity and Risk":
        equity()
    #Additional Resources
    if page == "Additional Resources":
        resources()

def homepage():
    st.write("""
        # Social Inequality Across LA County
        #### This project examines inequalities in regions of Los Angeles County based on crime rates, access to food, and access to quality education. 
        ###### This app was created by _**Yerkebulan B., Zihao H., and Soumeya K.**_
        #""")
    try:
        image = Image.open('homepage.jpg')
        st.image(image, caption='Original Map of Los Angeles County')
    except:
        st.write('')

def crime():
    st.title('Crime in Los Angeles County')
    DATE_COLUMN = 'date/time'
    DATA_URL = 'df_crime_last.csv.gz'
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
        st.subheader('Number of crimes per zipcode')        
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
        if st.checkbox('Show top 10 highest crime zipcodes'):
            st.subheader('Top 10 highest crime zipcodes')
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
        if st.checkbox('Show number of crimes by victim sex'):
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
    number = st.text_input('Insert a ZipCode or type/check "ALL" to see all crimes in LA county')
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
            st.write('Inserted ZipCode is not found')
    except:
        st.write('Please enter 5 main digits of ZipCode')
    
def food():
    st.title('Food in Los Angeles County')
    if not firebase_admin._apps:
        cred = credentials.Certificate(st.secrets)
        app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    docs = db.collection(u'foodbanks_LA').stream()
    FOOD_DF = pd.DataFrame()
    for doc in docs:
        FOOD_DF = FOOD_DF.append(doc.to_dict(), ignore_index=True) 
    docs2 = db.collection(u'grocery_LA').stream()
    Grocery_DF = pd.DataFrame()
    for doc in docs2:
        Grocery_DF = Grocery_DF.append(doc.to_dict(), ignore_index=True)
    
    def load_data():
        data = FOOD_DF[['Food Bank Name', 'Address', 'Zip Code', 'Latitude', 'Longitude']]
        data[['Zip Code','Latitude', 'Longitude']] = data[['Zip Code','Latitude', 'Longitude']].apply(pd.to_numeric)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data.rename(columns={'zip code': 'zipcode'}, inplace=True)
        return data
    
    def load_data2():
        data = Grocery_DF[['Grocery Name','Address','zipcode','latitude','longitude']]
        data[['zipcode','latitude','longitude']] = data[['zipcode','latitude','longitude']].apply(pd.to_numeric)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        return data
    
    def checkbox(data, data2):
        if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write('Food bank information')
            st.write(data)
            st.write('Grocery information')
            st.write(data2)
            
    def maps(data):
        st.map(data)
            
    data_load_state = st.text('Loading data...')
    # Load all rows of data into the dataframe.
    data = load_data()
    data2 = load_data2()
    # Notify the reader that the data was successfully loaded.
    data_load_state.text("Done! (using cache)")
    number = st.text_input('Insert a ZipCode or type/check "ALL" to see all crimes in LA county')
    
    try:
        listo = data['zipcode'].to_list()
        if number == 'ALL' or number == '"ALL"' or number == 'all' or number == '"all"' or st.checkbox('ALL'):
            checkbox(data, data2)
            st.subheader(f'Map of food banks')
            maps(data)
            st.subheader(f'Map of discount grocery stores')
            maps(data2)

        elif int(number) in listo:
            data=data[data['zipcode'] == int(number)]
            data2=data2[data2['zipcode'] == int(number)]
            checkbox(data, data2)
            st.subheader(f'Map of food banks')
            maps(data)
            st.subheader(f'Map of discount grocery stores')
            maps(data2)

        else:
            st.write('Inserted ZipCode is not found')
    except:
        st.write('Please enter 5 main digits of ZipCode')
        
    st.write('In addition to food banks and grocery stores, essential food can be obtained by applying for Cal Fresh benefits:')
    st.write('[Cal Fresh Benefits Application and Information](https://www.cdss.ca.gov/food-nutrition/calfresh)')
    
    try:
        image = Image.open('food.jpg')
        st.image(image)
    except:
        st.write('')    
        
def education():
    st.title('Education Opportunity')
    st.header('Schools')


    #df = pd.read_json(edu_url)
    #https://sspai.com/post/58474


    
    def load_data():

        edu_url='https://laequityeducation-default-rtdb.firebaseio.com/school.json'
        df = pd.read_json(edu_url)
        df = df
        return df

    df=  load_data()
    st.write(" ")
    st.write(f"there are {len(df)} schools in data set")
    RawData= st.checkbox('Show Raw Data')
    if RawData:
       st.dataframe(df)


    st.subheader('Education opportunity Density Map in Los Angeles County:')
    loc_df=pd.DataFrame([df["longitude"],df["latitude"]]).T
    st.pydeck_chart(pdk.Deck(
         map_style='mapbox://styles/mapbox/light-v9',
         initial_view_state=pdk.ViewState(
             latitude=df["latitude"].mean(),
             longitude=df["longitude"].mean(),
             zoom=8.5,
             pitch=33,
         ),
         layers=[
             pdk.Layer(
                'HexagonLayer',
                data=loc_df,
                get_position='[longitude, latitude]',
                radius=300,
                elevation_scale=5,
                elevation_range=[0, 2000],
                pickable=True,
                extruded=True,
             ),
             pdk.Layer(
                 'ScatterplotLayer',
                 data=loc_df,
                 get_position='[longitude, latitude]',
                 get_color='[66, 185, 245, 160]',
                 get_radius=200,
             ),
         ],
     ))
    st.caption('Scroll to zoom in/out')

    st.write(" ")
    def bubleplot(df):
       plot=st.vega_lite_chart(df, {
             "width": 800,
            "height": 750,

           "layer": [
            {
               'mark': {'type': 'circle', 'tooltip': True,"opacity": 0.6,"stroke": "lightblue","strokeWidth": 0.5},"encoding":{'color': {'field': 'sch_rating', 'type': 'quantitative'},'size': {'field': 'sch_rating', 'type': 'quantitative',"scale": {"rangeMax": 250}}}},
             {
                'mark': {'type': 'circle',"opacity": 0.3,"stroke": "#959595","strokeWidth": 0.5,'color':'#959595'},"encoding":{'y': {'field': 'latitude', 'type': 'quantitative',"scale": {"domain": [33.31, 34.99]}},
                'x': {'field': 'longitude', 'type': 'quantitative',"scale": {"domain": [-118.99, -117.395]}},
                'latitude': {'field': 'latitude', 'type': 'quantitative'},
                'longitude': {'field': 'longitude', 'type': 'quantitative'}},'color':'#959595'
             },

               {
                 "mark": {'type':"text","fontSize":4,'tooltip': True},"encoding":{"text": {"field": "sch_StdPerTchr", "type": "nominal"}}  
               }],
            'encoding': {
                'y': {'field': 'latitude', 'type': 'quantitative',"scale": {"domain": [33.31, 34.99]}},
                'x': {'field': 'longitude', 'type': 'quantitative',"scale": {"domain": [-118.99, -117.395]}},
                'latitude': {'field': 'latitude', 'type': 'quantitative'},
                'longitude': {'field': 'longitude', 'type': 'quantitative'},



            }

        })
       return plot

    def bubleplot2(df):
       plot=st.vega_lite_chart(df, {
             "width": 800,
            "height": 750,



               'mark': {'type': 'circle', 'tooltip': True,"opacity": 0.6,"stroke": "lightblue","strokeWidth": 0.5},"encoding":{'size': {'field': 'sch_rating', 'type': 'quantitative',"scale": {"rangeMax": 450}}},


            'encoding': {
                'y': {'field': 'latitude', 'type': 'quantitative',"scale": {"domain": [33.31, 34.99]}},
                'x': {'field': 'longitude', 'type': 'quantitative',"scale": {"domain": [-118.99, -117.395]}},
                'latitude': {'field': 'latitude', 'type': 'quantitative'},
                'longitude': {'field': 'longitude', 'type': 'quantitative'},
                'color': {'field': 'sch_rating', 'type': 'quantitative'},


            }

        })
       return plot  
    st.subheader('Search Schools')
    sch_type_list = df["sch_type"].unique()
    sch_type = st.multiselect(
        "Which kind of school types would you like to see?",
        sch_type_list
    )

    sch_grade_list = df["sch_grade"].unique()
    sch_grade = st.multiselect(
        "Which grade would you like to know?",
        sch_grade_list
    )
    Hide= st.checkbox('Want to hide no rating school?')
    if Hide:
       st.write("hidhing no rating shcool")
       if not sch_type:
          if not sch_grade:
            st.map(df) 
          else:
             part_df=df.loc[df["sch_grade"].isin(sch_grade)]
             bubleplot2(part_df)
       elif not sch_grade: 
          if not sch_type:
            st.map(df)
          else:
              part_df=df.loc[df["sch_type"].isin(sch_type)]
              bubleplot2(part_df)     
       else:
          part_df=df.loc[(df["sch_type"].isin(sch_type)&(df['sch_grade'].isin(sch_grade)))]     
          bubleplot2(part_df)

       if not sch_type+sch_grade:
             st.write(f"showing all {len(df)} schools")
       else:
             hide_df=pd.DataFrame()
             hide_df=hide_df.append(part_df.loc[-df['sch_rating'].isna()])
             if len(hide_df)>1:
                st.write(f"There are {len(hide_df)} schools found based on your preference")
             elif len(hide_df)==1:
                st.write(f"There is only {len(hide_df)} school found based on your preference")
             else:
                st.write(f"No result")
    else: 
       if not sch_type:
          if not sch_grade:
            st.map(df) 
          else:
             part_df=df.loc[df["sch_grade"].isin(sch_grade)]
             bubleplot(part_df)
       elif not sch_grade: 
          if not sch_type:
            st.map(df)
          else:
              part_df=df.loc[df["sch_type"].isin(sch_type)]
              bubleplot(part_df)     
       else:
          part_df=df.loc[(df["sch_type"].isin(sch_type)&(df['sch_grade'].isin(sch_grade)))]     
          bubleplot(part_df)

       if not sch_type+sch_grade:
             st.write(f"showing all {len(df)} schools")
       else:
             if len(part_df)>1:
                st.write(f"There are {len(part_df)} schools found based on your preference")
             elif len(part_df)==1:
                st.write(f"There is only {len(part_df)} school found based on your preference")
             else:
                st.write(f"No result")

    with st.expander("Show School detials"):
       try:
          st.write(hide_df.loc[:,['sch_name','sch_rating','sch_StdPerTchr','sch_add']])
       except:  
          try:
             st.write(part_df.loc[:,['sch_name','sch_rating','sch_StdPerTchr','sch_add']])
          except:
             st.write(df)


    st.subheader('Find Schools in your area')
    number = st.text_input('Insert a Zip Code')
    ziplist=df["zip_code"].values.tolist()
    if int(number) in ziplist:
       zipcode_df=df.loc[df["zip_code"]==int(number)]
       st.caption(f'schools in {number} area')
       st.dataframe(zipcode_df.loc[:,['sch_name','sch_rating','sch_StdPerTchr','sch_type','sch_grade','sch_add']])
       
       sch_type_count=pd.DataFrame(zipcode_df.groupby(['sch_type']).count().T.iloc[0,:].values.tolist(),columns=["count"],index=zipcode_df.groupby(['sch_type']).count().T.columns.tolist())
       sch_grade_count=pd.DataFrame(zipcode_df.groupby(['sch_grade']).count().T.iloc[0,:].values.tolist(),columns=["count"],index=zipcode_df.groupby(['sch_grade']).count().T.columns.tolist())
       st.caption('Count by type')   
       st.bar_chart(sch_type_count)
       st.caption('Count by grade')
       st.bar_chart(sch_grade_count)
       st.caption('Schools on map')
       st.map(zipcode_df)
    else:
      st.caption(f'{number} area is too far form LA County')  

def equity():
    st.title("Equity, Opportunity and Risk")
    
    data_load_state = st.text('Rendering Plot...')
    if not firebase_admin._apps:
          cred = credentials.Certificate("./ServiceAccountKey.json")
          app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    docs = db.collection(u'foodbanks_LA').stream()
    FOOD_DF = pd.DataFrame()
    for doc in docs:
          FOOD_DF = FOOD_DF.append(doc.to_dict(), ignore_index=True) 
    docs2 = db.collection(u'grocery_LA').stream()
    Grocery_DF = pd.DataFrame()
    for doc in docs2:
          Grocery_DF = Grocery_DF.append(doc.to_dict(), ignore_index=True)
    @st.cache
    def load_data1():
          DATA_URL = 'df_crime_last.csv.gz'
          DATE_COLUMN = 'date/time'
          data = pd.read_csv(DATA_URL)
          lowercase = lambda x: str(x).lower()
          data.rename(lowercase, axis='columns', inplace=True)
          data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
          return data

    def load_data2():
          data = FOOD_DF[['Food Bank Name', 'Address', 'Zip Code', 'Latitude', 'Longitude']]
          data[['Zip Code','Latitude', 'Longitude']] = data[['Zip Code','Latitude', 'Longitude']].apply(pd.to_numeric)
          lowercase = lambda x: str(x).lower()
          data.rename(lowercase, axis='columns', inplace=True)
          data.rename(columns={'zip code': 'zipcode'}, inplace=True)
          return data

    def load_data3():
          data = Grocery_DF[['Grocery Name','Address','zipcode','latitude','longitude']]
          data[['zipcode','latitude','longitude']] = data[['zipcode','latitude','longitude']].apply(pd.to_numeric)
          lowercase = lambda x: str(x).lower()
          data.rename(lowercase, axis='columns', inplace=True)
          return data

    def load_data4():

          edu_url='https://laequityeducation-default-rtdb.firebaseio.com/school.json'
          df = pd.read_json(edu_url)
          df = df
          return df
    df1=load_data1()
    df1.rename(columns={"lon":'longitude'},inplace=True)
    df1.rename(columns={"lat":'latitude'},inplace=True)
    df2=load_data2()
    df3=load_data3()
    df4=load_data4()

    loc_df4=pd.DataFrame([df4["longitude"],df4["latitude"]]).T
    loc_df3=pd.DataFrame([df3["longitude"],df3["latitude"]]).T
    loc_df2=pd.DataFrame([df2["longitude"],df2["latitude"]]).T
    loc_df1=pd.DataFrame([df1["longitude"],df1["latitude"]]).T
    st.header('Crime, Food, School Map')
    data_load_state.text("Done! (using cache)")
    st.pydeck_chart(pdk.Deck(
       map_style='mapbox://styles/mapbox/light-v9',
       initial_view_state=pdk.ViewState(
           latitude=df4["latitude"].mean(),
           longitude=df4["longitude"].mean(),
           zoom=8.5,
           pitch=36,
       ),
       layers=[
           pdk.Layer(
              'HexagonLayer',
              data=loc_df4,
              get_position='[longitude, latitude]',
              radius=250,
              elevation_scale=5,
              elevation_range=[0, 1200],
              pickable=True,
              extruded=True,
           ),
           pdk.Layer(
              "HeatmapLayer",
              data=loc_df1,
              opacity=0.9,
              get_position=["longitude", "latitude"],
           ),
           pdk.Layer(
               'ScatterplotLayer',
               data=loc_df3,
               get_position='[longitude, latitude]',
               get_color='[100,200, 50, 160]',
               get_radius=1300,
           ),
           pdk.Layer(
               'ScatterplotLayer',
               data=loc_df2,
               get_position='[longitude, latitude]',
               get_color='[50,100,200, 160]',
               get_radius=1300,
           ),
       ],
   ))
    st.caption('Scroll to zoom in/out')
    st.caption('Bar shows the density of the Schools')
    st.caption('Heatmap shows the density of the Crimes')
    st.caption('Green Spot shows Food Banks')
    st.caption('Blue Spot shows Groceries')
    
def resources():
    st.title('Additional Resources')
    st.write('_**A number of initiatives are listed below that aim to improve social equality across Los Angeles county to address issues such as public safety, food security, education equity, housing and healthcare.**_')
    st.write('**_Public Safety and Crime Related Initiatives_**')
    image = Image.open('publicsafety.jpg')
    st.image(image)
    st.write('[LA DOT Safety Programs](https://ladot.lacity.org/projects/safety-programs)')   
    st.write('[LAPD Crime and Initiatives](https://lapdonlinestrgeacc.blob.core.usgovcloudapi.net/lapdonlinemedia/2022/01/2021_crime_initiatives.pdf)')
    
    st.write('**_Food Initiatives_**')
    image2 = Image.open('foodsecurity.jpg')
    st.image(image2)    
    st.write('[Los Angeles Regional Food Bank](https://www.lafoodbank.org/about/hunger-in-l-a/)')
    st.write('[County of Los Angeles Public Health Food Insecurity Study](http://ph.lacounty.gov/nut/media/nutrition-physical-activity-resources/LA_County_Food_Insecurity_Report_2021_508Compliant.pdf)')
    st.write('[USC Public Exchange Enough to Eat Study](https://publicexchange.usc.edu/wp-content/uploads/2021/10/Enough-to-Eat.pdf)')
    
    st.write('**_Education Initiatives_**')
    image3 = Image.open('education.jpg')
    st.image(image3)
    st.write('[Los Angeles Education Partnership](https://www.laep.org/)')
    st.write('[Los Angeles Mayor Education Initiatives](https://www.lamayor.org/education)')
    
    st.write('**_Healthcare Initiatives_**')
    image4 = Image.open('healthcare.jpg')
    st.image(image4)
    st.write('[Los Angeles County of Public Health Initiatives](http://www.publichealth.lacounty.gov/arra.htm)')
    st.write('[Los Angeles Care Health Plan](http://www.lacare.org/sites/default/files/L_A_%20Care%20Fact%20Sheet%205_15_14.pdf)')
    
    st.write('**_Housing Initiatives_**')
    image5 = Image.open('housing.jpg')
    st.image(image5)
    st.write('[Los Angeles County Department of Regional Planning Housing Initiatives](https://planning.lacounty.gov/housing/initiatives)')
    st.write('[Housing Authority of the City of Los Angeles Homeless Initiatives](https://www.hacla.org/en/about-section-8/homeless-initiatives)')
    
#driver code
if __name__ == "__main__":
    main()
