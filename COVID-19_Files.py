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

today = datetime.date.today()

# starting from 1st Feb 2020 for COVID cases 

someday = datetime.date(2020, 2, 1)
diff = someday - today
diff = abs(diff.days-2)
print(diff)


resp = requests.get('https://api.covid19india.org/data.json')

if resp.status_code != 200:
    
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))

# convert into test 

data = (resp.text)

#load data on to json method

parsed = json.loads(data)

result_array = np.empty([0,100])
result_date = np.empty([0,100])

def daily_count(days):
    
    global result_array
    global result_date

    for x in range(33,diff) :
        daily_confirmed = parsed['cases_time_series'][x]
        
        # st.markdown(daily_confirmed['date'] + '-->'+ daily_confirmed['dailyconfirmed'] )
        
        result = daily_confirmed['dailyconfirmed']
            
        result_array = np.append(result_array,[result])
        
        result_d = daily_confirmed['date']
        
        result_date = np.append(result_date,[result_d])
        
st.title('COVID-19 Cases in India !')

# Latest Data to be displayed 

latest_count = (diff -1)
     
        
latest_Data = parsed['cases_time_series'][latest_count]
    
# st.write(latest_Data['dailyconfirmed'])   

# st.write('Daily Confirmed Cases - '+latest_Data['date'] +'--'+ latest_Data['dailyconfirmed'] +'  - Recovered :'+ latest_Data['totalrecovered'] + ' - Death :' + latest_Data['totaldeceased'] + '- Positive :'+ latest_Data['totalconfirmed'] + '- Daily Recovery :'+ latest_Data['dailyrecovered'] )  

st.write('Date : '+latest_Data['date'])
st.write('Daily Confirmed Cases :' + latest_Data['dailyconfirmed'])
st.write('Total Recovered :'+ latest_Data['totalrecovered'])
st.write('Total Death :' + latest_Data['totaldeceased'])
st.write('Total Positive Cases :'+ latest_Data['totalconfirmed'])
st.write('Daily Recovery :' + latest_Data['dailyrecovered'] )  
st.write('Daily Death :' + latest_Data['dailydeceased'])
        
# calling the daily_count function
daily_count(diff)


df_confirm_case = pd.DataFrame(result_array, columns=['dailyconfirmed'])

df_date = pd.DataFrame(result_date, columns=['Date'])


data = {'DailyCase': [df_confirm_case],
         'Date': [df_date]}


df = pd.DataFrame(data,columns=['dailyconfirmed','Date'])

# st.bar_chart(df)

st.area_chart(result_array)


# if __name__ == '__main__':
#     main(diff)   

# st.plyplot()

# @st.cache

# def data_cache():
#     url = "https://api.covid19india.org/data.json"
#     return pd.read_json(url)


# url = "https://api.covid19india.org/data.json"
# df = pd.read_json(url)




