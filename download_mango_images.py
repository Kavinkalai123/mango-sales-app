import requests
import os
from pathlib import Path

# Pixabay API key (free, get from https://pixabay.com/api/docs/)
API_KEY = "YOUR_PIXABAY_API_KEY"  # Replace with your key
SEARCH_TERM = "mango fruit"
NUM_IMAGES = 10

def download_mango_images():
    """Download mango images from Pixabay API"""
    url = f"https://pixabay.com/api/?key={API_KEY}&q={SEARCH_TERM}&image_type=photo&per_page={NUM_IMAGES}"

    response = requests.get(url)
    data = response.json()

    if 'hits' not in data:
        print("Error: Could not fetch images. Check API key.")
        return

    images_dir = Path(__file__).resolve().parent / "uploads" / "mango_images"
    images_dir.mkdir(parents=True, exist_ok=True)

    for i, hit in enumerate(data['hits'], 1):
        image_url = hit['largeImageURL']
        image_response = requests.get(image_url)

        filename = f"mango_{i}.jpg"
        filepath = images_dir / filename

        with open(filepath, 'wb') as f:
            f.write(image_response.content)

        print(f"Downloaded {filename}")

    print(f"Downloaded {len(data['hits'])} mango images to {images_dir}")

if __name__ == "__main__":
    download_mango_images()