import discord
import json
import asyncio
import character_sheet
import requests, bs4

arrowLeft = chr(0x2B05)
arrowRight = chr(0x27A1)
listEmoji = chr(0x1f4dc)

def CharCanon(canon, server):
    #url = 'https://heavensfall.jcink.net/index.php?showtopic=20'
    url = server["canonurl"]
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "lxml")
    print('Fetching url {}'.format(url))
    if(soup.select('[id="canon-list"]') != []):
    	canons = soup.select('[id="canon-list"]')[0].select('h2')
    else:
    	canons = soup.select('h2')
    if(canon.lower() in [tag.getText().lower() for tag in canons]):
        index = [tag.getText().lower() for tag in canons].index(canon.lower())
        characters = [character.getText().lower() for character in canons[index].find_next('ul').find_all('li')]
        return(characters)
    else:
        print('Canon {} not found.'.format(canon.lower()))
        return []

def CanonList(server):
    #url = 'https://heavensfall.jcink.net/index.php?showtopic=20'
    url = server["canonurl"]
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "lxml")
    if(soup.select('[id="canon-list"]') != []):
    	canons = [tag.getText().lower() for tag in soup.select('[id="canon-list"]')[0].select('h2')]
    	headings = soup.select('[id="canon-list"]')[0].select('h2')
    else:
    	canons = [tag.getText().lower() for tag in soup.select('h2')]
    	headings = soup.select('h2')
    counts = []
    for index in range(len(headings)):
    	count = len(headings[index].find_next('ul').find_all('li'))
    	counts.append(count)

    return list(zip(canons, counts))

class CanonMessage:
	def __init__(self, canon, user, ctx, servers):
		self.serverID = ctx.guild.id
		self.server = servers[str(self.serverID)]
		with open('servers/{}/data.json'.format(self.serverID)) as json_data:
			data = json.load(json_data)
		self.canon = canon
		self.user = user
		validCharacters = CharCanon(canon, self.server)
		self.characterList = [character for character in data if character.lower() in validCharacters]
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
		await self.Edit(content)
	async def Edit(self, content=''):
		with open('servers/{}/data.json'.format(self.serverID)) as json_data:
			data = json.load(json_data)
		self.embed = character_sheet.MakeEmbed(self.characterList[self.index], data[self.characterList[self.index]], self.server)
		self.embed.title = "{} - {}/{}: ".format(self.canon, self.index+1, len(self.characterList)) + self.embed.title
		self.embed.description = content
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

