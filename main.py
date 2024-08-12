import discord
from discord.ext import commands
from discord import app_commands
import wavelink
import json
import logging
from collections import deque

# Загрузка конфигурации из файла config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание бота с префиксом команды и всеми намерениями
bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
bot.remove_command("help")  # Удаление стандартной команды помощи

# Событие при запуске бота
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="/play /stop"))
    logger.info("Бот успешно запущен.")
    try:
        synced_commands = await bot.tree.sync()
        logger.info(f"Синхронизировано {len(synced_commands)} команд")
    except Exception as sync_error:
        logger.error(f"Ошибка синхронизации команд: {sync_error}")
    
    # Подключение к серверу Lavalink
    node = wavelink.Node(uri=f"http://{config['LAVALINK_HOST']}:{config['LAVALINK_PORT']}", password=config['LAVALINK_PASSWORD'])
    await wavelink.NodePool.connect(node)

# Очередь треков
queues = {}

# Получение или создание очереди для сервера
def get_queue(guild_id):
    if guild_id not in queues:
        queues[guild_id] = deque()
    return queues[guild_id]

# Команда для воспроизведения YouTube видео
@bot.tree.command(name="play", description="Воспроизведение видео с YouTube")
@app_commands.describe(query="Ссылка на видео или запрос")
async def play_video(interaction: discord.Interaction, query: str):
    user_voice_state = interaction.guild.get_member(interaction.user.id).voice
    if user_voice_state is None or user_voice_state.channel is None:
        await interaction.followup.send("Вы должны быть в голосовом канале.", ephemeral=True)
        return
    await interaction.response.defer()

    node = wavelink.NodePool.get_node()
    player = node.get_player(interaction.guild)
    
    if player is None:
        player = await user_voice_state.channel.connect(cls=wavelink.Player)

    search = await wavelink.YouTubeTrack.search(query=query, return_first=True)
    
    if not search:
        await interaction.followup.send("По вашему запросу ничего не найдено.")
        return

    queue = get_queue(interaction.guild.id)
    queue.append(search)
    
    if not player.is_playing():
        await player.play(queue.popleft())
    
    video_embed = discord.Embed(title=search.title, description=f"Длительность: {search.length // 60}:{search.length % 60:02d}")
    video_embed.set_footer(text=f"Добавлено пользователем {interaction.user.display_name}")
    await interaction.followup.send(embed=video_embed)

    # Автоудаление команды после отправки ответа
    await interaction.message.delete(delay=5)

# Команда для остановки воспроизведения и отключения бота от голосового канала
@bot.tree.command(name="stop", description="Остановка трека и выход из голосового канала")
async def stop_music(interaction: discord.Interaction):
    user_voice_state = interaction.guild.get_member(interaction.user.id).voice
    if user_voice_state is None или user_voice_state.channel is None:
        await interaction.response.send_message("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
        return
    await interaction.response.defer()

    try:
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)
        if player and player.is_playing():
            await player.stop()
            await interaction.followup.send("Воспроизведение музыки остановлено.", ephemeral=True)
            await player.disconnect()
        else:
            await interaction.followup.send("В данный момент ничего не воспроизводится.", ephemeral=True)
            await player.disconnect()
    except Exception as stop_error:
        logger.error(f'Произошла ошибка: {stop_error}')
        await interaction.followup.send(f'Произошла ошибка: {stop_error}', ephemeral=True)

# Команда для пропуска текущего трека
@bot.tree.command(name="skip", description="Пропуск текущего трека")
async def skip_track(interaction: discord.Interaction):
    user_voice_state = interaction.guild.get_member(interaction.user.id).voice
    if user_voice_state is None or user_voice_state.channel is None:
        await interaction.response.send_message("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
        return
    await interaction.response.defer()

    try:
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)
        queue = get_queue(interaction.guild.id)
        
        if queue:
            next_track = queue.popleft()
            await player.play(next_track)
            await interaction.followup.send(f"Сейчас играет: {next_track.title}", ephemeral=True)
        else:
            await player.stop()
            await interaction.followup.send("Очередь пуста, воспроизведение остановлено.", ephemeral=True)
            await player.disconnect()
    except Exception as skip_error:
        logger.error(f'Произошла ошибка: {skip_error}')
        await interaction.followup.send(f'Произошла ошибка: {skip_error}', ephemeral=True)

# Команда для отображения текущего трека
@bot.tree.command(name="nowplaying", description="Показать текущий трек")
async def now_playing(interaction: discord.Interaction):
    try:
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player and player.is_playing():
            current_track = player.current
            await interaction.followup.send(f"Сейчас играет: {current_track.title}", ephemeral=True)
        else:
            await interaction.followup.send("В данный момент ничего не воспроизводится.", ephemeral=True)
    except Exception as np_error:
        logger.error(f'Произошла ошибка: {np_error}')
        await interaction.followup.send(f'Произошла ошибка: {np_error}', ephemeral=True)

# Запуск бота с использованием токена
bot.run(config['DISCORD_TOKEN'])
