#!/usr/bin/env python3
# batchresize 1.2

import os, sys, time, datetime
from pathlib import Path
from PIL import Image
import inspect

cwDir = os.path.dirname(os.path.abspath(sys.argv[0]))
timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#logName = 'batchresize_log_' + str(timeStamp) + '.txt'

print('\nbatchresize 1.2\n')
print('The batchresize tool resizes all of the image files in a given folder and saves them in a separate one. The original files remain intact.')
print('You can enter the new size either as percentage or as pixel number.')
print('The source folder must be one level below the script (current working directory). \n')

time.sleep(0.5)

print('Current working directory:')

print(cwDir)
print()

while True:
    time.sleep(0.3)
    print('Provide the name of the source folder.')
    srcFold = input('> ')
    srcPath = cwDir / Path(str(srcFold))
    if os.path.exists(srcPath) is True:
        break
    else:
        print('\nPath does not exist. Please name an existing folder.\n')
        continue     

srcPath = cwDir / Path(str(srcFold))
srcPath2 = os.path.join(srcPath, "")

newfoldName = str(srcFold) + '_resized_' + (str(timeStamp))
destFolder = cwDir / Path(str(newfoldName))
os.mkdir(destFolder)

listDir = os.listdir(srcPath)
listDir.sort()

while True:
    time.sleep(0.3)
    print('\nHow do you want to enter the new size? By percentage of the new edges [p] or number of pixels for the new longer edge [n]?')
    choiceMode = input('> ')
    if choiceMode == "p" or choiceMode == "P":
        while True:
            time.sleep(0.3)
            print('\nEnter the new edge size as a percentage of the original. Give an integer.')
            newSize = input('> ')
            try:
                val = int(newSize)
                if val < 0 or val > 1000:
                    print('\nCannot work with this number. Please think of a reasonable size.')
                    continue
                break
            except:
                print('\nPlease provide a pure, positive integer.')
                continue
        break
    elif choiceMode == "n" or choiceMode == "N":
        while True:
            time.sleep(0.3)
            print('\nEnter the new longer edge as the number of pixels. Give an integer.')
            newSize = input('> ')
            try:
                val = int(newSize)
                if val < 0 or val > 100000:
                    print('\nCannot work with this number. Please think of a reasonable size.')
                    continue
                break
            except:
                print('\nPlease provide a pure, positive integer.')
                continue
        break
    else:
        print('\nPlease provide a valid answer by pressing "p" or "n".')

time.sleep(0.3)
print('\nDo you want to choose resampling filter? (LANCZOS is default.) ([y]/[n])')

filterChoice = input('> ')

if filterChoice.lower() in ["y", "yes"] or filterChoice.upper() in ["Y", "YES"]:
    time.sleep(0.3)
    print()
    print(inspect.cleandoc("""\n[1] NEAREST

    Pick one nearest pixel from the input image. Ignore all other input pixels.

[2] BOX

    Each pixel of source image contributes to one pixel of the destination image with identical weights.

[3] BILINEAR

    For resize calculate the output pixel value using linear interpolation on all pixels that may contribute to the output value. For other transformations linear interpolation over a 2x2 environment in the input image is used.

[4] HAMMING

    Produces a sharper image than BILINEAR, doesn’t have dislocations on local level like with BOX.

[5] BICUBIC

    For resize calculate the output pixel value using cubic interpolation on all pixels that may contribute to the output value. For other transformations cubic interpolation over a 4x4 environment in the input image is used.

[6] LANCZOS

    Calculate the output pixel value using a high-quality Lanczos filter (a truncated sinc) on all pixels that may contribute to the output value."""))

    time.sleep(0.3)
    print('\nChoos one of the options (or skip).')
    filterNum = input('> ')
    try:
        fN = int(filterNum)
        if fN == 1:
            filterType = 0
            filterName = 'NEAREST'
        elif fN == 2:
            filterType = 4
            filterName = 'BOX'
        elif fN == 3:
            filterType = 2
            filterName = 'BILINEAR'
        elif fN == 4:
            filterType = 5
            filterName = 'HAMMING'
        elif fN == 5:
            filterType = 3
            filterName = 'BICUBIC'
        else:
            filterType = 1
            filterName = 'LANCZOS'
    except:
        filterType = 1
        filterName = 'LANCZOS'

else:
    filterType = 1
    filterName = 'LANCZOS'

print('\nFilter: ' + filterName)
print('\nWorking...')

def validFile(fileName):
    try:
        with Image.open(str(srcPath2) + fileName) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False

for fileName in listDir:
    if validFile(fileName) == True:
        image = Image.open(str(srcPath2) + fileName)    
        width, height = image.size
        if choiceMode == "p" or choiceMode == "P":
            newWidth = width * (int(newSize) / 100)
            newHeight = height * (int(newSize) / 100)
        else:
            if height > width:
                newHeight = int(newSize)
                newWidth = (width / height) * int(newSize)
            else:
                newWidth = int(newSize)
                newHeight = (height / width) * int(newSize)            
        resImage = image.resize((int(newWidth), int(newHeight)), resample=filterType)
        resImage.save(f"{destFolder}/{fileName}")
    else:
        continue

countIm = os.listdir(destFolder)

if len(countIm) == 0:
    os.rmdir(destFolder)
    print('\nNo image in source folder.')
else:
    print('\nImages are resized and saved.') 

time.sleep(5)