import requests
from bs4 import BeautifulSoup
import os
import json


def fetch_images(query, limit):
    print(f"Starting to fetch images for query: {query}")
    url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    img_tags = soup.find_all("img")[:limit]

    os.makedirs("./randompics", exist_ok=True)

    downloaded = 0
    for i, img_tag in enumerate(img_tags):
        img_url = img_tag.get("src")
        if img_url.startswith("http"):
            img_data = requests.get(img_url).content
            with open(f"./randompics/{query}_{i}.jpg", "wb") as f:
                f.write(img_data)
            downloaded += 1
            print(f"Downloaded {downloaded} of {limit} images.")

    print(f"Finished downloading {downloaded} images for query: {query}")


# Fetch 10 random object images
fetch_images("objects", 11)
