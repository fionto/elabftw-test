
import os
import json
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

# Safety switch: set True to create the experiment
CREATE_EXPERIMENT = True

# Load prepared experiment from step 03
input_file = ROOT_DIR / "03_prepare_experiment" / "prepared_experiment.json"
with open(input_file, "r", encoding="utf-8") as f:
    prepared = json.load(f)

# Build API payload
payload = {
    "template": prepared["template_id"],
    "title": prepared["title"],
    "metadata": prepared["metadata"],
    "body": prepared["body_html"],
    "content_type": 1,
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

    # Retrieve created experiment information
    location = response.headers.get("Location")

    print("\nExperiment created successfully!")
    print("HTTP status:", response.status_code)
    print("Experiment URL:", location)