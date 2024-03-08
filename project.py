import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import datetime
sns.set(style='dark')

#Data Gathering
daily = pd.read_csv("day.csv")
daily.head()
hourly = pd.read_csv("hour.csv")
hourly.head()

#Data Assessing
daily.info()
hourly.info()
print(hourly.isna().sum())
print(daily.isna().sum())
print(daily.duplicated().sum())
print(hourly.duplicated().sum())
daily.describe()
hourly.describe()

#Data Cleaning
daily['dteday']= pd.to_datetime(daily['dteday'])
daily['season'].replace([1,2,3,4],['springer','summer', 'fall', 'winter'],inplace=True)
daily['yr'].replace([0,1],['2011','2012'],inplace=True)
daily['mnth'] = daily['mnth'].astype(str)
daily['holiday'].replace([0,1],['not holiday','holiday'],inplace=True)
daily['weekday'] = daily['weekday'].astype(str)
daily['workingday'].replace([0,1],['weekend/holiday','workingday'],inplace=True)
daily.info()

hourly['dteday']= pd.to_datetime(hourly['dteday'])
hourly['season'].replace([1,2,3,4],['springer','summer', 'fall', 'winter'],inplace=True)
hourly['yr'].replace([0,1],['2011','2012'],inplace=True)
hourly['mnth'] = hourly['mnth'].astype(str)
hourly['holiday'].replace([0,1],['not holiday','holiday'],inplace=True)
hourly['weekday'] = hourly['weekday'].astype(str)
hourly['workingday'].replace([0,1],['weekend/holiday','workingday'],inplace=True)
hourly.info()

#Download Clean Data
hourly.to_csv("hourly_clean.csv", index=False)
daily.to_csv("daily_clean.csv", indef=False)

#Exploratory Data Analysis
daily_clean.describe(include = "all")
hourly_clean.describe(include = "all")

##perbandingan sepeda tersewa holiday vs not holiday
daily_clean.groupby(by="holiday").agg({
    "instant": "nunique",
    "cnt": ["max", "min", "mean", "std"]
})
hourly_clean.groupby(by="hr").agg({
    "cnt": ["max", "min", "mean", "std"],
})

#jam-jam peak
hourly_clean.groupby(by="hr").agg({
    "cnt": ["max", "min", "mean", "std"],
})

#perbandingan tiap musim
seasonal = pd.DataFrame(daily_clean.groupby(by=["season","yr"]).agg({
    "cnt": ["sum"],
}).unstack())
#visualisasi tiap musim
grouped_data = seasonal.groupby(['season'])['cnt'].sum().unstack()
grouped_data.plot(kind='bar', colormap='tab20')

#perbandingan tiap jam
hourly_day = hourly_clean[hourly_clean["dteday"] == '2011-01-01']
#tanggalnya dapat diganti untuk melihat perubahan per hari
##visualisasi
plt.figure(figsize=(10, 5)) 
plt.plot(hourly_day["hr"], hourly_day["cnt"], marker='o', linewidth=2, color="#72BCD4") 
plt.title("Banyak Sepeda Tersewa per Jam", loc="center", fontsize=20) 
plt.xticks(fontsize=10) 
plt.yticks(fontsize=10) 
plt.show()

#dashboard
sidebarOpt = st.sidebar.selectbox(
    'Bike Share Dashboard Menu',
    ('Daily Report','Seasonal Report')
)
if sidebarOpt == 'Daily Report' or sidebarOpt =='':
    st.header('DAILY REPORT')
    #jumlah sepeda tersewa per jam setiap harinya
    dateInput = st.date_input(
        label='Pilih Tanggal',
        value = datetime.date(2011, 1, 1)
    )
    hourly_day = hourly_clean[hourly_clean["dteday"] == str(dateInput)] #subset data per hari
    daily_day = daily_clean[daily_clean["dteday"] == str(dateInput)]
    totalcnt = daily_day.cnt.sum()
    st.metric("Total Sepeda Tersewa", value = totalcnt)
    plt.figure(figsize=(10, 5)) 
    plt.plot(hourly_day["hr"], hourly_day["cnt"], marker='o', linewidth=2, color="#72BCD4") 
    plt.title("Banyak Sepeda Tersewa per Jam", loc="center", fontsize=20) 
    plt.xticks(fontsize=10) 
    plt.yticks(fontsize=10) 
    plt.show()
    st.pyplot(plt)
elif sidebarOpt == 'Seasonal Report':
    st.header("SEASONAL REPORT")
    #perbandingan peminjaman sepeda di tiap musim
    year = ['2011', '2012']
    selected_year = st.radio("Tahun", 
                             year, key="2011")
    subset_data = daily_clean[(daily_clean['yr'] == selected_year)]
    seasonal = subset_data.groupby('season')['cnt'].sum()
    fig, ax = plt.subplots(figsize = (10, 5))
    ax.bar(seasonal.index, seasonal.values,
           color='skyblue', label='Total')
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total")
    ax.set_title("Banyak Sepeda Tersewa tiap Musim")
    st.pyplot(fig)
