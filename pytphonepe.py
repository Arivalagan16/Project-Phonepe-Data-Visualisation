import streamlit as st
from streamlit_option_menu import option_menu
import os
import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import mysql.connector

# Sql Connection:

connection = mysql.connector.connect(
    host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port = 4000,
    user = "2ZyEJgr7d9Z3zUr.root",
    password = "Q970rGTYSeCyFYk2")

mycursor = connection.cursor(buffered=True)

with st.sidebar:

    menu = option_menu(
    menu_title='Dashboard',
    options=["Home","Count Information","Transaction Information","User Information","Top Charts","Insights"],
    menu_icon='cast',
    icons=['house','credit-card','person','bar-chart','bar-chart','person'],
    default_index=1)

if menu == "Home":
    st.markdown('<h1 style="color: gold;">Phonepe Pulse Data Visualization</h1>', unsafe_allow_html=True)
    st.subheader(":blue[PhonePe : The Best Unified Payments Interface in India]")
    st.write("Introducing PhonePe, PhonePe is one of India's leading digital payments platforms,founded in December 2015 by Sameer Nigam, Rahul Chari, and Burzin Engineer. It operates under the ownership of Flipkart, which is a subsidiary of Walmart. PhonePe is designed to facilitate seamless digital transactions and financial services using the Unified Payments Interface (UPI), an instant real-time payment system developed by the National Payments Corporation of India (NPCI). .")

    st.write(":blue[**Major Benefits of Using PhonePe :**]")
    st.write("1. **Ease of Use :** PhonePe provides a user-friendly interface that makes it easy for users to navigate and perform transactions quickly.")
    st.write("2. **Multiple Payment Options :** Users can link multiple bank accounts to PhonePe and make payments using various methods such as UPI, bank transfers, debit/credit cards, and wallets.")
    st.write("3. **Instant Money Transfers :** Transactions through UPI are fast, secure, and available 24/7, including weekends and holidays.")
    st.write("4. **Merchant Payments :** Users can pay using QR codes, UPI, or the PhonePe wallet, enhancing convenience and reducing the need for cash transactions.")
    st.write("5. **Offers and Cashback :** PhonePe frequently offers discounts, cashback, and rewards to users for making transactions and using specific services within the app.")

elif menu == "Count Information":

    def Agg_trans_count(state):
        query = "SELECT State, Year, SUM(Transaction_count) AS Transaction_Count FROM phonepe_data.aggregate_trans \
                WHERE State=%s \
                GROUP BY Year"
        
        mycursor.execute(query, (state,))
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        return df

    def Line_Plot(df):
        trace = go.Scatter(
            x=df['Year'],
            y=df['Transaction_Count'],
            mode='lines',
            name=df['State'].values[0],
            line=dict(color='orange'))

        layout = go.Layout(
            title=dict(text='Transaction Count Plot of ' + df['State'].values[0],font=dict(color='gold')),
            xaxis=dict(title='Years'),
            yaxis=dict(title='Transaction Count'))

        fig = go.Figure(data=[trace], layout=layout)

        return fig


    st.markdown('<h1 style="color: gold;">State-wise Transaction Count Information</h1>', unsafe_allow_html=True)
    states = ['Andaman & Nicobar','Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Lakshadweep', 'Puducherry']

    state_selected = st.selectbox(":blue[**Select State :**]", states)

    df = Agg_trans_count(state_selected)
    df2= df.sort_values(by="Year")
    df2 = df2.reset_index(drop=True)
    df2.index= df2.index + 1
    fig = Line_Plot(df)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h1 style="color: gold; font-size: 16px;">Table View of Year wise Total Transaction Count</h1>', unsafe_allow_html=True)

    st.dataframe(df2)

