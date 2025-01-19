import pandas as pd

file_path = './data/logs.csv'
group_by = 'IP_Address'
grouped_output_path = './data/humanized_logs.txt'

logs = pd.read_csv(file_path)

logs.columns = [
    'Date', 'Time', 'IP_Address', 'HTTP_Method', 'URL', 'HTTP_Version', 'Status', 'Referer', 'User_Agent', 'Additional_Data'
]

grouped_logs = logs.groupby(group_by)


with open(grouped_output_path, 'w') as f:
    for ip, group in grouped_logs:
        f.write(f"Group: {ip}\n")
        f.write(group.to_string(index=False))
        f.write("\n\n")