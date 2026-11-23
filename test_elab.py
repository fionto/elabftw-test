import os
import requests
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

# Configurazione del server
server_url = os.getenv("ELAB_URL")
api_key = os.getenv("ELAB_API_KEY")

if not server_url or not api_key:
    raise ValueError(
        "Controlla ELAB_URL e ELAB_API_KEY nel file .env"
    )

base_url = server_url.rstrip("/") + "/api/v2"

headers = {
    "Authorization": api_key,
    "Accept": "application/json",
}

# Prima richiesta: leggi gli esperimenti
response = requests.get(
    f"{base_url}/experiments",
    headers=headers,
    params={"limit": 5},
    timeout=30,
)

response.raise_for_status()

experiments = response.json()

print("Connessione a eLabFTW riuscita!")
print(f"Esperimenti ricevuti: {len(experiments)}")

for experiment in experiments:
    print(
        f"ID: {experiment.get('id')} | "
        f"Titolo: {experiment.get('title')}"
    )
