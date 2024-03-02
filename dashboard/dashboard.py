import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def cleaning_data(df):
    df = df.drop(columns=['instant','windspeed'])
    df= df.rename(columns={
    'dteday':'datetime',
    'yr':'year',
    'mnth':'month',
    'hr':'hour',
    'weathersit':'weather_situation',
    'cnt':'count'})
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['season'] = df['season'].map({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month_name()
    df['weekday'] = df['datetime'].dt.day_name()
    df['weather_situation'] = df['weather_situation'].map({1: 'Clear',2: 'Cloudy',3: 'Light Snow/Rain',4: 'Heavy Snow/Rain'})
    df['season'] = df['season'].astype('category')
    df['year'] = df['year'].astype('category')
    df['month'] = df['month'].astype('category')
    df['weekday'] = df['weekday'].astype('category')
    df['hour'] = df['hour'].astype('category')
    df['holiday'] = df['holiday'].astype('category')
    df['workingday'] = df['workingday'].astype('category')
    df['weather_situation'] = df['weather_situation'].astype('category')
    return df

def create_daily_bikers(df):
    bikers = df.groupby(by='datetime').agg({
    'count':'sum'}).reset_index()
    return bikers

def create_weather_sit(df):
    weathersit_df = df.groupby(by='weather_situation').agg({
    'count':'sum'}).reset_index()
    return weathersit_df

def create_hour_df(df):
    hour_df = df.groupby(by='hour').agg({
    'count':'mean'}).reset_index()
    return hour_df

def create_season_df(df):
    season = df.groupby(by='season').agg({
    'count':'sum'}).reset_index()
    return season

data = pd.read_csv('hour.csv')
df = cleaning_data(data)
daily_bikers_df = create_daily_bikers(df)
weather_sit_df = create_weather_sit(df)
hour_df = create_hour_df(df)
season_df = create_season_df(df)

st.header('Bike Sharing Dashboard')

st.subheader('Monthly Bikers')

plt.figure(figsize=(10,5)) 
plt.plot(daily_bikers_df['datetime'],daily_bikers_df['count'])
plt.title("Monthly Used")
st.pyplot(plt)

st.subheader('By Weather')

plt.figure(figsize=(10,5)) 
plt.bar(weather_sit_df['weather_situation'],weather_sit_df['count'])
plt.title("Best Weather for Ride")
st.pyplot(plt)

st.subheader('Hourly Demographics')
plt.figure(figsize=(10,5))
plt.plot(hour_df['hour'],hour_df['count'],marker='o')
plt.title("Hourly Use")
plt.xticks(hour_df['hour'])
st.pyplot(plt)

st.subheader('Season Demographics')
total_bikers = daily_bikers_df['count'].sum()

st.metric("Total bikers", value=total_bikers)

plt.figure(figsize=(10,5)) 
plt.bar(season_df['season'],season_df['count'])
plt.title("Best Season for a ride")
st.pyplot(plt)

st.caption('(C) Humaidi Fikri 2024')



