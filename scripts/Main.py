from classify import Classify 
#from trainModel import TrainModel
#from predictService import PredictService 

from globalServices import GlobalServices

args = {"pathToConfig":"scripts/config.ini",
        }

init = GlobalServices(**args)

cfg = init.configToDict()

print(dict(cfg["Classify"]))

#init.writeConfig("scripts/config.ini", "DEFAULT", "Property", "Newvalues")



classify = Classify(**dict(cfg["Classify"]))
classify.classifyMultipleImages()

#train = TrainModel("/Users/jonas/Downloads/output/", ["0","1","2","3","4","5","6","7","8","9"], 50, 2, 15, "/Users/jonas/Downloads/output/test.model")
#train.createModel()


#predict = PredictService("", "", "", "", "", "", "", "","","","","")
#predict.downloadImage()
#predict.predict()



