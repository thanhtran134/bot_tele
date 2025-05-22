import os
import replicate
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from dotenv import load_dotenv
import aiohttp
import json
import config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send a text prompt to generate an anime-style image.")

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    prompt = update.message.text
    await update.message.reply_text("Generating anime image, please wait...")

    client = replicate.Client(api_token=config.REPLICATE_API_TOKEN)
    output = client.run(
        "cjwbw/animagine-xl-3.1:6afe2e6b27dad2d6f480b59195c221884b6acc589ff4d05ff0e5fc058690fbb9",
        input={
            "prompt": f"1girl, {prompt}, masterpiece, best quality",
            "negative_prompt": "nsfw, lowres, bad, text, error, missing, worst quality, jpeg artifacts",
            "width": 832,
            "height": 1216,
            "guidance_scale": 7,
            "num_inference_steps": 28
        }
    )
    image_url = output[0] if isinstance(output, list) else output

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/generations/",
            json={"user_id": user_id, "prompt": prompt, "image_url": image_url}
        ) as response:
            if response.status != 200:
                await update.message.reply_text("Failed to save generation.")
                return

    # Send image to user
    await update.message.reply_photo(image_url)

async def list_generations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://localhost:8000/generations/{user_id}") as response:
            if response.status == 200:
                generations = await response.json()
                if not generations:
                    await update.message.reply_text("No generations found.")
                    return
                for gen in generations:
                    await update.message.reply_text(f"Prompt: {gen['prompt']}\nImage: {gen['image_url']}")
            else:
                await update.message.reply_text("Failed to retrieve generations.")

def main():
    app = Application.builder().token(config.TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_generations))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    app.run_polling()

if __name__ == "__main__":
    main()