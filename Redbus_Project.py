import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px 
import time
from streamlit_option_menu import option_menu 


# kerala bus
lists_k=[]
df_K=pd.read_csv("df_k.csv")
for i,r in df_K.iterrows():  #traverse through each row
    lists_k.append(r["Route_name"])  # add that row in new list

#Andhra bus
lists_AP=[]
df_AP=pd.read_csv("df_AP.csv")
for i,r in df_AP.iterrows():
    lists_AP.append(r['Route_name'])

#Telungana bus
lists_TL=[]
df_TL=pd.read_csv("df_TL.csv")
for i,r in df_TL.iterrows():  #traverse through each row
    lists_TL.append(r["Route_name"])  # add that row in new list
#goa bus
lists_KA=[]
df_KA=pd.read_csv("df_KA.csv")
for i,r in df_KA.iterrows():
    lists_KA.append(r['Route_name'])

#rajasthan bus
lists_RS=[]
df_RS=pd.read_csv("df_RS.csv")
for i,r in df_RS.iterrows():
    lists_RS.append(r['Route_name'])

#west bengal bus
lists_WB=[]
df_WB=pd.read_csv("df_WB.csv")
for i,r in df_WB.iterrows():
    lists_WB.append(r['Route_name'])

#south bengal bus
lists_SB=[]
df_SB=pd.read_csv("df_SB.csv")
for i,r in df_SB.iterrows():
    lists_SB.append(r["Route_name"])

#uttar pradesh bus
lists_UP=[]
df_UP=pd.read_csv("df_UP.csv")
for i,r in df_UP.iterrows():
    lists_UP.append(r['Route_name'])

#haryana
lists_HR=[]
df_HR=pd.read_csv("df_HR.csv")
for i,r in df_HR.iterrows():
    lists_HR.append(r['Route_name'])

#Assam
lists_AS=[]
df_AS=pd.read_csv("df_AS.csv")
for i,r in df_AS.iterrows():
    lists_AS.append(r["Route_name"])
###############################################

#Settings Streamlit Page

st.set_page_config(layout="wide")

selected_option = st.sidebar.radio('Navigation', ['Home', 'States And Routes'])

web = option_menu(
    menu_title="Online Travel Buses",  # Title of the menu
    options=["Home", "📍States And Routes"],  # List of options in the menu
    icons=["house", "map"],  # Optional: Icons corresponding to each option
    menu_icon="bus",  # Optional: Icon for the menu title
    default_index=0  # Optional: Default index of the selected option
)
#Home Page setting
if selected_option == 'Home':
    st.write("Welcome to Online Travel Buses!")
    st.image("C:\\Users\\prem\\Desktop\\New folder\\Redbus Project\\rdc-redbus-logo.webp", width=200)
    st.title(" :red    Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit Application")
    st.subheader(":red[Domain:] Transportation")
    st.subheader(" :red[Objective:]")
    st.markdown("The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry. ")
    st.subheader(":blue[Overview:]")
    st.subheader(":red[Selenium:]")
    st.markdown("Selenium is a popular open-source tool used for automating web browsers. It allows you to write scripts to control a web browser’s actions and interact with web elements. This is useful for various tasks, including:Automated Testing,Web Scraping,Browser Automation. ")
    st.subheader(" :red[Pandas:]")
    st.markdown("Pandas is a powerful, open-source data analysis and manipulation library for Python. It provides data structures and functions needed to efficiently handle and analyze structured data, such as tables and time series.")
    st.subheader(" :red[Mysql:]")
    st.markdown("Mysql:MySQL is an open-source relational database management system (RDBMS) that uses Structured Query Language (SQL) for managing and querying data.")
    st.subheader(" :red[Streamlit:]")
    st.markdown("Streamlit:Streamlit is an open-source framework for creating interactive web applications in Python. It simplifies the process of building and sharing data applications and dashboards, making it especially popular among data scientists and machine learning engineers who want to quickly visualize and share their work.")
    st.subheader(":violet Skill-Take:")
    st.markdown(" *Python, *Selenium, *Pandas, *Mysql, *Streamlit. ")
    st.subheader(":blue[Developed-by:] :red Ranjana Devi.G")

