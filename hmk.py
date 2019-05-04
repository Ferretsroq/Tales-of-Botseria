import discord
from enum import Enum
import asyncio
import json
import random
import character_sheet
import numpy as np

hEmoji = chr(0x1F1ED)
mEmoji = chr(0x1F1F2)
kEmoji = chr(0x1F1F0)
arrowLeft = chr(0x2B05)
arrowRight = chr(0x27A1)
listEmoji = chr(0x1f4dc)
emojiQuestion = '\u2754'

class Answer(Enum):
    hug = hEmoji
    marry = mEmoji
    kill = kEmoji

class Game:
	'''Object to hold fmk game data'''
	def __init__(self, initialMessage=None, challenger=None, target=None, serverID=0, server={}):
		self.server = server
		self.serverID = serverID
		# Populate data
		if(challenger != None and target != None):
			self.valid = True
			self.initialMessage = initialMessage
			self.challenger = challenger
			self.target = target
			self.targetContent = 'You have been challenged by {} to a rousing game of hug-marry-kill!\nYour options:'.format(challenger.display_name)
			self.characterMessage = CharacterMessage(target, self.targetContent, self.serverID, self.server)
			self.targetEmbed = self.characterMessage.embed
			self.targetMessage = None
			self.targetResponse = None
		# Allow the game to be initialized with nothing in it
		else:
			self.valid = False
			self.initialMessage = None
			self.challenger = None
			self.target = None
			self.challengerContent = None
			self.targetContent = None
			self.challengerEmbed = None
			self.targetEmbed = None
			self.challengerMessage = None
			self.targetMessage = None
			self.challengerResponse = None
			self.targetResponse = None
	# Send initial game messages to players
	async def Send(self):
		self.targetMessage = await self.characterMessage.Send(self.initialMessage.channel)
		await self.SetReactions(self.targetMessage)
	# Set rock/paper/scissors emoji on the message. We can not call clear_reactions on a DM.
	async def SetReactions(self, message):
		pass
	# Determine the winner and clear the game
	async def winner(self):
		if(len(list(set([self.characterMessage.hug, self.characterMessage.marry, self.characterMessage.kill]))) == 3 and
			None not in [self.characterMessage.hug, self.characterMessage.marry, self.characterMessage.kill]):
			if(self.target.nick == None):
				name = self.target.name
			else:
				name = self.target.nick
			await self.initialMessage.channel.send('{} says....\nHUG - {}\nMARRY - {}\nKILL - {}'.format(name, self.characterMessage.hug, self.characterMessage.marry, self.characterMessage.kill))
			self.Reset()
			self.UpdateScores()
		elif(self.characterMessage.responses[0] == self.characterMessage.responses[1] == self.characterMessage.responses[2] and None not in self.characterMessage.responses):
			await self.initialMessage.channel.send("Hey there {} could you do me a real solid and not be such a SOGGY MARSHMALLOW who picks the same answers that'd be great! Thanks! xoxo".format(self.target.mention))
			self.Reset()
			self.UpdateScores()

	def UpdateScores(self):
		scoreFile = open('./servers/{}/hmk_scores.json'.format(self.serverID))
		scores = json.load(scoreFile)
		scoreFile.close()
		# Initialize character score if not present
		if(self.characterMessage.hug.lower() not in scores):
			scores[self.characterMessage.hug.lower()] = {'hug': 0, 'marry': 0, 'kill': 0}
		if(self.characterMessage.marry.lower() not in scores):
			scores[self.characterMessage.marry.lower()] = {'hug': 0, 'marry': 0, 'kill': 0}
		if(self.characterMessage.kill.lower() not in scores):
			scores[self.characterMessage.kill.lower()] = {'hug': 0, 'marry': 0, 'kill': 0}
		# Update scores
		scores[self.characterMessage.hug.lower()]['hug'] += 1
		scores[self.characterMessage.marry.lower()]['marry'] += 1
		scores[self.characterMessage.kill.lower()]['kill'] += 1
		scoreFile = open('./servers/{}/hmk_scores.json'.format(self.serverID), 'w')
		json.dump(scores, scoreFile)
		scoreFile.close()


	# Set the target's response based on their reaction
	async def UpdateTargetResponse(self, reaction):
		self.characterMessage.RegisterAnswer(reaction)
		await self.winner()
	# Clear all game data
	def Reset(self):
		self.valid = False
		self.initialMessage = None
		self.challenger = None
		self.target = None
		self.challengerContent = None
		self.targetContent = None
		self.challengerEmbed = None
		self.targetEmbed = None
		self.challengerMessage = None
		self.targetMessage = None
		self.challengerResponse = None
		self.targetResponse = None
	async def Advance(self):
		await self.characterMessage.Advance()
	async def Back(self):
		await self.characterMessage.Back()
	async def ListNames(self):
		await self.characterMessage.ListNames()
	async def RegisterAnswer(self, response):
		await self.characterMessage.RegisterAnswer(response)
		await self.winner()

