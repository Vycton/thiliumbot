import discord
import command_handlers as commands
from secrets import token

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    else:
        print('Message received:\n{}'.format(message.content))

    if message.content.startswith('$test'):
        response = commands.test(message)
        await message.channel.send(response)

    if message.content.startswith('$lotto'):
        response = commands.lotto(message)
        await message.channel.send(response)

client.run(token)
