import pandas as pd
import torch.nn as nn
import random
from datetime import datetime, timedelta

def read_form_csv_and_return_data_with_label(input_csv, group_column_index, extract_columns):

    csv_file = pd.read_csv(input_csv, header=None)

    csv_file[extract_columns[0]] = csv_file[extract_columns[0]].fillna("").astype(str)

    grouped = csv_file.groupby(csv_file[group_column_index])

    concatenated_payloads = (
        grouped[extract_columns[0]]
        .apply(lambda x: " ".join(filter(None, map(str.strip, x))).strip())
        .tolist()
    )

    labels = grouped[extract_columns[1]].first().tolist()
    return concatenated_payloads, labels

used_ips = []
def generate_unique_ip():
    while True:
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        if ip not in used_ips:
            return ip
     
def generate_timestamp(start_date, end_date):
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

class MultiClassificationModel(nn.Module):
    def __init__(self, input_dim, num_classes):
        super(MultiClassificationModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, num_classes)
        )

    def forward(self, x):
        return self.network(x)

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
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /transaction", "POST /transaction", "GET /transakcja,e9da7ade10sadasdsadsad4a18ef129f7e17fd5", "POST /transakcja,e9da7ade10sadasdsadsad4a18ef129f7e17fd5"],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /transaction", "POST /transaction", "GET /transakcja,e9da7ade10sadasdsadsad4a18ef12seryyti634", "POST /transakcja,e9da7ade10sadasdsadsad4a18ef12seryyti634", "GET /transakcja,sdfsdfsadasdsa676934ad4a18ef12serhej689087", "POST /transakcja,sdfsdfsadasdsa676934ad4a18ef12serhej689087"],
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

bruteforce_patterns = [
    ["GET /dashboard", "GET /logowanie"] + ["POST /logowanie" for _ in range(5, random.randint(5, 20))],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /resetpassword"] + ["POST /resetpassword" for _ in range(5, random.randint(5, 20))],
    ["GET /dashboard", "GET /rejestracja"] + ["POST /rejestracja" for _ in range(5, random.randint(5, 20))],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /transaction"] + ["POST /transaction" for _ in range(5, random.randint(5, 20))],
    ["GET /dashboard", "GET /logowanie", "POST /logowanie", "GET /transaction", "POST /transaction", "GET /transakcja,e9da7ade10sadasdsadsad4a18ef129f7e17fd5"] + ["POST /transakcja,e9da7ade10sadasdsadsad4a18ef129f7e17fd5" for _ in range(5, random.randint(5, 20))],
]

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