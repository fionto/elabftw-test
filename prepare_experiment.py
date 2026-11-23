
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
}

# Retrieve template
template_id = 6

response = requests.get(
    f"{base_url}/experiments_templates/{template_id}",
    headers=headers,
    timeout=30,
)

response.raise_for_status()
template = response.json()

# Parse template metadata
metadata = json.loads(template["metadata"])

# Define test values
sample_data = {
    "Sample_ID": "DEV-001",
    "Device_Type": "Diode",
    "Operator": "Test User",

    "Instrument": "Keithley 2470",
    "Instrument_ID": "K2470-001",
    "Measurement_Mode": "Source V / Measure I",
    "Connection": "USB",

    "Sweep_Type": "Forward_Backward",
    "V_Start": "-1",
    "V_Stop": "1",
    "V_Step": "0.01",
    "I_Compliance": "0.001",
    "NPLC": "1",
    "N_Sweeps": "1",

    "Measurement_Status": "Completed",
    "Data_File": "DEV-001_IV_test.csv"
}

# Fill custom fields
extra_fields = metadata["extra_fields"]

for field_name, value in sample_data.items():
    if field_name not in extra_fields:
        raise KeyError(f"Field not found in template: {field_name}")

    extra_fields[field_name]["value"] = value

# Prepare output
output = {
    "template_id": template_id,
    "title": "I(V) Measurement - DEV-001",
    "metadata": metadata,
    "body_html": template.get("body_html", ""),
}

# Save prepared experiment
with open("prepared_experiment.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("Experiment prepared successfully!")
print("Output saved to prepared_experiment.json")
