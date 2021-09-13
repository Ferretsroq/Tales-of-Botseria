import discord
from discord.ext import commands
import asyncio

emojiDict = {
	'proxima' : '<:proxima:881256641876615198>',
	'camelot' : '<:camelot:881256307066294303>',
	'greyhawk' : '<:greyhawk:881256750941085736>',
	'yushan': '<:yushan:881256768838197248>',
	'itinerant': '<:itinerant:881256694364139651>',
	'she/her': '🟩',
	'he/him': '🔶',
	'they/them': '🟣'
}
emojiDictTransposed = {
	'<:proxima:881256641876615198>' : 'proxima',
	'<:camelot:881256307066294303>' : 'camelot',
	'<:greyhawk:881256750941085736>' : 'greyhawk',
	'<:yushan:881256768838197248>': 'yushan',
	'<:itinerant:881256694364139651>': 'itinerant',
	'🟩': 'she/her',
	'🔶': 'he/him',
	'🟣': 'they/them'
}
roleDict = {
	'proxima':   880965946943086614, 
	'camelot':   880966223079280701, 
	'greyhawk':  880966124718669844, 
	'yushan':    880966308206882816, 
	'itinerant': 880966402486460457,
	'she/her':   881582099847585792, 
	'he/him':    881582147440373791, 
	'they/them': 881582183339409450
}
class RoleMessage:
	def __init__(self, ctx):
		self.ctx = ctx
		self.embed = discord.Embed()
		self.embed.description = "React to add role:\n{} she/her\n{} he/him\n{} they/them\n{} proxima\n{} camelot\n{} greyhawk\n{} yushan\n{} itinerant".format(emojiDict['she/her'],
			emojiDict['he/him'],
			emojiDict['they/them'],
			emojiDict['proxima'],
			emojiDict['camelot'],
			emojiDict['greyhawk'],
			emojiDict['yushan'],
			emojiDict['itinerant'])
		self.message = None
	async def Send(self, ctx):
		self.message = await ctx.send(embed=self.embed)
		await self.SetReactions()
	async def SetReactions(self):
		await self.message.add_reaction(emojiDict['she/her'])
		await self.message.add_reaction(emojiDict['he/him'])
		await self.message.add_reaction(emojiDict['they/them'])
		await self.message.add_reaction(emojiDict['proxima'])
		await self.message.add_reaction(emojiDict['camelot'])
		await self.message.add_reaction(emojiDict['greyhawk'])
		await self.message.add_reaction(emojiDict['yushan'])
		await self.message.add_reaction(emojiDict['itinerant'])
	async def SetRole(self, reaction, user):
		#if(reaction.guild.get_role(self.role) in interaction.user.roles):
	#		await interaction.user.remove_roles(interaction.guild.get_role(self.role))
	#	else:
	#		await interaction.user.add_roles(interaction.guild.get_role(self.role))
		if(reaction in emojiDictTransposed):
			if(self.ctx.guild.get_role(roleDict[emojiDictTransposed[reaction]]) in user.roles):
				await user.remove_roles(self.ctx.guild.get_role(roleDict[emojiDictTransposed[reaction]]))
			else:
				await user.add_roles(self.ctx.guild.get_role(roleDict[emojiDictTransposed[reaction]]))
		await self.message.remove_reaction(reaction, user)



class RoleButton(discord.ui.Button['RoleAssignment']):
	def __init__(self, id: str, role: str, row=0):
		super().__init__(style=discord.ButtonStyle.secondary, label='', row=row)
		self.emoji = emojiDict[id]
		self.id = id
		self.role = role
	async def callback(self, interaction: discord.Interaction):
		assert self.view is not None
		view: RoleAssignment = self.view
		content = self.id
		if(interaction.guild.get_role(self.role) in interaction.user.roles):
			await interaction.user.remove_roles(interaction.guild.get_role(self.role))
		else:
			await interaction.user.add_roles(interaction.guild.get_role(self.role))

class RoleAssignment(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
		self.add_item(RoleButton('proxima', 880965946943086614, 0))
		self.add_item(RoleButton('camelot', 880966223079280701, 0))
		self.add_item(RoleButton('greyhawk', 880966124718669844, 0))
		self.add_item(RoleButton('yushan', 880966308206882816, 0))
		self.add_item(RoleButton('itinerant', 880966402486460457, 0))
		self.add_item(RoleButton('she/her', 881582099847585792, 1))
		self.add_item(RoleButton('he/him', 881582147440373791, 1))
		self.add_item(RoleButton('they/them', 881582183339409450, 1))
		