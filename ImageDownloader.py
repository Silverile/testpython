import requests
from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import Entry, Button, Label
import threading


def fetch_images(query, limit):
    print(f"Starting to fetch images for query: {query}")
    url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    desktop = os.path.expanduser("~/Desktop")
    folder_path = os.path.join(desktop, query)

    img_tags = soup.find_all("img")[:limit]

    os.makedirs(folder_path, exist_ok=True)

    downloaded = 0
    for i, img_tag in enumerate(img_tags):
        img_url = img_tag.get("src")
        if img_url.startswith("http"):
            img_data = requests.get(img_url).content
            with open(os.path.join(folder_path, f"{query}_{i}.jpg"), "wb") as f:
                f.write(img_data)
            downloaded += 1
            print(f"Downloaded {downloaded} of {limit} images.")

    print(f"Finished downloading {downloaded} images for query: {query}")


# Function to be called when the button is clicked
def on_button_click():
    query = query_entry.get()
    limit = int(limit_entry.get())
    threading.Thread(target=fetch_images, args=(query, limit)).start()


# Create the main window
root = tk.Tk()
root.title("Image Downloader")

# Create widgets
query_label = Label(root, text="Enter Query:")
query_entry = Entry(root)
limit_label = Label(root, text="Enter Limit:")
limit_entry = Entry(root)
search_button = Button(root, text="Search", command=on_button_click)

# Place widgets on the grid
query_label.grid(row=0, column=0)
query_entry.grid(row=0, column=1)
limit_label.grid(row=1, column=0)
limit_entry.grid(row=1, column=1)
search_button.grid(row=2, columnspan=2)

# Run the Tkinter event loop
root.mainloop()
