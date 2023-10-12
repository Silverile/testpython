import scrapy
import json
import os


class GoogleImagesSpider(scrapy.Spider):
    name = 'google_images'

    def __init__(self, query='', num_images=5, *args, **kwargs):
        super(GoogleImagesSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.num_images = int(num_images)

    def start_requests(self):
        # Google image search URL
        google_url = f'https://www.google.com/search?q={self.query}&tbm=isch'

        # Additional URLs for example
        additional_urls = [
            'http://example.com/page1',
            'http://example.com/page2',
        ]

        # Create requests for Google image search
        yield scrapy.Request(google_url, self.parse, meta={'proxy': 'http://your_proxy_here'})

        # Create requests for additional URLs
        for url in additional_urls:
            yield scrapy.Request(url, self.parse, meta={'proxy': 'http://your_proxy_here'})

    def parse(self, response):
        # Extract image URLs from JavaScript data
        page_script = response.xpath('//script[contains(., "_setImagesSrc")]/text()').extract_first()
        start_idx = page_script.find('AF_initDataCallback(') + len('AF_initDataCallback(')
        end_idx = page_script.find('}]});') + len('}]});')
        json_data = json.loads(page_script[start_idx:end_idx])
        img_urls = [img[-1][0] for img in json_data['afData']]

        # Create folder to save images
        folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', self.query)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Download images
        for i, img_url in enumerate(img_urls[:self.num_images]):
            yield scrapy.Request(img_url, callback=self.save_image, meta={'folder_path': folder_path, 'img_num': i})

    def save_image(self, response):
        folder_path = response.meta['folder_path']
        img_num = response.meta['img_num']
        img_name = f"{self.query}_{img_num}.jpg"
        img_path = os.path.join(folder_path, img_name)
        with open(img_path, 'wb') as img_file:
            img_file.write(response.body)
