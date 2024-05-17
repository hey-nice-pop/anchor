import discord
from discord.ext import commands
import requests

# 地域名と地域IDのマッピング
region_id_mapping = {
    "東京": "130010",
    "大阪": "270000",
    "福岡": "400040",
    # 必要に応じて他の地域も追加
}

# 天気情報を取得する関数
def get_weather_info(region_id):
    url = f'https://weather.tsukumijima.net/api/forecast/city/{region_id}'
    response = requests.get(url)
    data = response.json()
    
    if 'forecasts' not in data:
        return None

    # 今日と明日の天気情報を取得
    today = data['forecasts'][0]
    tomorrow = data['forecasts'][1]

    weather_info = {
        'location': data['location']['city'],
        'today': {
            'date': today['date'],
            'weather': today['telop'],
            'high_temp': today['temperature']['max']['celsius'] if today['temperature']['max'] else 'N/A',
            'low_temp': today['temperature']['min']['celsius'] if today['temperature']['min'] else 'N/A',
            'precip_morning': today['chanceOfRain']['T06_12'] if 'T06_12' in today['chanceOfRain'] else 'N/A',
            'precip_afternoon': today['chanceOfRain']['T12_18'] if 'T12_18' in today['chanceOfRain'] else 'N/A'
        },
        'tomorrow': {
            'date': tomorrow['date'],
            'weather': tomorrow['telop'],
            'high_temp': tomorrow['temperature']['max']['celsius'] if tomorrow['temperature']['max'] else 'N/A',
            'low_temp': tomorrow['temperature']['min']['celsius'] if tomorrow['temperature']['min'] else 'N/A',
            'precip_morning': tomorrow['chanceOfRain']['T06_12'] if 'T06_12' in tomorrow['chanceOfRain'] else 'N/A',
            'precip_afternoon': tomorrow['chanceOfRain']['T12_18'] if 'T12_18' in tomorrow['chanceOfRain'] else 'N/A'
        },
        'description': data['description']['text'] if 'description' in data else '概要はありません。'
    }
    return weather_info

class RegionSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="東京", value="130010"),
            discord.SelectOption(label="大阪", value="270000"),
            discord.SelectOption(label="福岡", value="400040"),
            # 必要に応じて他の地域も追加
        ]
        super().__init__(placeholder="地域を選択してください", options=options)

    async def callback(self, interaction: discord.Interaction):
        region_id = self.values[0]
        weather_info = get_weather_info(region_id)

        if not weather_info:
            await interaction.response.send_message('天気情報を取得できませんでした。')
            return

        # 天気情報を整形して返信
        description_message = f"概要:\n{weather_info['description']}"

        formatted_weather_info = f"【{weather_info['today']['date']}の天気】\n" \
                                f"天気: {weather_info['today']['weather']}\n" \
                                f"最高気温: {weather_info['today']['high_temp']}℃\n" \
                                f"最低気温: {weather_info['today']['low_temp']}℃\n" \
                                f"午前の降水確率: {weather_info['today']['precip_morning']}%\n" \
                                f"午後の降水確率: {weather_info['today']['precip_afternoon']}%\n\n" \
                                f"【{weather_info['tomorrow']['date']}の天気】\n" \
                                f"天気: {weather_info['tomorrow']['weather']}\n" \
                                f"最高気温: {weather_info['tomorrow']['high_temp']}℃\n" \
                                f"最低気温: {weather_info['tomorrow']['low_temp']}℃\n" \
                                f"午前の降水確率: {weather_info['tomorrow']['precip_morning']}%\n" \
                                f"午後の降水確率: {weather_info['tomorrow']['precip_afternoon']}%\n\n" \
                                f"{description_message}"

        await interaction.response.send_message(f'{weather_info["location"]}の天気予報です:\n{formatted_weather_info}')  # 天気情報を送信

class WeatherView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RegionSelect())

# setup関数でBotにコマンドを登録
def setup(bot: commands.Bot):
    @bot.tree.command(name="weather", description="指定した地名の天気を表示します")
    async def weather(interaction: discord.Interaction):
        await interaction.response.send_message("地域を選択してください", view=WeatherView())