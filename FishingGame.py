import discord
from discord.ext import commands
import asyncio
import random

fishPhrases = ["You caught a bitterling! It's mad at you, but only a little.",
			   "You caught a pale chub! That name seems a bit judgy...",
			   "You caught a crucian carp! Your skills are sharp!",
			   "You caught a dace! Hope you have some space!",
			   "You caught a carp! If you catch another, they can carpool!",
			   "You caught a koi! I don't know why it's so shy... or such a bad speller...",
			   "You caught a goldfish! It's worth its weight in fish!",
			   "You caught a pop-eyed goldfish! It looks so...surprised!"	,
			   "You caught a Ranchu Goldfish! But I prefer balsamicu goldfish!"	,
			   "You caught a killifish! The streams are safe again."	,
			   "You caught a crawfish! Or else it's a lobster, and I'm a giant!"	,
			   "You caught a soft-shelled turtle! You should take a shellfie!"	,
			   "You caught a soft-shelled turtle! It's more sensitive than other turtles.",
			   "You caught a snapping turtle! How can it snap without fingers?"	,
			   "You caught a tadpole... It's just a tad small."	,
			   "You caught a frog! Or it's a new neighbor... and you have some apologizing to do."	,
			   "You caught a freshwater goby! Time to go bye-bye!"	,
			   "You caught a loach! It's...looking at you with reproach."	,
			   "You caught a catfish! I'm more of a dogfish person..."	,
			   "You caught a giant snakehead! Um...but I asked for a medium?"	,
			   "You caught a bluegill! Do you think it calls you \"pinklung\"?"	,
			   "You caught a yellow perch! Those yellow birds have to sit somewhere!"	,
			   "You caught a black bass! The most metal of all fish!"	,
			   "You caught a tilapia! It makes me happy-a!"	,
			   "You caught a pike! Think a swordfish would be up for a duel?"	,
			   "You caught a pond smelt! Whoever smelt it dealt it!"	,
			   "You caught a sweetfish! Hope it's not artificially sweet!"	,
			   "You caught a cherry salmon! It's the perfect topper for a marlin sundae!"	,
			   "You caught a char! Now I'm gonna sit on it!"	,
			   "You caught a golden trout! But the real treasure? Friendship."	,
			   "OH MY GOSH! You caught a stringfish! Five more and you'll have a guitarfish!"	,
			   "I caught a salmon! It's all upstream from here!"	,
			   "WOO-HOO! You caught a king salmon! Checkmate!"	,
			   "You caught a mitten crab! One more and you're ready for winter!"	,
			   "You caught a guppy! Welcome to the team, newbie!"	,
			   "You caught a nibble fish! Come to think of it, I could use a bite!"	,
			   "You caught an angelfish! That other fish told me to do it!"	,
			   "You caught a betta! You betta not drop it!"	,
			   "You caught a neon tetra! Wasn't hard to track."	,
			   "You caught a rainbowfish! Where's my pot of goldfish?"	,
			   "You caught a piranha! Sure hope it was the only one!"	,
			   "You caught an arowana! I'd make a joke but I don't 'wana."	,
			   "You caught a dorado! ♪I say \"Dorado\", you say \"Doraydo.\"♪"	,
			   "You caught a gar! Yar! It's a gar! Har Har!"	,
			   "You caught an arapaima! How did it get here? Arapaiknow!"	,
			   "Wow! A saddled bichir! And me without my tiny riding crop..."	,
			   "You caught a sturgeon! Wonder if it can perform sturgery..."	,
			   "You caught a sea butterfly! Try not to confuse it for a sea moth!"	,
			   "You caught a sea horse! But... where's its sea jockey?"	,
			   "You caught a clown fish! How many can fit in a carfish?"	,
			   "You caught a surgeonfish! Scalpel! Forceps! Fish hook!"	,
			   "You caught a butterfly fish! Did it change from a caterpillar fish?"	,
			   "You caught a Napoleonfish! It's not as big as it thinks!"	,
			   "You caught a zebra turkeyfish! Land, air, water—make up your mind!"	,
			   "You caught a blowfish! I'm blown away!"	,
			   "You caught a puffer fish! I thought you would be tougher, fish!"	,
			   "You caught an anchovy! Stay away from my pizza!"	,
			   "You caught a horse mackerel! Of course, mack...er...el."	,
			   "You caught a barred knifejaw! They must have a hard time eating!"	,
			   "You caught a sea bass! No, wait-it's at least a C+!"	,
			   "You caught a red snapper! It looks pretty dapper!",
			   "You caught a dab! Not bad!"	,
			   "You caught an olive flounder! That's not the pits!"	,
			   "You caught a squid! Do they...not actually \"bloop\"?",
			   "You caught a squid! It's off the hook!",
			   "You caught a squid! I had an inkling you might!",
			   "You caught a moray eel! When you're in love, that's a moray!"	,
			   "You caught a ribbon eel! Can it tie itself into a bow?"	,
			   "You caught a tuna! It's a little off-key!"	,
			   "You caught a blue marlin! Listen to this fish. It's got a point."	,
			   "You caught a giant trevally! Yeah, I'm pretty well-trevalled."	,
			   "You caught a mahi-mahi! It's all mahine-mahine."	,
			   "You caught an ocean sunfish! Good thing I'm wearing ocean sunscreen!"	,
			   "You caught a ray! A few more and I'll have a tan!"	,
			   "You caught a saw shark! You could call it a sea saw!"	,
			   "You caught a hammerhead shark! You hit the nail on the head!"	,
			   "You caught a great white shark! Watch out for its jaws!"	,
			   "Thar she blows! You caught a whale shark! I'm tellin' ya, it was thiiiiiiiiiiiiiiiiiiiis big!"	,
			   "You caught a suckerfish! I thought it was a shark! Oh, wait - now I get it. \"Sucker\"...",
			   "You caught a football fish! Some countries call it a soccer fish!"	,
			   "You caught an oarfish! I hope you catch morefish!"	,
			   "You caught a barreleye! Like eyeing fish in a barrel!"	,
			   "Blast from the past! You caught a coelacanth! Think positive! Be a coela-CAN!"]

class FishButton(discord.ui.Button['FishingGame']):
	def __init__(self, id: str, row=0):
		super().__init__(style=discord.ButtonStyle.secondary, label=id, row=row)
	async def callback(self, interaction: discord.Interaction):
		assert self.view is not None
		view: RoleAssignment = self.view
		await self.view.ReelIn()
		

class FishingGame(discord.ui.View):
	def __init__(self, ctx):
		super().__init__(timeout=None)
		self.add_item(FishButton('Reel In', 0))
		self.status='Fishing'
		self.finished = False
		self.ctx = ctx
	async def ReelIn(self):
		if(self.finished == False):
			if(self.status == 'Bite'):
				#await self.ctx.send("You got a fish!")
				await self.ctx.send(random.choice(fishPhrases))
			elif(self.status == 'Fishing'):
				await self.ctx.send("You were too early!")
			elif(self.status == 'Got Away'):
				await self.ctx.send("You were too late!")
		self.finished = True
	async def ChangeStatus(self, status='Fishing'):
		self.status = status
		