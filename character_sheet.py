import requests, bs4, string, json, discord

def repopulate():

    charList = {}

    req = requests.get('https://heavensfall.jcink.net/index.php')
    soups = bs4.BeautifulSoup(req.text, "lxml")
    newest = int(soups.find(id="newest_member").find('a').get('href').split("showuser=",1)[1])
    print('newest: {}'.format(newest))
    for x in range(0, newest):
        print('x: {}'.format(x))
        res = requests.get('https://heavensfall.jcink.net/index.php?showuser='+str(x+1))
        soup = bs4.BeautifulSoup(res.text, "lxml")
        print('Fetching url {}'.format('https://heavensfall.jcink.net/index.php?showuser='+str(x+1)))
        try:
            name = soup.select('[id="profilename"]')[0].text.lower()
            print(name)
        except:
            print('No name')
            continue
            

        group =  soup.find("div",{"class":"site_profile"})['id']
        print(group)
        if group.lower() in ('admin', 'banned', 'validating', 'guest', 'members'):
            print('bad group')
            continue
            
        #image = soup.select('[id="100x100_image"]')[0].text
        print('Populating {}'.format(name))
        image = soup.find('object', attrs={'id' : '100x100_image'})['data']
        deity = soup.select('[id="deity"]')[0].text
        age = soup.select('[id="age"]')[0].text
        series = soup.select('[id="series"]')[0].text
        pronouns = soup.select('[id="pronouns"]')[0].text
        app = soup.find("a",{"id":"application"})['href']
        plot = soup.find("a",{"id":"plotter"})['href']
        ooc = soup.select('[id="ooc_name"]')[0].text
        
        charList[name] = {
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
        for key in charList[name].keys():
            if(charList[name][key] == ''):
                charList[name][key] = ' '

    with open('data.json', 'w') as outfile:
        json.dump(charList, outfile)

def MakeEmbed(name, characterData):
    print('MakeEmbed!')
    embed=discord.Embed(title=name, color=ChooseColor(characterData['deity']))
    embed.set_thumbnail(url=characterData['image'])
    embed.add_field(name='Series:', value=characterData['series'], inline=True)
    embed.add_field(name='Deity:', value=characterData['deity'], inline=True)
    embed.add_field(name='App Link:', value=characterData['app'], inline=False)
    embed.add_field(name='Plot Link:', value=characterData['plot'], inline=False)
    embed.set_footer(text="Played by {}".format(characterData['ooc']))
    print('Returning Embed!')
    return embed

def ChooseColor(deity):
    if(deity.lower() == 'admin'):
        return 0xe52161
    if(deity.lower() == 'solara'):
        return 0xe44c3f
    elif(deity.lower() == 'tiamat'):
        return 0x276791
    elif(deity.lower() == 'mistral'):
        return 0x2d8951
    elif(deity.lower() == 'prosperpina'):
        return 0xa4563c
    elif(deity.lower() == 'skirnir'):
        return 0xc27c0e
    elif(deity.lower() == 'lucifiel'):
        return 0x9b59b6
    else:
        return 0x000000