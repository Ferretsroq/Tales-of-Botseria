import discord
from discord.ext import commands, tasks
import datetime
import character_sheet, json, asyncio
import random
import Googlify, RockPaperScissors, boons, DeityMessage, CanonList, OocMessage, hmk, valentine_generator, roll, RoleAssignment, TrickOrTreat
import re, time, os
import BotseriaServers

intents = discord.Intents.default()
intents.dm_reactions = True
intents.members = True

TOKEN = open('token.token').read()

bot = commands.Bot(command_prefix='>', case_insensitive=True, intents=intents, activity=discord.Game('with 0 pets today.'))
servers = BotseriaServers.PopulateServers()

bot.hmkGames = []
bot.rpsGames = []
bot.totGames = []
bot.factionMessages = BotseriaServers.PopulateFactionMessages(servers)
bot.canonMessages = {}
bot.oocMessages = {}
bot.hmkScoreMessages = {}
bot.roleMessages = {}
bot.petCounter = 0

def check_if_test_channel(ctx):
	#return ctx.channel.id == TESTCHANNEL
	if(str(ctx.guild.id) in servers):
		testchannels = [servers[guild]['testchannel'] for guild in servers]
		return ctx.channel.id in testchannels
	return False

def check_if_staff_or_test(ctx):
	#return ctx.guild.get_role(STAFFROLE) in ctx.author.roles or check_if_test_channel(ctx)
	if(str(ctx.guild.id) in servers):
		staffrole = servers[str(ctx.guild.id)]['staff']
		#print([servers[guild].keys() for guild in servers])
		#staffrole = [servers[guild]['staff'] for guild in servers if ctx.guild.get_role(int(servers[guild]['staff'])) != None][0]
		return ctx.guild.get_role(int(staffrole)) in ctx.author.roles or check_if_test_channel(ctx)
	return False

def check_if_december(ctx):
	return (time.localtime().tm_mon == 12) or (check_if_staff_or_test(ctx))

def check_if_february(ctx):
	return (time.localtime().tm_mon == 2) or (check_if_staff_or_test(ctx))

def check_if_bot_spam(ctx):
	if(str(ctx.guild.id) in servers):
		botchannel = int(servers[str(ctx.guild.id)]['botchannel'])
		return (ctx.channel.id == botchannel or check_if_staff_or_test(ctx))
	return False




@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

@bot.command()
@commands.check(check_if_staff_or_test)
async def logout(ctx):
	await bot.logout()
	await bot.close()

@bot.command()
@commands.check(check_if_staff_or_test)
async def repopulate(ctx):
	'''***STAFF ONLY***'''
	await character_sheet.repopulate(ctx, servers)
	await ctx.send('Repopulated character list!')

@bot.command()
@commands.check(check_if_staff_or_test)
async def fetch(ctx):
	'''***STAFF ONLY***'''
	await character_sheet.Fetch(ctx.channel, ctx, servers)

@bot.command()
async def char(ctx, *, arg):
	name = arg.lower()
	if(str(ctx.guild.id) in servers):
		with open('servers/{}/data.json'.format(ctx.guild.id)) as json_data:
			data = json.load(json_data)
		if(name in data.keys()):
			characterInfo = data[name]
			output = character_sheet.MakeEmbed(name.title(), characterInfo, servers[str(ctx.guild.id)])
			await ctx.send(embed=output)
		else:
			output = 'Invalid character!\n```{}```'.format(name)
			await ctx.send(output)

