import csv
import random
from datetime import datetime, timedelta

# Define a function to generate random IP addresses
used_ips = []
def generate_ip():
    while True:
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        if ip not in used_ips:
            return ip
     

# Define a function to generate random timestamps
def generate_timestamp(start_date, end_date):
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

# Define log patterns
valid_patterns = [
    ["GET /dashboard"],
    ["GET /dashboard", "GET /logowanie"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "POST /logowanie"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "POST /logowanie", "POST /logowanie"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /resetpassword", "POST /resetpassword"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /resetpassword", "POST /resetpassword", "POST /resetpassword"],
    ["GET /dashboard", "GET /rejestracja", "POST /rejestracja"],
    ["GET /dashboard", "GET /rejestracja", "POST /rejestracja", "GET /logowanie", "POST /logowanie"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /settings"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /profile"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /transaction", "POST /transaction"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /transaction", "POST /transaction", "POST /transaction"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /transaction", "POST /transaction", "GET /dashboard"],
]

injection_patterns = [
    ["GET /dashboard", "GET /logowanie", "POST /logowanie"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "POST /logowanie"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "POST /logowanie", "POST /logowanie"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /resetpassword", "POST /resetpassword"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /resetpassword", "POST /resetpassword", "POST /resetpassword"],
    ["GET /dashboard", "GET /rejestracja", "POST /rejestracja"],
    ["GET /dashboard", "GET /rejestracja", "POST /rejestracja", "GET /logowanie", "POST /logowanie"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /settings"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /profile"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /transaction", "POST /transaction"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /transaction", "POST /transaction", "POST /transaction"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /transaction", "POST /transaction", "GET /dashboard"],
]

# Templates for valid and SQL injection payloads
def generate_log_entry(ip, timestamp, url, http_method, is_sql_injection, user_agent):
    referrers = [
        "https://kingbank.pl/", 
        "https://kingbank.pl/logowanie", 
        "https://kingbank.pl/dashboard",
        "https://kingbank.pl/profile",
        "https://kingbank.pl/settings"
    ]

    valid_payloads = {
        "/logowanie": "login=user{}&password=&action=login",
        "/resetpassword": "email=user{}@example.com&action=resetpassword",
        "/transakcja": "recipientAccount=97+8817+1010+{}+5548+0858+2750&recipientName=EduProgress+Polska&street=ul.+Promienna&houseNumber=27&apartmentNumber=13&postalCode={}&city=Kasztan%C3%B3w&transferTitle=Wynajem+salki+konferencyjnej&action=send&savedRecipient=1",
        "/profile": "profile_id={}&update=address",
        "/settings": "setting=darkmode&enabled=true",
        "/rejestracja": "firstName=user{}&lastName=user{}&email=user{}mouse780@onet.pl&password=&confirmPassword=&dataConsent=1&action=register"
    }

    sql_injections = [
        "login=test' OR '1'='1'--&password=&action=login",
        "search=test' UNION SELECT NULL,NULL,NULL;--",
        "username=admin'--",
        "id=1 OR 1=1;--",
        "email=test@example.com' AND 1=2 UNION SELECT 'a', 'b', 'c';--",
        "name=xyz' OR 'a'='a'/*",
        "product_id=1; DROP TABLE users;--",
        "order_id=1' UNION ALL SELECT NULL, NULL, NULL;--",
        "user=admin' EXEC xp_cmdshell('dir');--",
        "session_id=1' WAITFOR DELAY '0:0:5';--",
        "item_id=1' OR '1'='1';--",
        "search=\"; DROP TABLE orders;--",
        "password=' OR 1=1;--",
        "input=\" UNION ALL SELECT username, password FROM users;--"
    ]

    additional_data = ""
    if is_sql_injection and http_method == "POST":
        additional_data = random.choice(sql_injections)
    elif http_method == "POST" and url in valid_payloads:
        additional_data = valid_payloads[url].format(
            random.randint(1000, 9999), random.randint(1, 100), random.uniform(0.1, 999.9),
            random.randint(100, 999)
        )

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
        "Additional_Data": additional_data if http_method == "POST" else "",
        "Is_SQL_Injection": 1 if is_sql_injection else 0
    }

# Main function to generate CSV file
def generate_csv(filename, group_count):
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 1, 10)

    logs = []
    sql_injection_count = 0

    for i in range(group_count):
        if i % 1000 == 0:
            print(i)

        group_ip = generate_ip()
        group_timestamp = generate_timestamp(start_date, end_date)
        user_agent = "Mozilla/5.0 (Group {}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36".format(random.randint(1000, 9999))
        is_sql_injection = random.choice([False, False, False, True])
        group_patterns = []
        if is_sql_injection:
            sql_injection_count += 1
            group_patterns = random.sample(injection_patterns, random.randint(1, 5))
        else:
            group_patterns = random.sample(valid_patterns, random.randint(1, 5))

        for pattern in group_patterns:
            for action in pattern:
                http_method, url = action.split()
                log_entry = generate_log_entry(group_ip, group_timestamp, url, http_method, is_sql_injection, user_agent)
                logs.append(log_entry)
                group_timestamp += timedelta(seconds=random.randint(1, 300))  # Increment time

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
generate_csv("generated_logs.csv", group_count=10000) # 4956
