from classify import Classify 
from trainModel import TrainModel
from predictService import PredictService 

from globalServices import GlobalServices

args = {"pathToConfig":"/Users/jonas/Desktop/config.ini",
        }

init = GlobalServices(**args)

cfg = init.configToDict()

#print(dict(cfg["Classify"]))

#init.writeConfig("scripts/config.ini", "DEFAULT", "Property", "Newvalues")



classify = Classify(**dict(cfg["Classify"]))
#classify.classifyMultipleImages()

train = TrainModel(**dict(cfg["Train"]))
#train.createModel()

predict = PredictService(**dict(cfg["Predict"]))
#predict.downloadImage()
#predict.predict()