elif menu == "Transaction Information":

    #Geo visualisation:

    with open(r'C:\Users\goddy\Downloads\india_states [MConverter.eu].json') as data:
        india_states_geojson = json.load(data)


    def Agg_trans(year, quarter):
        query = "SELECT State, SUM(Transaction_amount) AS transaction_amount FROM phonepe_data.aggregate_trans \
                WHERE Year = %s and Quarter = %s \
                GROUP BY State"
        mycursor.execute(query, (year, quarter))
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])
        
        return df

    def geo_amount_map(df, year, quarter):
        df_geo = pd.json_normalize(india_states_geojson['features']).rename(columns={'properties.ST_NM': 'State'})
        df1 = pd.merge(df, df_geo, on='State')
        fig = px.choropleth_mapbox(df1, geojson=india_states_geojson, 
                                locations='State', 
                                featureidkey='properties.ST_NM',
                                color='transaction_amount', 
                                color_continuous_scale='Rainbow', 
                                range_color=(df1['transaction_amount'].min(), df1['transaction_amount'].max()),
                                mapbox_style='carto-positron', 
                                zoom=3.5, center={'lat': 22, 'lon': 82})
        
        fig.update_layout(title=dict(
            text=f'Transaction Amount Map of Year-{year}/Q{quarter}',
            font=dict(size=18, color='gold')),
            height=700,
            width=650)
        return fig

    st.markdown('<h1 style="color: gold;">State-wise Transaction Amount Information</h1>', unsafe_allow_html=True)

    years = ["Select",2018, 2019, 2020, 2021, 2022, 2023]
    quarters = ["Select",1, 2, 3, 4]

    year_selected = st.selectbox(":blue[**Select Year :**]", years)
    quarter_selected = st.selectbox(":blue[**Select Quarter :**]", quarters)

    df = Agg_trans(year_selected, quarter_selected)
    df2=df.sort_values(by="transaction_amount",ascending= False)
    df2 = df2.reset_index(drop=True)
    df2.index= df2.index + 1
    fig = geo_amount_map(df, year_selected, quarter_selected)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h1 style="color: gold; font-size: 20px;">Leading States in Net Transaction Amount</h1>', unsafe_allow_html=True)

    st.dataframe(df2)


elif menu == "User Information":

    def Agg_user(year, quarter):
        query = "SELECT State, SUM(Total_count) AS total_count FROM phonepe_data.aggregate_user \
                WHERE Year = %s \
                GROUP BY State"
        
        mycursor.execute(query, (year,))
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])
        return df

    def geo_count_map(df, year, quarter):
        df_geo = pd.json_normalize(india_states_geojson['features']).rename(columns={'properties.ST_NM': 'State'})
        df1 = pd.merge(df, df_geo, on='State')
        fig = px.choropleth_mapbox(df1, geojson=india_states_geojson, 
                                locations='State', 
                                featureidkey='properties.ST_NM',
                                color='total_count', 
                                color_continuous_scale='Viridis', 
                                range_color=(df1['total_count'].min(), df1['total_count'].max()),
                                mapbox_style='carto-positron', 
                                zoom=3.5, center={'lat': 22, 'lon': 82})
        
        fig.update_layout(title=dict(
            text=f'Net Transaction User Count State-wise of Year-{year}/Q{quarter}',
            font=dict(size=18, color='gold')),
            height=700,
            width=650)
        return fig

    with open(r'C:\Users\goddy\Downloads\india_states [MConverter.eu].json') as data:
        india_states_geojson = json.load(data)

    st.markdown('<h1 style="color: gold;">Transaction User Count Information State-wise</h1>', unsafe_allow_html=True)    

    years = ["Select",2018, 2019, 2020, 2021, 2022]
    quarters = ["Select",1, 2, 3, 4]

    year_selected = st.selectbox(":blue[**Select Year:**]", years)
    quarter_selected = st.selectbox(":blue[**Select Quarter:**]", quarters)

    df = Agg_user(year_selected, quarter_selected)
    df2=df.sort_values(by="total_count",ascending= False)
    df2 = df2.reset_index(drop=True)
    df2.index= df2.index + 1
    fig = geo_count_map(df, year_selected, quarter_selected)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h1 style="color: gold; font-size: 20px;">Leading States in Net Transaction Count</h1>', unsafe_allow_html=True)

    st.dataframe(df2)

