class PredictService:

    import tensorflow as tf
    from skimage import transform
    import imageio
    import io
    import time
    from datetime import datetime
    from PIL import Image 
    import requests  
    import os
    import shutil
    from influxdb import InfluxDBClient
    import pytz
    import numpy as np
    from globalServices import GlobalServices
    from classify import Classify 


    __slots__ = ['dbUser', 'dbPassword', 'dbHost', 'dbPort', 'dbMeasurement', 'dbHostTag', 'dbName', 'getImageUrl', 'predictedImagesPath', 'rootPath', 'logPath',
                'modelPath', 'img_size', 'configPath', 'collectData', 'collectDataConfidence']

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


    #Connection to InfluxDB
    def dbconnect(self, kwh):

        tz = self.pytz.timezone('Europe/Berlin')
        now = self.datetime.now(tz)
        unixtimens = int(self.time.mktime(now.timetuple()))*10**9

        json_body = [
                    {
                            "measurement": getattr(self, 'dbMeasurement'),
                            "tags": {
                                    "host": getattr(self, 'dbHostTag')
                            },
                            "time": unixtimens,
                            "fields":{
                                    "kwh": kwh,
                            }
                    }
            ]

        try:

            """Instantiate the connection to the InfluxDB client."""
            influxClient = self.InfluxDBClient(getattr(self, 'dbHost'), getattr(self, 'dbPort'), getattr(self, 'dbUser'), getattr(self, 'dbPassword'))

            print("Create database: " + getattr(self, 'dbName'))
            influxClient.create_database(getattr(self, 'dbName'))
	
            print("Get DB")
            influxClient.get_list_database()

            print("Switch DB")
            influxClient.switch_database(getattr(self, 'dbName'))

            print("Write points: {0}".format(json_body))
            influxClient.write_points(json_body)

            #print("Read DataFrame")
            #client.query("select * from gps")

            #print("Delete database: " + getattr(self, 'dbName'))
            #client.drop_database(getattr(self, 'dbName'))

            pass

        except Exception as e:

            print("Database error!")
            print(e)
            print("\n")

            pass

        pass


    # Loads and compiles the model
    def loadModel(self):
    
        imported_model = self.tf.keras.models.load_model(getattr(self, 'modelPath'), compile=False)
    
        imported_model.compile(optimizer=self.tf.optimizers.Adam(),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    
        return imported_model


    # Downloads and processes image from ESP32 CAM webserver
    def downloadImage(self):
    
        r = self.requests.get(getattr(self, 'getImageUrl'), timeout=4.0)
        if r.status_code != self.requests.codes.ok:
            assert False, 'Status code error: {}.'.format(r.status_code)
    
        # Opens image from web request
        with self.Image.open(self.io.BytesIO(r.content)) as im:

            args = {"pathToConfig":getattr(self, 'configPath'),}

            # Passes image to prepImage() function 
            classify = self.Classify(**dict(self.GlobalServices(**args).configToDict()["Classify"]))
            classify.prepImage(im, 5, "predict")      
    
        pass


    # Predicts digit and moves the image to the specific category folder. In the future the program should automatically train the model with the new data from the predictions
    def predict(self):
    
        currentProcessingStatus = 0
        now = self.datetime.now()
        now = now.strftime("%d-%m-%Y-%H-%M-%S")

        with open(getattr(self, 'logPath'), "a") as log:
            log.write("Timestamp: " + str(now)+ "\n")
            log.close()
    
        currentPrediction = []

        for img in sorted(self.os.listdir(getattr(self, 'predictedImagesPath'))):
    
            print(str(currentProcessingStatus) + " images from " + str(len(self.os.listdir(getattr(self, 'predictedImagesPath')))) + " processed." )

            pathToPredictedImage = getattr(self, 'predictedImagesPath') + img
        
            try:
            
                # Read current image
                img_array = self.imageio.imread(pathToPredictedImage, as_gray=True)
                img_array = self.transform.resize(img_array,(int(getattr(self, 'img_size')), int(getattr(self, 'img_size'))))
                img_array = img_array.astype(int)
                featureArray = self.np.array(img_array).reshape(-1, int(getattr(self, 'img_size')), int(getattr(self, 'img_size'))) / 255
                print("Import and compile model...")
                imported_model = self.loadModel()
                # Saves predictions
                predictions = imported_model.predict(featureArray)
                print("Prediction: " + str(predictions[0].argmax()) + " Confidence: " + str(predictions[0].max()))
            
                # Checks the confidence of the prediction 
                if predictions[0].max() > float(getattr(self, 'collectDataConfidence')):

                    if(str(getattr(self, 'collectData')) == "yes"):

                        pathToPredictedCategorie = str(getattr(self, 'rootPath')) + str(predictions[0].argmax()) + "/" + str(img)
                        self.shutil.move(pathToPredictedImage, pathToPredictedCategorie)
                        print("SAVE DATA")
                    else:

                        self.os.remove(pathToPredictedImage)

                    currentPrediction.append(predictions[0].argmax())
                
                elif predictions[0].max() < float(getattr(self, 'collectDataConfidence')):

                    if str(getattr(self, 'collectData')) == "yes":

                        # Moves image to "failed" folder, those images have to be classified manually
                        pathToPredictedCategorie = str(getattr(self, 'rootPath')) + "failed/" + str(predictions[0].argmax()) + "/" + str(img)
                        self.shutil.move(pathToPredictedImage, pathToPredictedCategorie)
                        print("SAVE DATA")
                    else:

                        self.os.remove(pathToPredictedImage)
            
                with open(getattr(self, 'logPath'), "a") as log:
                    log.write("Prediction: " +  str(predictions[0].argmax()) + " Confidence:  " + str(predictions[0].max()) +"\n")
                    log.close()

            except Exception as e:

                print(e)

                pass
 
            currentProcessingStatus += 1
 
        with open(getattr(self, 'logPath'), "a") as log:
            log.write("###############################################" + "\n")
            log.close()
        
        # If all five predictions confidence is > 95, the values are stored in InfluxDB.
        if len(currentPrediction) == 5:

            args = {"pathToConfig":getattr(self, 'configPath'),}
            tmp = str(currentPrediction[0]) + str(currentPrediction[1]) + str(currentPrediction[2]) + str(currentPrediction[3]) + str(currentPrediction[4]) 
            kwh = int(tmp)

            if kwh < int(self.GlobalServices(**args).readConfig("Global","lastPrediction")) or kwh > int(self.GlobalServices(**args).readConfig("Global","lastPrediction"))+5:

                print("Conflict with last prediction")
                return

            else:

                self.GlobalServices(**args).writeConfig("Global", "lastPrediction", kwh)
                self.dbconnect(kwh)

        pass


    pass