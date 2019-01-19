import discord
from discord.ext import commands
import character_sheet, json, asyncio
import random
import Googlify, RockPaperScissors, boons, DeityMessage, CanonList, OocMessage, hmk
import re, time

TOKEN = open('token.token').read()

bot = commands.Bot(command_prefix='>', case_insensitive=True)

ROLES = {
		"solara": 503993134037073932,
		"tiamat": 503993293378420746,
		"mistral": 503993326672806119,
		"proserpina": 503993351876378644,
		"skirnir": 503993370302218241,
		"lucifiel": 503993386588700672,
		"open": 503994473655697408,
		"closed": 503994494690131969,
		"hiatus": 503994516148191242,
		"he/him": 522482243004923914,
		"she/her": 522482193067671561,
		"they/them": 522482276798431232
		}
STAFFROLE = 503948857298780160
FACTIONS = ["SOLARA", "TIAMAT", "MISTRAL", "PROSERPINA", "SKIRNIR", "LUCIFIEL"]
BOTCHANNEL = 503997270841229346
TESTCHANNEL = 379374543237545985
bot.hmkGames = []
bot.rpsGames = []
bot.factionMessages = {'solara': None,
							'tiamat': None,
							'mistral': None,
							'proserpina': None,
							'skirnir': None,
							'lucifiel': None,
							'all': None}
bot.canonMessages = {}
bot.oocMessages = {}

def check_if_test_channel(ctx):
	return ctx.channel.id == TESTCHANNEL

def check_if_staff_or_test(ctx):
	return ctx.guild.get_role(STAFFROLE) in ctx.author.roles or check_if_test_channel(ctx)

def check_if_december(ctx):
	return (time.localtime().tm_mon == 12) or (check_if_test_channel(ctx))

def check_if_bot_spam(ctx):
	return ctx.channel.id == BOTCHANNEL or check_if_test_channel(ctx)



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
	await character_sheet.repopulate(ctx.channel)
	await ctx.send('Repopulated character list!')

@bot.command()
@commands.check(check_if_staff_or_test)
async def fetch(ctx):
	'''***STAFF ONLY***'''
	await character_sheet.Fetch(ctx.channel)

@bot.command()
async def char(ctx, *, arg):
	name = arg.lower()
	with open('data.json') as json_data:
		data = json.load(json_data)
	if(name in data.keys()):
		characterInfo = data[name]
		output = character_sheet.MakeEmbed(name.title(), characterInfo)
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
			bot.factionMessages['all'] = DeityMessage.DeityMessage('all', ctx.author)
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
			bot.factionMessages[deity] = DeityMessage.DeityMessage(deity, ctx.author)
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
	elif(command in [canon[0] for canon in CanonList.CanonList()]):
		canon = command
		# List all characters of that canon
		if(number == None):
			bot.canonMessages[canon] = CanonList.CanonMessage(canon, ctx.author)
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
	elif(command in OocMessage.OocList()):
		oocName = command
		# List all characters of that OOC
		if(number == None):
			bot.oocMessages[oocName] = OocMessage.OocMessage(ctx.author, oocName)
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
	canonList = CanonList.CanonList()
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
async def iam(ctx, *, arg=''):
	if(arg == ''):
		await ctx.send('I need to know what role you want, silly! Valid roles:\n```{}```'.format('\n'.join(list(ROLES.keys()))))
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
		Googlify.Batmanify(Googlify.ImageFromURL(ctx.author.avatar_url)).save('tempBat.png')
		await ctx.send(file=discord.File('tempBat.png'))
	else:
		desiredRole = arg.lower()
		if(desiredRole in ROLES.keys()):
			if(ctx.guild.get_role(ROLES[desiredRole]) in ctx.author.roles):
				await ctx.send('You already have role\n```{}```'.format(desiredRole))
			else:
				await ctx.author.add_roles(ctx.guild.get_role(ROLES[desiredRole]))
				await ctx.send('Role `{}` assigned!'.format(desiredRole))
		else:
			await ctx.send('Role `{}` not found.'.format(desiredRole))

@bot.command()
async def iamnot(ctx, *, arg=''):
	if(arg == ''):
		await ctx.send('I need to know what role you aren\'t, silly! Valid roles:\n```{}```'.format('\n'.join(list(ROLES.keys()))))	
	else:
		desiredRole = arg.lower()
		if(desiredRole in ROLES.keys()):
			if(ctx.guild.get_role(ROLES[desiredRole]) in ctx.author.roles):
				await ctx.author.remove_roles(ctx.guild.get_role(ROLES[desiredRole]))
				await ctx.send('Removed role\n```{}```'.format(desiredRole))
			else:
				await ctx.send('You do not have role\n```{}```'.format(desiredRole))
		else:
			await ctx.send('Role `{}` not found.'.format(desiredRole))

