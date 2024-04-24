#Import necessary packages
import streamlit as st
from datetime import date, datetime, timedelta
import pandas as pd
import altair as alt
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import sqlite3
import base64
import time
from userdefined import *
import logging
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
import base64

#Set page width to wide
st.set_page_config(layout="wide", initial_sidebar_state='collapsed')

# logging
logging.basicConfig(filename='/data/Reporting-Project/error.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info("Error log for Reporting-Project")

#Css for graph div and image div
pagecss = '''    
<style>
    [data-testid="stVerticalBlock"] {
        stArrowVegaLiteChart: -2px 5px 17px 11px grey;
    }
</style>
'''

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
     
@st.cache_data(ttl=1800)  # 1800 seconds = 30 minutes
def readSqlite(query,dbPath):
    conn = sqlite3.connect(dbPath)
    df = pd.read_sql_query(query, conn)
    return df
    
    
#buildChart() takes dataframe, xAxis, yAxis and title of the graph to plot images
def buildChart(df,xAxis,yAxis,title):
    df["xAxis"] = pd.to_datetime(df["xAxis"])
    # Extract just the time part from "xAxis"
    df["xAxis"] = df["xAxis"].dt.strftime("%H:%M:%S")
    xAxis = xAxis
    #initialize chart object and add data
    chart = alt.Chart(df).mark_circle().encode(
        
        alt.X('xAxis', title='time of day'),
        alt.Y(yAxis, title='Value'),
        tooltip=[
            alt.X(xAxis, title='time of day'),
            alt.Y(yAxis, title='Value')
        
        ]
    ).interactive()
        
    #set chart properties
    chart = chart.properties(
        title={
            'text': title,
            'fontSize': 16,
            'font': 'Courier',
            'anchor': 'middle'
            },
            width=550,
            height=200

        ).configure_axis(
            labelFontSize=12,
            titleFontSize=12
        )
        
    return chart

# Function to save DataFrames and images to a PDF
def save_to_pdf(dataframes, images, pdf_file):
    pdf_file = BytesIO()  # Create a BytesIO object to store PDF content
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    story = []

    for room, params in dataframes.items():
        for param, df in params.items():
            # Convert DataFrame to HTML table
            table_data = [df.columns.tolist()] + df.values.tolist()
            table = Table(table_data)
            story.append(table)
    doc.build(story)
    return pdf_file.getvalue()

# Function to create a download link for a file
def get_binary_file_downloader_html(bin_file, file_label='File'):
    encoded_pdf = base64.b64encode(bin_file).decode()  # Encode PDF content
    href = f'<a href="data:application/pdf;base64,{encoded_pdf}" download="{file_label}.pdf">Click here to download {file_label}</a>'

# Load required file
local_css("/data/Reporting-Project/static/css/style.css")
config = readJson("/data/Reporting-Project/config.json")
QueryDict = config["Query"]

#DB path on webserver
dbPath = "/data/SensorsData/Data-Store.db"

# Main container
main = st.container()

try:
    # Inside main container
    with main:
        # Create header
        header = st.container()
        with header:
            header.subheader("Sensor - Report")
            headerCol1, headerCol2 = header.columns([1,1])
            today = date.today()
            selected_date = headerCol1.date_input('Select Date', today, key="1")
            selected_date = selected_date.strftime("%Y-%m-%d 00:00:00")
            selected_date_temp = datetime.strptime(selected_date, "%Y-%m-%d %H:%M:%S")
            
            selected_datetime_end = selected_date_temp + timedelta(days=1)
            selected_datetime_end_str = selected_datetime_end.strftime("%Y-%m-%d 00:00:00") 
                
            # Read current day data of all RPIs
            df_list = []
            for k, v in QueryDict.items():
                #print(v.format(selected_date,selected_datetime_end_str))
                temp = readSqlite(v.format(selected_date,selected_datetime_end_str), dbPath)
                if not temp.empty:
                    df_list.append(temp)
                    
            if df_list:
                df = pd.concat(df_list)
                #st.write(df)  # For debugging purposes, remove it later
    
        # Create body
        body = st.container()
        dataframesPDF = {}
        imagePDF = {}
        if not df.empty:
            df['xAxis'] = pd.to_datetime(df['xAxis'])
            df['xAxis_temp'] = df['xAxis'].dt.date
            df['time'] = df['xAxis'].dt.time
            
            # Based on our entire data get unique Rooms
            options = list(df["room"].unique())
            
            #print("--options before--",options)
            for i, room in enumerate(options):
                tempDf = df[df['room'] == room]
                imagePDF[options[i]] = list(tempDf["image"])
                
                dataframesPDF[options[i]] = {"Temperature": df[["xAxis", "yAxisTemp"]], "Humidity": df[["xAxis", "yAxisHumid"]], "Brightness": df[["xAxis", "yAxisBrightness"]]}
                if "#1" in room:
                    options[i] = room.replace("#1", "")
                if room == "":
                    del options[i]
                      
                
            selected_option = headerCol2.selectbox('Select Room', options)
            
            
            if "Middle" in selected_option:
                selected_option = "growth room #1 (Middle)"
            if "right" in selected_option:
                selected_option = "growth room #1 (right)"
                
            # Filter data based on room selected
            df_room = df[df['room'] == selected_option]
            
            # Create two columns with relative widths of 2 and 2
            left_column, right_column = body.columns([2, 2])
            
            with left_column:
                # Create three tabs
                Temperature, Humidity, Brightness = left_column.tabs(["Temperature", "Humidity", "Brightness"])
                
                # Temperature
                data = df_room[["xAxis", "yAxisTemp"]]
                chart = buildChart(data, "xAxis", "yAxisTemp", "Temperature")
                Temperature.altair_chart(chart)
                
                # Humidity
                if 'yAxisHumid' in df_room.columns:
                    data = df_room[["xAxis", "yAxisHumid"]]
                    chart = buildChart(data, "xAxis", "yAxisHumid", "Humidity")
                    Humidity.altair_chart(chart)
    
                # Brightness
                data = df_room[["xAxis", "yAxisBrightness"]]
                chart = buildChart(data, "xAxis", "yAxisBrightness", "Brightness")
                Brightness.altair_chart(chart)
    
            with right_column:
                # Create 4 tabs
                import datetime
                tab1, tab2, tab3, tab4 = right_column.tabs(["12AM-6AM", "6AM-12PM", "12PM-6PM", "6PM-12AM"])
                time_ranges = [
                    (datetime.time(0, 0, 0), datetime.time(6, 0, 0)),
                    (datetime.time(6, 0, 0), datetime.time(12, 0, 0)),
                    (datetime.time(12, 0, 0), datetime.time(18, 0, 0)),
                    (datetime.time(18, 0, 0), datetime.time(23, 59, 59))
                ]
    
                for idx, (start_time, end_time) in enumerate(time_ranges, start=1):
                    time_range_data = df_room[(df_room['xAxis'].dt.time >= start_time) & (df_room['xAxis'].dt.time < end_time)]
                    time_range_images = time_range_data["image"].dropna().head(12)
                    grid_cols = [tab1, tab2, tab3, tab4][idx - 1]
                    images_container = grid_cols.columns(6)  # Adjust the number of columns here
                    for i, (img_raw, img_time) in enumerate(zip(time_range_images, time_range_data['time'])):
                        try:
                            img_decoded = base64.b64decode(img_raw)
                            #img_in_mem = Image.open(BytesIO(img_decoded)).resize((80, 65))
                            img_in_mem = Image.open(BytesIO(img_decoded)).resize((800, 650))
                            
                            
                            images_container[i % 6].image(img_in_mem, caption=img_time)  # Display 6 images per row
                        
                        except:
                            pass
        
                #if st.button("Download PDF"):
                #    # Generate the PDF
                #    pdf_content = save_to_pdf(dataframesPDF, imagePDF, "output.pdf")
                #
                #    # Provide a download link for the PDF
                #    b64_pdf = base64.b64encode(pdf_content).decode()
                #    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="output.pdf">Click here to download PDF</a>'
                #    st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("No data to show")
            # body.markdown("<center><h3>No data to show...</h3></center>", unsafe_allow_html=True)
except:
    st.error("No data to show")
