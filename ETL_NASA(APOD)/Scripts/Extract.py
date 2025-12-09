"""
extract_apod.py
Extract NASA Astronomy Picture of the Day (APOD) and save JSON + image.
"""

import os
import json
from pathlib import Path
from datetime import datetime
import requests
from dotenv import load_dotenv

# ----------------------------
# Load .env file
# ----------------------------
load_dotenv()

# ----------------------------
# Setup directories
# ----------------------------
DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Read key from environment
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")


def extract_apod(date: str = None, hd: bool = True):
    """
    Fetch NASA APOD for a given date (YYYY-MM-DD) or today's date.
    Saves:
        • JSON metadata
        • Image file (if media_type == 'image')
    """
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": NASA_API_KEY,
        "hd": str(hd).lower()
    }

    if date:
        params["date"] = date

    # Request APOD
    print("Requesting APOD with params:", params)
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()

    data = resp.json()

    # ---------------------------------------------
    # Save JSON metadata
    # ---------------------------------------------
    json_filename = DATA_DIR / f"apod_{datetime.now().strftime('%y%m%d_%H%M%S')}.json"
    json_filename.write_text(json.dumps(data, indent=2))

    print(f"APOD JSON saved → {json_filename}")

    # ---------------------------------------------
    # Download image (only if APOD is an image)
    # ---------------------------------------------
    if data.get("media_type") == "image":
        img_url = data.get("hdurl") or data.get("url")
        ext = Path(img_url).suffix or ".jpg"

        image_filename = DATA_DIR / f"apod_image_{datetime.now().strftime('%y%m%d_%H%M%S')}{ext}"

        img_resp = requests.get(img_url, stream=True)
        img_resp.raise_for_status()

        with open(image_filename, "wb") as f:
            for chunk in img_resp.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"APOD Image downloaded → {image_filename}")
        data["_saved_image"] = str(image_filename)

    else:
        print("APOD is not an image (Video/YouTube). No image saved.")

    return data


# Run directly
if __name__ == "__main__":
    extract_apod()  # Fetch today's APOD