@bot.command()
async def charlist(ctx, *, arg=''):
	if(len(arg) > 0):
		messageList = arg.split()
		if(messageList[-1].isdigit()):
			command = ' '.join(messageList[0:-1]).lower()
			number = int(messageList[-1])
		else:
			command = arg.lower()
			number = None
	else:
		command = ''
		number = None
	if(command == ''):
		# List all characters on Heavensfall
		if(number == None):
			bot.factionMessages['all'] = DeityMessage.DeityMessage('all', ctx.author, ctx, servers)
			await bot.factionMessages['all'].Send(ctx.channel)
			await bot.factionMessages['all'].ListNames()
		# Skip to a specific number of an existing message
		else:
			allMessage = bot.factionMessages['all']
			if(ctx.author == allMessage.user):
				if(number <= len(allMessage.characterList) and number >= 1):
					allMessage.index = number - 1
					await allMessage.Edit()
	# Deity character lists
	elif(command in bot.factionMessages):
		deity = command.lower()
		# List all characters of that deity
		if(number == None):
			bot.factionMessages[deity] = DeityMessage.DeityMessage(deity, ctx.author, ctx, servers)
			await bot.factionMessages[deity.lower()].Send(ctx.channel)
			await bot.factionMessages[deity].ListNames()
		# Skip to a specific number of an existing message
		else:
			factionMessage = bot.factionMessages[command]
			if(ctx.author == factionMessage.user):
				if(number <= len(factionMessage.characterList) and number >= 1):
					factionMessage.index = number-1
					await factionMessage.Edit()
	# Canon character lists
	elif(command in [canon[0] for canon in CanonList.CanonList(servers[str(ctx.guild.id)])]):
		canon = command
		# List all characters of that canon
		if(number == None):
			bot.canonMessages[canon] = CanonList.CanonMessage(canon, ctx.author, ctx, servers)
			await bot.canonMessages[canon].Send(ctx.channel)
			await bot.canonMessages[canon].ListNames()
		# Skip to a specific number of an existing message
		else:
			if(canon in bot.canonMessages):
				canonMessage = bot.canonMessages[canon]
				if(ctx.author == canonMessage.user):
					if(number <= len(canonMessage.characterList) and number >= 1):
						canonMessage.index = number - 1
						await canonMessage.Edit()
	# OOC character lists
	elif(command in OocMessage.OocList(ctx)):
		oocName = command
		# List all characters of that OOC
		if(number == None):
			bot.oocMessages[oocName] = OocMessage.OocMessage(ctx.author, oocName, ctx, servers)
			await bot.oocMessages[oocName].Send(ctx.channel)
			await bot.oocMessages[oocName].ListNames()
		# Skip to a specific number of an existing message
		else:
			oocMessage = bot.oocMessages[oocName]
			if(ctx.author == oocMessage.user):
				if(number <= len(oocMessage.characterList) and number >= 1):
					oocMessage.index = number - 1
					await oocMessage.Edit()

@bot.command()
async def canonlist(ctx):
	canonList = CanonList.CanonList(servers[str(ctx.guild.id)])
	index = 0
	sendString = 'Valid canons: ```'
	while(index < len(canonList)):
		while(len(sendString) < 1900):
			sendString += ('\n' + '{:<30}: {} characters'.format(canonList[index][0], canonList[index][1]))
			index += 1
			if(index >= len(canonList)):
				break
		sendString += '```'
		await ctx.send(sendString)
		sendString = '```'
	await ctx.send('>charlist [canon] to list characters for a canon')

@bot.command()
async def forward(ctx):
	await ctx.send('and back')
	await asyncio.sleep(2)
	await ctx.send('and then forward and back')
	await asyncio.sleep(2)
	await ctx.send('and then go forward and back')
	await asyncio.sleep(2)
	await ctx.send('and put one foot')
	await ctx.send('forward')

@bot.command()
async def rolemessage(ctx):
	#await ctx.send('Test',view=RoleAssignment.RoleAssignment())
	#embed = discord.Embed()
	#embed.description = "React to add role:\n👩 she/her\n👨 he/him\n👤 they/them"
	#bot.roleMessages[ctx.guild.id] = await ctx.send(embed=embed)
	#await bot.roleMessages[ctx.guild.id].add_reaction('👩')
	#await bot.roleMessages[ctx.guild.id].add_reaction('👨')
	#await bot.roleMessages[ctx.guild.id].add_reaction('👤')
	bot.roleMessages[ctx.guild.id] = RoleAssignment.RoleMessage(ctx)
	print(ctx.guild.id)
	await bot.roleMessages[ctx.guild.id].Send(ctx)

