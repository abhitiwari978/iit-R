import pandas as pd
import numpy as np
from datetime import timedelta,datetime
import warnings
warnings.filterwarnings("ignore")

def format_time(time):
    if isinstance(time, timedelta):
        total_seconds = int(time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{hours:02}:{minutes:02}:{seconds:02}'
    elif isinstance(time, datetime):
        return time.strftime('%H:%M:%S')

schedule=pd.read_excel("328-H New_ Summary_Schedule_3min_Headway 40 buses 202408155.xlsx",sheet_name="Schedule")
new_start_time=timedelta(hours=15,minutes=57)
new_start_time=format_time(new_start_time)
start_stop_to_check="Attibele Bus Stand"
# Group by 'start_stop'
grouped = schedule.groupby('start_stop')['start_time'].apply(list)
# print(grouped)
while(True):
        # Check if new_start_time is in the list for the specific start_stop
        # if start_stop_to_check in grouped:
        #     print("1")
            if new_start_time in grouped[start_stop_to_check]:
                print("2")
                new_start_time=pd.to_datetime(new_start_time, format='%H:%M:%S')+timedelta(minutes=2)
            else:
                 break
print(new_start_time)
