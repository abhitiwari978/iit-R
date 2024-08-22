import pandas as pd
import numpy as np
from datetime import timedelta,datetime
import warnings
warnings.filterwarnings("ignore")

schedule=pd.read_excel("328-H New_ Summary_Schedule_3min_Headway 40 buses 202408155.xlsx",sheet_name="Schedule")

limit_df=pd.read_excel("headway_limit.xlsx")

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
    return timedelta(minutes=60)

def get_distance():
    return 30

def convert_to_timedelta(time_str):
    return pd.to_timedelta(time_str)
schedule[schedule["headway"].apply(convert_to_timedelta)>timedelta(minutes=15)]["bus_id"]
sc=[]

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


k=1
for hour in range(24):
    limit = limit_df[hour].iloc[0]  # Assuming the limit is in the first row for each hour
    # print(limit)
    # Identify rows where headway exceeds the limit
    exceeded_df = schedule[(pd.to_datetime(schedule['start_time']).apply(lambda x: x.hour) == hour) & 
                              (pd.to_datetime(schedule['headway']).dt.minute > limit)]
    for index, row in exceeded_df.iterrows():
        # print(row)
        # print(hour)
        # Calculate the new start time by adding half the headway to the previous start time
        k=k+1
        bus_id=f'ABD{k}'
        shift=row['Shift']
        trip=row['trip_no']
        print(trip)
        start_stop=row['start_stop']
        new_start_time = (pd.to_datetime(row['start_time'], format='%H:%M:%S') + 
                          pd.to_timedelta(row['headway'])/2)
        midnight = pd.Timestamp('1900-01-01')  # Reference point for midnight
        new_start_time = pd.to_timedelta(new_start_time - midnight)
        start_time=new_start_time
        print(start_time)
        if(shift=="General Shift"):
            # print(exceeded_df)
            # print("General")
            trip_no=0
            for i in range(0,trip-2):
                if(start_stop=="Hosakote Bus Stand (Old)"):
                    start_stop="Attibele Bus Stand"
                elif(start_stop=="Attibele Bus Stand"):
                    start_stop="Hosakote Bus Stand (Old)"
                if(trip%2!=0):
                    min_break=timedelta(minutes=30)
                else:
                    min_break=timedelta(minutes=5)
                run_time=get_travel_time(start_time)
                start_time=start_time-run_time-min_break
                print(start_time)

            if(start_stop=="Hosakote Bus Stand (Old)"):
                trip_no+=1
                run_time=timedelta(minutes=5)
                min_break=timedelta(minutes=5)
                start_time=start_time-run_time-min_break
                end_time=start_time+run_time
                ready_time=end_time+min_break
                end_stop=start_stop
                start_stop="Depot-39"
                direction="UP"
                distance=2
                route_id="328-H"
                route_name="N/A"

                sc.append({
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
                                'runtime': format_time(run_time),
                                'minBreak_time': format_time(min_break),
                                'ready_time': format_time(ready_time),
                                'actualBreak_time': format_time(min_break),
                                'shift_id': 'NightOut 1',
                                'isDeadTrip': False
                                })

            elif(start_stop=="Attibele Bus Stand"):
                trip_no+=1
                run_time=timedelta(minutes=5)
                min_break=timedelta(minutes=5)
                start_time=start_time-run_time-min_break
                end_time=start_time+run_time
                ready_time=end_time+min_break
                end_stop=start_stop
                start_stop="Depot-32"
                direction="DN"
                distance=2
                route_id="328-H"
                route_name="N/A"

                sc.append({
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
                                'runtime': format_time(run_time),
                                'minBreak_time': format_time(min_break),
                                'ready_time': format_time(ready_time),
                                'actualBreak_time': format_time(min_break),
                                'shift_id': 'NightOut 1',
                                'isDeadTrip': False
                                })

            actual_start=ready_time
            start_stop=end_stop
            start_hour = 7
            start_minute = 0
            end_hour = 19
            end_minute = 30
            start_time_of_day = timedelta(hours=start_hour,minutes=end_minute)              #input
            end_time_of_day = timedelta(hours=end_hour, minutes=end_minute)
            s=0
            n=actual_start+get_travel_time(actual_start) 
            while start_time_of_day <= n + get_travel_time(n) <= end_time_of_day:

                        if(start_stop=="Attibele Bus Stand"):
                            for k in range(0,2):
                                trip_no+=1
                                if(k==0):
                                    start_stop = 'Attelebe Bus Stand'
                                    end_stop = 'Hosakote Bus Stand (Old)'
                                    direction='UP'
                                    route_id = '328-UP'
                                    starting='Hosakote'


                                else:
                                    start_stop = 'Hosakote Bus Stand (Old)'
                                    end_stop = 'Attelebe Bus Stand'
                                    direction='DN'
                                    route_id = '328-DN'
                                    starting='Attebele'

                                route_name = '328H'
                                runtime = get_travel_time(actual_start)
                                min_break = timedelta(minutes=5)
                                start_time = actual_start
                                distance=40

                                

                                if s%2!=0:
                                    min_break = timedelta(minutes=30)

                                end_time = actual_start + runtime
                                ready_time = end_time+min_break 


                                sc.append({
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

                            n=actual_start+get_travel_time(actual_start) 

                        else:
                            for k in range(0,2):
                                trip_no+=1
                                if(k==1):
                                    start_stop = 'Attelebe Bus Stand'
                                    end_stop = 'Hosakote Bus Stand (Old)'
                                    direction='UP'
                                    route_id = '328-UP'
                                    starting='Hosakote'


                                else:
                                    start_stop = 'Hosakote Bus Stand (Old)'
                                    end_stop = 'Attelebe Bus Stand'
                                    direction='DN'
                                    route_id = '328-DN'
                                    starting='Attebele'

                                route_name = '328H'
                                runtime = get_travel_time(actual_start)
                                min_break = timedelta(minutes=5)
                                start_time = actual_start
                                distance=40

                                

                                if s%2!=0:
                                    min_break = timedelta(minutes=30)

                                end_time = actual_start + runtime
                                ready_time = end_time+min_break 


                                sc.append({
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

                            n=actual_start+get_travel_time(actual_start)
                        

            if(n+2*timedelta(hours=1)-get_travel_time(actual_start)<end_time_of_day):
                        start_stop=end_stop
                        if(start_stop=="Attelebe Bus Stand"):
                            end_stop = select_nearest_stop('Attibele')
                        elif(start_stop=="Hosakote Bus Stand (Old)"):
                             end_stop=select_nearest_stop('Hosakote')
                        runtime = get_runtime()
                        distance = get_distance()
                        route_name = '328H'
                        min_break = timedelta(minutes=5)
                        start_time = actual_start
                        # # Calculate the duration since the start time
                        # elapsed_time = actual_start - temp_time

                        # if elapsed_time > max_runtime_duration:
                        #     min_break = timedelta(minutes=30)
                        #     elapsed_time = timedelta()
                        end_time = actual_start + runtime
                        ready_time = end_time+min_break

                        sc.append({
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

                        start_stop=end_stop
                        if(start_stop=="Kadugudi"):
                            end_stop = "Attebele Bus Stand"
                        elif(start_stop=="Sarjapura"):
                            end_stop="Hosakote Bus Stand (Old)"
                        runtime = get_runtime()
                        distance = get_distance()
                        route_name = '328H'
                        min_break = timedelta(minutes=5)
                        start_time = actual_start

                        # if elapsed_time > max_runtime_duration:
                        #     min_break = timedelta(minutes=30)
                           
                        end_time = actual_start + runtime
                        ready_time = end_time+min_break

                        sc.append({
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

            start_stop=end_stop
            if(start_stop=="Attebele Bus Stand"):
                        end_stop="Depot 32"
                        distance=7
            else:
                        end_stop="Depot 39"
                        distance=2
            trip_no+=1
            route_id="328H"
            start_time=ready_time
            min_break=timedelta(hours=0,minutes=0)
            runtime=timedelta(minutes=5)
            end_time=start_time+runtime
            ready_time=end_time+min_break+timedelta(hours=1,minutes=30)
            sc.append({
                            'bus_id': bus_id,
                            'trip_number': trip_no,
                            'start_stop': start_stop,
                            'end_stop': end_stop,
                            'route_name': route_name,
                            'direction': "",
                            'route_id': route_id,
                            'distance': distance,
                            'start_time': format_time(start_time),
                            'end_time': format_time(end_time),
                            'runtime': format_time(runtime),
                            'minBreak_time': format_time(min_break),
                            'ready_time': format_time(ready_time),
                            'actualBreak_time': format_time(timedelta(hours=1,minutes=30)),
                            'shift_id': 'NightOut 1',
                            'isDeadTrip': True
                        })
            actual_start = ready_time

df = pd.DataFrame(sc)

output_file_path = 'check2.csv'
schedule_df = pd.DataFrame(df)
schedule_df.to_csv(output_file_path, index=False)