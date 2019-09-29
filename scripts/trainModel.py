# To create numpy arrays for training data
import numpy as np
# For filesystem interaction
import os
# For processing images
import cv2
# Create, train and save the model
import tensorflow as tf
# To randmize training data
import random

# Array for training data
training_data = []
# Parrent folder of categorie folders
DATADIR = "Z:/"
# Defines the categories
CATEGORIES = ["0","1","2","3","4","5","6","7","8","9"]
# Size in which images will be stored and processed
IMG_SIZE = 50
# Max amount of training data per category
dataAmount = 1200
# Path to save model file
modelOutputPath = "Z:/model/energy.model"
# Defines the number of training periods
epochs = 20

# Extracts pixels from training data images and appends them to the array
def create_training_data():
    
    # Loop through categories   
    for digit in CATEGORIES:
        # Path to the categorie folder
        path = os.path.join(DATADIR, digit)
        # Translates categories to digits. Model can't work with strings. (Index 0 = Categorie 1. In this case categorie 1 is the digit 0)
        class_num = CATEGORIES.index(digit)
        
        # Loops through the images in categorie folder
        for idx, img in enumerate(os.listdir(path)):
            
            # Breaks loop if max amount of training images in this categoriy is reached
            if idx == dataAmount:
                break
            
            # Try to read the current image in grayscale, resize it to the defined size and append it to the training data array / label array.
            try:
                img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
            except Exception as e:
                pass
        pass
    pass
pass

# Shuffles the training data and creates an array for the features and one for the labels
def shuffleData():
    
    # Shuffle function randomizes the training data
    random.shuffle(training_data)
    
    # Two arrays fo features and labels
    x = []
    y = []
    
    # Loop trough training data
    for features, label in training_data:
        # Append features and labels to array
        x.append(features)
        y.append(label)
    
    # Create numpy array and reshape array size
    x = np.array(x).reshape(-1, IMG_SIZE, IMG_SIZE)
    y = np.array(y)
    # Normalize values (values < 1)
    x = x / 255
    return x, y
    
    pass

# Create and compile the model
def createModel():
    
    # Defines model properties
    model = tf.keras.Sequential ([
    
        tf.keras.layers.Flatten(input_shape=(50, 50)),
        tf.keras.layers.Dense(128, activation=tf.nn.relu),
        tf.keras.layers.Dense(10, activation=tf.nn.softmax)
    
    ])
    
    # Compiles the model
    model.compile(optimizer=tf.train.AdamOptimizer(),
                 loss='sparse_categorical_crossentropy',
                 metrics=['accuracy'])
    # Returnes the model 
    return model
    
    pass



# 1. Create training data
create_training_data()
# 2. Shuffle training data
features, label = shuffleData()
# 3. Create the model
model = createModel()
# 4. Train the model
model.fit(features, label, epochs = epochs)
# 5. Save the model
model.save(modelOutputPath)