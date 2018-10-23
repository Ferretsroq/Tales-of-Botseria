#Work with Python 3.6
import discord, character_sheet, json

TOKEN = open('token.token').read()

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #hashtag yolo
    if message.content.startswith('>hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
        #await client.send_message(message.channel, msg)

    #will repopulate the character list, it actually takes a while??
    if message.content.startswith('>repopulate'):
        character_sheet.repopulate()
        #await client.send_message(message.channel, 'Repopulated character list!')
        await message.channel.send('Repopulated character list!')


    #prints out character shit
    if message.content.startswith('>char'):
        name = message.content.split(">char ",1)[1]
        with open('data.json') as json_data:
            data = json.load(json_data)

        try:
            characterInfo =  data[name.lower()]
            output = character_sheet.MakeEmbed(name.title(), characterInfo)
            await message.channel.send(embed=output)
        except:
            output = 'Invalid character name!'
            await message.channel.send(output)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
client.logout()
client.close()