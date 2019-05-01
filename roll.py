import random
import re

pattern = '(?P<Number>\d+)d(?P<Die>\d+)(?P<Kept>k\d+)?(?P<Modifier>[\+|-]\d+)?'

def roll(arg):
	pattern = '(?P<Number>\d+)d(?P<Die>\d+)(?P<Kept>k\d+)?(?P<Modifier>[\+|-]\d+)?'
	try:
		roll = arg
		if(re.match(pattern, roll)):
			rollDict = re.match(pattern, roll).groupdict()
			try:
				notes = ' '.join(message.content.split()[2:])
			except:
				notes = ''
			numberOfDice = int(rollDict['Number'])
			die = int(rollDict['Die'])
			diceKept = numberOfDice
			modifier = 0
			if(rollDict['Kept']):
				diceKept = int(rollDict['Kept'][1:])
			else:
				diceKept = numberOfDice
			if(rollDict['Modifier']):
				modifier = int(rollDict['Modifier'])
			else:
				modifier = 0
			rolls = []
			for dieRoll in range(numberOfDice):
				rolls.append(random.randint(1, die))
			rolls.sort(reverse=True)
			keptRolls = rolls[0:diceKept]
			result = sum(keptRolls) + modifier
			return 'You rolled {} and got {}.\n```[{}]```'.format(roll, result, rolls)
	except:
		return 'I\'m sorry, I couldn\'t parse your roll.\nProlematic roll: {} <@111529517541036032>'.format(arg)