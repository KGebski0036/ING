import pandas as pd
import os

file_path = './data/generated_logs.csv'
group_by = 'IP_Address'

logs = pd.read_csv(file_path)

logs.columns = [
    'Date', 'Time', 'IP_Address', 'HTTP_Method', 'URL', 'HTTP_Version', 'Status', 'Referer', 'User_Agent', 'Additional_Data', 'Is_SQL_Injection'
]


grouped_logs = logs.groupby(group_by)

grouped_output_path = './data/grouped_logs_new.txt'

# Write grouped logs to a file with adaptive spacing for readability
with open(grouped_output_path, 'w') as f:
    for ip, group in grouped_logs:
        # Add a header for each group
        f.write(f"Group: {ip}\n")
        # Write the group data with adaptive spacing
        f.write(group.to_string(index=False))
        # Add a separator line after each group
        f.write("\n\n")