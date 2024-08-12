# EN
**GenDiscordMusicBot** is a powerful and feature-rich Discord bot for playing music directly from YouTube using Lavalink. This bot supports queue management, custom commands, and more.

## Features
- Play music from YouTube
- Queue management
- Custom commands
- Automatic message deletion for clean chat
- Logging for easy debugging

## Installation
### Requires
- Python 3.8+
- Discord bot token
- Lavalink server

### Setup
1. **Clone the repository**:
    ```bash
    git clone https://github.com/geniuszlyy/GenDiscordMusicBot.git
    cd GenDiscordMusicBot
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure your bot**:
    Create a `config.json` file in the root directory and add your credentials:
    ```json
    {
        "DISCORD_TOKEN": "your_discord_token",
        "LAVALINK_HOST": "your_lavalink_host",
        "LAVALINK_PORT": 2333,
        "LAVALINK_PASSWORD": "your_lavalink_password"
    }
    ```

4. **Run the bot**:
    ```bash
    python main.py
    ```

## Commands

### General Commands
- `?play <URL or query>`: Play a track from YouTube or add it to the queue.
- `?stop`: Stop the current track and disconnect from the voice channel.
- `?skip`: Skip the current track.
- `?nowplaying`: Display the currently playing track.

### Example
1. **To play a song:**
    ```markdown
    ?play https://www.youtube.com/watch?v=dQw4w9WgXcQ
    ```
2. **To stop the music**:
    ```markdown
    ?stop
    ```
3. **To skip the current track**:
    ```markdown
    ?skip
    ```


# RU
**GenDiscordMusicBot** — это мощный и многофункциональный бот для Discord, который воспроизводит музыку прямо с YouTube с использованием Lavalink. Этот бот поддерживает управление очередью, настраиваемые команды и многое другое.

## Особенности
- Воспроизведение музыки с YouTube
- Управление очередью
- Настраиваемые команды
- Автоматическое удаление сообщений для чистоты чата
- Логирование для упрощенной отладки

## Установка
### Требования
- Python 3.8+
- Токен бота Discord
- Сервер Lavalink

### Настройка
1. **Клонируйте репозиторий**:
    ```bash
    git clone https://github.com/geniuszlyy/GenDiscordMusicBot.git
    cd GenDiscordMusicBot
    ```

2. **Установите зависимости**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Настройте бота**:
    Создайте файл `config.json` в корневом каталоге и добавьте свои учетные данные:
    ```json
    {
        "DISCORD_TOKEN": "ваш_дискорд_токен",
        "LAVALINK_HOST": "ваш_хост_lavalink",
        "LAVALINK_PORT": 2333,
        "LAVALINK_PASSWORD": "ваш_пароль_lavalink"
    }
    ```

4. **Запустите бота**:
    ```bash
    python main.py
    ```

## Команды

### Общие команды
- `?play <URL или запрос>`: Воспроизвести трек с YouTube или добавить его в очередь.
- `?stop`: Остановить текущий трек и отключиться от голосового канала.
- `?skip`: Пропустить текущий трек.
- `?nowplaying`: Показать текущий трек.

### Пример
1. **Чтобы воспроизвести песню**:
    ```markdown
    ?play https://www.youtube.com/watch?v=dQw4w9WgXcQ
    ```
2. **Чтобы остановить музыку**:
    ```markdown
    ?stop
    ```
3. **Чтобы пропустить текущий трек**:
    ```markdown
    ?skip
    ```

