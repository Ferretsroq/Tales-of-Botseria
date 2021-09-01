from PIL import Image, ImageDraw
import random
import numpy as np
from io import BytesIO
import requests

# Define a circle based on the center and radius, rather than a bounding box
def DrawEllipse(drawObj, center, radius, fill, outline):
    drawObj.ellipse((center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius), fill, outline)

# Add a set of googly eyes to an image in random positions
def Googlify(inputImage, static=False):
    image = inputImage.copy()
    draw = ImageDraw.Draw(image)
    # In case the image is not square, define x and y separately and take averages
    imageX = image.size[0]
    imageY = image.size[1]
    radius = int((((imageX + imageY)/2)/4) - 1)
    # The eyes have static x positions but random y positions
    if(not static):
        center1 = (int(imageX/4), random.randint(int(((imageY/2)-radius)),int(((imageY/2)+radius))))
        center2 = (int(3*imageX/4), random.randint(int(((imageY/2)-radius)),int(((imageY/2)+radius))))
    else:
        center1 = (int(imageX/4), int(imageY/2))
        center2 = (int(3*imageX/4), int(imageY/2))
    pupilRadius = int(((imageX + imageY)/2)/10)
    # The pupils of the googly eyes can be anywhere within the eye but can't go outside of the eye
    pupilDistance1 = random.randint(0, int(radius-pupilRadius))
    pupilAngle1 = random.randint(0, 359)*np.pi/180.0
    pupilDistance2 = random.randint(0, int(radius-pupilRadius))
    pupilAngle2 = random.randint(0, 359)*np.pi/180.0
    if(static):
        pupilDistance1 = int(radius-pupilRadius)
        pupilDistance2 = int(radius-pupilRadius)
    # Determine pupil centers based on distance and angle
    pupilCenter1 = (center1[0] + pupilDistance1*np.cos(pupilAngle1), center1[1]+pupilDistance1*np.sin(pupilAngle1))
    pupilCenter2 = (center2[0] + pupilDistance2*np.cos(pupilAngle2), center2[1]+pupilDistance2*np.sin(pupilAngle2))
    # Draw the googly eyes onto the image
    DrawEllipse(draw, center1, radius, 'white', 'black')
    DrawEllipse(draw, center2, radius, 'white', 'black')
    DrawEllipse(draw, pupilCenter1, pupilRadius, 'black', 'black')
    DrawEllipse(draw, pupilCenter2, pupilRadius, 'black', 'black')
    return image

# Add a Santa hat and beard to an image
def Santafy(inputImage, rand=False):
    base = inputImage.copy()
    hat = Image.open('./Image Resources/santa-hat.png')
    beard = Image.open('./Image Resources/santa-beard.png')
    x,y = base.size
    hat = hat.resize(base.size)
    beard = beard.resize(base.size)
    if(rand):
        data = np.array(hat)
        r, g, b, a = data.T
        red_areas = (r >= 100) & (g <= 220) & (b <= 200)
        data[..., :-1][red_areas.T] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        hat = Image.fromarray(data)
    base.paste(hat, box=(0,-int(y/4)), mask=hat)
    base.paste(beard, box=(0, int(y/2)),mask=beard)
    return base

# Add an image to the head of a spooky skeleton
def Spookify(inputImage):
    options = ["skeleton", "witch", "cat"]
    choice = random.choice(options)
    if(choice == 'skeleton'):
        base = inputImage.copy().convert('RGBA')
        skeleton = Image.open('./Image Resources/skeleton.png')
        base = base.resize((300,300))
        skeleton.paste(base, box=(100,30), mask=base)
        return skeleton
    elif(choice == 'witch'):
        base = inputImage.copy().convert('RGBA')
        witch = Image.open('./Image Resources/witch.png')
        base = base.resize((100,100))
        witch.paste(base, box=(40,80), mask=base)
        return witch
    elif(choice == 'cat'):
        base = inputImage.copy().convert('RGBA')
        cat = Image.open('./Image Resources/blackcat.png')
        base = base.resize((150,150))
        cat.paste(base, box=(410,230), mask=base)
        return cat

# Add a Batman mask to an image
def Batmanify(inputImage):
    base = inputImage.copy()
    mask = Image.open('./Image Resources/batman.png')
    logo = Image.open('./Image Resources/batmanlogo.png')
    logo = logo.resize(base.size)
    logo = logo.rotate(angle=random.randint(0,359))
    x,y = base.size
    mask = mask.resize(base.size)
    base.paste(mask, box=(0, -int(y/5)), mask=mask)
    base.paste(logo, box=(random.randint(-int(0.5*x), int(0.5*x)), random.randint(-int(0.5*y), int(0.5*y))), mask=logo)
    return base

# Add 2019 glasses to an image
def Happy2019(inputImage):
    base = inputImage.copy()
    glassesNum = random.randint(0,8)
    glasses = Image.open('./Image Resources/2019/2019_{}.png'.format(glassesNum))
    x,y = base.size
    glasses = glasses.resize(base.size)
    base.paste(glasses, (0, random.randint(int(-0.5*y), 0)), mask=glasses)
    return base
    
def ImageFromURL(url):
    if(url == '' or url == ' '):
        return Image.new('RGBA', (100,100), (255,0,0,0))
    elif(url.endswith('.gif') or url.endswith('.gifv')):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img.convert(mode='RGBA')
    elif('.webp' in url):
    	# Discord profile pictures suck and come in as .webp by default, instead get a .png like a human being
    	response = requests.get(url.split('.webp')[0]+'.png')
    	img = Image.open(BytesIO(response.content))
    	return img
    else:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img.convert(mode='RGBA')
