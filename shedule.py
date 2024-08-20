import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import datetime
import math
import warnings
warnings.filterwarnings("ignore")

freq=pd.read_excel('input.xlsx')
# freq=freq.loc[0:1] #for weekdays
freq

bus_id = 0
schedule = []

def get_travel_time(current_time):
    current_minutes = current_time.total_seconds() // 60
    if 4 * 60 <= current_minutes < 6 * 60:
        return timedelta(minutes=90)
    elif 6 * 60 <= current_minutes < 7 * 60:
        return timedelta(minutes=100)
    elif 7 * 60 <= current_minutes < 10 * 60:
        return timedelta(minutes=110)
    elif 10 * 60 <= current_minutes < 16 * 60:
        return timedelta(minutes=100)
    elif 16 * 60 <= current_minutes < 20 * 60:
        return timedelta(minutes=110)
    elif 20 * 60 <= current_minutes < 22 * 60:
        return timedelta(minutes=100)
    else:
        return timedelta(minutes=100)

def select_nearest_stop(input):
    if input == 'Attibele':
        return 'Kadugudi'
    elif input == 'Hosakote':
        return 'Sarjapura'

def format_time(time):
    if isinstance(time, timedelta):
        total_seconds = int(time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{hours:02}:{minutes:02}:{seconds:02}'
    elif isinstance(time, datetime):
        return time.strftime('%H:%M:%S')

def get_runtime():
    return timedelta(minutes=120)

def get_distance():
    return 30

# Initialize variables
stops = ['Attibele', 'Hosakote']
# Replace with actual frequency values
up_freq = freq.loc[0, 0:].tolist() # used as input
dn_freq = freq.loc[1, 0:].tolist() #used as input
start_hour = 4
start_minute = 0
end_hour = 11
end_minute = 30

# Initialize the start time (using timedelta only for time calculations)
# current_time = timedelta(hours=start_hour, minutes=start_minute)

# Define the start and end times of the day as timedelta objects
start_time_of_day = timedelta(hours=start_hour,minutes=end_minute)              #input
end_time_of_day = timedelta(hours=end_hour, minutes=end_minute)                 #input

# Define the maximum runtime duration for comparison
max_runtime_duration = timedelta(hours=4)

for j in range(len(up_freq)):  # Adjusted to use length of frequency list
    upfreq = int(up_freq[j])
    dnfreq = int(dn_freq[j])
    current_time = timedelta(hours=j, minutes=start_minute)
    if (j in range(4,6)): #for Nightout 1
        if(upfreq>0):
            starting='Attebele'
            for k in range (0,upfreq):
                    bus_id += 1
                    trip_no = 0
                    temp_time = current_time
                    a=(60//upfreq)*k
                    print(a)
                    temp_time+=timedelta(minutes=a)
                    actual_start=temp_time
                    
                    while start_time_of_day <= actual_start+timedelta(hours=1,minutes=30) <= end_time_of_day:
                        trip_no += 1
                        if(starting=='Attebele'):    
                            start_stop = 'Attelebe'
                            end_stop = 'Hosakote'
                            direction='DN'
                            route_id = '328-UP'
                            starting='Hosakote'

                        elif(starting=='Hosakote'):
                            start_stop = 'Hosakote'
                            end_stop = 'Attebele'
                            direction = 'DN'
                            route_id = '328-DN'
                            starting='Attebele'

                        route_name = '328H'
                        runtime = get_travel_time(actual_start)
                        min_break = timedelta(minutes=6)
                        start_time = actual_start
                        distance=40
                        
                        if (actual_start + 2*runtime) > end_time_of_day:
                            if(starting=='Hosakote'):
                                end_stop = select_nearest_stop('Attibele')
                            else:
                                end_stop = select_nearest_stop('Hosakote')
                                run_time = get_runtime()
                                distance = get_distance()
                        

                        # Calculate the duration since the start time
                        elapsed_time = actual_start - temp_time

                        if elapsed_time > max_runtime_duration:
                            min_break = timedelta(minutes=31)
                            elapsed_time = timedelta()

                        end_time = actual_start + runtime
                        ready_time = end_time+min_break  # Ready time is just the break time

                        schedule.append({
                            'bus_id': bus_id,
                            'trip_number': trip_no,
                            'start_stop': start_stop,
                            'end_stop': end_stop,
                            'route_name': route_name,
                            'direction': direction,
                            'route_id': route_id,
                            'distance': distance,
                            'start_time': format_time(start_time),
                            'end_time': format_time(end_time),
                            'runtime': format_time(runtime),
                            'minBreak_time': format_time(min_break),
                            'ready_time': format_time(ready_time),
                            'actualBreak_time': format_time(min_break),
                            'shift_id': 'NightOut 1',
                            'isDeadTrip': False
                        })

                        actual_start = ready_time
                    
        if(dnfreq>0):
            starting='Hosakote'
            for k in range (0,dnfreq):
                    bus_id += 1
                    trip_no = 0
                    temp_time = current_time
                    a=(60//dnfreq)*k
                    print(a)
                    temp_time+=timedelta(minutes=a)
                    actual_start=temp_time
                    
                    while start_time_of_day <= actual_start+timedelta(hours=1,minutes=30) <= end_time_of_day:
                        trip_no += 1
                        if(starting=='Attebele'):    
                            start_stop = 'Attelebe'
                            end_stop = 'Hosakote'
                            direction='DN'
                            route_id = '328-UP'
                            starting='Hosakote'

                        elif(starting=='Hosakote'):
                            start_stop = 'Hosakote'
                            end_stop = 'Attebele'
                            direction = 'DN'
                            route_id = '328-DN'
                            starting='Attebele'

                        route_name = '328H'
                        runtime = get_travel_time(actual_start)
                        min_break = timedelta(minutes=6)
                        start_time = actual_start
                        distance=40
                        
                        if (actual_start + 2*runtime) > end_time_of_day:
                            if(starting=='Hosakote'):
                                end_stop = select_nearest_stop('Attibele')
                            else:
                                end_stop = select_nearest_stop('Hosakote')
                                run_time = get_runtime()
                                distance = get_distance()
                        

                        # Calculate the duration since the start time
                        elapsed_time = actual_start - temp_time

                        if elapsed_time > max_runtime_duration:
                            min_break = timedelta(minutes=31)
                            elapsed_time = timedelta()

                        end_time = actual_start + runtime
                        ready_time = end_time+min_break  # Ready time is just the break time

                        schedule.append({
                            'bus_id': bus_id,
                            'trip_number': trip_no,
                            'start_stop': start_stop,
                            'end_stop': end_stop,
                            'route_name': route_name,
                            'direction': direction,
                            'route_id': route_id,
                            'distance': distance,
                            'start_time': format_time(start_time),
                            'end_time': format_time(end_time),
                            'runtime': format_time(runtime),
                            'minBreak_time': format_time(min_break),
                            'ready_time': format_time(ready_time),
                            'actualBreak_time': format_time(min_break),
                            'shift_id': 'NightOut 1',
                            'isDeadTrip': False
                        })

                        actual_start = ready_time        

                


# Save the schedule to a CSV file
output_file_path = 'bus_sch.csv'
schedule_df = pd.DataFrame(schedule)
schedule_df.to_csv(output_file_path, index=False)