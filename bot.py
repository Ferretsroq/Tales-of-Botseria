#Work with Python 3.6
import discord, character_sheet, json, asyncio
import Googlify, RockPaperScissors, boons, DeityMessage, CanonList, OocMessage, fmk
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
        self.fmkGames = []
        self.rpsGames = []
        #self.rockPaperScissorsGame = RockPaperScissors.Game()
        self.fmkGame = fmk.Game()
        self.factionMessages = {'solara': None,
                                'tiamat': None,
                                'mistral': None,
                                'proserpina': None,
                                'skirnir': None,
                                'lucifiel': None,
                                'all': None}
        self.canonMessages = {}
        self.oocMessages = {}

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author == client.user:
            return
        if(message.content.startswith('>help')):
            await message.channel.send("Available commands:\n```hello\nrepopulate ***STAFF ONLY***\nfetch ***STAFF ONLY***\ntemplates\nchar [charname]\ncanonlist\ncharlist [deity OR canon OR ooc] [number]\niam <rolename>\niamnot <rolename>\nfaction\nboons <number> <min EX> <min S> **STAFF ONLY**\nforward\ngooglify [charname OR @user]\nsantafy [charname OR @user]\nrps <@player2>```")
        # Test echo command
        if message.content.startswith('>hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await message.channel.send(msg)
            

        # Repopulate the character list, saves to file
        elif(message.content.startswith('>repopulate') and (message.guild.get_role(STAFFROLE) in message.author.roles or message.channel.id == 379374543237545985)):
            await character_sheet.repopulate(message.channel)
            await message.channel.send('Repopulated character list!')
        elif(message.content.lower().startswith('>fetch') and (message.guild.get_role(STAFFROLE) in message.author.roles or message.channel.id == 379374543237545985)):
            await character_sheet.Fetch(message.channel)


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
                    elif(len(message.content.split(maxsplit=1)) == 2 and message.content.split(maxsplit=1)[1].lower() in [canon[0] for canon in CanonList.CanonList()]):
                        canon = message.content.split(maxsplit=1)[1].lower()
                        self.canonMessages[canon] = CanonList.CanonMessage(canon, message.author)
                        await self.canonMessages[canon].Send(message.channel)
                        await self.canonMessages[canon].ListNames()
                    elif(len(message.content.split()) > 1 and ' '.join(message.content.split()[1:-1]).lower() in self.canonMessages and message.content.split()[-1].isdigit()):
                        canonMessage = self.canonMessages[' '.join(message.content.split()[1:-1]).lower()]
                        number = int(message.content.split()[-1])
                        if(number <= len(canonMessage.characterList) and number >= 1):
                            canonMessage.index = number-1
                            await canonMessage.Edit()
                    # ooc character lists
                    elif(len(message.content.split(maxsplit=1)) == 2 and message.content.split(maxsplit=1)[1].lower() in OocMessage.OocList()):
                        oocName = message.content.split(maxsplit=1)[1].lower()
                        self.oocMessages[oocName] = OocMessage.OocMessage(message.author, oocName)
                        await self.oocMessages[oocName].Send(message.channel)
                        await self.oocMessages[oocName].ListNames()
                    elif(len(message.content.split()) > 1 and ' '.join(message.content.split()[1:-1]).lower() in self.oocMessages and message.content.split()[-1].isdigit()):
                        oocMessage = self.oocMessages[' '.join(message.content.split()[1:-1]).lower()]
                        number = int(message.content.split()[-1])
                        if(number <= len(oocMessage.characterList) and number >= 1):
                            oocMessage.index = number-1
                            await oocMessage.Edit()
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
            canonList = CanonList.CanonList()
            index = 0
            sendString = 'Valid canons: ```'
            while(index < len(canonList)):
                while(len(sendString) < 1900):
                    sendString += ('\n'+'{:<30}: {} characters'.format(canonList[index][0], canonList[index][1]))
                    index += 1
                    if(index >= len(canonList)):
                        break
                sendString += '```'
                await message.channel.send(sendString)
                sendString = '```'
            await message.channel.send('>charlist [canon] to list characters for a canon')

            #await message.channel.send('Valid canons: ```{}``` >charlist [canon] to list characters for a canon'.format('\n'.join(['{:<30}: {} Characters'.format(element[0], element[1]) for element in canonList])))#CanonList.CanonList()])))

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
        elif(message.content.lower().startswith('>iam') and not message.content.lower().startswith('>iamnot')):
            if(message.content.lower() == '>iam'):
                await message.channel.send('I need to know what role you want, silly! Valid roles:\n```{}```'.format('\n'.join(list(ROLES.keys()))))
            # Kat is a weeb
            elif(message.content.lower() == '>iam the bone of my sword'):
                await message.channel.send('Steel is my Body and Fire is my Blood.')
                await asyncio.sleep(2)
                await message.channel.send('I have created over a Thousand Blades,')
                await asyncio.sleep(2)
                await message.channel.send('Unknown to Death,')
                await asyncio.sleep(2)
                await message.channel.send('Nor known to Life.')
                await asyncio.sleep(2)
                await message.channel.send('Have withstood Pain to create many Weapons')
                await asyncio.sleep(2)
                await message.channel.send('Yet those Hands will never hold Anything.')
                await asyncio.sleep(2)
                await message.channel.send('So, as I Pray-')
                await asyncio.sleep(2)
                await message.channel.send('**UNLIMITED BLADE WORKS**')
                await asyncio.sleep(1)
                await message.channel.send(':crossed_swords:'*125)
            elif(message.content.lower() == '>iam the night'):
                Googlify.Batmanify(Googlify.ImageFromURL(message.author.avatar_url)).save('tempBat.png')
                await message.channel.send(file=discord.File('tempBat.png'))
            else:
                desiredRole = message.content.lower().split(">iam ",1)[1].lower()
                if(desiredRole in ROLES.keys()):
                    if(message.guild.get_role(ROLES[desiredRole]) in message.author.roles):
                        await message.channel.send('You already have role\n```{}```'.format(desiredRole))
                    else:
                        await message.author.add_roles(message.guild.get_role(ROLES[desiredRole]))
                        await message.channel.send("Role `{}` assigned!".format(desiredRole))
                else:
                    await message.channel.send("Role `{}` not found.".format(desiredRole))

        elif(message.content.lower().startswith('>iamnot')):
            if(message.content.lower() == '>iamnot'):
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
        elif(message.content.lower().startswith('>faction')):
            faction = random.choice(FACTIONS)
            text = ['Uplander! Uplander, make lookings! Swooshy spellycastings is sayings....um....is sayings {} is good choosymakes!'.format(faction),
                        'According to the position of the stars, the placement of your bedroom, and the ripeness of this pickle - {} is the best deity for you!'.format(faction),
                        'The fates have chosen, oh indecisive one - {} has found you worthy to fight in their name!'.format(faction)]
            await message.channel.send(random.choice(text))
            #await message.channel.send('The fates have chosen, oh indecisive one - {} is the deity that you may call as your home!'.format(faction))

        elif(message.content.lower() == '>templates'):
            await message.channel.send('You can find Magician\'s templates here!\nhttp://heavensfall.jcink.net/index.php?showtopic=22')
        # Eyes
        elif(message.content.lower().startswith('>googlify')):
            if(message.content == '>googlify'):
                Googlify.Googlify(Googlify.ImageFromURL(message.author.avatar_url)).save('tempGoogly.png')
                await message.channel.send(file=discord.File('tempGoogly.png'))
            elif(len(message.content.split(' ',1)) > 1 and len(message.mentions)==0):
                with open('data.json') as json_data:
                    data = json.load(json_data)
                if(message.content.split(' ',1)[1].lower() in data.keys()):
                    Googlify.Googlify(Googlify.ImageFromURL(data[message.content.split(' ',1)[1].lower()]['image'])).save('tempGoogly.png')
                    await message.channel.send(file=discord.File('tempGoogly.png'))
                else:
                    await message.channel.send("Character not found:```{}```".format(message.content.split(' ',1)[1].lower()))
            elif(len(message.content.split(' ',1)) > 1 and len(message.mentions) > 0):
                Googlify.Googlify(Googlify.ImageFromURL(message.mentions[0].avatar_url)).save('tempGoogly.png')
                await message.channel.send(file=discord.File('tempGoogly.png'))

        # Santa hat/beard
        elif(message.content.startswith('>santafy')):
            if(message.content == '>santafy'):
                Googlify.Santafy(Googlify.ImageFromURL(message.author.avatar_url)).save('tempSanta.png')
                await message.channel.send(file=discord.File('tempSanta.png'))
            elif(len(message.content.split(' ',1)) > 1 and len(message.mentions)==0):
                with open('data.json') as json_data:
                    data = json.load(json_data)
                if(message.content.split(' ',1)[1].lower() in data.keys()):
                    Googlify.Santafy(Googlify.ImageFromURL(data[message.content.split(' ',1)[1].lower()]['image'])).save('tempSanta.png')
                    await message.channel.send(file=discord.File('tempSanta.png'))
                else:
                    await message.channel.send("Character not found:```{}```".format(message.content.split(' ',1)[1].lower()))
            elif(len(message.content.split(' ',1)) > 1 and len(message.mentions) > 0):
                Googlify.Santafy(Googlify.ImageFromURL(message.mentions[0].avatar_url)).save('tempSanta.png')
                await message.channel.send(file=discord.File('tempSanta.png'))
        elif(message.content.startswith('>santafly')):
            if(message.content == '>santafly'):
                Googlify.Santafy(Googlify.ImageFromURL(message.author.avatar_url), rand=True).save('tempSanta.png')
                await message.channel.send(file=discord.File('tempSanta.png'))
            elif(len(message.content.split(' ',1)) > 1 and len(message.mentions)==0):
                with open('data.json') as json_data:
                    data = json.load(json_data)
                if(message.content.split(' ',1)[1].lower() in data.keys()):
                    Googlify.Santafy(Googlify.ImageFromURL(data[message.content.split(' ',1)[1].lower()]['image']), rand=True).save('tempSanta.png')
                    await message.channel.send(file=discord.File('tempSanta.png'))
                else:
                    await message.channel.send("Character not found:```{}```".format(message.content.split(' ',1)[1].lower()))
            elif(len(message.content.split(' ',1)) > 1 and len(message.mentions) > 0):
                Googlify.Santafy(Googlify.ImageFromURL(message.mentions[0].avatar_url), rand=True).save('tempSanta.png')
                await message.channel.send(file=discord.File('tempSanta.png'))





        # Rock-Paper-Scissors
        elif(message.content.startswith('>rps') and len(message.mentions) > 0):
            # Purge completed games
            self.rpsGames.sort(key=lambda x: x.valid, reverse=True)
            while(False in [game.valid for game in self.rpsGames]):
                self.rpsGames.pop()

            if(message.mentions[0].dm_channel == None):
                await message.mentions[0].create_dm()
            if(message.author.dm_channel == None):
                await message.author.create_dm()
            self.rpsGames.append(RockPaperScissors.Game(message, message.author, message.mentions[0]))
            await self.rpsGames[-1].Send()
            #self.rockPaperScissorsGame = RockPaperScissors.Game(message, message.author, message.mentions[0])
            #await self.rockPaperScissorsGame.Send()
        # Fuck-Marry-Kill
        elif(message.content.lower().startswith('>fmk') and len(message.mentions) > 0):
            # Purge completed games
            self.fmkGames.sort(key=lambda x: x.valid, reverse=True)
            while(False in [game.valid for game in self.fmkGames]):
                self.fmkGames.pop()
            print(self.fmkGames)
            self.fmkGames.append(fmk.Game(message, message.author, message.mentions[0]))
            await self.fmkGames[-1].Send()

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
        if(user != client.user):
            for rpsGame in self.rpsGames:
                if(rpsGame.valid):
                    if(reaction.message.id == rpsGame.challengerMessage.id and user == rpsGame.challenger):
                        await rpsGame.UpdateChallengerResponse(reaction)
                    elif(reaction.message.id == rpsGame.targetMessage.id and user == rpsGame.target):
                        await rpsGame.UpdateTargetResponse(reaction)
            for fmkGame in self.fmkGames:
                if(fmkGame.valid):
                    #print(reaction.message.id)
                    #print(fmkGame.targetMessage.id)
                    if(reaction.message.id == fmkGame.targetMessage.id and user == fmkGame.target):
                        if(str(reaction) == str(fmk.arrowLeft)):
                            await fmkGame.Back()
                        elif(str(reaction) == str(fmk.arrowRight)):
                            await fmkGame.Advance()
                        elif(str(reaction) == str(fmk.listEmoji)):
                            await fmkGame.ListNames()
                        else:
                            await fmkGame.RegisterAnswer(reaction.emoji)
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
            for ooc in self.oocMessages:
                if(self.oocMessages[ooc] != None):
                    if(self.oocMessages[ooc].message.id == reaction.message.id and self.oocMessages[ooc].user == user):
                        if(str(reaction) == str(OocMessage.arrowLeft)):
                            await self.oocMessages[ooc].Back()
                        elif(str(reaction) == str(OocMessage.arrowRight)):
                            await self.oocMessages[ooc].Advance()
                        elif(str(reaction) == str(OocMessage.listEmoji)):
                            await self.oocMessages[ooc].ListNames()


client = MyClient()
client.run(TOKEN)
client.logout()
client.close()