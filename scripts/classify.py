class Classify:

    # For filesystem interaction
    import os
    # For image processing
    from PIL import Image
    # For timestamps
    import calendar
    import time


    # Path were the raw images are located
    unprocessedImagePath = ""
    # Parent folder, were the categorie folders are located
    rootPath = ""
    # Path to log file
    logPath = ""
    # Number of digits / categories 
    numberOfCategories = 0
    # Area where the focus lies
    cropArea = ()


    def __init__(self,unprocessedImagePath, rootPath, logPath, numberOfCategories, cropArea):

        print("This is the constructor method of \""+type(self).__name__+"\" class.")
        
        self.unprocessedImagePath = unprocessedImagePath
        self.rootPath = rootPath
        self.logPath = logPath
        self.numberOfCategories = numberOfCategories
        self.cropArea = cropArea

        print("Successfully initialized\n")

        pass


    # Crops the raw picture to cut unnecessary pixels
    def prepImage (self, pathToImage, numberOfCuts, mode):
    
        if mode == "classify":
            # Open the raw picture from path
            currentPic = self.Image.open(pathToImage)
        elif mode =="predict":
            # Open the raw picture 
            currentPic = pathToImage
        else:
            print("Unsupported mode!")
            return

        # Crops pic. Has to be defined individually.
        currentPic = currentPic.crop(self.cropArea)
        uncutImage = currentPic
        # Get width and height from cropped pic
        w, h = currentPic.size

        # In this case we use the cropped pics original size. We divide it in width into an certain number.
        a1 = 0
        a2 = 0
        a3 = w / numberOfCuts
        a4 = h
    
        # Cut current pic into a certain number of pics
        for cuts in range(numberOfCuts):
        
            # Cut cropped pic into a smaller one. In this case it displays one digit.
            croppedPic = currentPic.crop((a1, a2, a3, a4))

            # Check current mode
            if mode == "classify":
                # Shows uncut image once
                if cuts < 1:
                    uncutImage.show()    
                # Shows current cropped pic
                croppedPic.show()
                # Enter number of digit which is currently displayed
                digit = input("Which number is displayed ?")
                # Save the classified image to a specific categorie folder. Image is a png file with the current timestamp as name.
                croppedPic.save(self.rootPath + str(digit) + "/" + str(self.calendar.timegm(self.time.gmtime())) + ".png")
            elif mode == "predict":

                print("Predict mode")
                croppedPic.save(self.rootPath + str(self.calendar.timegm(self.time.gmtime())) + ".png")
                time.sleep(2)

            # Expand width parameter to display the next digit in the cropped image.
            a1 = a1 + w / numberOfCuts
            a3 = a3 + w / numberOfCuts

            pass
        
        pass

    # Semi automatic image classification from all images in a folder
    def classifyMultipleImages(self):

        # Variable to display processing status
        currentProcessingStatus = 1

        # loops through all files in raw image folder
        for img in self.os.listdir(self.unprocessedImagePath):
    
            # Shows current status
            print(str(currentProcessingStatus) + " images from " + str(len(self.os.listdir(self.unprocessedImagePath))) + " processed." )
            print("Current file: " + str(img))
            # Writes current file to log. If program is terminated, previous images can be deleted
            log = open(self.logPath,'w')
            log.write(img)
            log.close()
            # Creates path to file
            arg = self.unprocessedImagePath + img
            # Try to execute prepImage()
            try:
                self.prepImage (arg, 5, "classify")
            except Exception as e:
                print("File can't be processed!")
                print(e)
        
            currentProcessingStatus += 1
    
            pass

    pass