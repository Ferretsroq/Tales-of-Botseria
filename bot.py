#Work with Python 3.6
import discord, character_sheet, json, asyncio

TOKEN = open('token.token').read()
ROLES = {
        "solara": 503993134037073932,
        "tiamat": 503993293378420746,
        "mistral": 503993326672806119,
        "proserpina": 503993351876378644,
        "skirnir": 503993370302218241,
        "lucifiel": 503993386588700672,
        "want more threads": 503994473655697408,
        "am cool thanks": 503994494690131969,
        "hiatus": 503994516148191242
        }

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if(message.content.startswith('>help')):
        await message.channel.send("Available commands:\n```hello\nrepopulate\nchar <charname>\nforward```")
    # Test echo command
    if message.content.startswith('>hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
        

    # Repopulate the character list, saves to file
    elif message.content.startswith('>repopulate'):
        character_sheet.repopulate()
        await message.channel.send('Repopulated character list!')


    # Sends character info to discord embed
    elif message.content.startswith('>char'):
        if(message.content == '>char'):
            await message.channel.send('```>char must be followed by a valid character name.```')
        else:
            name = message.content.split(">char ",1)[1]
            with open('data.json') as json_data:
                data = json.load(json_data)
            if(name.lower() in data.keys()):
                characterInfo =  data[name.lower()]
                print(characterInfo)
                output = character_sheet.MakeEmbed(name.title(), characterInfo)
                print(output)
                await message.channel.send(embed=output)
            else:
                output = 'Invalid character!\n```{}```'.format(name.lower())
                await message.channel.send(output)

    # Memes
    elif(message.content.startswith('>forward')):
        await message.channel.send('and back')
        await asyncio.sleep(2)
        await message.channel.send('and then forward and back')
        await asyncio.sleep(2)
        await message.channel.send('and then go forward and back')
        await asyncio.sleep(2)
        await message.channel.send('and put one foot')
        await message.channel.send('forward')

    # Role assignment
    elif(message.content.startswith('>iam')):
        if(message.content == '>iam'):
            await message.channel.send('I need to know what role you want, silly! Valid roles:\n```{}```'.format('\n'.join(list(ROLES.keys()))))
        else:
            print(message.guild.roles)
            desiredRole = message.content.split("iam ",1)[1].lower()
            if(desiredRole in ROLES.keys()):
                if(message.guild.get_role(ROLES[desiredRole]) in message.author.roles):
                    await message.channel.send('You already have role\n```{}```'.format(desiredRole))
                else:
                    await message.author.add_roles(message.guild.get_role(ROLES[desiredRole]))
                    await message.channel.send("Role `{}` assigned!".format(desiredRole))
            else:
                await message.channel.send("Role `{}` not found.".format(desiredRole))



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
client.logout()
client.close()