@bot.command()
async def iam(ctx, *, arg=''):
	if(arg == ''):
		validRoles = servers[str(ctx.guild.id)]["roles"]
		#await ctx.send('I need to know what role you want, silly! Valid roles:\n```{}```'.format('\n'.join(list(ROLES.keys()))))
		await ctx.send('I need to know what role you want, silly! Valid roles:\n```{}```'.format('\n'.join(list(validRoles.keys()))))
	elif(arg.lower() == 'the bone of my sword'):
		# Kat is a weeb
		await ctx.send('Steel is my Body and Fire is my Blood.')
		await asyncio.sleep(2)
		await ctx.send('I have created over a Thousand Blades,')
		await asyncio.sleep(2)
		await ctx.send('Unknown to Death,')
		await asyncio.sleep(2)
		await ctx.send('Nor known to Life.')
		await asyncio.sleep(2)
		await ctx.send('Have withstood Pain to create many Weapons')
		await asyncio.sleep(2)
		await ctx.send('Yet those Hands will never hold Anything.')
		await asyncio.sleep(2)
		await ctx.send('So, as I Pray-')
		await asyncio.sleep(2)
		await ctx.send('**UNLIMITED BLADE WORKS**')
		await asyncio.sleep(1)
		await ctx.send(':crossed_swords:'*125)
	elif(arg.lower() == 'the night'):
		Googlify.Batmanify(Googlify.ImageFromURL(str(ctx.author.avatar))).save('tempBat.png')
		await ctx.send(file=discord.File('tempBat.png'))
	else:
		desiredRole = arg.lower()
		validRoles = servers[str(ctx.guild.id)]["roles"]
		#if(desiredRole in ROLES.keys()):
		if(desiredRole in validRoles.keys()):
			#if(ctx.guild.get_role(ROLES[desiredRole]) in ctx.author.roles):
			if(ctx.guild.get_role(validRoles[desiredRole]) in ctx.author.roles):
				await ctx.send('You already have role\n```{}```'.format(desiredRole))
			else:
				#await ctx.author.add_roles(ctx.guild.get_role(ROLES[desiredRole]))
				await ctx.author.add_roles(ctx.guild.get_role(validRoles[desiredRole]))
				await ctx.send('Role `{}` assigned!'.format(desiredRole))
		else:
			await ctx.send('Role `{}` not found.'.format(desiredRole))

@bot.command()
async def iamnot(ctx, *, arg=''):
	if(arg == ''):
		validRoles = servers[str(ctx.guild.id)]["roles"]
		#await ctx.send('I need to know what role you aren\'t, silly! Valid roles:\n```{}```'.format('\n'.join(list(ROLES.keys()))))	
		await ctx.send('I need to know what role you aren\'t, silly! Valid roles:\n```{}```'.format('\n'.join(list(validRoles.keys()))))	
	else:
		validRoles = servers[str(ctx.guild.id)]["roles"]
		desiredRole = arg.lower()
		if(desiredRole in validRoles.keys()):
			#if(ctx.guild.get_role(ROLES[desiredRole]) in ctx.author.roles):
			if(ctx.guild.get_role(validRoles[desiredRole]) in ctx.author.roles):
				#await ctx.author.remove_roles(ctx.guild.get_role(ROLES[desiredRole]))
				await ctx.author.remove_roles(ctx.guild.get_role(validRoles[desiredRole]))
				await ctx.send('Removed role\n```{}```'.format(desiredRole))
			else:
				await ctx.send('You do not have role\n```{}```'.format(desiredRole))
		else:
			await ctx.send('Role `{}` not found.'.format(desiredRole))

@bot.command()
async def faction(ctx):
	#faction = random.choice(FACTIONS)
	factions = servers[str(ctx.guild.id)]['factions']
	faction = random.choice(factions)
	text = ['Uplander! Uplander, make lookings! Swooshy spellycastings is sayings....um....is sayings {} is good choosymakes!'.format(faction),
			'According to the position of the stars, the placement of your bedroom, and the ripeness of this pickle - {} is the best deity for you!'.format(faction),
			'The fates have chosen, oh indecisive one - {} has found you worthy to fight in their name!'.format(faction)]
	await ctx.send(random.choice(text))

@bot.command()
async def hitme(ctx):
	with open('servers/{}/data.json'.format(ctx.guild.id)) as json_data:
		data = json.load(json_data)
	character = random.choice(list(data.keys()))
	characterInfo = data[character]
	output = character_sheet.MakeEmbed(character.title(), characterInfo, servers[str(ctx.guild.id)])
	await ctx.send(embed=output)

@bot.command()
async def templates(ctx):
	await ctx.send('You can find Magician\'s templates here!\n{}'.format(servers[str(ctx.guild.id)]["templates"]))

