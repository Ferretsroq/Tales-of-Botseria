import discord
from enum import Enum
import asyncio
import json
import random
import character_sheet

fEmoji = chr(0x1F1EB)
mEmoji = chr(0x1F1F2)
kEmoji = chr(0x1F1F0)
arrowLeft = chr(0x2B05)
arrowRight = chr(0x27A1)
listEmoji = chr(0x1f4dc)
emojiQuestion = '\u2754'

class Answer(Enum):
    fuck = fEmoji
    marry = mEmoji
    kill = kEmoji

class Game:
	'''Object to hold fmk game data'''
	def __init__(self, initialMessage=None, challenger=None, target=None):
		# Populate data
		if(challenger != None and target != None):
			self.valid = True
			self.initialMessage = initialMessage
			self.challenger = challenger
			self.target = target
			self.targetContent = 'You have been challenged by {} to a rousing game of fuck-marry-kill!\nYour options:'.format(challenger.display_name)
			self.characterMessage = CharacterMessage(target, self.targetContent)
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
		'''
		result = (Answer[self.targetResponse].value - Answer[self.challengerResponse].value)%3
		gameWinner = ''
		if(result == 1):
			gameWinner = self.target.display_name
		elif(result == 0):
			gameWinner = 'It\'s a draw!'
		elif(result == 2):
			gameWinner = self.challenger.display_name
		await self.initialMessage.channel.send('Winner: {}'.format(gameWinner))
		'''
		if(self.characterMessage.responses.count(str(fEmoji)) == 1 and 
			self.characterMessage.responses.count(str(mEmoji)) == 1 and
			self.characterMessage.responses.count(str(kEmoji)) == 1):
			await self.initialMessage.channel.send('{} says....\nFUCK - {}\nMARRY - {}\nKILL - {}'.format(self.target.name, self.characterMessage.fuck, self.characterMessage.marry, self.characterMessage.kill))
			self.Reset()
		#print(self.characterMessage.responses)
	# Set the challenger's response based on their reaction
	'''
	async def UpdateChallengerResponse(self, reaction):
		if(str(reaction) == str(rock)):
			self.challengerResponse = 'rock'
		elif(str(reaction) == str(paper)):
			self.challengerResponse = 'paper'
		elif(str(reaction) == str(scissors)):
			self.challengerResponse = 'scissors'
		if(self.challengerResponse != None):
			self.challengerEmbed = discord.Embed(title="ROCK PAPER SCISSORS", description=self.challengerContent+'\nYou have chosen {}!'.format(self.challengerResponse))
			await self.challengerMessage.edit(embed=self.challengerEmbed)
		# If both players have answered, end the game
		if(self.challengerResponse!= None and self.targetResponse != None):
			await self.winner()
	'''
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
	def __init__(self, user, targetContent):
		with open('data.json') as json_data:
			data = json.load(json_data)
		self.user = user
		self.characterList = random.choices(list(data.keys()), k=3)
		self.responses = [None, None, None]
		#self.characterList = [character for character in data if character.lower() in validCharacters]
		self.index = 0
		self.message = None
		self.targetContent = targetContent
		self.embed = discord.Embed(title="FUCK MARRY KILL", description=self.targetContent)
		self.fuck = None
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
	async def ListNames(self):
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
		with open('data.json') as json_data:
			data = json.load(json_data)
		self.embed = character_sheet.MakeEmbed(self.characterList[self.index], data[self.characterList[self.index]])
		self.embed.title = "FUCK MARRY KILL - {}".format(self.characterList[self.index])
		self.embed.description = await self.ListNames()
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
		await self.message.add_reaction(fEmoji)
		await self.message.add_reaction(mEmoji)
		await self.message.add_reaction(kEmoji)
	async def RegisterAnswer(self, response):
		self.responses[self.index] = str(response)
		if(str(response) == str(fEmoji)):
			self.fuck = self.characterList[self.index]
		elif(str(response) == str(mEmoji)):
			self.marry = self.characterList[self.index]
		elif(str(response) == str(kEmoji)):
			self.kill = self.characterList[self.index]
		await self.Edit()