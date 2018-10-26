import discord
from enum import Enum
import asyncio

# Shoutouts to Haruka-Sama, a v v v good /r/pokemon mod who understands emoji wizardry
rock = chr(0x1f315)
paper = chr(0x1f4dc)
scissors = '\u2702'

class Answer(Enum):
	rock = 0
	paper = 1
	scissors = 2

class Game:
	'''Object to hold rock paper scissors game data'''
	def __init__(self, initialMessage=None, challenger=None, target=None):
		# Populate data
		if(challenger != None and target != None):
			self.valid = True
			self.initialMessage = initialMessage
			self.challenger = challenger
			self.target = target
			self.challengerContent = 'You have challenged {} to a rousing bout of rock-paper-scissors!\nChoose your weapon:'.format(target.display_name)
			self.targetContent = 'You have been challenged by {} to a rousing bout of rock-paper-scissors!\nChoose your weapon:'.format(challenger.display_name)
			self.challengerEmbed = discord.Embed(title="ROCK PAPER SCISSORS", description=self.challengerContent)
			self.targetEmbed = discord.Embed(title="ROCK PAPER SCISSORS", description=self.targetContent)
			self.challengerMessage = None
			self.targetMessage = None
			self.challengerResponse = None
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
		self.challengerMessage = await self.challenger.dm_channel.send(embed=self.challengerEmbed)
		self.targetMessage = await self.target.dm_channel.send(embed=self.targetEmbed)
		await self.SetReactions(self.challengerMessage)
		await self.SetReactions(self.targetMessage)
	# Set rock/paper/scissors emoji on the message. We can not call clear_reactions on a DM.
	async def SetReactions(self, message):
		await message.add_reaction(rock)
		await message.add_reaction(paper)
		await message.add_reaction(scissors)
	# Determine the winner and clear the game
	async def winner(self):
		result = (Answer[self.targetResponse].value - Answer[self.challengerResponse].value)%3
		gameWinner = ''
		if(result == 1):
			gameWinner = self.target.display_name
		elif(result == 0):
			gameWinner = 'It\'s a draw!'
		elif(result == 2):
			gameWinner = self.challenger.display_name
		await self.initialMessage.channel.send('Winner: {}'.format(gameWinner))
		self.Reset()
	# Set the challenger's response based on their reaction
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
	# Set the target's response based on their reaction
	async def UpdateTargetResponse(self, reaction):
		if(str(reaction) == str(rock)):
			self.targetResponse = 'rock'
		elif(str(reaction) == str(paper)):
			self.targetResponse = 'paper'
		elif(str(reaction) == str(scissors)):
			self.targetResponse = 'scissors'
		if(self.targetResponse != None):
			self.targetEmbed = discord.Embed(title="ROCK PAPER SCISSORS", description=self.targetContent+'\nYou have chosen {}!'.format(self.targetResponse))
			await self.targetMessage.edit(embed=self.targetEmbed)
		# If both players have answered, end the game
		if(self.challengerResponse != None and self.targetResponse != None):
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