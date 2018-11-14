#Work with Python 3.6
import discord, character_sheet, json, asyncio
import Googlify, RockPaperScissors, boons, DeityMessage, CanonList
import random
import re

TOKEN = open('token.token').read()
ROLES = {
        "solara": 503993134037073932,
        "tiamat": 503993293378420746,
        "mistral": 503993326672806119,
        "proserpina": 503993351876378644,
        "skirnir": 503993370302218241,
        "lucifiel": 503993386588700672,
        "open": 503994473655697408,
        "closed": 503994494690131969,
        "hiatus": 503994516148191242
        }
STAFFROLE = 503948857298780160
FACTIONS = ["SOLARA", "TIAMAT", "MISTRAL", "PROSERPINA", "SKIRNIR", "LUCIFIEL"]

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
        self.rockPaperScissorsGame = RockPaperScissors.Game()
        self.factionMessages = {'solara': None,
                                'tiamat': None,
                                'mistral': None,
                                'proserpina': None,
                                'skirnir': None,
                                'lucifiel': None,
                                'all': None}
        self.canonMessages = {}

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author == client.user:
            return
        if(message.content.startswith('>help')):
            await message.channel.send("Available commands:\n```hello\nrepopulate ***STAFF ONLY***\nchar [charname] (or) [ooc=playername]\ncanonlist\ncharlist [deity OR canon] [number]\niam <rolename>\niamnot <rolename>\nfaction\nboons <number> <min EX> <min S> **STAFF ONLY**\nforward\ngooglify [charname]\nrps <@player2>```")
        # Test echo command
        if message.content.startswith('>hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await message.channel.send(msg)
            

        # Repopulate the character list, saves to file
        elif(message.content.startswith('>repopulate') and (message.guild.get_role(STAFFROLE) in message.author.roles or message.channel.id == 379374543237545985)):
            character_sheet.repopulate()
            await message.channel.send('Repopulated character list!')


        # Sends character info to discord embed
        elif message.content.startswith('>char'):
            # Error message for bad syntax
            if(message.content == '>char'):
                await message.channel.send('```>char must be followed by a valid character name, or include ooc=<ooc name>```')
            else:
                # List of characters
                if(message.content.startswith('>charlist')):
                    # List all characters on Heavensfall
                    if(message.content == '>charlist'):
                        self.factionMessages['all'] = DeityMessage.DeityMessage('all', message.author)
                        await self.factionMessages['all'].Send(message.channel)
                        #await self.factionMessages['all'].Edit()
                        await self.factionMessages['all'].ListNames()
                    # List all characters of one faction
                    if(len(message.content.split()) == 2 and message.content.split()[1].lower() in self.factionMessages):
                        deity = message.content.split()[1]
                        if(deity.lower() in self.factionMessages):
                            self.factionMessages[deity.lower()] = DeityMessage.DeityMessage(deity.lower(), message.author)
                            await self.factionMessages[deity.lower()].Send(message.channel)
                            #await self.factionMessages[deity.lower()].Edit()
                            await self.factionMessages[deity.lower()].ListNames()
                    # Update the character list to a number
                    elif(len(message.content.split()) == 2 and message.content.split()[1].isdigit()):
                        if(self.factionMessages['all'] != None):
                            factionMessage = self.factionMessages['all']
                            if(message.author == factionMessage.user):
                                number = int(message.content.split()[1])
                                if(number <= len(factionMessage.characterList) and number >= 1):
                                    factionMessage.index = number-1
                                    await factionMessage.Edit()
                    elif(len(message.content.split()) == 3 and message.content.split()[1].lower() in self.factionMessages):
                        if(message.content.split()[1].lower() in self.factionMessages):
                            factionMessage = self.factionMessages[message.content.split()[1].lower()]
                            if(message.author == factionMessage.user):
                                if(message.content.split()[2].isdigit()):
                                    number = int(message.content.split()[2])
                                    if(number <= len(factionMessage.characterList) and number >= 1):
                                        factionMessage.index = number-1
                                        await factionMessage.Edit()
                    # Canon character lists
                    #elif(len(message.content.split()) == 2 and message.content.split()[1].lower() in CanonList.CanonList()):
                    elif(len(message.content.split(maxsplit=1)) == 2 and message.content.split(maxsplit=1)[1].lower() in CanonList.CanonList()):
                        canon = message.content.split(maxsplit=1)[1].lower()
                        #if(canon not in self.canonMessages):
                        self.canonMessages[canon] = CanonList.CanonMessage(canon, message.author)
                        await self.canonMessages[canon].Send(message.channel)
                            #await self.canonMessages[canon].Edit()
                        await self.canonMessages[canon].ListNames()
                    #elif(len(message.content.split()) == 3 and message.content.split()[1].lower() in self.canonMessages and message.content.split()[2].isdigit()):
                    elif(len(message.content.split()) > 1 and ' '.join(message.content.split()[1:-1]).lower() in self.canonMessages and message.content.split()[-1].isdigit()):
                        #canonMessage = self.canonMessages[message.content.split()[1].lower()]
                        canonMessage = self.canonMessages[' '.join(message.content.split()[1:-1]).lower()]
                        number = int(message.content.split()[-1])
                        if(number <= len(canonMessage.characterList) and number >= 1):
                            canonMessage.index = number-1
                            await canonMessage.Edit()
                elif(message.content.startswith('>char ooc=')):
                    oocName = message.content.split('=',1)[1].lower()
                    with open('data.json') as json_data:
                        data = json.load(json_data)
                    characters = [character for character in data if data[character]['ooc'].lower()==oocName]
                    for character in characters:
                        await message.channel.send(embed=character_sheet.MakeEmbed(character, data[character]))
                    if(len(characters) == 0):
                        await message.channel.send("No characters found for ooc name ```{}```".format(oocName))
                else:
                    name = message.content.split(">char ",1)[1]
                    with open('data.json') as json_data:
                        data = json.load(json_data)
                    if(name.lower() in data.keys()):
                        characterInfo =  data[name.lower()]
                        output = character_sheet.MakeEmbed(name.title(), characterInfo)
                        await message.channel.send(embed=output)
                    else:
                        output = 'Invalid character!\n```{}```'.format(name.lower())
                        await message.channel.send(output)

        # Moves charlist to a number in the list



        elif(message.content == '>canonlist'):
            await message.channel.send('Valid canons: ```{}``` >charlist [canon] to list characters for a canon'.format('\n'.join(CanonList.CanonList())))

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
        elif(message.content.startswith('>iam') and not message.content.startswith('>iamnot')):
            if(message.content == '>iam'):
                await message.channel.send('I need to know what role you want, silly! Valid roles:\n```{}```'.format('\n'.join(list(ROLES.keys()))))
            else:
                desiredRole = message.content.split(">iam ",1)[1].lower()
                if(desiredRole in ROLES.keys()):
                    if(message.guild.get_role(ROLES[desiredRole]) in message.author.roles):
                        await message.channel.send('You already have role\n```{}```'.format(desiredRole))
                    else:
                        await message.author.add_roles(message.guild.get_role(ROLES[desiredRole]))
                        await message.channel.send("Role `{}` assigned!".format(desiredRole))
                else:
                    await message.channel.send("Role `{}` not found.".format(desiredRole))

        elif(message.content.startswith('>iamnot')):
            if(message.content == '>iamnot'):
                await message.channel.send('I need to know what role you aren\'t, silly! Valid roles:\n```{}```'.format('\n'.join(list(ROLES.keys()))))
            else:
                desiredRole = message.content.split(">iamnot ",1)[1].lower()
                if(desiredRole in ROLES.keys()):
                    if(message.guild.get_role(ROLES[desiredRole]) in message.author.roles):
                        await message.author.remove_roles(message.guild.get_role(ROLES[desiredRole]))
                        await message.channel.send('Removed role\n```{}```'.format(desiredRole))
                    else:
                        await message.channel.send("You do not have role\n```{}```".format(desiredRole))
                else:
                    await message.channel.send("Role `{}` not found.".format(desiredRole))
        elif(message.content.startswith('>faction')):
            faction = random.choice(FACTIONS)
            text = ['Uplander! Uplander, make lookings! Swooshy spellycastings is sayings....um....is sayings {} is good choosymakes!'.format(faction),
                        'According to the position of the stars, the placement of your bedroom, and the ripeness of this pickle - {} is the best deity for you!'.format(faction),
                        'The fates have chosen, oh indecisive one - {} has found you worthy to fight in their name!'.format(faction)]
            await message.channel.send(random.choice(text))
            #await message.channel.send('The fates have chosen, oh indecisive one - {} is the deity that you may call as your home!'.format(faction))

        # Eyes
        elif(message.content.startswith('>googlify')):
            if(message.content == '>googlify'):
                Googlify.Googlify(Googlify.ImageFromURL(message.author.avatar_url)).save('tempGoogly.png')
                await message.channel.send(file=discord.File('tempGoogly.png'))
            elif(len(message.content.split(' ',1)) > 1):
                with open('data.json') as json_data:
                    data = json.load(json_data)
                if(message.content.split(' ',1)[1].lower() in data.keys()):
                    Googlify.Googlify(Googlify.ImageFromURL(data[message.content.split(' ',1)[1].lower()]['image'])).save('tempGoogly.png')
                    await message.channel.send(file=discord.File('tempGoogly.png'))
                else:
                    await message.channel.send("Character not found:```{}```".format(message.content.split(' ',1)[1].lower()))

        # Rock-Paper-Scissors
        elif(message.content.startswith('>rps') and len(message.mentions) > 0):
            if(message.mentions[0].dm_channel == None):
                await message.mentions[0].create_dm()
            if(message.author.dm_channel == None):
                await message.author.create_dm()
            self.rockPaperScissorsGame = RockPaperScissors.Game(message, message.author, message.mentions[0])
            await self.rockPaperScissorsGame.Send()

        # Boons
        elif(message.content.startswith('>boons') and message.guild.get_role(STAFFROLE) in message.author.roles):
            if(len(message.content.split()) > 1):
                pattern = '(?P<Number>\d+) (?P<EX>\d+) (?P<S>\d+)'
                if(re.match(pattern, ' '.join(message.content.split()[1:]))):
                    matchDict = re.match(pattern, ' '.join(message.content.split()[1:])).groupdict()
                    batch = boons.BoonBatch(number=int(matchDict['Number']), minEX=int(matchDict['EX']), minS=int(matchDict['S']))
                else:
                    await message.channel.send("Usage: ```>boons <number> <min EX> <min S>``` Instead using default (10 boons, min 1 EX min 1 S)")
                    batch = boons.BoonBatch(number=10, minEX=1, minS=1)
            else:
                batch = boons.BoonBatch(number=10, minEX=1, minS=1)
            embeds = [boons.BoonEmbed(boon) for boon in batch]
            for embed in embeds:
                await message.channel.send(embed=embed)

    async def on_reaction_add(self, reaction, user):
        if(self.rockPaperScissorsGame.valid):
            if(reaction.message.id == self.rockPaperScissorsGame.challengerMessage.id and user == self.rockPaperScissorsGame.challenger):
                await self.rockPaperScissorsGame.UpdateChallengerResponse(reaction)
            elif(reaction.message.id == self.rockPaperScissorsGame.targetMessage.id and user == self.rockPaperScissorsGame.target):
                await self.rockPaperScissorsGame.UpdateTargetResponse(reaction)
        for deity in self.factionMessages:
            if(self.factionMessages[deity] != None):
                if(self.factionMessages[deity].message.id == reaction.message.id and self.factionMessages[deity].user == user):
                    if(str(reaction) == str(DeityMessage.arrowLeft)):
                        await self.factionMessages[deity].Back()
                    elif(str(reaction) == str(DeityMessage.arrowRight)):
                        await self.factionMessages[deity].Advance()
                    elif(str(reaction) == str(DeityMessage.listEmoji)):
                        await self.factionMessages[deity].ListNames()
        for canon in self.canonMessages:
            if(self.canonMessages[canon] != None):
                if(self.canonMessages[canon].message.id == reaction.message.id and self.canonMessages[canon].user == user):
                    if(str(reaction) == str(CanonList.arrowLeft)):
                        await self.canonMessages[canon].Back()
                    elif(str(reaction) == str(CanonList.arrowRight)):
                        await self.canonMessages[canon].Advance()
                    elif(str(reaction) == str(CanonList.listEmoji)):
                        await self.canonMessages[canon].ListNames()


client = MyClient()
client.run(TOKEN)
client.logout()
client.close()