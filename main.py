import discord
from discord.ext import commands
import config

import game.minesweeper as minesweeper

YOUR_BOT_TOKEN = config.BOT_TOKEN

# インテントを有効化
intents = discord.Intents.all()

# Botオブジェクトの生成
bot = commands.Bot(
    command_prefix='/', 
    intents=intents, 
    sync_commands=True,
    activity=discord.Game("テスト")
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'ログイン完了: {bot.user}')

# マインスイーパー機能のセットアップ
minesweeper.setup(bot)

# wiki.pyからコマンドをロード
import wiki
wiki.setup(bot)

# news.pyのコマンドをセットアップする
import news  # news.pyモジュールをインポート
news.setup(bot)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 他のコマンドも処理
    await bot.process_commands(message)

# Discordボットを起動
bot.run(YOUR_BOT_TOKEN)
