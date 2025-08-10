import requests, time, random


def make_request_with_retry(cleaned_number, url, headers, max_retries=3):
    files = {"searchNumber": (None, cleaned_number)}

    for attempt in range(max_retries):
        try:
            response = requests.post(url, files=files, headers=headers, timeout=15)
            if response.status_code == 200:
                return response
            print(f"[!] HTTP {response.status_code} on attempt {attempt+1} for {cleaned_number}")
        except Exception as e:
            print(f"[!] Error on attempt {attempt+1} for {cleaned_number}: {e}")
        
        time.sleep(random.uniform(1.5, 3))  # backoff

    return None  # when all retries failed
