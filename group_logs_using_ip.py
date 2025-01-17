import pandas as pd
import os

file_path = './data/logs.csv'
group_by = 'IP_Address'

logs = pd.read_csv(file_path)

logs.columns = [
    'Date', 'Time', 'IP_Address', 'HTTP_Method', 'URL', 'HTTP_Version', 'Status', 'Referer', 'User_Agent', 'Additional_Data'
]


grouped_logs = logs.groupby(group_by)

grouped_output_path = './data/grouped_logs.csv'

for ip, group in grouped_logs:
    group.to_csv(grouped_output_path, mode='a', header=not os.path.exists(grouped_output_path), index=False)


