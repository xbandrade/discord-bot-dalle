import os

import discord
from dotenv import load_dotenv
from PIL import Image

from dalle import Dalle
from log import setup

load_dotenv()
logger = setup(__name__)


def find_image(msg):
    pic_extensions = ['.jpg', '.png', '.jpeg']
    for ext in pic_extensions:
        if msg.filename.endswith(ext):
            return True


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)
        self.activity = discord.Activity(
            type=discord.ActivityType.watching, name="Netflix")


async def send_message(interaction, user_message, k=0):
    await interaction.response.defer()
    try:
        if k == 0:
            dalle_instance = Dalle(prompt=user_message)
            dalle_instance.generate_from_prompt()
            await interaction.followup.send(
                f'`{user_message}`', file=discord.File(f'output\\{user_message}.png')
            )
        elif k == 1:
            msg = 'image_variation'
            input_path = f'input\\{msg}.png'
            if find_image(user_message):
                await user_message.save(input_path)
            else:
                await interaction.followup.send('Error: File is not an image!')
                logger.warning('Error: File is not an image')
                return
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
                f'\x1b[31m{interaction.user}\x1b[0m : Successfully created image variation!'
            )
            await interaction.followup.send(
                '`Here is a variation of the image:`', file=discord.File(f'output\\{msg}.png')
            )
        else:
            await interaction.followup.send("Error: Something went wrong!")
            logger.warning('Error: Invalid k value')

    except Exception as e:
        await interaction.followup.send("Error: Something went wrong!")
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
        await send_message(interaction, message, 0)

    @client.tree.command(name="var", description="Ask the AI to create a variation")
    async def dalle_var(interaction, *, file: discord.Attachment):
        if interaction.user == client.user:
            return
        logger.info(
            f'\x1b[31m{interaction.user}\x1b[0m : ({interaction.channel})'
        )
        await send_message(interaction, file, 1)

    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    client.run(TOKEN)
