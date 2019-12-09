class GlobalServices:

    import configparser
    import os

    __slots__ = ['pathToConfig']

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


    # Reads config and returns value of a key in a specific section
    def readConfig(self, configSection, configKey):
        
        try:

            config = self.configparser.RawConfigParser()
            config.optionxform = str 
            config.read(getattr(self,"pathToConfig"))

            pass

        except Exception as e:

            print("Can't parse config.")
            print(e)
            print("\n")

            pass

        return config.get(configSection, configKey)


    # Reads config and returns it as dict
    def configToDict(self):
        
        try:

            config = self.configparser.RawConfigParser()
            config.optionxform = str 
            config.read(getattr(self,"pathToConfig"))

            pass

        except Exception as e:

            print("Can't parse config.")
            print(e)
            print("\n")

            pass

        return config._sections


    # Write value for specific key in a section to config file
    def writeConfig(self, configSection, configKey, keyValue):

        try:
            
            config = self.configparser.RawConfigParser()
            config.optionxform = str 
            config.read(getattr(self,"pathToConfig"))
            cfgfile = open(getattr(self,"pathToConfig"),'w')
            config.set(configSection, configKey, keyValue)
            config.write(cfgfile)
            cfgfile.close()

            pass

        except Exception as e:

            print("Can't write to config.")
            print(e)
            print("\n")

            pass

        pass


    # Create default folder structure
    def prepareFolders(self, folderName):

        rootFolder = self.readConfig("Prepare", "pathToFolders")

        try:

            self.os.makedirs(rootFolder+folderName)

        except FileExistsError:

            print("Folder already exists")

        try:

            self.os.makedirs(rootFolder+folderName+"/predict")

        except FileExistsError:

            print("Folder already exists")

        try:

            self.os.makedirs(rootFolder+folderName+"/predict/model")

        except FileExistsError:

            print("Folder already exists")

        try:

            self.os.makedirs(rootFolder+folderName+"/predict/raw")

        except FileExistsError:

            print("Folder already exists")

        try:

            self.os.makedirs(rootFolder+folderName+"/predict/failed")

        except FileExistsError:

            print("Folder already exists")

        try:

            self.os.makedirs(rootFolder+folderName+"/predict/predicted")

        except FileExistsError:

            print("Folder already exists")

        for n in range(10):

            try:

                self.os.makedirs(rootFolder+folderName+"/"+str(n))

            except FileExistsError:

                print("Folder already exists")

            try:

                self.os.makedirs(rootFolder+folderName+"/predict/"+str(n))

            except FileExistsError:

                print("Folder already exists")


        if input("Would you like to update paths in config with recently created folder structure ? y/[n]\n") == "y":
                                       
            try:
                    self.writeConfig("Train","rootPath",rootFolder+folderName+"/")
                    self.writeConfig("Train","modelOutputPath",rootFolder+folderName+"/predict/model/energy.h5")
                    self.writeConfig("Classify","unprocessedImagePath",rootFolder+folderName+"/predict/raw/")
                    self.writeConfig("Classify","rootPath",rootFolder+folderName+"/predict/")
                    self.writeConfig("Classify","logPath",rootFolder+folderName+"/log.txt")
                    self.writeConfig("Predict","predictedImagesPath",rootFolder+folderName+"/predict/predicted/")
                    self.writeConfig("Predict","rootPath",rootFolder+folderName+"/predict/")
                    self.writeConfig("Predict","logPath",rootFolder+folderName+"/log.txt")
                    self.writeConfig("Predict","modelPath",rootFolder+folderName+"/predict/model/energy.h5")

            except Exception:
                    pass

    pass

