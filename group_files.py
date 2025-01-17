import pandas as pd
import re


def annotate_and_extract_logins(input_csv, output_csv):
    # Define the expected columns
    columns = [
        'Date', 'Time', 'IP_Address', 'HTTP_Method', 'URL', 'HTTP_Version',
        'Status', 'Referer', 'User_Agent', 'Additional_Data'
    ]

    # Load the CSV file
    logs = pd.read_csv(input_csv, header=None)  # Assuming no headers in the input file
    logs.columns = columns  # Assign column names

    # Function to extract 'login' value from the Additional_Data column
    def extract_login(data):
        if pd.isnull(data):
            return None
        match = re.search(r'login=([^&]+)', data)
        return match.group(1) if match else None

    # Apply the extraction function to the Additional_Data column
    logs['Login'] = logs['Additional_Data'].apply(extract_login)

    # Save the annotated CSV with the new 'Login' column
    logs.to_csv(output_csv, index=False)
    print(f"Annotated CSV saved to '{output_csv}'.")


# Example usage
input_csv = 'data/logs.csv'  # Replace with your input CSV file
output_csv = 'annotated_logs.csv'  # Replace with your desired output file name
annotate_and_extract_logins(input_csv, output_csv)
