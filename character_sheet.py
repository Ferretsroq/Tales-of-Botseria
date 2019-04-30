import requests, bs4, string, json, discord
from discord.ext import commands
import asyncio, aiohttp
import time

async def repopulate(ctx, servers):
    channel = ctx.channel
    startTime = time.perf_counter()
    message = await channel.send("Repopulating...")
    charList = {}
    server = servers[str(ctx.guild.id)]
    siteURL = server['url']
    #print(url)
    async with aiohttp.ClientSession() as session:
        #async with session.get('https://heavensfall.jcink.net/index.php') as response:
        async with session.get(siteURL) as response:
            soups = bs4.BeautifulSoup(await response.text(), "lxml")
            newest = int(soups.find(id="newest_member").find('a').get('href').split("showuser=",1)[1])
            print('newest: {}'.format(newest))
            for x in range(0, newest):
                print('x: {}'.format(x))
                #async with session.get('https://heavensfall.jcink.net/index.php?showuser='+str(x+1)) as res:
                async with session.get('{}?showuser='.format(siteURL)+str(x+1)) as res:
                    if(x in range(0,newest,int(newest/4))):
                        await message.edit(content="Repopulating... {}/{}".format(x+1, newest))
                    #res = requests.get('https://heavensfall.jcink.net/index.php?showuser='+str(x+1))
                    soup = bs4.BeautifulSoup(await res.text(), "lxml")
                    #print('Fetching url {}'.format('https://heavensfall.jcink.net/index.php?showuser='+str(x+1)))
                    print('Fetching url {}'.format('{}?showuser='.format(siteURL)+str(x+1)))
                    try:
                        name = soup.select('[id="profilename"]')[0].text.lower()
                        print(name)
                    except:
                        print('No name')
                        continue
                

                    group =  soup.find("div",{"class":"site_profile"})#['id']
                    if(group != None):
                        group = group['id']
                    else:
                        group = soup.select('[id="membergroup"]')[0].text
                    print(group)
                    if group.lower() in ('admin', 'banned', 'validating', 'guest', 'members', 'archived', 'management'):
                        print('bad group')
                        continue
                    else:
                        deity = group
                
                    print('Populating {}'.format(name))
                    #image = soup.find('object', attrs={'id' : '100x100_image'})['data']
                    image = soup.select('[id="100x100_image"]')
                    if(image != []):
                        if('data' in image[0].attrs):
                            image = image[0].attrs['data']
                        else:
                            image = image[0].text
                    else:
                        image = ''
                    if('No Information' in image):#image == '<i>No Information</i>'):
                        image = ''
                    #age = soup.select('[id="age"]')[0].text
                    series = soup.select('[id="series"]')[0].text
                    pronouns = soup.select('[id="pronouns"]')[0].text
                    app = soup.find("a",{"id":"application"})#['href']
                    if(app != [] and app != None):
                        app = app['href']
                    else:
                        app = '{}?showuser={}'.format(siteURL, x+1)
                    plot = soup.find("a",{"id":"plotter"})#['href']
                    if(plot != []):
                        plot = plot['href']
                    else:
                        plot = 'No plotter'
                    ooc = soup.select('[id="ooc_name"]')[0].text
            
                    charList[name] = {
                        'group': group,
                        'image': image,
                        'deity': deity,
                        #'age': age,
                        'series': series,
                        'pronouns': pronouns,
                        'app': app,
                        'plot': plot,
                        'ooc': ooc
                        }
                    for key in charList[name].keys():
                        if(charList[name][key] == ''):
                            charList[name][key] = ' '

            with open('servers/{}/data.json'.format(ctx.guild.id), 'w') as outfile:
                json.dump(charList, outfile)
    await message.delete()
    print("Time: {}".format(time.perf_counter() - startTime))

async def Fetch(channel, ctx, servers):
    server = servers[str(ctx.guild.id)]
    siteURL = server['url']
    startTime = time.perf_counter()
    message = await channel.send("Fetching Accounts...")
    charList = []
    async with aiohttp.ClientSession() as session:
        #async with session.get('https://heavensfall.jcink.net/index.php') as response:
        async with session.get(siteURL) as response:
            soups = bs4.BeautifulSoup(await response.text(), "lxml")
            newest = int(soups.find(id="newest_member").find('a').get('href').split("showuser=",1)[1])
            print('newest: {}'.format(newest))
            for x in range(0, newest):
                print('x: {}'.format(x))
               # async with session.get('https://heavensfall.jcink.net/index.php?showuser='+str(x+1)) as res:
                async with session.get('{}?showuser='.format(siteURL)+str(x+1)) as res:
                    if(x in range(0,newest,int(newest/4))):
                        await message.edit(content="Fetching Accounts... {}/{}".format(x+1, newest))
                    #res = requests.get('https://heavensfall.jcink.net/index.php?showuser='+str(x+1))
                    soup = bs4.BeautifulSoup(await res.text(), "lxml")
                    #print('Fetching url {}'.format('https://heavensfall.jcink.net/index.php?showuser='+str(x+1)))
                    print('Fetching url {}'.format('{}?showuser='.format(siteURL)+str(x+1)))
                    try:
                        name = soup.select('[id="profilename"]')[0].text.lower()
                        if(soup.find("div", {"class":"site_profile"}) != None):
                            group =  soup.find("div",{"class":"site_profile"})['id']
                        else:
                            group = soup.select('[id="membergroup"]')[0].text
                        if(group.lower() != servers[str(ctx.guild.id)]['admin'].lower()):
                            charList.append(name)
                        else:
                            continue
                    except:
                        #charList.append('NO NAME {}'.format('https://heavensfall.jcink.net/index.php?showuser='+str(x+1)))
                        charList.append('NO NAME {}'.format('{}?showuser='.format(siteURL)+str(x+1)))
                        continue
                

    await message.delete()
    charList.sort()
    index = 0
    sendString = 'Accounts: ```'
    while(index < len(charList)):
        while(len(sendString) < 1900):
            sendString += ('\n'+'{}'.format(charList[index]))
            index += 1
            if(index >= len(charList)):
                break
        sendString += '```'
        await message.channel.send(sendString)
        sendString = '```'


    print("Time: {}".format(time.perf_counter() - startTime))


def MakeEmbed(name, characterData, server={}):
    #print('MakeEmbed!')
    embed=discord.Embed(title=name, color=ChooseColor(characterData['deity'], server))
    embed.set_thumbnail(url=characterData['image'])
    embed.add_field(name='Series:', value=characterData['series'], inline=True)
    embed.add_field(name='{}:'.format(server['faction']), value=characterData['deity'], inline=True)
    embed.add_field(name='App Link:', value=characterData['app'], inline=False)
    embed.add_field(name='Plot Link:', value=characterData['plot'], inline=False)
    embed.set_footer(text="Played by {}".format(characterData['ooc']))
    #print('Returning Embed!')
    return embed

def ChooseColor(deity, server):
    """
    if(deity.lower() == 'admin'):
        return 0xe52161
    if(deity.lower() == 'solara'):
        return 0xe44c3f
    elif(deity.lower() == 'tiamat'):
        return 0x276791
    elif(deity.lower() == 'mistral'):
        return 0x2d8951
    elif(deity.lower() == 'proserpina'):
        return 0xa4563c
    elif(deity.lower() == 'skirnir'):
        return 0xc27c0e
    elif(deity.lower() == 'lucifiel'):
        return 0x9b59b6
    else:
        return 0x000000
    """
    return int(server["colors"][deity.lower()], 0)