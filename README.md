# DSCI551-project - Final project description
# 1. About the project 
The group project created by Yerke Bauyrzhanov, Soumeya Kerrar, Zihao Han 

**The streamlit link:**

https://share.streamlit.io/bauyrzha/dsci551-project/main/main.py

**Project title:** Social Inequality Across Los Angeles County
**Topic:** This project will examine inequalities in regions of Los Angeles based on crime rates, access to food, and access to quality education.

**Motivation:**
With the abundance of data available in today’s age, data science is a tool that can be yielded to
make significant contributions to society. One of today’s most pressing issues, both domestically
and abroad, is social inequity. Specifically, income inequality and public safety threaten the
quality of life of many individuals. We can see this right here in Los Angeles County, with issues
such as housing affordability, homelessness, food insecurity, crime rates, education access and
others permeating the county. In this project, we aim to address some of these issues in order to
provide users with awareness about specific inequalities and issues, and offer information and
solutions to these issues. The purpose of this project is to build an app that compares different
inequalities in different areas of the county in order to determine which areas need most
improvement, funding, resources and public safety. With income inequality continuing to grow in
this area of the state, it is important to examine who is most impacted in order to know what
types of changes need to be made. This app will help people by providing necessary
information about criminality, food availability, and education quality in LA county. By
understanding existing inequality in LA, we can better help our city and neighborhoods
especially at this special time. The app will also provide information on resources and initiatives
currently available to address these issues. Users will be able to search by neighborhood/region
to see which areas are most negatively impacted, and also filter by categories of “crime”,
“education” and “food”.

# 2.Crime Rates
**Source:**

● LA City Crime Data: https://data.lacity.org/browse?q=crime%20data&sortBy=relevance

**Description:** This dataset reflects incidents of crime in the City of Los Angeles dating back to 2020. This data is transcribed from original crime reports that are typed on paper and therefore there may be some inaccuracies within the data. Some location fields with missing data are noted as (0°, 0°). Address fields are only provided to the nearest hundred block in order to maintain privacy. This data is as accurate as the data in the database. 

**Features to include:**

- Number of crimes by hour
- Number of crimes in context of zipcodes
- Locations of highest crime rates
- Locations of lowest crime rates
- Types of crimes(ranked more common and less common)
- Victim Sex

Step 1 (data extracting and data cleaning):

1) download dataset and clean/remove unnecessary/irrelevant data.
  run jupyter notebook **crime_cleaning.ipynb**
2) get zipcodes for locations of crimes. Need to use google colab.
  run jupyter notebook **get_zip_google_colab.ipynb** on google colab.
  
Step 2 (show data):

1) create python code using stremlit library to create stremlit application.
2) create requirements.txt with the list of necessary libraries.
   run command line **streamlit run main.py** for local machine

Step 3 (data analysis):

1) According to the histogram, we can notice that the peak of crime rates is at 12:00 pm. However, we guess that it is a default time when the time of the crime is unknown.
Therefore, we consider the majority number of crimes take place in the evening time with the peak at 6 pm.
2) According to the plot, many crimes take place in a range of zipcodes 90000-90080.
3) The most dangerous regions are locations with zipcodes 90003, 90037, 90028 with 14479, 12551, and 11145 crimes respectively from 2020 to the present. 
4) The safest regions are locations with zipcodes 90245, 91506, and 90802 with only 2, 3, and 3 crimes respectively from 2020 to the present. 
5) Top crime types are stealing vehicles, simple assault of batteries, burglary from vehicles, and vandalism. 
6) According to the categorical plot, crimes against male occur more often than against female

_More detailed results of the analysis can be found in final_report.pdf_
  
# 3. Food Access
-------

-------
# 4. Education Equity
------

------
**Description of files:**

To find out the whole usage, check out final_report.pdf.
