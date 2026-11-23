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
}

# 1. Retrieve accessible experiment templates
response = requests.get(
    f"{base_url}/experiments_templates",
    headers=headers,
    params={"limit": 100, "full": 1},
    timeout=30,
)

response.raise_for_status()
templates = response.json()

# 2. Display available templates
print("\n=== AVAILABLE EXPERIMENT TEMPLATES ===")

for template in templates:
    print(
        f"ID: {template.get('id')} | "
        f"Title: {template.get('title')}"
    )

# 3. Find our template
target = [
    t for t in templates
    if "IV_K2470" in t.get("title", "")
]

if not target:
    print("\nTemplate IV_K2470 not found.")
    print("Check its title or template visibility.")
    raise SystemExit

# 4. Retrieve full template details
template_id = target[0]["id"]

response = requests.get(
    f"{base_url}/experiments_templates/{template_id}",
    headers=headers,
    timeout=30,
)

response.raise_for_status()
template_details = response.json()


# 5. Parse metadata JSON string into a Python dictionary
metadata = json.loads(template_details.get("metadata", "{}"))

# 6. Extract template structure
output = {
    "id": template_details.get("id"),
    "title": template_details.get("title"),
    "groups": metadata.get("elabftw", {}).get("extra_fields_groups", []),
    "extra_fields": metadata.get("extra_fields", {}),
    "body_html": template_details.get("body_html"),
}

# 7. Print formatted JSON
print("\n=== TEMPLATE DETAILS ===")
print(json.dumps(output, indent=4, ensure_ascii=False))

# 8. Save structured JSON file in the script's directory
output_file = SCRIPT_DIR / "template_structure.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print(f"\nStructure saved to {output_file}")