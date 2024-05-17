import discord
from discord.ext import commands
import config

import game.minesweeper as minesweeper

import wiki

import news

import weather

import voice

YOUR_BOT_TOKEN = config.BOT_TOKEN

# インテントを有効化
intents = discord.Intents.all()

# Botオブジェクトの生成
bot = commands.Bot(
    command_prefix='/', 
    intents=intents, 
    sync_commands=True,
    activity=discord.Game("双眼鏡")
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'ログイン完了: {bot.user}')
'''
minesweeper.setup(bot)

wiki.setup(bot)

news.setup(bot)

weather.setup(bot)

voice.setup(bot)
'''

# Discordボットを起動
bot.run(YOUR_BOT_TOKEN)
