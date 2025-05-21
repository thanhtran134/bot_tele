# Anime Style Converter Telegram Bot

This Telegram bot converts regular images to anime style using OpenAI's GPT-4 Vision model.

## Features

- Convert regular images to anime style
- Simple and intuitive interface
- Real-time processing
- Error handling and user feedback

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Get your Telegram bot token:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot using the `/newbot` command
   - Copy the token provided

5. Get your OpenAI API key:
   - Visit [OpenAI Platform](https://platform.openai.com)
   - Create an account or sign in
   - Generate an API key

## Running the Bot

1. Start the bot:
   ```bash
   python bot.py
   ```

2. Open Telegram and search for your bot
3. Start a conversation with `/start`
4. Send any image to convert it to anime style

## Usage

1. Send `/start` to see the welcome message
2. Send `/help` to see usage instructions
3. Send any image to convert it to anime style
4. Wait for the processing to complete
5. Receive your anime-style image description

## Note

- The bot uses OpenAI's GPT-4 Vision model, which requires an API key
- Processing time may vary depending on the image size and complexity
- Make sure you have a stable internet connection 