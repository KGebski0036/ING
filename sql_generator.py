import csv
import random
from datetime import datetime, timedelta


# Define a function to generate random IP addresses
def generate_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


# Define a function to generate random timestamps
def generate_timestamp(start_date, end_date):
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)


# Templates for log entries
def generate_log_entry(ip, timestamp, is_sql_injection):
    methods = ["GET", "POST"]
    urls = ["/logowanie", "/resetpassword", "/dashboard", "/transaction"]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/115.0",
    ]

    referrers = [
        "https://kingbank.pl/",
        "https://kingbank.pl/logowanie",
        "https://kingbank.pl/dashboard"
    ]

    additional_data = ""
    http_method = random.choice(methods)

    if is_sql_injection and http_method == "POST":
        sql_injections = [
            "login=test' OR '1'='1'--&password=&action=login",
            "search=test' UNION SELECT NULL,NULL,NULL;--",
            "username=admin'--",
            "id=1 OR 1=1;--",
            "email=test@example.com' AND 1=2 UNION SELECT 'a', 'b', 'c';--",
            "name=xyz' OR 'a'='a'/*",
            "product_id=1; DROP TABLE users;--",
            "order_id=1' UNION ALL SELECT NULL, NULL, NULL;--"
        ]
        additional_data = random.choice(sql_injections)
    elif http_method == "POST":
        additional_data = "login=user{}&password={}&action=login".format(
            random.randint(1000, 9999), "pass"
        )

    return {
        "Date": timestamp.strftime("%d/%b/%Y"),
        "Time": timestamp.strftime("%H:%M:%S"),
        "IP_Address": ip,
        "HTTP_Method": http_method,
        "URL": random.choice(urls),
        "HTTP_Version": "HTTP/1.1",
        "Status": random.choice([200, 403]),
        "Referer": random.choice(referrers),
        "User_Agent": random.choice(user_agents),
        "Additional_Data": additional_data if http_method == "POST" else "",
        "Is_SQL_Injection": 1 if is_sql_injection else 0
    }


# Main function to generate CSV file
def generate_csv(filename, group_count):
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 1, 10)

    logs = []
    sql_injection_count = 0

    for _ in range(group_count):
        group_ip = generate_ip()
        group_timestamp = generate_timestamp(start_date, end_date)
        is_sql_injection = random.choice([True, False])
        if is_sql_injection:
            sql_injection_count += 1

        for _ in range(random.randint(1, 3)):  # 1 to 3 trials per group
            log_entry = generate_log_entry(group_ip, group_timestamp, is_sql_injection)
            logs.append(log_entry)
            secounds = (int)(random.randint(1, 300))
            group_timestamp += timedelta(seconds=secounds)  # Increment time

    # Sort logs by date and time
    logs.sort(key=lambda x: datetime.strptime(x["Date"] + " " + x["Time"], "%d/%b/%Y %H:%M:%S"))

    # Write logs to CSV
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Date", "Time", "IP_Address", "HTTP_Method", "URL", "HTTP_Version", "Status", "Referer", "User_Agent", "Additional_Data", "Is_SQL_Injection"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(logs)

    print(f"Generated {len(logs)} logs with {sql_injection_count} SQL injection attempts.")


# Example usage
generate_csv("generated_logs.csv", group_count=10000)
