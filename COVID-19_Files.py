# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 21:33:43 2020

@author: Ramesh

Read COVID-19 json data from covid19india.org 

"""
import json
import pandas as pd
import requests
import streamlit as st
import datetime
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import pyplot as plt_r

today = datetime.date.today()

# starting from 1st Feb 2020 for COVID cases 

someday = datetime.date(2020, 2, 1)
diff = someday - today
diff = abs(diff.days-2)
start_date_cnt = (diff - 8)


resp = requests.get('https://api.covid19india.org/data.json')

if resp.status_code != 200:
    
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))

# convert into test 

data = (resp.text)

#load data on to json method

parsed = json.loads(data)

result_array = np.empty([0,100])
result_date = np.empty([0,100])
result_daily_rec = np.empty([0,100])

def daily_count(days):
    
    global result_array
    global result_date
    global result_daily_rec

    for x in range(start_date_cnt,diff) :
        
        daily_confirmed = parsed['cases_time_series'][x]
        
       
        result = daily_confirmed['dailyconfirmed']
            
        result_array = (np.append(result_array,[result]))
        
        result_d = daily_confirmed['date']
        
        result_date = np.append(result_date,[result_d])
        
        result_daily_r = daily_confirmed['dailyrecovered']
        
        result_daily_rec = np.append(result_daily_rec,[result_daily_r])
        
        
        
st.title('COVID-19 Cases in India !')

# Latest Data to be displayed 

latest_count = (diff -1)
     
        
latest_Data = parsed['cases_time_series'][latest_count]

st.markdown('<style>h3{color: Blue;} </style>', unsafe_allow_html=True)

st.markdown('Date : '+latest_Data['date'])

st.write('Confirmed Case :' + latest_Data['totalconfirmed'])
st.write('Active Case :' + str(int(latest_Data['totalconfirmed']) - int(latest_Data['totalrecovered'])))

st.write('Total Death :' + latest_Data['totaldeceased'])
st.write('Total Recovered :' + latest_Data['totalrecovered'])
st.write('Daily Confirmed Cases :' + latest_Data['dailyconfirmed'])

st.write('Daily Recovery :' + latest_Data['dailyrecovered'] )  
st.write('Daily Death :' + latest_Data['dailydeceased'])
        
# calling the daily_count function
daily_count(diff)

date = pd.Series(result_date)
confirm = pd.Series(result_array)

# convert into list into integer list
result_array = list(map(int,result_array))

plt.bar(result_date,result_array)

plt.title('COVID-19: Daily +ve cases from past 8 days !')
plt.ylabel('+ve cases')
plt.xlabel('Days')

st.pyplot(plt)

result_daily_rec = list(map(int,result_daily_rec))

agree = st.checkbox("Deep Dive")

if agree:
    
    # plt_r.bar(result_daily_rec,label="Recovery",width=5,height=.5)
    plt_r.bar(result_date,result_daily_rec)
    plt_r.title('COVID-19: Recoveries from past 8 days !')
    plt_r.ylabel('Recovery')
    plt_r.xlabel('Days')
    st.pyplot(plt_r)
