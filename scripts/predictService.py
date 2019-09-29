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

# URL to get image from ESP32 CAM
url = 'http://10.0.10.103/capture'
# Path to save raw images
rawPath = '/home/jonas/esp32_cam/raw/'
# Amount of categories / digits
pics = 5
# Path to save cropped images temporarily
outputPath = '/home/jonas/esp32_cam/predict/'
# Parten folder of categoriy folders
newPath = '/home/jonas/esp32_cam/'
# Path to log file
logPath = '/home/jonas/esp32_cam/log.txt'
# Path where model file is located
modelPath = '/home/jonas/esp32_cam/energy.model'

# Loads and compiles the model
def loadModel(path):
    
    # Loads model with Keras
    imported_model = tf.keras.models.load_model(path, compile=False)
    
    # Compiles model because Tensorflow optimizers can't be compiled by Keras while loading the model
    imported_model.compile(optimizer=tf.train.AdamOptimizer(),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    
    return imported_model
    pass

# Crops raw image and stores them temporarily
def prepImage (img,outputPath,pics):
    
    # Image from parameter
    pic = img
    pic = pic.crop((635, 200, 1450, 400))
    # Get width and height from cropped pic
    w, h = pic.size
    # In this case we use the cropped pics original size. We divide it in width into an certain number.
    a1 = 0
    a2 = 0
    a3 = w / pics
    a4 = h
    
    # Loop through certain number of pics
    for x in range(pics):
        # Cut cropped pic into a smaller one. In this case it displays one digit.
        croppedPic = pic.crop((a1, a2, a3, a4))
        # Save the classified image to a specific categorie folder. Image is a png file with the current timestamp as name.
        croppedPic.save(outputPath + str(calendar.timegm(time.gmtime())) + ".png")
        # Saving needs some time
        time.sleep(2)
        # Expand width parameter to display the next digit in the cropped image.
        a1 = a1 + w / pics
        a3 = a3 + w / pics
        
    pass

# Downloads and processes image from ESP32 CAM webserver
def download_image(url):
    
    # Creates request from url parameter
    r = requests.get(url, timeout=4.0)
    # Displays request errors
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)
    
    # Get current time
    now = datetime.now()
    # Format time to day-month-year-hour-minute-second
    now = now.strftime("%d-%m-%Y-%H-%M-%S")
    # Creates path to file and filename with current timestamp
    image_file_path = rawPath + now + ".png"
    # Writes current file to console
    print(image_file_path)
    
    # Opens image from web request
    with Image.open(io.BytesIO(r.content)) as im:
        # Passes image to prepImage() function
        prepImage(im, outputPath, pics)
        # Saves raw image
        im.save(image_file_path)
    # Displays status information in console
    print('Image downloaded from url: {} and saved to: {}.'.format(url, image_file_path))
    
    pass

# Predicts digit and moves the image to the specific category folder. In the future the program should automatically train the model with the new data from the predictions
def predict(path, newpath):
    
    # Variable for status information
    count = 0
    # Get current time
    now = datetime.now()
    # Format time day-month-year-hour-minute-second
    now = now.strftime("%d-%m-%Y-%H-%M-%S")
    # Write timestamp to log file
    with open(logPath, "a") as log:
        log.write("Timestamp: " + str(now)+ "\n")
        log.close()
    
    # Loops through temporarily saved images in predicct folder
    for img in sorted(os.listdir(path)):
        # Shows current processing status
        print(str(count) + " images from " + str(len(os.listdir(path))) + " processed." )
        # Creates path to current image
        arg = path + img
        
        # Catch errors while predicting digits
        try:
            
            # Read current image
            img_array = imageio.imread(arg, as_gray=True)
            img_array = transform.resize(img_array,(50, 50))
            img_array = img_array.astype(int)
            # Reshape image array
            img_array = img_array.reshape(50, 50) / 255
            # Creates predict array
            predict_array = [(img_array, img_array)]
            # Saves predictions
            predictions = imported_model.predict(predict_array)
            # Shows current prediction
            print("Prediction: " + str(predictions[0].argmax()) + " Confidence: " + str(predictions[0].max()))
            
            # Checks the confidence of the prediction
            if predictions[0].max() > 0.85:
                # Creates path to categoriy folder from predicted digit
                newArg = str(newpath) + str(predictions[0].argmax()) + "/" + str(img)
                # Moves image from predicted digit to the specifiy category folder
                shutil.move(arg, newArg)
            else:
                # If the confidence is not high enough, the file will be deleted
                os.remove(arg)
            
            # Write prediction to log file
            with open(logPath, "a") as log:
                log.write("Prediction: " +  str(predictions[0].argmax()) + " Confidence:  " + str(predictions[0].max()) +"\n")
                log.close()

        except Exception as e:
            print(e)
            pass
        # Add 1 to status variable     
        count += 1
    # Marks end of prediction in log file    
    with open(logPath, "a") as log:
        log.write("###############################################" + "\n")
        log.close()
pass
            
        
    

# 1. Load and compile model   
imported_model = loadModel(modelPath)
# 2. Download raw image from ESP32 CAM and prepare prediction  
download_image(url)
# 3. Predict digits and store predictions with high confidence to train model in the future
predict(outputPath, newPath)
