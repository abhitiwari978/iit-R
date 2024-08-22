import pandas as pd
schedule=pd.read_excel("328-H New_ Summary_Schedule_3min_Headway 40 buses 20240815.xlsx",sheet_name="Schedule")
schedule
limit=15
limit = pd.to_timedelta(f'00:{limit}:00')  
hour=7
schedule['start_time'] = pd.to_datetime(schedule['start_time'], format='%H:%M:%S')
schedule['headway'] = pd.to_timedelta(schedule['headway'])
exceeded_df = schedule[(schedule['start_time'].dt.hour == hour) & 
                       (schedule['headway'] > limit)]
print(exceeded_df)