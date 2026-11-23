from pathlib import Path
from dotenv import load_dotenv  # Permette di caricare API key definita nel file .env
import os  # Permette di leggere le variabili d'ambiente
import requests  # Permette di effettuare richieste HTTP verso le API di eLabFTW

# Carica le variabili dal file .env nella root della repository
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# Configurazione del server
server_url = os.getenv("ELAB_URL")
api_key = os.getenv("ELAB_API_KEY")

# Controlla che le variabili di ambiente siano popolate
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
