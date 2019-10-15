class Classify:

    import os
    from PIL import Image
    import calendar
    import time
    from globalServices import GlobalServices


    __slots__ = ['unprocessedImagePath', 'rootPath', 'logPath', 'cropArea','configPath']

    def __init__(self, **kwargs):

        print("This is the constructor method of \""+type(self).__name__+"\" class.")
        print("The following args are necessary: ", self.__slots__,"")

        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
                pass
            except Exception as e:
                print("Can't init object.\n")
                raise Exception(e)

        print("Successfully initialized\n")

        pass


    # Crops the raw picture to into a defined number. Predict mode just saves image. Classify mode asks which number is displayed before saving.
    def prepImage (self, pathToImage, numberOfCuts, mode):
    
        if mode == "classify":
            currentPic = self.Image.open(pathToImage)
        elif mode =="predict":
            currentPic = pathToImage
            args = {"pathToConfig":getattr(self, 'configPath'),}         
            init = self.GlobalServices(**args)
            cfg = init.configToDict()
        else:
            print("Unsupported mode!")
            return

        currentPic = currentPic.crop((int(value) for value in str(getattr(self, 'cropArea')).split(",")))
        uncutImage = currentPic
        w, h = currentPic.size

        a1 = 0
        a2 = 0
        a3 = w / numberOfCuts
        a4 = h
    
        for cuts in range(numberOfCuts):
        
            croppedPic = currentPic.crop((a1, a2, a3, a4))

            if mode == "classify":

                if cuts < 1:
                    uncutImage.show()    
                croppedPic.show()
                digit = input("Which number is displayed ?")
                croppedPic.save(getattr(self, 'rootPath') + str(digit) + "/" + str(self.calendar.timegm(self.time.gmtime())) + ".png")

            elif mode == "predict":

                print("Predict mode")
                croppedPic.save(cfg['Predict']['predictedImagesPath']  + str(self.calendar.timegm(self.time.gmtime())) + ".png")
                self.time.sleep(2)

            a1 = a1 + w / numberOfCuts
            a3 = a3 + w / numberOfCuts

            pass
        
        pass


    # Semi automatic image classification from all images in a folder
    def classifyMultipleImages(self):

        currentProcessingStatus = 1

        for img in self.os.listdir(getattr(self,'unprocessedImagePath')):
    
            print(str(currentProcessingStatus) + " images from " + str(len(self.os.listdir(getattr(self,'unprocessedImagePath')))) + " processed." )
            print("Current file: " + str(img))

            log = open(getattr(self, 'logPath'),'w')
            log.write(img)
            log.close()

            pathToImage = getattr(self,'unprocessedImagePath') + img

            try:

                self.prepImage (pathToImage, 5, "classify")

            except Exception as e:

                print("File can't be processed!")
                print(e)
        
            currentProcessingStatus += 1
    
            pass


    pass