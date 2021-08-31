import discord
from enum import Enum
import asyncio

candyEmoji = chr(0x1F36C)
ghostEmoji = chr(0x1F47B)

class Game:
	'''Object to hold rock paper scissors game data'''
	def __init__(self, initialMessage=None, challenger=None, target=None):
		# Populate data
		if(challenger != None and target != None):
			self.valid = True
			self.initialMessage = initialMessage
			self.challenger = challenger
			self.target = target
			#self.challengerContent = ''
			self.targetContent = 'Knock knock! {} is here and they shout "TRICK OR TREAT!"'.format(challenger.display_name)
			#self.challengerEmbed = discord.Embed(title="ROCK PAPER SCISSORS", description=self.challengerContent)
			self.targetEmbed = discord.Embed(title="TRICK OR TREAT!", description=self.targetContent)
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
		#self.challengerMessage = await self.challenger.dm_channel.send(embed=self.challengerEmbed)
		self.targetMessage = await self.target.dm_channel.send(embed=self.targetEmbed)
		#await self.SetReactions(self.challengerMessage)
		await self.SetReactions(self.targetMessage)
	# Set emoji on the message. We can not call clear_reactions on a DM.
	async def SetReactions(self, message):
		await message.add_reaction(candyEmoji)
		await message.add_reaction(ghostEmoji)
	# Set the target's response based on their reaction
	async def UpdateTargetResponse(self, reaction):
		if(str(reaction) == str(candyEmoji)):
			self.targetResponse = 'treat'
		elif(str(reaction) == str(ghostEmoji)):
			self.targetResponse = 'trick'
		if(self.targetResponse != None):
			self.targetEmbed = discord.Embed(title="TRICK OR TREAT!", description=self.targetContent+'\nYou have chosen {}!'.format(self.targetResponse))
			await self.targetMessage.edit(embed=self.targetEmbed)
		# If both players have answered, end the game
		if(self.targetResponse != None):
			await self.EndGame()
	async def EndGame(self):
		if(self.targetResponse == 'trick'):
			await self.initialMessage.channel.send('{} has been TRICKED!!! {}{}{}'.format(self.challenger.display_name, ghostEmoji, ghostEmoji, ghostEmoji))
		else:
			await self.initialMessage.channel.send('{} has been TREATED!!! {}{}{}'.format(self.challenger.display_name, candyEmoji, candyEmoji, candyEmoji))
		self.valid = False
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