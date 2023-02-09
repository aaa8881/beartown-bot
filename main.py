import logging
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(verbose=True)
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Running as {bot.user.name}")


@bot.command(name="del")
async def delete(ctx):
    channels = ctx.guild.channels
    for channel in channels:
        if 'closed' in channel.name:
            await ctx.send(f'Deleting {channel.name}')
            await channel.delete()


@bot.command(name="purge")
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    formatter = logging.Formatter('[%(levelname)s: %(asctime)s] %(name)s: %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    for e in os.listdir('extensions'):
        if e == '__pycache__' or e.startswith('-'):
            continue
        try:
            bot.load_extension(f'extensions.{e.replace(".py", "")}')
        except:
            logger.error('오류가 발생하였습니다.', exc_info=True)
    bot.run(os.environ['TOKEN'], reconnect=True)
