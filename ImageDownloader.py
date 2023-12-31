import scrapy
import json
import os


class GoogleImagesSpider(scrapy.Spider):
    name = 'google_images'

    def __init__(self, query='', num_images=5, *args, **kwargs):
        super(GoogleImagesSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.num_images = int(num_images)
        self.start_urls = [f'https://www.google.com/search?q={self.query}&tbm=isch']

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
