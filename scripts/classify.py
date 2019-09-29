# For filesystem interaction
import os
# For image processing
from PIL import Image
# For timestamps
import calendar
import time

# Path were the raw images are located
path = "Z:/raw/"
# Parent folder, were the categorie olders are located
rootPath = "Z:/"
# Path to log file
logPath = "Z:/log.txt"
# Number of digits / categories 
anzahlDigits = 5
# Variable to display processing status
count = 0


# Crops the raw picture to cut unnecessary pixels
def prepImage (path,outputPath,pics):
    
    # Open the raw picture from path
    pic = Image.open(path)
    # Crops pic. Has to be defined individually.
    pic = pic.crop((600, 200, 1450, 400))
    pic.show()
    # Get width and height from cropped pic
    w, h = pic.size

    # In this case we use the cropped pics original size. We divide it in width into an certain number.
    a1 = 0
    a2 = 0
    a3 = w / pics
    a4 = h
    
    # Loop through certain number of pics
    for currentPic in range(pics):
        
        # Cut cropped pic into a smaller one. In this case it displays one digit.
        croppedPic = pic.crop((a1, a2, a3, a4))
        # Shows current cropped pic
        croppedPic.show()
        # Enter number of digit which is currently displayed
        digit = input("Which number is displayed ?")
        # Save the classified image to a specific categorie folder. Image is a png file with the current timestamp as name.
        croppedPic.save(outputPath + str(digit) + "/" + str(calendar.timegm(time.gmtime())) + ".png")
        # Expand width parameter to display the next digit in the cropped image.
        a1 = a1 + w / pics
        a3 = a3 + w / pics
        pass
        
    pass


# loops through all files in raw image folder
for img in os.listdir(path):
    
    # Shows current status
    print(str(count) + " images from " + str(len(os.listdir(path))) + " processed." )
    print("Current file: " + str(img))
    # Writes current file to log. If program is terminated, previous images can be deleted
    log = open(logPath,'w')
    log.write(img)
    log.close()
    # Creates path to file
    arg = path + img
    # Try to execute prepImage()
    try:
        prepImage(arg,rootPath,anzahlDigits)
    except:
        print("File can't be processed!")
        
    count += 1
    
    pass