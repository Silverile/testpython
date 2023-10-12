import tkinter as tk
from threading import Thread
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from ImageDownloader.spiders.image_downloader_spider import GoogleImagesSpider  # Import your spider here


def start_crawl(query, num_images):
    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl(GoogleImagesSpider, query=query, num_images=num_images)
    d.addBoth(lambda _: reactor.stop())
    reactor.run(installSignalHandlers=0)  # Disable signal handlers


def on_button_click():
    query = query_entry.get()
    num_images = num_images_entry.get()
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