class CharacterMessage:
	def __init__(self, user, targetContent, serverID=0, server={}):
		#with open('data.json') as json_data:
	#		data = json.load(json_data)
		self.serverID = serverID
		self.server = server
		with open('servers/{}/data.json'.format(self.serverID)) as json_data:
			data = json.load(json_data)
		self.user = user
		self.characterList = list(np.random.choice(list(data.keys()), size=3, replace=False))
		self.responses = [None, None, None]
		#self.characterList = [character for character in data if character.lower() in validCharacters]
		self.index = 0
		self.message = None
		self.targetContent = targetContent
		self.embed = discord.Embed(title="HUG MARRY KILL", description=self.targetContent)
		self.hug = None
		self.marry = None
		self.kill = None
	async def Advance(self):
		self.index += 1
		if(self.index+1 > len(self.characterList)):
			self.index = 0
		await self.Edit()
	async def Back(self):
		self.index -= 1
		if(self.index < 0):
			self.index = len(self.characterList)-1
		await self.Edit()
	def ListNames(self):
		names = ['{}: {}'.format(x+1, self.characterList[x]) for x in range(len(self.characterList))]
		for name in range(len(names)):
			if(self.responses[name] in [answer.value for answer in Answer]):
				names[name] += ' - **{}**'.format(Answer(self.responses[name]).name)
		#names[self.index] = '**{}**'.format(names[self.index])
		#content = '\n'.join(['{}: {}'.format(x+1, self.characterList[x]) for x in range(len(self.characterList))])
		content = '\n'.join(names)
		return content
		#await self.Edit(content)
	async def Edit(self, content=''):
		#with open('data.json') as json_data:
		#	data = json.load(json_data)
		with open('servers/{}/data.json'.format(self.serverID)) as json_data:
			data = json.load(json_data)
		self.embed = character_sheet.MakeEmbed(self.characterList[self.index], data[self.characterList[self.index]], self.server)
		self.embed.title = "HUG MARRY KILL - {}".format(self.characterList[self.index])
		self.embed.description = self.ListNames()
		await self.message.edit(embed=self.embed)
		#content = await self.ListNames()
		await self.SetReactions()
	async def Send(self, channel):
		self.message = await channel.send(embed=self.embed)
		await self.Edit()
		return self.message
	async def SetReactions(self):
		await self.message.clear_reactions()
		await self.message.add_reaction(arrowLeft)
		await self.message.add_reaction(arrowRight)
		#await self.message.add_reaction(listEmoji)
		await self.message.add_reaction(hEmoji)
		await self.message.add_reaction(mEmoji)
		await self.message.add_reaction(kEmoji)
	async def RegisterAnswer(self, response):
		self.responses[self.index] = str(response)
		if(str(response) == str(hEmoji)):
			self.hug = self.characterList[self.index]
		elif(str(response) == str(mEmoji)):
			self.marry = self.characterList[self.index]
		elif(str(response) == str(kEmoji)):
			self.kill = self.characterList[self.index]
		await self.Edit()