import pandas as pd

# Load the Excel file
schedule = pd.read_excel("328-H New_ Summary_Schedule_3min_Headway 40 buses 202408155.xlsx", sheet_name="Schedule")

# Define the headway limit
limit =15  # 15 minutes limit
hour = 7


# Filter rows where headway exceeds the limit and 'start_time' hour is 7
exceeded_df = schedule[
    (pd.to_datetime(schedule['headway']).dt.minute > limit) &
    (pd.to_datetime(schedule['start_time']).apply(lambda x: x.hour) == hour)
]
output_file_path = 'check1.csv'
schedule_df = pd.DataFrame(exceeded_df)
schedule_df.to_csv(output_file_path, index=False)
