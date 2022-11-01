import discord
import asyncio

TOKEN="OTcxNjcyNDcyMTAzNTU1MDky.Gj_e36.dNJyjlgbjiNnZEM2uRQ12btOaHa6PjRvst4Ijs"
client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_message(message):
    global tickani
    print(tickani)
    if message.content.startswith("!zacnitickat"):
        await message.delete()
        tickani = True
        while tickani:
            await asyncio.sleep(5)
            await message.channel.send("!tick")
    if message.content.startswith("!netickej"):
        tickani = False
tickani = False
client.run('ODUxOTM3NzY2NTU5NDQ5MTI4.Gmjy45.IMswLND9iZnrsTXql1xQoZTvLPYdf2ClEY9b9I')