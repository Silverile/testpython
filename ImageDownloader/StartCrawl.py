import tkinter as tk
from threading import Thread
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from ImageDownloader.spiders.image_downloader_spider import YandexImagesSpider  # Import your spider here


# scrapy crawl yandex_images -a query="eva elfie" -a num_images=2

def start_crawl(query, num_images):
    print("Starting crawl")  # Debugging line
    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl(YandexImagesSpider, query=query, num_images=num_images)
    d.addBoth(lambda _: reactor.stop())
    reactor.run(installSignalHandlers=0)  # Disable signal handlers
    print("Crawl finished")  # Debugging line


def on_button_click():
    query = query_entry.get()
    num_images = num_images_entry.get()
    print(f"Query: {query}, Num Images: {num_images}")  # Debugging line
    t = Thread(target=start_crawl, args=(query, num_images))
    t.start()


root = tk.Tk()
root.title("Scrapy UI")

query_label = tk.Label(root, text="Query:")
query_label.pack()
query_entry = tk.Entry(root)
query_entry.pack()

num_images_label = tk.Label(root, text="Number of Images:")
num_images_label.pack()
num_images_entry = tk.Entry(root)
num_images_entry.pack()

start_button = tk.Button(root, text="Start Scraping", command=on_button_click)
start_button.pack()

root.mainloop()
