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

Variables we have:

**dr_no** - Division of Records Number: Official file number

**date/time** - date and time crimes occur

**crm cd desc** - definition of crime

**vict age** - victim age

**vict sex**  - victim sex (F - Female M - Male X - Unknown)

**location** - address where crimes occur

**lat** - latitude

**lon** - longitude

**zipcode** - zipcode

 
# 3. Food Access
We used the foodpantries.org list of food banks as well as the Grocery Outlet Store Locator, as this is considered an affordable grocery option, to give a general idea of food resources across the county.
Foodpantries.org: https://www.foodpantries.org/co/ca-los_angeles
Grocery Outlet Store Locator: https://www.groceryoutlet.com/store-locator?store_location=&store_region=Los+Angeles
 
Description: The foodpantries.org website offers a list of food banks in the county, while the Grocery Store outlet store locator website offers a list of Grocery Outlet locations in the county.
 
Features included:
Locations of food banks
Locations of Grocery Outlet stores

Variables:
Food Bank Name
Food Bank Address
Food Bank Zip Code
Food Bank Latitude
Food Bank Longitude
Grocery Store Name
Grocery Store Address
Grocery Store Zip Code
Grocery Store Latitude
Grocery Store Longitude
 
Data extracting and data cleaning:
Data was obtained by scraping the foodpantries.org and Grocery Outlet websites.
Addresses were converted to coordinates (latitude and longitude) using the geopy package in python
 
Data storage:
Extracted and cleaned food datasets are stored in Cloud Firestore. To connect with Firestore we generated a private key. Normally you should NEVER store a key in a public GitHub. Therefore, we used Secrets Management in Streamlit sharing to securely connect to private data sources. The sample python code of creating TOML secrets provided. (key-to-toml.py) 
 
# 4. Education Equity
Description: This data was obtained from https://www.greatschools.org/. All schools in LA County can be searched by their LA County zipcode. The number of schools can reflect the distribution and concentration of education around the county. Ratings reflect the evaluation of each school as well as the diversity and inclusiveness within the school. The teacher-student ratio can reflect the educational resources that each student can receive. Through these, we can understand the educational equality of the whole county.
 
Features included:
School distribution and density distribution
Multi-tab search based on school type
Multi-tab search based on school grade
List multi-label search results
Mouse suspension shows the proportion of teachers and students
Search for schools by zip code
Table of Postal Code Search Results
Count by school type and grade
 
Variables:
sch_name: school name
sch_add: school address
zip_code: school zip code
add_dist: school block
sch_rating: school evaluation (based on test scores and school equality ratings)
sch_StdPerTchr: school-teacher-student ratio
sch_type: school type
sch_garde: school grade
longitude: longitude
latitude: latitude
 
Data extracting and data cleaning: 
Obtain the required zipcode from the LA County Open Data website (https://data.lacounty.gov/GIS-Data/ZIP-Codes-and-Postal-Cities/c3xr-3jw2/data). Use the selenium package to scrape data from greatschool's dynamic web page, based on the zipcode obtained earlier. Use the geocoder package to access the Bing map service to obtain the latitude and longitude corresponding to the address. Clean up the data, check whether the newly acquired address matches the previous address, and correct the erroneous data. Insert missing data, according to the principle of proximity. 
	
Data storage:
Data is stored locally and uploaded to firebase cloud database.
