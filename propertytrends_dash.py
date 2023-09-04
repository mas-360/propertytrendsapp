# -*- coding: utf-8 -*-
"""
Created on Sun May 21 11:05:35 2023

@author: anthea sago
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
from datetime import datetime

# Setup for Storytelling (matplotlib):
plt.rcParams['font.family'] = 'monospace'
plt.rcParams['font.size'] = 8
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['figure.facecolor'] = '#606C38' 
plt.rcParams['axes.facecolor'] = '#606C38' 
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.titlecolor'] = 'black'
plt.rcParams['axes.titlesize'] = 9
plt.rcParams['axes.labelcolor'] = 'darkgray'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.edgecolor'] = 'darkgray'
plt.rcParams['axes.linewidth'] = 0.2
plt.rcParams['ytick.color'] = 'darkgray'
plt.rcParams['xtick.color'] = 'darkgray'
plt.rcParams['axes.titlecolor'] = '#FAF6F5'
plt.rcParams['axes.titlecolor'] = '#FAF6F5'
plt.rcParams['axes.edgecolor'] = 'darkgray'
plt.rcParams['axes.linewidth'] = 0.85
plt.rcParams['ytick.major.size'] = 0

# --- App (begin):
property_trends_df = pd.read_csv("Property_Trends.csv")

# Page setup:
st.set_page_config(
    page_title="Residential properties (South Africa)",
    page_icon="🏢",
    layout="centered",
    initial_sidebar_state="expanded",
)


# Header:
st.header('Appreciation of residential properties in South Africa')

st.sidebar.markdown(''' > **How to use this dashboard:**

1. To Select a city (**green dot**) & year.
2. To compare for the selected city against other 7 cities (**white dots**).
3. To compare the chosen city against **national average** and the data distribution.
4. **Insight Gained:** An appreciation above national average + selling price below average = possible *opportunity*

''')
st.sidebar.markdown("---")
st.sidebar.markdown(''' > **Keys:**  
                    
<span style="color:white;font-size:12pt"> ⚪ Each point represents a city </span>  
<span style="color:#f77f00;font-size:12pt"> ▫ <b> Average value </b></span>  
<span style="color:#FAF6F5;font-size:12pt"> ◽ Lowest values (<b> bottom </b>)  
◽ Highest values (<b> top </b>) <br>
◽ **Q1** (first quartile): where 25% of data falls under  
◽ **Q3** (third quartile): where 75% of data falls under  
</span>

''',unsafe_allow_html=True)


# Widgets:
cities = list(property_trends_df['City'].unique())
your_city = st.selectbox(
    '🌎 Select a city',
    cities,
)

year = sorted(list(property_trends_df['Year'].unique()))
year_ = st.selectbox(
    "🗓 Select a year",
    year,
)

selected_city = property_trends_df.query('City == @your_city & Year ==@year_')
other_cities = property_trends_df.query('City != @your_city & Year ==@year_') 


# CHART 1: Annual appreciation (12 months):
chart_1, ax = plt.subplots(figsize=(3, 4.125))
# Background:
sns.stripplot(
    data= other_cities,
    y = 'Annual_Appreciation(%)',
    color = 'white',
    jitter=0.85,
    size=8,
    linewidth=1,
    edgecolor='gainsboro',
    alpha=0.7
)
# Highlight:
sns.stripplot(
    data= selected_city,
    y = 'Annual_Appreciation(%)',
    color = '#00FF7F',
    jitter=0.15,
    size=12,
    linewidth=1,
    edgecolor='k',
    label=f'{your_city}'
)

# Showing up position measures:
avg_annual_val = property_trends_df['Annual_Appreciation(%)'].median()
q1_annual_val = np.percentile(property_trends_df['Annual_Appreciation(%)'], 25)
q3_annual_val = np.percentile(property_trends_df['Annual_Appreciation(%)'], 75)

# Plotting lines (reference):
ax.axhline(y=avg_annual_val, color='#f77f00', linestyle='--', lw=0.75)
ax.axhline(y=q1_annual_val, color='white', linestyle='--', lw=0.75)
ax.axhline(y=q3_annual_val, color='white', linestyle='--', lw=0.75)

# Adding the labels for position measures:
ax.text(1.15, q1_annual_val, 'Q1', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
ax.text(1.3, avg_annual_val, 'Median', ha='center', va='center', color='#f77f00', fontsize=8, fontweight='bold')
ax.text(1.15, q3_annual_val, 'Q3', ha='center', va='center', color='white', fontsize=8, fontweight='bold')

# to fill the area between the lines:
ax.fill_betweenx([q1_annual_val, q3_annual_val], -2, 1, alpha=0.2, color='gray')
# to set the x-axis limits to show the full range of the data:
ax.set_xlim(-1, 1)

# Axes and titles:
plt.xticks([])
plt.ylabel('Average appreciation (%)')
plt.title('Annual Appreciation (%)', weight='bold', loc='center', pad=15, color='gainsboro')
plt.legend(loc='center', bbox_to_anchor=(0.5, -0.1), ncol=2, framealpha=0, labelcolor='#00FF7F')
plt.tight_layout()  

# CHART 2: Price (R$) by m²:
chart_2, ax = plt.subplots(figsize=(3, 4.125))
# Background:
sns.stripplot(
    data= other_cities,
    y = 'Avg_SalePrice',
    color = 'white',
    jitter=0.85,
    size=8,
    linewidth=1,
    edgecolor='gainsboro',
    alpha=0.7
)
# Highlight:
sns.stripplot(
    data= selected_city,
    y = 'Avg_SalePrice',
    color = '#00FF7F',
    jitter=0.15,
    size=12,
    linewidth=1,
    edgecolor='k',
    label=f'{your_city}'
)

# Showing up position measures:
avg_price_m2 = property_trends_df['Avg_SalePrice'].median()
q1_price_m2 = np.percentile(property_trends_df['Avg_SalePrice'], 25)
q3_price_m2 = np.percentile(property_trends_df['Avg_SalePrice'], 75)

# Plotting lines (reference):
ax.axhline(y=avg_price_m2, color='#f77f00', linestyle='--', lw=0.75)
ax.axhline(y=q1_price_m2, color='white', linestyle='--', lw=0.75)
ax.axhline(y=q3_price_m2, color='white', linestyle='--', lw=0.75)

# Adding the labels for position measures:
ax.text(1.15, q1_price_m2, 'Q1', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
ax.text(1.35, avg_price_m2, 'Median', ha='center', va='center', color='#f77f00', fontsize=8, fontweight='bold')
ax.text(1.15, q3_price_m2, 'Q3', ha='center', va='center', color='white', fontsize=8, fontweight='bold')

# to fill the area between the lines:
ax.fill_betweenx([q1_price_m2, q3_price_m2], -2, 1, alpha=0.2, color='gray')
# to set the x-axis limits to show the full range of the data:
ax.set_xlim(-1, 1)


# Axes and titles:
plt.xticks([])
plt.ylabel('Sales Price (Millions)')
plt.legend(loc='center', bbox_to_anchor=(0.5, -0.1), ncol=2, framealpha=0, labelcolor='#00FF7F')
plt.title('Average Sales Price (R)', weight='bold', loc='center', pad=15, color='gainsboro')
plt.tight_layout()

# Splitting the charts into two columns:
left, right = st.columns(2)

# Columns (content):
with left:
    st.pyplot(chart_1)
with right:
    st.pyplot(chart_2)

# Showing up the numerical data (as a dataframe):
st.dataframe(
    property_trends_df.query('City == @your_city & Year ==@year_')[[
      'City', 'Annual_Appreciation(%)', 
      'Number_of_Sales']], hide_index=True
)


def get_last_update_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")

st.markdown('---')
# Adding some reference and last update:
st.write(f"Last Update: {get_last_update_date()}")    
    
st.markdown('''
Source: Data based on market trends from Property24 (2014 - 2023)  
Contact: masinsight360@gmail.com
''')
