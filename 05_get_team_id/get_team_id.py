from pathlib import Path
import json
import os
from dotenv import load_dotenv
import requests

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

# Recupera il profilo dell'utente autenticato (inclusi i team associati)
response = requests.get(
    f"{base_url}/users/me",
    headers=headers,
    timeout=30,
)

response.raise_for_status()

user_info = response.json()

print("Profilo utente recuperato con successo!")
print(f"Utente: {user_info.get('fullname')} (ID: {user_info.get('userid')})")

# In eLabFTW API v2, i team dell'utente sono presenti nel campo 'teams'
teams = user_info.get("teams", [])

if teams:
    print(f"\nTeam trovati ({len(teams)}):")
    for team in teams:
        if isinstance(team, dict):
            print(f"  - ID: {team.get('id')} | Nome: {team.get('name')}")
        else:
            print(f"  - Team: {team}")
else:
    # Fallback nel caso il campo abbia un formato diverso (es. 'team')
    print("\nNessuna lista 'teams' trovata. Dati grezzi rilevanti:")
    print(json.dumps({k: v for k, v in user_info.items() if "team" in k.lower()}, indent=2, ensure_ascii=False))