@bot.command()
@commands.check(check_if_bot_spam)
async def googlify(ctx, *, arg=''):
	#print(type(ctx.author.avatar))
	if(arg == ''):
		Googlify.Googlify(Googlify.ImageFromURL(str(ctx.author.avatar))).save('tempGoogly.png')
		await ctx.send(file=discord.File('tempGoogly.png'))
	elif(len(ctx.message.mentions) > 0):
		Googlify.Googlify(Googlify.ImageFromURL(str(ctx.message.mentions[0].avatar))).save('tempGoogly.png')
		await ctx.send(file=discord.File('tempGoogly.png'))
	else:
		with open('servers/{}/data.json'.format(ctx.guild.id)) as json_data:
			data = json.load(json_data)
		if(arg.lower() in data.keys()):
			Googlify.Googlify(Googlify.ImageFromURL(data[arg.lower()]['image'])).save('tempGoogly.png')
			await ctx.send(file=discord.File('tempGoogly.png'))
		else:
			await ctx.send('Character not found:```{}```'.format(arg.lower()))


@bot.command()
@commands.check(check_if_december)
async def santafy(ctx, *, arg=''):
	if(arg == ''):
		Googlify.Santafy(Googlify.ImageFromURL(str(ctx.author.avatar))).save('tempSanta.png')
		await ctx.send(file=discord.File('tempSanta.png'))
	elif(len(ctx.message.mentions) > 0):
		Googlify.Santafy(Googlify.ImageFromURL(str(ctx.message.mentions[0].avatar))).save('tempSanta.png')
		await ctx.send(file=discord.File('tempSanta.png'))
	else:
		with open('servers/{}/data.json'.format(ctx.guild.id)) as json_data:
			data = json.load(json_data)
		if(arg.lower() in data.keys()):
			Googlify.Santafy(Googlify.ImageFromURL(data[arg.lower()]['image'])).save('tempSanta.png')
			await ctx.send(file=discord.File('tempSanta.png'))
		else:
			await ctx.send('Character not found:```{}```'.format(arg.lower()))

@bot.command()
async def spookify(ctx, *, arg=''):
	if(arg == ''):
		Googlify.Spookify(Googlify.ImageFromURL(str(ctx.author.avatar))).save('tempSpooky.png')
		await ctx.send(file=discord.File('tempSpooky.png'))
	elif(len(ctx.message.mentions) > 0):
		Googlify.Spookify(Googlify.ImageFromURL(str(ctx.message.mentions[0].avatar))).save('tempSpooky.png')
		await ctx.send(file=discord.File('tempSpooky.png'))
	else:
		with open('servers/{}/data.json'.format(ctx.guild.id)) as json_data:
			data = json.load(json_data)
		if(arg.lower() in data.keys()):
			Googlify.Spookify(Googlify.ImageFromURL(data[arg.lower()]['image'])).save('tempSpooky.png')
			await ctx.send(file=discord.File('tempSpooky.png'))
		else:
			await ctx.send('Character not found:```{}```'.format(arg.lower()))

@bot.command()
@commands.check(check_if_december)
async def santafly(ctx, *, arg=''):
	if(arg == ''):
		Googlify.Santafy(Googlify.ImageFromURL(str(ctx.author.avatar)), rand=True).save('tempSanta.png')
		await ctx.send(file=discord.File('tempSanta.png'))
	elif(len(ctx.message.mentions) > 0):
		Googlify.Santafy(Googlify.ImageFromURL(str(ctx.message.mentions[0].avatar)), rand=True).save('tempSanta.png')
		await ctx.send(file=discord.File('tempSanta.png'))
	else:
		with open('servers/{}/data.json'.format(ctx.guild.id)) as json_data:
			data = json.load(json_data)
		if(arg.lower() in data.keys()):
			Googlify.Santafy(Googlify.ImageFromURL(data[arg.lower()]['image']), rand=True).save('tempSanta.png')
			await ctx.send(file=discord.File('tempSanta.png'))
		else:
			await ctx.send('Character not found:```{}```'.format(arg.lower()))

