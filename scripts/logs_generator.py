import csv
import random
from datetime import datetime, timedelta
from helper import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename",
                    help="write logs to FILE", metavar="FILE", required=True)
parser.add_argument("-g", "--groups", dest="groups", default=1000,
                    help="Numbers of generated groups")

args = parser.parse_args()

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 1, 10)

def generate_log_entry(ip, timestamp, url, http_method, attack_type, user_agent):

    additional_data = ""
    if http_method == "POST":
        if attack_type == 1:
            additional_data = random.choice(sql_injections)
        elif url in valid_payloads:
            additional_data = valid_payloads[url].format(
                random.randint(1000, 9999), random.randint(1000, 9999), random.randint(1000, 9999)
            )
        elif "/transakcja" in url:
            additional_data = "action=execute"


    return {
        "Date": timestamp.strftime("%d/%b/%Y"),
        "Time": timestamp.strftime("%H:%M:%S"),
        "IP_Address": ip,
        "HTTP_Method": http_method,
        "URL": url,
        "HTTP_Version": "HTTP/1.1",
        "Status": random.choice([200, 403]),
        "Referer": random.choice(referrers),
        "User_Agent": user_agent,
        "Additional_Data": additional_data,
        "Attack_Type": attack_type
    }

def generate_csv(filename, group_count):
    logs = []
    sql_injection_count = 0
    bruteforce_count = 0

    for i in range(group_count):

        if i % 1000 == 0:
            print(str(i) + " logs generated")

        group_ip = generate_unique_ip()
        group_timestamp = generate_timestamp(start_date, end_date)
        user_agent = "Mozilla/5.0 (Group {}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36".format(random.randint(1000, 9999))
        attack_type = random.choice([0, 0, 0, 1, 2, 2])
        group_patterns = []

        if attack_type == 1:
            sql_injection_count += 1
            group_patterns = random.sample(injection_patterns, random.randint(1, 5))
        elif attack_type == 2:
            bruteforce_count += 1
            group_patterns = random.sample(bruteforce_patterns, random.randint(1, 2))
        else:
            group_patterns = random.sample(valid_patterns, random.randint(1, 5))

        for pattern in group_patterns:
            for action in pattern:
                http_method, url = action.split()
                log_entry = generate_log_entry(group_ip, group_timestamp, url, http_method, attack_type, user_agent)
                logs.append(log_entry)
                group_timestamp += timedelta(seconds=random.randint(1, 300))

    logs.sort(key=lambda x: datetime.strptime(x["Date"] + " " + x["Time"], "%d/%b/%Y %H:%M:%S"))

    print("Saving to file...")
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Date", "Time", "IP_Address", "HTTP_Method", "URL", "HTTP_Version", "Status", "Referer", "User_Agent", "Additional_Data", "Attack_Type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerows(logs)

    print(f"Generated {len(logs)} logs with {sql_injection_count} SQL injection attempts, and {bruteforce_count}  brute force attempts ")

generate_csv(args.filename, int(args.groups))