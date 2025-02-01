#! /usr/bin python3
# batchresize 1.0

import os, sys, time, datetime
from pathlib import Path
from PIL import Image

cwDir = os.path.dirname(os.path.abspath(sys.argv[0]))
timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#logName = 'batchresize_log_' + str(timeStamp) + '.txt'

print('\nbatchresize 1.0\n')
print('The batchresize tool resizes all of the image files in a given folder and saves them in a separate one. The original files remain intact.')
print('You can enter the new size either as percentage or as pixel number.')
print('The source folder must be one level below the script (current working directory). \n')

time.sleep(1)

print('Current working directory:')

print(cwDir)
print()

while True:
    time.sleep(0.5)
    print('Provide the name of the source folder.')
    srcFold = input()
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
    time.sleep(0.5)
    print('\nHow do you want to enter the new size? By percentage of the new edges [p] or number of pixels for the new width [n]?')
    choiceMode = input()
    if choiceMode == "p" or choiceMode == "P":
        while True:
            time.sleep(0.5)
            print('\nEnter the new edge size as a percentage of the original. Give an integer.')
            newSize = input()
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
            time.sleep(0.5)
            print('\nEnter the new width as the number of pixels. Give an integer.')
            newSize = input()
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
            newWidth = int(newSize)
            newHeight = (height / width) * int(newSize)
        resImage = image.resize((int(newWidth), int(newHeight)))
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