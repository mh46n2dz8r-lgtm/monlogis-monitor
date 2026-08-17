import hashlib
import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.monlogis.ch/vacants"
STATE_FILE = "state.txt"
NTFY_TOPIC = os.environ["NTFY_TOPIC"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

text = soup.get_text(" ", strip=True)
text = " ".join(text.split())

current_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

old_hash = None

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        old_hash = f.read().strip()

if old_hash is None:
    print("Premier lancement : création de la référence.")

elif current_hash != old_hash:
    print("Changement détecté !")

    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data="La page Mon Logis VACANTS a changé !",
        headers={
            "Title": "Mon Logis",
            "Click": URL,
            "Priority": "high"
        },
        timeout=30
    )

else:
    print("Aucun changement.")

with open(STATE_FILE, "w") as f:
    f.write(current_hash)
