import os

import discord
from dotenv import load_dotenv
from PIL import Image

from dalle import Dalle
from log import setup

load_dotenv()
logger = setup(__name__)


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)
        self.activity = discord.Activity(
            type=discord.ActivityType.watching, name="Netflix")


async def send_message(message, user_message):
    await message.response.defer()
    try:
        if isinstance(user_message, str):
            dalle_instance = Dalle(prompt=user_message)
            dalle_instance.generate_from_prompt()
            await message.followup.send(
                f'`{user_message}`', file=discord.File(f'output\\{user_message}.png')
            )
        else:
            msg = 'image_variation'
            input_path = f'input\\{msg}.png'
            await user_message.save(input_path)
            with Image.open(input_path) as im:
                width, height = im.size
                max_size = max(width, height)
                fill_color = (255, 255, 255, 0)
                new_im = Image.new('RGBA', (max_size, max_size), fill_color)
                new_im.paste(im, (int((max_size - width) / 2),
                             int((max_size - height) / 2)))
                new_im.save(input_path)
            dalle_instance = Dalle(input_image=input_path)
            dalle_instance.create_image_variation()
            logger.info(
                f'\x1b[31m{message.user}\x1b[0m : Successfully created image variation!'
            )
            await message.followup.send(
                f'`Here is a variation of the image:`', file=discord.File(f'output\\{msg}.png')
            )
    except Exception as e:
        await message.followup.send("Error: Something went wrong!")
        logger.exception(f"Error: {e}")


def run_bot():
    client = Client()

    @client.event
    async def on_ready():
        await client.tree.sync()
        logger.info(f'{client.user} is running!')

    @client.tree.command(name="dalle", description="Ask the AI to create an image")
    async def dalle(interaction, *, message: str):
        if interaction.user == client.user:
            return
        logger.info(
            f"\x1b[31m{interaction.user}\x1b[0m : '{message}' ({interaction.channel})"
        )
        await send_message(interaction, message)

    @client.tree.command(name="var", description="Ask the AI to create a variation")
    async def dalle_var(interaction, *, file: discord.Attachment):
        if interaction.user == client.user:
            return
        logger.info(
            f'\x1b[31m{interaction.user}\x1b[0m : ({interaction.channel})'
        )
        await send_message(interaction, file)

    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    client.run(TOKEN)
