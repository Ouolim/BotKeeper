import discord
import asyncio

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_message(message):
    global tickani
    print(f"{message.author} napsal {message.content}")
    if message.content.startswith("!zacnitickat"):
        print("zapinam tickani")
        await message.delete()
        tickani = True
        while tickani:
            await asyncio.sleep(5)
            await message.channel.send("!tick")
    if message.content.startswith("!netickej"):
        print("Vypinam tickani")
        tickani = False
tickani = False


from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv('TOKENTIKATOR')

client.run('ODUxOTM3NzY2NTU5NDQ5MTI4.G15jCL.VGXxwbeNpjUWU03tesCTuZ4_fn7Q7gppzEK4gM')