import os
import json
import discord
from discord.ext import commands
import RoleAssignment

def PopulateServers():
	returnDict = {}
	directory = './servers/'
	for server in os.listdir(directory):
		for jsonfilename in os.listdir(directory+'{}/'.format(server)):
			if(jsonfilename.endswith('.json') and jsonfilename.split('.')[0].isdigit()):
				jsonfile = open(directory+'{}/'.format(server)+jsonfilename)
				returnDict[jsonfilename.replace('.json', '')] = json.load(jsonfile)
				jsonfile.close()
	return returnDict


def PopulateFactionMessages(servers):
	factionMessages = {}
	for server in servers:
		for faction in servers[server]["factions"]:
			factionMessages[faction.lower()] = None
	return factionMessages

def PopulateRoleMessages(servers):
	roleMessages = {}
	for server in servers:
		if("roleMessage" in servers[server]):
			roleMessages[server] = servers[server]["roleMessage"]
	print(roleMessages)
	return roleMessages