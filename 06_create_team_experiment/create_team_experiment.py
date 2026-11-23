import json
import os
from pathlib import Path
import requests
from dotenv import load_dotenv

# Directory paths
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

# Load environment variables from repository root
load_dotenv(ROOT_DIR / ".env")

# Server configuration
server_url = os.getenv("ELAB_URL")
api_key = os.getenv("ELAB_API_KEY")

if not server_url or not api_key:
    raise ValueError("Check ELAB_URL and ELAB_API_KEY in .env")

base_url = server_url.rstrip("/") + "/api/v2"

headers = {
    "Authorization": api_key,
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# Target team name and safety switch
TARGET_TEAM_NAME = "Axial Lab"
CREATE_EXPERIMENT = True


def get_team_id_by_name(team_name: str) -> int:
    """Retrieve the ID of the specified team from the authenticated user's profile."""
    response = requests.get(
        f"{base_url}/users/me",
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    user_info = response.json()
    for team in user_info.get("teams", []):
        if isinstance(team, dict) and team.get("name") == team_name:
            return int(team["id"])

    raise ValueError(f"Team '{team_name}' not found for the authenticated user.")


# 1. Dynamically retrieve the team ID for "Axial Lab"
team_id = get_team_id_by_name(TARGET_TEAM_NAME)
print(f"Team '{TARGET_TEAM_NAME}' found with ID: {team_id}")

# 2. Load prepared experiment from step 03
input_file = ROOT_DIR / "03_prepare_experiment" / "prepared_experiment.json"
with open(input_file, "r", encoding="utf-8") as f:
    prepared = json.load(f)

# 3. Configure visibility: readable by the team, writable only by the creator
canread = json.dumps({"teams": [team_id], "users": [], "teamgroups": []})
canwrite = json.dumps({"teams": [], "users": [], "teamgroups": []})

# 4. Build API payload
payload = {
    "template": prepared["template_id"],
    "title": prepared["title"],
    "metadata": prepared["metadata"],
    "body": prepared["body_html"],
    "content_type": 1,
    "canread": canread,
    "canwrite": canwrite,
}

# Display payload before submission
print("\n=== EXPERIMENT PAYLOAD ===")
print(json.dumps(payload, indent=4, ensure_ascii=False))

if not CREATE_EXPERIMENT:
    print("\nDRY RUN: no experiment created.")
    print("Set CREATE_EXPERIMENT = True to submit to eLabFTW.")
else:
    # Create experiment on eLabFTW
    response = requests.post(
        f"{base_url}/experiments",
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()

    location = response.headers.get("Location")
    print("\nExperiment created successfully!")
    print("HTTP status:", response.status_code)
    print("Experiment URL:", location)
