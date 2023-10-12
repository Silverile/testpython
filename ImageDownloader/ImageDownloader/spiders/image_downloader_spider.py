import logging

import scrapy
import os
from urllib.parse import parse_qs, urlparse


class YandexImagesSpider(scrapy.Spider):
    name = 'yandex_images'

    def __init__(self, query='', num_images=5, *args, **kwargs):
        super(YandexImagesSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.num_images = int(num_images)

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537'
        }
        yandex_url = f'https://yandex.com/images/search?text={self.query}'
        yield scrapy.Request(yandex_url, self.parse, headers=headers)

    def parse(self, response):
        logging.info("Visited %s", response.url)

        # Updated CSS selector to match the new class
        yandex_urls = response.css('a.serp-item__link::attr(href)').extract()
        image_urls = []

        for yandex_url in yandex_urls:
            parsed_url = urlparse(yandex_url)
            query_params = parse_qs(parsed_url.query)
            if 'img_url' in query_params:
                image_url = query_params['img_url'][0]
                image_urls.append(image_url)

        logging.info("Extracted image URLs: %s", image_urls)

        # Create folder to save images
        folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', self.query)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logging.info("Created folder at %s", folder_path)

        # Download images
        for i, img_url in enumerate(image_urls[:self.num_images]):
            logging.info("Downloading image %d from URL: %s", i+1, img_url)
            yield scrapy.Request(img_url, callback=self.save_image, meta={'folder_path': folder_path, 'img_num': i})

    def save_image(self, response):
        folder_path = response.meta['folder_path']
        img_num = response.meta['img_num']
        img_name = f"{self.query}_{img_num}.jpg"
        img_path = os.path.join(folder_path, img_name)
        with open(img_path, 'wb') as img_file:
            img_file.write(response.body)
            self.logger.info("Saved image to %s", img_path)