@bot.command(name='2019ify')
@commands.check(check_if_december)
async def Happy2019(ctx, *, arg=''):
	if(arg == ''):
		Googlify.Happy2019(Googlify.ImageFromURL(str(ctx.author.avatar))).save('temp2019.png')
		await ctx.send(file=discord.File('temp2019.png'))
	elif(len(ctx.message.mentions) > 0):
		Googlify.Happy2019(Googlify.ImageFromURL(str(ctx.message.mentions[0].avatar))).save('temp2019.png')
		await ctx.send(file=discord.File('temp2019.png'))
	else:
		with open('servers/{}/data.json'.format(ctx.guild.id)) as json_data:
			data = json.load(json_data)
		if(arg.lower() in data.keys()):
			Googlify.Happy2019(Googlify.ImageFromURL(data[arg.lower()]['image'])).save('temp2019.png')
			await ctx.send(file=discord.File('temp2019.png'))
		else:
			await ctx.send('Character not found:```{}```'.format(arg.lower()))

@bot.command()
@commands.check(check_if_february)
async def valentines(ctx, fromChar='', toChar=''):
	""">valentines "character 1" "character 2" for a cheesy MS Paint Valentine's card.
	   Character names need to be enclosed in "quotation marks" """
	if(fromChar == '' or toChar == ''):
		ctx.send("I need to know who's sending a valentines to whom, silly!")
	else:
		with open('servers/{}/data.json'.format(ctx.guild.id)) as json_data:
			data = json.load(json_data)
		if(fromChar.lower() not in data.keys()):
			await ctx.send('Character not found:```{}```'.format(fromChar.lower()))
		elif(toChar.lower() not in data.keys()):
			await ctx.send('Character not found:```{}```'.format(toChar.lower()))
		else:
			fromImage = Googlify.ImageFromURL(data[fromChar.lower()]['image'])
			toImage = Googlify.ImageFromURL(data[toChar.lower()]['image'])
			valentine_generator.MakeImage(fromImage, toImage).save('tempValentine.png')
			await ctx.send(file=discord.File('tempValentine.png'))

@bot.command()
@commands.check(check_if_bot_spam)
async def rps(ctx):
	'''Mention someone with @<username> to challenge them to a rousing bout of rock-paper-scissors.
	   Check your DMs and respond with an emoji to play the game. The winner will be announced publicly.'''
	if(len(ctx.message.mentions) > 0):
		bot.rpsGames.sort(key=lambda x: x.valid, reverse=True)
		while(False in [game.valid for game in bot.rpsGames]):
			bot.rpsGames.pop()

		if(ctx.message.mentions[0].dm_channel == None):
			await ctx.message.mentions[0].create_dm()
		if(ctx.author.dm_channel == None):
			await ctx.author.create_dm()
		bot.rpsGames.append(RockPaperScissors.Game(ctx.message, ctx.author, ctx.message.mentions[0]))
		await bot.rpsGames[-1].Send()

@bot.command()
@commands.check(check_if_bot_spam)
async def tot(ctx):
	'''Mention someone with @<username> to challenge them to a rousing bout of trick or treat.
	   Check your DMs and respond with an emoji. The result will be announced publicly.'''
	if(len(ctx.message.mentions) > 0):
		bot.totGames.sort(key=lambda x: x.valid, reverse=True)
		while(False in [game.valid for game in bot.rpsGames]):
			bot.rpsGames.pop()
		if(ctx.message.mentions[0].dm_channel == None):
			await ctx.message.mentions[0].create_dm()
		if(ctx.author.dm_channel == None):
			await ctx.author.create_dm()
		bot.totGames.append(TrickOrTreat.Game(ctx.message, ctx.author, ctx.message.mentions[0]))
		await bot.totGames[-1].Send()