# States and Routes Page settings

if selected_option == 'States And Routes':
    st.write("Here are the States and Routes!")
    S=st.selectbox("List of States",["Kerala","Andhra Pradesh","Telangana","Goa","Rajasthan","West Bengal","South Bengal",
                                     "Assam","Uttar Pradesh","Haryana"])

    col1,col2=st.columns(2)
    with col1:
        select_type = st.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_fare = st.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))
    TIME=st.time_input("select the time")

    # Kerala bus fare filtering
    if S == "Kerala":
        K = st.selectbox("List of routes",lists_k)

        def type_and_fare(bus_type, fare_range):
            conn=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",port=4000,
                                         user="4CZT8hVJPdoVHSB.root",password="L7QmBiLoWXAZZrBp",database="RED_BUS_DETAILS")
            my_cursor=conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            sqlquery  = f'''
                SELECT * FROM bus_details 
                WHERE Prices BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{K}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Prices and Start_time DESC
            '''
            my_cursor.execute(sqlquery)
            out=my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Seats_Available",
                "Prices","Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        st.dataframe(df_result)


    #2.Andhra Pradesh Bus Fare Filter
    if S == "Andhra Pradesh":
        AP = st.selectbox("List of routes",lists_AP)

        def type_and_fareAP(bus_type, fare_range):
            conn=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",port=4000,
                                         user="4CZT8hVJPdoVHSB.root",password="L7QmBiLoWXAZZrBp",database="RED_BUS_DETAILS")
            my_cursor=conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            sqlquery  = f'''
                SELECT * FROM bus_details 
                WHERE Prices BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{AP}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Prices and Start_time DESC
            '''
            my_cursor.execute(sqlquery)
            out=my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Seats_Available",
                "Prices","Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fareAP(select_type, select_fare)
        st.dataframe(df_result)


    #3.Telangana Bus Fare Filter
    if S=="Telangana":
        TL= st.selectbox("List of routes",lists_TL)

        def type_and_fareTL(bus_type, fare_range):
            conn=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",port=4000,
                                         user="4CZT8hVJPdoVHSB.root",password="L7QmBiLoWXAZZrBp",database="RED_BUS_DETAILS")
            my_cursor=conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            sqlquery  = f'''
                SELECT * FROM bus_details 
                WHERE Prices BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{TL}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Prices and Start_time DESC
            '''
            my_cursor.execute(sqlquery)
            out=my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Seats_Available",
                "Prices","Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fareTL(select_type, select_fare)
        st.dataframe(df_result)


    #4.Goa Bus Fare Filter
    if S=="Goa":
        KA = st.selectbox("List of routes",lists_KA)

        def type_and_fareKA(bus_type, fare_range):
            conn=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",port=4000,
                                         user="4CZT8hVJPdoVHSB.root",password="L7QmBiLoWXAZZrBp",database="RED_BUS_DETAILS")
            my_cursor=conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            sqlquery  = f'''
                SELECT * FROM bus_details 
                WHERE Prices BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{KA}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Prices and Start_time DESC
            '''
            my_cursor.execute(sqlquery)
            out=my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Seats_Available",
                "Prices","Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fareKA(select_type, select_fare)
        st.dataframe(df_result)

    

    #5.Rajasthan Bus Fare Filter
    if S=="Rajasthan":
        RS = st.selectbox("List of routes",lists_RS)

        def type_and_fareRS(bus_type, fare_range):
            conn=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",port=4000,
                                         user="4CZT8hVJPdoVHSB.root",password="L7QmBiLoWXAZZrBp",database="RED_BUS_DETAILS")
            my_cursor=conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            sqlquery  = f'''
                SELECT * FROM bus_details 
                WHERE Prices BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{RS}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Prices and Start_time DESC
            '''
            my_cursor.execute(sqlquery)
            out=my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Seats_Available"
                "Prices", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fareRS(select_type, select_fare)
        st.dataframe(df_result)

    #6.West Bengal Bus Fare Filter
    if S=="West Bengal":
        WB = st.selectbox("List of routes",lists_WB)

        def type_and_fareWB(bus_type, fare_range):
            conn=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",port=4000,
                                         user="4CZT8hVJPdoVHSB.root",password="L7QmBiLoWXAZZrBp",database="RED_BUS_DETAILS")
            my_cursor=conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            sqlquery  = f'''
                SELECT * FROM bus_details 
                WHERE Prices BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{WB}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Prices and Start_time DESC
            '''
            my_cursor.execute(sqlquery)
            out=my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
               "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Seats_Available",
                "Prices","Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fareWB(select_type, select_fare)
        st.dataframe(df_result)

    #7.South Bengal Bus Fare Filter
    if S=="South Bengal":
        SB = st.selectbox("List of routes",lists_SB)

        def type_and_fareSB(bus_type, fare_range):
            conn=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",port=4000,
                                         user="4CZT8hVJPdoVHSB.root",password="L7QmBiLoWXAZZrBp",database="RED_BUS_DETAILS")
            my_cursor=conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            sqlquery  = f'''
                SELECT * FROM bus_details 
                WHERE Prices BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{SB}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Prices and Start_time DESC
            '''
            my_cursor.execute(sqlquery)
            out=my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Seats_Available",
                "Prices","Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fareSB(select_type, select_fare)
        st.dataframe(df_result)


    #8.Assam Bus Fare Filter
    if S=="Assam":
        AS = st.selectbox("List of routes",lists_AS)

        def type_and_fareAS(bus_type, fare_range):
            conn=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",port=4000,
                                         user="4CZT8hVJPdoVHSB.root",password="L7QmBiLoWXAZZrBp",database="RED_BUS_DETAILS")
            my_cursor=conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            sqlquery  = f'''
                SELECT * FROM bus_details 
                WHERE Prices BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{AS}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Prices and Start_time DESC
            '''
            my_cursor.execute(sqlquery)
            out=my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Seats_Available",
                "Prices","Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fareAS(select_type, select_fare)
        st.dataframe(df_result)


    #9.Uttar Pradesh Bus Fare Filter
    if S=="Uttar Pradesh":
        UP = st.selectbox("List of routes",lists_UP)

        def type_and_fareUP(bus_type, fare_range):
            conn=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",port=4000,
                                         user="4CZT8hVJPdoVHSB.root",password="L7QmBiLoWXAZZrBp",database="RED_BUS_DETAILS")
            my_cursor=conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            sqlquery  = f'''
                SELECT * FROM bus_details 
                WHERE Prices BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{UP}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Prices and Start_time DESC
            '''
            my_cursor.execute(sqlquery)
            out=my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Seats_Available",
                "Prices","Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fareUP(select_type, select_fare)
        st.dataframe(df_result)


    #10.Haryana Bus Fare Filter
    if S=="Haryana":

        HR = st.selectbox("List of routes",lists_HR)

        def type_and_fareHR(bus_type, fare_range):
            conn=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",port=4000,
                                         user="4CZT8hVJPdoVHSB.root",password="L7QmBiLoWXAZZrBp",database="RED_BUS_DETAILS")
            my_cursor=conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            sqlquery  = f'''
                SELECT * FROM bus_details 
                WHERE Prices BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{HR}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Prices and Start_time DESC
            '''
            my_cursor.execute(sqlquery)
            out=my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration","Seats_Available",
                "Prices","Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fareHR(select_type, select_fare)
        st.dataframe(df_result)
