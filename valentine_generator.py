from PIL import Image, ImageDraw, ImageFont
import json
import random

def MakeImage(toImage, fromImage):
    font = ImageFont.truetype('comic.ttf', 40)
    messageFile = open('./Valentines/valentines.json', 'r')
    messages = json.load(messageFile)
    messageFile.close()
    colors = ['pink', 'red', 'blue', 'yellow', 'orange', 'white', 'gray', 'turquoise', 'magenta', 'purple']
    backgroundColor = random.choice(colors)
    colors.remove(backgroundColor)
    im = Image.new(mode='RGBA', size=(800,400), color=backgroundColor)
    draw = ImageDraw.Draw(im)
    x,y = 0,0
    fillColor = random.choice(colors)
    outlineColor='black'
    lines = messages[random.choice(list(messages.keys()))]
    if('image' in lines.keys()):
        jokeImage = Image.open('./Image Resources/Valentines/{}.png'.format(lines['image']))
        jokeImage = jokeImage.resize((200,200))
    else:
        jokeImage = Image.new(mode='RGBA', size=(150,150), color=backgroundColor)
    OutlineText(draw, 0, 0, lines['line0'], font, fillColor, outlineColor)
    OutlineText(draw, 50, 50, lines['line1'], font, fillColor, outlineColor)
    OutlineText(draw, 450, 150, 'To:', font, fillColor, outlineColor)
    OutlineText(draw, 450, 300, 'From:', font, fillColor, outlineColor)
    im.paste(toImage.resize((100,100)), (560, 150))
    im.paste(fromImage.resize((100,100)), (610, 300))
    im.paste(jokeImage, (100,200), mask=jokeImage)
    im = im.convert('RGB')
    im.save('tempValentine.jpg', quality=10)
    jpgim = Image.open('tempValentine.jpg')
    return jpgim

def OutlineText(drawObject, x, y, text, font, fill, outline):
    drawObject.text((x-1,y), text, font=font, fill=outline)
    drawObject.text((x+1,y), text, font=font, fill=outline)
    drawObject.text((x,y-1), text, font=font, fill=outline)
    drawObject.text((x,y+1), text, font=font, fill=outline)
    drawObject.text((x,y), text, font=font, fill=fill)