@bot.command(name='hmk')
@commands.check(check_if_bot_spam)
async def hugmarrykill(ctx, *, arg=''):
	'''Mention someone with @<username> to begin a hug-marry-kill game.
	   Use >hmk with no arguments to show the scores for all characters.
	   Use >hmk <charname> to show the scores for a particular character.'''
	# Start a game if someone is mentioned
	if(len(ctx.message.mentions) > 0):
		# Sort games by validity, so invalid games are at the end of the list
		bot.hmkGames.sort(key = lambda x: x.valid, reverse=True)
		# Remove all invalid games. Games are invalid if they failed to start or ended.
		while(False in [game.valid for game in bot.hmkGames]):
			bot.hmkGames.pop()
		# Initialize a new game
		bot.hmkGames.append(hmk.Game(ctx.message, ctx.author, ctx.message.mentions[0], ctx.guild.id, servers[str(ctx.guild.id)]))
		await bot.hmkGames[-1].Send()
	# Search for the scores of a character
	elif(arg != ''):
		name = arg.lower()
		# Check if the server is valid
		if(str(ctx.guild.id) in servers):
			# Fetch character data
			with open('servers/{}/data.json'.format(ctx.guild.id)) as json_data:
				data = json.load(json_data)
			# Fetch hmk score data
			with open('servers/{}/hmk_scores.json'.format(ctx.guild.id)) as json_data:
				hmkdata = json.load(json_data)
			# Check if the character is valid
			if(name in data.keys()):
				characterInfo = data[name]
				# Check if the character has scores. If so, send their scores.
				if(name in hmkdata.keys()):
					output = hmk.HMKEmbed(name.title(), characterInfo, hmkdata[name], servers[str(ctx.guild.id)])
				# If the character has no hmk scores, give them 0 in each category.
				else:
					output = hmk.HMKEmbed(name.title(), characterInfo, {'hug': 0, 'marry': 0, 'kill': 0}, servers[str(ctx.guild.id)])
				await ctx.send(embed=output)
			else:
				output = 'Invalid character!\n```{}```'.format(name)
				await ctx.send(output)
	# Show all scores with an interactable embed.
	else:
		bot.hmkScoreMessages[ctx.author] = hmk.ScoreMessage(ctx.author, ctx, servers)
		await bot.hmkScoreMessages[ctx.author].Send(ctx.channel)
		await bot.hmkScoreMessages[ctx.author].ListNames()

@bot.command()
@commands.check(check_if_bot_spam)
async def pet(ctx):
	'''Pet the bot. It is a good bot.
	Shoutouts to my friend Haruka for implementing this in a different bot, which I stole it from.'''
	responses = ['woof', 'bwoof', 'bark', 'bork', 'arf']
	bot.petCounter += 1
	await bot.change_presence(activity=discord.Game("with {} pets today.".format(bot.petCounter)))
	await ctx.send('{}'.format(random.choice(responses)))

#@bot.command(name='boons')
#@commands.check(check_if_staff_or_test)
#async def boonslist(ctx, number=10, minEX=1, minS=1):
#async def boonslist(ctx, *args):
#	if(len(args) > 0):
#		number= args[0]
#	minEX = 1
#	minS = 1
#	if(len(args) > 1):
#		names = args[1:]
#	batch = boons.BoonBatch(number, minEX, minS)
#	embeds = []
#	for boon in range(len(batch)):
#		if(boon < len(names)):
#			embeds.append(boons.BoonEmbed(batch[boon], names[boon]))
#		else:
#			embeds.append(boons.BoonEmbed(batch[boon]))
#	#embeds = [boons.BoonEmbed(batch[boon], names[boon]) for boon in range(len(batch))]
#	for embed in embeds:
#		await ctx.send(embed=embed)

@bot.command(name='boons')
async def boonslist(ctx, *, arg=''):
	args = arg.split('\n')
	if(len(args) > 0):
		number = len(args)
	else:
		number = 10
	minEX = 1
	minS = 1
	if(len(args) > 0):
		names = args
	else:
		names = []
	batch = boons.BoonBatch(number, minEX, minS)
	embeds = []
	for boon in range(len(batch)):
		if(boon < len(names)):
			embeds.append(boons.BoonEmbed(batch[boon], names[boon]))
		else:
			embeds.append(boons.BoonEmbed(batch[boon]))
	for embed in embeds:
		await ctx.send(embed=embed)

@bot.command(name='roll')
async def rolldie(ctx, *, arg=''):
	await ctx.send(roll.roll(arg))

@tasks.loop(hours=24)
async def ResetPetCounter():
	bot.petCounter = 0
	await bot.change_presence(activity=discord.Game("with {} pets today.".format(bot.petCounter)))

@ResetPetCounter.before_loop
async def before_ResetPetCounter():
	now = datetime.datetime.utcnow()
	later = now.replace(hour=4,minute=0,second=0)
	if(later < now):
		later += datetime.timedelta(days=1)
	#await asyncio.sleep_until(later)
	await discord.utils.sleep_until(later)

