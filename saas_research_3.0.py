import pandas as pd
import requests
from bs4 import BeautifulSoup
import threading
import queue
import time

NUM_THREADS = 1000
saas_words = ["SaaS", "Software as a service", "Software application", "software", "application", "app", "cloud", "Cloud", "service", "Service", "platform", "Platform", "software-as-a-service", "Software-as-a-service", "saas"]

def get_text(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f'Error in domain : {e}')
        return ""

def check_saas(url):
    text = get_text(url)
    if any(word in text for word in saas_words):
        print(f'{url} contains SaaS adding to the queue')
        return True
    return False

def worker():
    while True:
        url = q.get()
        if check_saas(url):
            with open("new_saas_test.csv", "a") as f:
                for i in range(len(df)):
                    if df.loc[i, 'Website'] == url:
                        f.write(f"{url},{df.loc[i, 'Industries']}" + "\n")
        q.task_done()

q = queue.Queue()
for i in range(NUM_THREADS):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

df = pd.read_csv("need_to_find_new_saas.csv")
for url in df["Website"]:
    q.put(url)

q.join()