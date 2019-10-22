class Main:
        
        import configparser
        from globalServices import GlobalServices
        import os

        __slots__ = ['pathToConfig', 'mode']
    
    
        def __init__(self, **kwargs):

                print("\nThis is the constructor method of \""+type(self).__name__+"\" class.\n")
                print("The following args are optional: ", self.__slots__,"")

                for key, value in kwargs.items():

                        try:
                                setattr(self, key, value)
                                pass

                        except Exception as e:
                                print("Can't init object.\n")
                                raise Exception(e)

                try:

                        self.selectMode(self.initConfig(getattr(self, "pathToConfig")), True)
                        getattr(self, "mode")

                        pass

                except Exception as e:

                        print("\n\n#####Welcome#####\n")

                        pathToConfig = input("Please enter path to config.ini file:")

                        while self.os.path.isfile(pathToConfig) != True:

                                pathToConfig = input("ERROR path is not vaild.\nPlease enter path to config.ini file:\n")
                                if pathToConfig[-3:] != "ini":
                                        pathToConfig = ""

                        print("\nInitialize config from \"", pathToConfig ,"\"\n")
  
                        self.selectMode(self.initConfig(pathToConfig), False)

                pass


        # Starts selected mode
        def selectMode(self, configDict, automatic):

                mode = ""

                if automatic == True:

                        mode = getattr(self, "mode")

                else:

                        while not mode:

                                mode = input("Enter mode. \'prepare\' , \'classify\' , \'train\' or \'predict\'\n")
                                if mode == "classify" or mode == "train" or mode == "predict" or mode == "prepare":
                                        print("Correct mode chosen.")
                                else:
                                        print("Wrong mode!")
                                        mode = ""
                                        
                                        

                if mode == "classify": 

                        from classify import Classify 

                        classify = Classify(**dict(configDict["Classify"]))
                        classify.classifyMultipleImages()

                elif mode == "train":

                        from trainModel import TrainModel
                        train = TrainModel(**dict(configDict["Train"]))
                        train.createModel()

                elif mode == "predict":

                        from predictService import PredictService
                        predict = PredictService(**dict(configDict["Predict"]))
                        predict.downloadImage()
                        predict.predict()

                elif mode == "prepare":

                        args = {"pathToConfig":configDict["Prepare"]["configPath"],}

                        self.GlobalServices(**args).prepareFolders(input("Enter root folder name. (Contains default folder structure.)\n"))

                        pass       

                pass

        def initConfig(self, pathToConfig):

                args = {"pathToConfig":pathToConfig,}

                cfg = self.GlobalServices(**args)

                for section in dict(cfg.configToDict()):
                        
                        try:
                                cfg.writeConfig(section,"configPath",pathToConfig)
                        except Exception:
                                pass

                return cfg.configToDict()


        pass

#########################################################

import sys

args = {}
print(sys.argv.index)
if len(sys.argv) == 3:
        args = {"pathToConfig":sys.argv[1], "mode":sys.argv[2],}

print(args)
run = Main(**args)





                








