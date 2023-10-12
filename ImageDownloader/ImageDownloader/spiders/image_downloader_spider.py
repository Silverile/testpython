import scrapy
import os
import random


class GoogleImagesSpider(scrapy.Spider):
    name = 'google_images'

    def __init__(self, query='', num_images=5, *args, **kwargs):
        super(GoogleImagesSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.num_images = int(num_images)
        self.proxies = [
            'http://37.19.220.129:8443',
            'http://52.71.249.112:80',
            'http://138.199.48.1:8443',
            'http://138.199.48.4:8443',
            'http://67.217.61.162:80',
            'http://192.240.106.146:3128',
            'http://64.189.106.6:3129',
            'http://107.175.243.183:80',
            'http://23.152.40.14:3128',
            'http://144.24.181.61:3128',
            'http://43.157.10.238:8888',
            'http://164.215.103.30:3128',
        ]

    def start_requests(self):
        # Google image search URL
        google_url = f'https://www.google.com/search?q={self.query}&tbm=isch'
        # Create requests for Google image search
        yield scrapy.Request(google_url, self.parse, meta={'proxy': random.choice(self.proxies)})

    def save_image(self, response):
        folder_path = response.meta['folder_path']
        img_num = response.meta['img_num']
        img_name = f"{self.query}_{img_num}.jpg"
        img_path = os.path.join(folder_path, img_name)
        with open(img_path, 'wb') as img_file:
            img_file.write(response.body)
