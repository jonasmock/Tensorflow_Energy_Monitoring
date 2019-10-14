class PredictService:

    # Load, compile and predict model
    import tensorflow as tf
    # Process and transform images
    from skimage import transform,io
    # Open images
    import imageio
    import io
    # Used for timestamps
    import calendar
    import time
    from datetime import datetime
    # Get image from URL
    from PIL import Image 
    # Web request 
    import requests  
    # For interacton with the filesystem
    import os
    import shutil
    from globalServices import GlobalServices
    from influxdb import InfluxDBClient
    import pytz
    from classify import Classify 


    __slots__ = ['dbUser', 'dbPassword', 'dbHost', 'dbPort', 'dbMeasurement', 'dbHostTag', 'dbName', 'getImageUrl', 'predictedImagesPath', 'rootPath', 'logPath',
                'modelPath', 'img_size', 'configPath']

    def __init__(self, **kwargs):

        print("This is the constructor method of \""+type(self).__name__+"\" class.\n")
        print("The following args are necessary: ", self.__slots__,"\n")

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
    
        # Loads model with Keras
        imported_model = self.tf.keras.models.load_model(getattr(self, 'modelPath'), compile=False)
    
        # Compiles model because Tensorflow optimizers can't be compiled by Keras while loading the model
        imported_model.compile(optimizer=self.tf.train.AdamOptimizer(),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    
        return imported_model


    # Downloads and processes image from ESP32 CAM webserver
    def downloadImage(self):
    
        # Creates request from url parameter
        r = self.requests.get(getattr(self, 'getImageUrl'), timeout=4.0)
        # Displays request errors
        if r.status_code != self.requests.codes.ok:
            assert False, 'Status code error: {}.'.format(r.status_code)
    
        # Opens image from web request
        with self.Image.open(self.io.BytesIO(r.content)) as im:

            args = {"pathToConfig":getattr(self, 'configPath'),}
            
            init = self.GlobalServices(**args)

            cfg = init.configToDict()


            # Passes image to prepImage() function
            classify = self.Classify(**dict(cfg["Classify"]))
            classify.prepImage(im, 5, "predict")      
    
        pass

    # Predicts digit and moves the image to the specific category folder. In the future the program should automatically train the model with the new data from the predictions
    def predict(self):
    
        # Variable for status information
        currentProcessingStatus = 0
        # Get current time
        now = self.datetime.now()
        # Format time day-month-year-hour-minute-second
        now = now.strftime("%d-%m-%Y-%H-%M-%S")
        # Write timestamp to log file
        with open(getattr(self, 'logPath'), "a") as log:
            log.write("Timestamp: " + str(now)+ "\n")
            log.close()
    
        currentPrediction = []

        # Loops through temporarily saved images in predicct folder
        for img in sorted(self.os.listdir(getattr(self, 'predictedImagesPath'))):
    
            # Shows current processing status
            print(str(currentProcessingStatus) + " images from " + str(len(self.os.listdir(getattr(self, 'predictedImagesPath')))) + " processed." )
            # Creates path to current image
            pathToPredictedImage = getattr(self, 'predictedImagesPath') + img
        
            # Catch errors while predicting digits
            try:
            
                # Read current image
                img_array = self.imageio.imread(pathToPredictedImage, as_gray=True)
                img_array = self.transform.resize(img_array,(int(getattr(self, 'img_size')), int(getattr(self, 'img_size'))))
                img_array = img_array.astype(int)
                # Reshape image array
                img_array = img_array.reshape(int(getattr(self, 'img_size')), int(getattr(self, 'img_size'))) / 255
                # Creates predict array
                predict_array = [(img_array, img_array)]
                print("Import and compile model...")
                imported_model = self.loadModel()
                # Saves predictions
                predictions = imported_model.predict(predict_array)
                # Shows current prediction
                print("Prediction: " + str(predictions[0].argmax()) + " Confidence: " + str(predictions[0].max()))
            
                # Checks the confidence of the prediction
                if predictions[0].max() > 0.95:
                    # Creates path to categoriy folder from predicted digit
                    pathToPredictedCategorie = str(getattr(self, 'rootPath')) + str(predictions[0].argmax()) + "/" + str(img)
                    # Moves image from predicted digit to the specifiy category folder
                    self.shutil.move(pathToPredictedImage, pathToPredictedCategorie)
                    currentPrediction.append(predictions[0].argmax())
                
                else:
                    # Creates path to categoriy folder from predicted digit
                    pathToPredictedCategorie = str(getattr(self, 'rootPath')) + "failed/" + str(img)
                    # Moves image to "failed" folder, those images have to be classified manually
                    self.shutil.move(pathToPredictedImage, pathToPredictedCategorie)
            
                # Write prediction to log file
                with open(getattr(self, 'logPath'), "a") as log:
                    log.write("Prediction: " +  str(predictions[0].argmax()) + " Confidence:  " + str(predictions[0].max()) +"\n")
                    log.close()
            except Exception as e:
                print(e)
                pass
            # Add 1 to status variable     
            currentProcessingStatus += 1
        # Marks end of prediction in log file    
        with open(getattr(self, 'logPath'), "a") as log:
            log.write("###############################################" + "\n")
            log.close()
        
        if len(currentPrediction) == 5:
            tmp = str(currentPrediction[0]) + str(currentPrediction[1]) + str(currentPrediction[2]) + str(currentPrediction[3]) + str(currentPrediction[4]) 
            kwh = int(tmp)
            self.dbconnect(kwh)
        pass

    pass