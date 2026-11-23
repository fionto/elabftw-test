
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Load prepared experiment
with open("prepared_experiment.json", "r", encoding="utf-8") as f:
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