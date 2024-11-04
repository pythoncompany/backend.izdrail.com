from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import json
import os

router = APIRouter()

class ScrapperAction(BaseModel):
    network: str
    query: str

@router.post("/run/scrapper")
def run_cli(scrapper: ScrapperAction):
    skraper_path = '/usr/local/bin/skraper'

    # Check if file exists and is executable
    if not os.path.exists(skraper_path):
        return {"error": "Skraper binary not found"}
    if not os.access(skraper_path, os.X_OK):
        return {"error": "Skraper binary not executable"}

    try:
        # Run the original command
        result = subprocess.run(
            [skraper_path, scrapper.network, scrapper.query, '-t', 'json'],
            capture_output=True,
            text=True,
            check=True
        )

        # Extract the file path from the output
        for line in result.stdout.split('\n'):
            if "has been written to" in line:
                file_path = line.split("has been written to ")[-1].strip()
                print(file_path)

                # Open and load JSON data from the file path
                try:
                    with open(file_path, 'r') as json_file:
                        json_data = json.load(json_file)
                    return {
                        "execution_log": result.stdout,
                        "scraped_data": json_data
                    }
                except FileNotFoundError:
                    return {"error": f"Generated file not found at {file_path}"}
                except json.JSONDecodeError:
                    return {"error": "Failed to parse generated JSON file"}

        return {"error": "Could not find generated file path in output"}
    except subprocess.CalledProcessError as e:
        return {"error": f"Command failed: {e.stderr}"}
