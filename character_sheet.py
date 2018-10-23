import requests, bs4, string, json, discord

def repopulate():

    charlist = {}

    req = requests.get('https://heavensfall.jcink.net/index.php')
    soups = bs4.BeautifulSoup(req.text, "lxml")
    newest = int(soups.find(id="newest_member").find('a').get('href').split("showuser=",1)[1])

    for x in range(0, newest):

        res = requests.get('https://heavensfall.jcink.net/index.php?showuser='+str(x+1))
        soup = bs4.BeautifulSoup(res.text, "lxml")

        try:
            name = soup.select('div[id="profilename"]')[0].text.lower()
        except:
            continue
            
        group = soup.select('td[id="member_group"]')[0].text
        if group.lower() in ('admin', 'banned', 'validating', 'guest', 'members'):
            continue
            
        image = soup.select('td[id="100x100_image"]')[0].text
        deity = soup.select('td[id="deity"]')[0].text
        age = soup.select('td[id="age"]')[0].text
        series = soup.select('td[id="series"]')[0].text
        pronouns = soup.select('td[id="pronouns"]')[0].text
        app = soup.select('td[id="application"]')[0].text
        plot = soup.select('td[id="plotter"]')[0].text
        ooc = soup.select('td[id="ooc_name"]')[0].text
        
        charlist[name] = {
                'group': group,
                'image': image,
                'deity': deity,
                'age': age,
                'series': series,
                'pronouns': pronouns,
                'app': app,
                'plot': plot,
                'ooc': ooc
            }

    with open('data.json', 'w') as outfile:
        json.dump(charlist, outfile)

def MakeEmbed(name, characterData):
    embed=discord.Embed(title=name, color=ChooseColor(characterData['deity']))
    embed.add_field(name='Series:', value=characterData['series'], inline=True)
    embed.add_field(name='Deity:', value=characterData['deity'], inline=True)
    embed.add_field(name='App Link:', value=characterData['app'], inline=False)
    embed.add_field(name='Plot Link:', value=characterData['plot'], inline=False)
    embed.set_footer(text="Played by {}".format(characterData['ooc']))
    return embed

def ChooseColor(deity):
    if(deity.lower() == 'solara'):
        return 0xe52161
    elif(deity.lower() == 'tiamat'):
        return 0xe44c3f
    elif(deity.lower() == 'mistral'):
        return 0x2d8951
    elif(deity.lower() == 'prosperpina'):
        return 0xa4563c
    elif(deity.lower() == 'skirnir'):
        return 0xc27c0e
    elif(deity.lower() == 'lucifel'):
        return 0x9b59b6
    else:
        return 0x000000