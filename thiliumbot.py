import discord
from secrets import token

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print('Message received:\n{}'.format(message.content))
    if message.author == client.user:
        return

    if message.content.startswith('$test'):
        await message.channel.send('Test')


client.run(token)