@bot.command()
async def faction(ctx):
	faction = random.choice(FACTIONS)
	text = ['Uplander! Uplander, make lookings! Swooshy spellycastings is sayings....um....is sayings {} is good choosymakes!'.format(faction),
			'According to the position of the stars, the placement of your bedroom, and the ripeness of this pickle - {} is the best deity for you!'.format(faction),
			'The fates have chosen, oh indecisive one - {} has found you worthy to fight in their name!'.format(faction)]
	await ctx.send(random.choice(text))

@bot.command()
async def templates(ctx):
	await ctx.send('You can find Magician\'s templates here!\nhttp://heavensfall.jcink.net/index.php?showtopic=22')

@bot.command()
async def googlify(ctx, *, arg=''):
	if(arg == ''):
		Googlify.Googlify(Googlify.ImageFromURL(ctx.author.avatar_url)).save('tempGoogly.png')
		await ctx.send(file=discord.File('tempGoogly.png'))
	elif(len(ctx.message.mentions) > 0):
		Googlify.Googlify(Googlify.ImageFromURL(ctx.message.mentions[0].avatar_url)).save('tempGoogly.png')
		await ctx.send(file=discord.File('tempGoogly.png'))
	else:
		with open('data.json') as json_data:
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
		Googlify.Santafy(Googlify.ImageFromURL(ctx.author.avatar_url)).save('tempSanta.png')
		await ctx.send(file=discord.File('tempSanta.png'))
	elif(len(ctx.message.mentions) > 0):
		Googlify.Santafy(Googlify.ImageFromURL(ctx.message.mentions[0].avatar_url)).save('tempSanta.png')
		await ctx.send(file=discord.File('tempSanta.png'))
	else:
		with open('data.json') as json_data:
			data = json.load(json_data)
		if(arg.lower() in data.keys()):
			Googlify.Santafy(Googlify.ImageFromURL(data[arg.lower()]['image'])).save('tempSanta.png')
			await ctx.send(file=discord.File('tempSanta.png'))
		else:
			await ctx.send('Character not found:```{}```'.format(arg.lower()))

@bot.command()
@commands.check(check_if_december)
async def santafly(ctx, *, arg=''):
	if(arg == ''):
		Googlify.Santafy(Googlify.ImageFromURL(ctx.author.avatar_url), rand=True).save('tempSanta.png')
		await ctx.send(file=discord.File('tempSanta.png'))
	elif(len(ctx.message.mentions) > 0):
		Googlify.Santafy(Googlify.ImageFromURL(ctx.message.mentions[0].avatar_url), rand=True).save('tempSanta.png')
		await ctx.send(file=discord.File('tempSanta.png'))
	else:
		with open('data.json') as json_data:
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
		Googlify.Happy2019(Googlify.ImageFromURL(ctx.author.avatar_url)).save('temp2019.png')
		await ctx.send(file=discord.File('temp2019.png'))
	elif(len(ctx.message.mentions) > 0):
		Googlify.Happy2019(Googlify.ImageFromURL(ctx.message.mentions[0].avatar_url)).save('temp2019.png')
		await ctx.send(file=discord.File('temp2019.png'))
	else:
		with open('data.json') as json_data:
			data = json.load(json_data)
		if(arg.lower() in data.keys()):
			Googlify.Happy2019(Googlify.ImageFromURL(data[arg.lower()]['image'])).save('temp2019.png')
			await ctx.send(file=discord.File('temp2019.png'))
		else:
			await ctx.send('Character not found:```{}```'.format(arg.lower()))

@bot.command()
@commands.check(check_if_bot_spam)
async def rps(ctx):
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

@bot.command(name='hmk')
@commands.check(check_if_bot_spam)
async def hugmarrykill(ctx):
	if(len(ctx.message.mentions) > 0):
		bot.hmkGames.sort(key = lambda x: x.valid, reverse=True)
		while(False in [game.valid for game in bot.hmkGames]):
			bot.hmkGames.pop()
		bot.hmkGames.append(hmk.Game(ctx.message, ctx.author, ctx.message.mentions[0]))
		await bot.hmkGames[-1].Send()


@bot.command(name='boons')
@commands.check(check_if_staff_or_test)
async def boonslist(ctx, number=10, minEX=1, minS=1):
	batch = boons.BoonBatch(number, minEX, minS)
	embeds = [boons.BoonEmbed(boon) for boon in batch]
	for embed in embeds:
		await ctx.send(embed=embed)


@bot.event
async def on_reaction_add(reaction, user):
	if(user != bot.user):
		for rpsGame in bot.rpsGames:
			if(rpsGame.valid):
				if(reaction.message.id == rpsGame.challengerMessage.id and user == rpsGame.challenger):
					await rpsGame.UpdateChallengerResponse(reaction)
				elif(reaction.message.id == rpsGame.targetMessage.id and user == rpsGame.target):
					await rpsGame.UpdateTargetResponse(reaction)
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


if(__name__ == '__main__'):
	bot.run(TOKEN)
