import discord
from discord.ext import commands
from discord.player import FFmpegPCMAudio
import pyopenjtalk
import numpy as np
import pydub
import tempfile
import os

voice_clients = {}

def setup(bot):
    @bot.tree.command(name='join', description='Voice channelに参加します。')
    async def join(interaction: discord.Interaction):
        if interaction.user.voice:
            voice_channel = interaction.user.voice.channel
            if voice_channel:
                vc = await voice_channel.connect()
                voice_clients[interaction.guild.id] = vc
                await interaction.response.send_message('BOTが参加しました！')
            else:
                await interaction.response.send_message('あなたはボイスチャンネルにいません！')
        else:
            await interaction.response.send_message('あなたはボイスチャンネルにいません！')

    @bot.tree.command(name='leave', description='Voice channelから退出します。')
    async def leave(interaction: discord.Interaction):
        if interaction.guild.id in voice_clients:
            await voice_clients[interaction.guild.id].disconnect()
            del voice_clients[interaction.guild.id]
            await interaction.response.send_message('BOTが退出しました！')
        else:
            await interaction.response.send_message('BOTがボイスチャンネルにいません。')

    @bot.event
    async def on_message(message):
        if message.guild.id in voice_clients and message.content:
            await play_voice(message.content, voice_clients[message.guild.id])

        # 他のコマンドも処理
        await bot.process_commands(message)

async def play_voice(text, voice_client):
    # テキストから音声データとサンプリングレートを取得
    wave, sr = pyopenjtalk.tts(text)

    # 音声データの振幅を正規化
    wave_norm = wave / np.max(np.abs(wave))

    # 正規化した音声データをバイト配列に変換
    sound = np.int16(wave_norm * 32767).tobytes()

    # 正規化された音声データをpydub.AudioSegmentオブジェクトに変換
    # サンプリングレート(sr)をpyopenjtalk.ttsから取得した値に設定
    audio = pydub.AudioSegment(sound, sample_width=2, frame_rate=sr, channels=1)

    # 一時ファイルにMP3として保存
    fd, tmpfile_path = tempfile.mkstemp(suffix='.mp3')
    os.close(fd)  # tempfile.mkstemp()で得られるfdは不要なのでクローズ
    audio.export(tmpfile_path, format="mp3")

    def after_playing(error):
        os.remove(tmpfile_path)

    # 再生
    if not voice_client.is_playing():
        voice_client.play(FFmpegPCMAudio(tmpfile_path), after=after_playing)
