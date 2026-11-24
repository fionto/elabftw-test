import json
import mimetypes
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

# Safety switch: set True to create the experiment and upload the data file
CREATE_EXPERIMENT = True

# Input files (DATA_FILE can be a .csv or .txt raw measurement file)
METADATA_FILE = SCRIPT_DIR / "experiment_metadata.json"
DATA_FILE = SCRIPT_DIR / "20 kV@ +0,00V.txt"

# Optional: set to a team name (e.g., "Axial Lab") to share read access with the team,
# or leave as None for default experiment visibility.
TARGET_TEAM_NAME = "Axial Lab"


def get_team_id_by_name(team_name: str) -> int:
    """Retrieve the ID of the specified team from the authenticated user's profile."""
    response = requests.get(
        f"{base_url}/users/me",
        headers={"Authorization": api_key, "Accept": "application/json"},
        timeout=30,
    )
    response.raise_for_status()

    user_info = response.json()
    for team in user_info.get("teams", []):
        if isinstance(team, dict) and team.get("name") == team_name:
            return int(team["id"])

    raise ValueError(f"Team '{team_name}' not found for the authenticated user.")


def main() -> None:
    if not METADATA_FILE.is_file():
        raise FileNotFoundError(f"Metadata file not found: {METADATA_FILE}")
    if not DATA_FILE.is_file():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        prepared = json.load(f)

    # Build API payload for experiment creation
    payload = {
        "template": prepared["template_id"],
        "title": prepared["title"],
        "metadata": prepared["metadata"],
        "body": prepared.get("body_html", ""),
        "content_type": 1,
    }

    if TARGET_TEAM_NAME:
        team_id = get_team_id_by_name(TARGET_TEAM_NAME)
        payload["canread"] = json.dumps({"teams": [team_id], "users": [], "teamgroups": []})
        payload["canwrite"] = json.dumps({"teams": [], "users": [], "teamgroups": []})
        print(f"Team '{TARGET_TEAM_NAME}' found with ID: {team_id}")

    print("\n=== EXPERIMENT PAYLOAD ===")
    print(json.dumps(payload, indent=4, ensure_ascii=False))
    print(f"\nData file to upload: {DATA_FILE.name} ({DATA_FILE.stat().st_size} bytes)")

    if not CREATE_EXPERIMENT:
        print("\nDRY RUN: no experiment created and no file uploaded.")
        print("Fill in experiment_metadata.json and set CREATE_EXPERIMENT = True to submit.")
        return

    # 1. Create experiment on eLabFTW
    json_headers = {
        "Authorization": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.post(
        f"{base_url}/experiments",
        headers=json_headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()

    location = response.headers.get("Location")
    if not location:
        raise RuntimeError("Experiment created, but 'Location' header was missing in response.")

    experiment_id = location.rstrip("/").split("/")[-1]
    print("\nExperiment created successfully!")
    print("HTTP status:", response.status_code)
    print("Experiment ID:", experiment_id)
    print("Experiment URL:", location)

    # 2. Upload the raw data file to the newly created experiment
    # Note: do NOT set Content-Type manually when using files=...; requests sets multipart/form-data.
    upload_headers = {
        "Authorization": api_key,
        "Accept": "application/json",
    }
    mime_type, _ = mimetypes.guess_type(DATA_FILE.name)
    mime_type = mime_type or "text/csv"

    with open(DATA_FILE, "rb") as f:
        files = {"file": (DATA_FILE.name, f, mime_type)}
        upload_response = requests.post(
            f"{base_url}/experiments/{experiment_id}/uploads",
            headers=upload_headers,
            files=files,
            timeout=60,
        )
    upload_response.raise_for_status()

    print("\nData file uploaded successfully!")
    print("HTTP status:", upload_response.status_code)
    try:
        print("Upload response:", json.dumps(upload_response.json(), indent=4, ensure_ascii=False))
    except ValueError:
        pass


if __name__ == "__main__":
    main()