elif menu == "Top Charts":

    st.markdown('<h1 style="color: gold;">Top Charts</h1>', unsafe_allow_html=True)


    query_select = st.selectbox(":blue[**Select Query :**]",("Select",
                                "Top 10 States with Highest Net Transaction counts in 2023",
                                "Top 10 States of Net Registered users In 2023",
                                "State-wise Net Transaction Amount Data",
                                "State-wise Net Transaction Type Count Data",
                                "Year-wise Net Transaction Type Count Data",
                                "Brand-wise Overall Percentage of Net Users",
                                "State-wise Overall Percentage of Net Registered Users",
                                "State-wise Overall Percentage of Net App opens in 2023"))
    
    if query_select=="Select the Query:":
        st.write("  ")

#Query 1:

    elif query_select=="Top 10 States with Highest Net Transaction counts in 2023":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">Top 10 States with Highest Net Transaction counts in 2023</h1>', unsafe_allow_html=True)
    
        mycursor.execute("SELECT State,SUM(Total_count) AS Total_Count FROM phonepe_data.top_trans \
                        Where Year=2023\
                        GROUP BY State \
                        ORDER BY Total_Count DESC LIMIT 10")

        states = []
        total_counts = []
        for row in mycursor.fetchall():
            states.append(row[0])
            total_counts.append(row[1])


        fig, ax = plt.subplots(figsize=(15, 6))
        colors = ['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta', 'brown', 'pink']

        ax.bar(states, total_counts, color=colors)
        ax.set_xlabel('States')
        ax.set_ylabel('Total Count')
        ax.set_title('Top 10 States with Highest Net Transaction counts in 2023')

        st.pyplot(fig)

# Query 2:

    elif query_select=="Top 10 States of Net Registered users In 2023":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">Top 10 States of Net Registered users In 2023</h1>', unsafe_allow_html=True)


        mycursor.execute("SELECT State,SUM(Register_user) AS Register_User FROM phonepe_data.top_user \
                        Where Year=2023\
                        GROUP BY State \
                        ORDER BY Register_User DESC LIMIT 10")
        states = []
        register_users = []
        for row in mycursor.fetchall():
            states.append(row[0])
            register_users.append(row[1])

        fig, ax = plt.subplots(figsize=(15,6))
        colors = ['orange', 'cyan', 'magenta', 'brown', 'pink','blue', 'red', 'green', 'yellow', 'purple']

        ax.bar(states, register_users,color=colors)
        ax.set_xlabel('States')
        ax.set_ylabel('Register Users')
        ax.set_title('Top 10 States of Net Registered users In 2023')

        st.pyplot(fig)

# Query-3:

    elif query_select=="State-wise Net Transaction Amount Data":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">State-wise Net Transaction Amount Data Chart</h1>', unsafe_allow_html=True)
        
        mycursor.execute("SELECT State,Year,Transaction_amount \
                        FROM phonepe_data.aggregate_trans\
                        WHERE year between 2018 and 2023\
                        GROUP by State,Year,Transaction_amount")
        
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])


        fig = px.bar(df, x=df.State, 
                        y=df.Transaction_amount,
                        color=df.State,
                        title='State-wise Net Transaction Amount Data',
                        height=700,width=650)

        st.plotly_chart(fig)

# Query-4:

    elif query_select== "State-wise Net Transaction Type Count Data":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">State-wise Net Transaction Type Count Data Chart</h1>', unsafe_allow_html=True)

        mycursor.execute("SELECT State,Year,Transaction_type,SUM(Transaction_count) Transaction_count \
                            FROM phonepe_data.aggregate_trans \
                            GROUP by State,Year,Transaction_type")
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        fig = px.bar(df, x=df.State,
                        y=df.Transaction_count,
                        color=df.Transaction_type,
                        title='State-wise Net Transaction Type Count Data',
                        height=700,width=650)

        st.plotly_chart(fig)

