import json
import random
import numpy as np
import discord

class Boon:
    def __init__(self, name, data, rank):
        self.name = name
        self.data = data
        self.formFactor = random.choice(self.data['Form Factor'])
        self.rank = rank
        self.effect = self.data['Ranks'][self.rank]
    def __repr__(self):
        return '***{}***\nForm: {}\nRank: {}\nEffect: {}'.format(self.name, self.formFactor, self.rank, self.effect)

def BoonBatch(number=1, minEX=0, minS=0):
    boonFile = open('boons.json')
    boonData = boonFile.read()
    boonFile.close()
    boons = json.loads(boonData)
    batch = []
    while((len([boon for boon in batch if boon.rank=='EX']) < minEX) and len(batch) < number):
        boon = random.choice([boon for boon in list(boons.keys()) if 'EX' in boons[boon]['Ranks'].keys()])
        batch.append(Boon(boon, boons[boon], 'EX'))
    while((len([boon for boon in batch if boon.rank=='S']) < minS) and len(batch) < number):
        boon = random.choice([boon for boon in list(boons.keys()) if 'S' in boons[boon]['Ranks'].keys()])
        batch.append(Boon(boon, boons[boon], 'S'))
    while(len(batch) < number):
        rank = np.random.choice(['C', 'B', 'A', 'S', 'EX'], 1, p=[0.1, 0.2, 0.5, 0.15, 0.05])[0]
        boon = random.choice([boon for boon in list(boons.keys()) if rank in boons[boon]['Ranks'].keys()])
        batch.append(Boon(boon, boons[boon], rank))
    return batch

def BoonEmbed(boon, name=''):
    embed = discord.Embed(title="{}".format(name), color=ChooseColor(boon.rank))
    embed.description = "<p>@[{}]<br>\n<b>Boon:</b> {}<br>\n<b>Rank:</b> {}<br>\n<b>Form Factor:</b> {}<br>\n<b>Effect:</b> {}</p>".format(name, boon.name, boon.rank, boon.formFactor, boon.effect)
    return embed


def ChooseColor(rank):
	if(rank == 'C'):
		return 0xe44c3f
	elif(rank == 'B'):
		return 0x276791
	elif(rank == 'A'):
		return 0x9b59b6
	elif(rank == 'S'):
		return 0x2d8951
	elif(rank == 'EX'):
		return 0xe52161
	else:
		return 0x000000