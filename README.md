# Discord Bot DALL·E

A discord bot that uses OpenAI's DALL·E 2 API to generate AI images from a text prompt and create variations and edits of a picture.


## Slash Commands
* `/dalle [prompt]` - Generate an image from the text prompt
* `/var [image]` - Create a variation of the image sent
* `/edit [original_image] [mask] [prompt]` - Generate a completion to transparent areas in [mask] from the text prompt


## Setup
* Install the requirements using `pip install -r requirements.txt`
* Rename `.env-keys` to `.env` and store your Discord bot token and OpenAI API key
* Run `python main.py` to start the Discord bot
