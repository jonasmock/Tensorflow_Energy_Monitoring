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

                except Exception:

                        print("\n\n#####Welcome#####\n")

                        pathToConfig = input("Please enter path to config.ini file:")

                        while self.os.path.isfile(pathToConfig) != True:

                                pathToConfig = input("ERROR path is not vaild.\nPlease enter path to config.ini file:")
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

                                mode = input("Enter mode. \'classify\' , \'train\' or \'predict\'")
                                if mode == "classify" or mode == "train" or mode == "predict":
                                        print("Correct mode chosen.")
                                else:
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


                pass

        def initConfig(self, pathToConfig):

                args = {"pathToConfig":pathToConfig,}

                init = self.GlobalServices(**args)

                return init.configToDict()


        pass

#########################################################

import sys

args = {}
print(sys.argv.index)
if len(sys.argv) == 3:
        args = {"pathToConfig":sys.argv[1], "mode":sys.argv[2],}

print(args)
run = Main(**args)





                