# Query-5:

    elif query_select== "Year-wise Net Transaction Type Count Data":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">Year-wise Net Transaction Type Count Data Chart</h1>', unsafe_allow_html=True)

        mycursor.execute("SELECT Year,Transaction_type,SUM(Transaction_count) Transaction_count \
                            FROM phonepe_data.aggregate_trans \
                            GROUP by Year,Transaction_type")
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        fig = px.bar(df, x=df.Transaction_type, 
                        y=df.Transaction_count,
                        color=df.Year,
                        title='Year-wise Net Transaction Type Count Data',
                        height=750,width=650)

        st.plotly_chart(fig)

# Query-6:

    elif query_select=="Brand-wise Overall Percentage of Net Users":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">Overall Percentage of Leading Brands Chart</h1>', unsafe_allow_html=True)        

        mycursor.execute("SELECT State,Year,sum(Percentage) as Percentage,Brand \
                        FROM phonepe_data.aggregate_user\
                        GROUP BY State,Year,Brand")
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        fig = px.pie(df, values='Percentage',
                        names='Brand',
                        color_discrete_sequence=px.colors.sequential.Viridis_r,
                        title='Brand-wise Overall Percentage of Net Users')
        
        fig.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig)

# Query-7:

    elif query_select=="State-wise Overall Percentage of Net Registered Users":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">Overall Percentage of Leading States Chart</h1>', unsafe_allow_html=True)
        
        mycursor.execute("SELECT State,SUM(Register_user) as Registeruser \
                            FROM phonepe_data.map_user \
                            GROUP BY State ")
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        fig = px.pie(df, values='Registeruser', names='State',title='State-wise Overall Percentage of Net Registered Users')
        fig.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig)

# Query-8:

    elif query_select=="State-wise Overall Percentage of Net App opens in 2023":
        st.markdown('<h1 style="color: gold; font-size: 15px; ">Overall Percentage of Leading States in App Opens in 2023</h1>', unsafe_allow_html=True)

        mycursor.execute("SELECT State,SUM(Register_user) as Registeruser,SUM(App_opened) as App_open \
                            FROM phonepe_data.map_user \
                            WHERE year=2023 \
                            GROUP BY State")
        out = mycursor.fetchall()
        connection.commit()
        df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

        fig = px.pie(df, values='App_open', names='State',title='State-wise Overall Percentage of Net App opens in 2023')
        fig.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig)

elif menu == "Insights":

    st.title(":blue[Five Major Insights :]")

    st.markdown('<h1 style="color: gold; font-size: 25px; "> --> Top 3 States With Most Transaction Count</h1>', unsafe_allow_html=True)
    st.write("1. Karnataka")
    st.write("2. Telengana")
    st.write("3. Maharashtra") 

    st.markdown('<h1 style="color: gold; font-size: 25px; "> --> Top 3 States With Most Transaction Amount</h1>', unsafe_allow_html=True)
    st.write("1. Maharashtra")
    st.write("2. Telengana")
    st.write("3. Karnataka") 

    st.markdown('<h1 style="color: gold; font-size: 25px; "> --> Top 3 States With Most Registered Users</h1>', unsafe_allow_html=True)
    st.write("1. Maharashtra")
    st.write("2. Uttar Pradesh")
    st.write("3. Karnataka")

    st.markdown('<h1 style="color: gold; font-size: 25px; "> --> Top 3 States With Most App Opens in 2023</h1>', unsafe_allow_html=True)
    st.write("1. Rajasthan")
    st.write("2. Maharashtra")
    st.write("3. Madhya Pradesh")

    st.markdown('<h1 style="color: gold; font-size: 25px; "> --> Top 3 Brands With Most Users in India</h1>', unsafe_allow_html=True)
    st.write("1. Xiaomi")
    st.write("2. Samsung")
    st.write("3. Vivo")