@bot.event
async def on_reaction_add(reaction, user):
	if(user != bot.user):
		for rpsGame in bot.rpsGames:
			if(rpsGame.valid):
				if(reaction.message.id == rpsGame.challengerMessage.id and user == rpsGame.challenger):
					await rpsGame.UpdateChallengerResponse(reaction)
				elif(reaction.message.id == rpsGame.targetMessage.id and user == rpsGame.target):
					await rpsGame.UpdateTargetResponse(reaction)
		for totGame in bot.totGames:
			if(totGame.valid):
				if(reaction.message.id == totGame.targetMessage.id and user == totGame.target):
					await totGame.UpdateTargetResponse(reaction)
		for hmkGame in bot.hmkGames:
			if(hmkGame.valid):
				if(reaction.message.id == hmkGame.targetMessage.id and user == hmkGame.target):
					if(str(reaction) == str(hmk.arrowLeft)):
						await hmkGame.Back()
					elif(str(reaction) == str(hmk.arrowRight)):
						await hmkGame.Advance()
					elif(str(reaction) == str(hmk.listEmoji)):
						await hmkGame.ListNames()
					else:
						await hmkGame.RegisterAnswer(reaction.emoji)
		for deity in bot.factionMessages:
			if(bot.factionMessages[deity] != None):
				if(bot.factionMessages[deity].message.id == reaction.message.id and bot.factionMessages[deity].user == user):
					if(str(reaction) == str(DeityMessage.arrowLeft)):
						await bot.factionMessages[deity].Back()
					elif(str(reaction) == str(DeityMessage.arrowRight)):
						await bot.factionMessages[deity].Advance()
					elif(str(reaction) == str(DeityMessage.listEmoji)):
						await bot.factionMessages[deity].ListNames()
		for canon in bot.canonMessages:
			if(bot.canonMessages[canon] != None):
				if(bot.canonMessages[canon].message.id == reaction.message.id and bot.canonMessages[canon].user == user):
					if(str(reaction) == str(CanonList.arrowLeft)):
						await bot.canonMessages[canon].Back()
					elif(str(reaction) == str(CanonList.arrowRight)):
						await bot.canonMessages[canon].Advance()
					elif(str(reaction) == str(CanonList.listEmoji)):
						await bot.canonMessages[canon].ListNames()
		for ooc in bot.oocMessages:
			if(bot.oocMessages[ooc] != None):
				if(bot.oocMessages[ooc].message.id == reaction.message.id and bot.oocMessages[ooc].user == user):
					if(str(reaction) == str(OocMessage.arrowLeft)):
						await bot.oocMessages[ooc].Back()
					elif(str(reaction) == str(OocMessage.arrowRight)):
						await bot.oocMessages[ooc].Advance()
					elif(str(reaction) == str(OocMessage.listEmoji)):
						await bot.oocMessages[ooc].ListNames()
		for hmkScore in bot.hmkScoreMessages:
			if(bot.hmkScoreMessages[hmkScore] != None):
				if(bot.hmkScoreMessages[hmkScore].message.id == reaction.message.id and bot.hmkScoreMessages[hmkScore].user == user):
					if(str(reaction) == str(hmk.arrowLeft)):
						await bot.hmkScoreMessages[hmkScore].Back()
					if(str(reaction) == str(hmk.arrowRight)):
						await bot.hmkScoreMessages[hmkScore].Advance()
					if(str(reaction) == str(hmk.listEmoji)):
						await bot.hmkScoreMessages[hmkScore].ListNames()
					if(str(reaction) == str(hmk.hEmoji)):
						await bot.hmkScoreMessages[hmkScore].Sort(str(reaction))
					if(str(reaction) == str(hmk.mEmoji)):
						await bot.hmkScoreMessages[hmkScore].Sort(str(reaction))
					if(str(reaction) == str(hmk.kEmoji)):
						await bot.hmkScoreMessages[hmkScore].Sort(str(reaction))
		for roleMsg in bot.roleMessages:
			if(bot.roleMessages[roleMsg].message.id == reaction.message.id):
				await bot.roleMessages[roleMsg].SetRole(str(reaction), user)


if(__name__ == '__main__'):
	ResetPetCounter.start()
	bot.run(TOKEN)
	