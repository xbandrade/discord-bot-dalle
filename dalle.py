import os
import urllib.request

import openai
from dotenv import load_dotenv


class Dalle:
    def __init__(self, prompt='image_variation', mask=None, input_image=None, img_size=256, n_images=1):
        self._output_location = './output'
        self._img_size = img_size
        self._n_images = n_images
        self._input_image = input_image
        self._image_url = None
        self._prompt = prompt
        self._mask = mask
        self._response = None
        self.initialize_api()

    def initialize_api(self):
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_KEY')

    def _generate_image(self):
        self._response = openai.Image.create(
            prompt=self._prompt,
            n=self._n_images,
            size=f'{self._img_size}x{self._img_size}',
        )

    def _image_variation(self):
        self._response = openai.Image.create_variation(
            image=open(self._input_image, 'rb'),
            n=self._n_images,
            size=f'{self._img_size}x{self._img_size}',
        )

    def _edit_with_mask(self):
        self._response = openai.Image.create_edit(
            image=open(self._input_image, 'rb'),
            mask=open(self._mask, 'rb'),
            prompt=self._prompt,
            n=self._n_images,
            size=f'{self._img_size}x{self._img_size}',
        )

    def save_url_as_image(self):
        self._image_url = self._response['data'][0]['url']
        if not os.path.isdir(self._output_location):
            os.mkdir(self._output_location)
        file_name = f'{self._output_location}\\{self._prompt}.png'
        urllib.request.urlretrieve(self._image_url, file_name)

    def generate_from_prompt(self):
        self._generate_image()
        self.save_url_as_image()

    def create_image_variation(self):
        self._image_variation()
        self.save_url_as_image()

    def create_edit_from_mask(self):
        self._edit_with_mask()
        self.save_url_as_image()
