Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly

📘 Introduction
This project involves cloning the PhonePe Pulse dataset using Git
then transforming the data into dataframe by using Pandas.
Transformed data is subsequently stored in a SQL database with help of SQL conncetor and SQL-Alchemy engine.
Additionally, an interactive dashboard is developed with Streamlit and Plotly, featuring geoplots and other visualization elements for enhanced data exploration and insights.

🎨 Skills Takeaway
Github Cloning, Python Scripting , MySQL Database,mysql-connector-python, Streamlit, and Plotly.

🛠 Technology and Tools
Python 3.12.2
MYSQL
Streamlit
Plotly

📚 Packages and Libraries
import os
import json
import git
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector

📂 Data Sources
The data utilized in this project predominantly consists of openly available datasets sourced from PhonePe.click here to view

📘 Overview

✂️ Data Extraction:
the data is extracted from the PhonePe Pulse GitHub repository and cloned to the local environment, ensuring access to the latest dataset for analysis.

🔁 Data Transformation:
The raw data undergoes transformation, including cleaning, formatting, and structuring in dataframe format using pandas

🗃️ Database Integration:
Mysql connector used for connection between Python and MySQL database with XAMPP, enabling data transfer. SQLAlchemy's engine facilitates efficient data insertion and querying, simplifying database interactions for Python.

📊 Data Visualization And Analysis:
With the assistance of Streamlit and Plotly, a dashboard and charts are created, offering geospatial visualizations and top insights. This setup empowers users to explore and reveal trends within the dataset, facilitating insightful analysis.

📘 Features

🌐 GEO visualization:
The geo visualization showcases transaction amounts and counts across Indian states, plotted on a map. Additionally, it incorporates registered user counts, providing a state-wise overview on the map

🔝 TOP Insights:
Top insights encompass various key findings derived from the data, visualized through charts showcasing the most significant trends.

👨‍🏫 Reference
TIDB Cloud Documentation
Streamlit Documentation
Plotly Documentation
