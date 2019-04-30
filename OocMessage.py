import discord
import json
import asyncio
import requests, bs4
import character_sheet
import Googlify

arrowLeft = chr(0x2B05)
arrowRight = chr(0x27A1)
listEmoji = chr(0x1f4dc)

def OocList(ctx):
	with open('servers/{}/data.json'.format(ctx.guild.id)) as json_data:
		data = json.load(json_data)
	oocList = []
	for character in data:
		if(data[character]['ooc'].lower() not in oocList):
			oocList.append(data[character]['ooc'].lower())
	return oocList

class OocMessage:
	def __init__(self, user, ooc, ctx, servers):
		self.serverID = ctx.guild.id
		self.server = servers[str(self.serverID)]
		with open('servers/{}/data.json'.format(self.serverID)) as json_data:
			data = json.load(json_data)
		self.ooc = ooc
		self.user = user
		self.characterList = [character for character in data if data[character]['ooc'].lower()==ooc.lower()]
		self.index = 0
		self.message = None
		self.embed = discord.Embed()
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
		names[self.index] = '**{}**'.format(names[self.index])
		#content = '\n'.join(['{}: {}'.format(x+1, self.characterList[x]) for x in range(len(self.characterList))])
		content = '\n'.join(names)
		await self.Edit(content, googlify=True)
	async def Edit(self, content='', googlify=False):
		#with open('data.json') as json_data:
		#	data = json.load(json_data)
		with open('servers/{}/data.json'.format(self.serverID)) as json_data:
			data = json.load(json_data)
		self.embed = character_sheet.MakeEmbed(self.characterList[self.index], data[self.characterList[self.index]], self.server)
		self.embed.title = "{} - {}/{}: ".format(self.ooc, self.index+1, len(self.characterList)) + self.embed.title
		self.embed.description = content
		#if(googlify):
	#		Googlify.Googlify(Googlify.ImageFromURL(data[self.characterList[self.index]]['image'])).save('tempGoogly.png')
	#		self.embed.set_thumbnail(url='attachment://tempGoogly.png')
		await self.message.edit(embed=self.embed)
		await self.SetReactions()
	async def Send(self, channel):
		self.message = await channel.send(embed=self.embed)
		await self.Edit()
	async def SetReactions(self):
		await self.message.clear_reactions()
		await self.message.add_reaction(arrowLeft)
		await self.message.add_reaction(arrowRight)
		await self.message.add_reaction(listEmoji)

