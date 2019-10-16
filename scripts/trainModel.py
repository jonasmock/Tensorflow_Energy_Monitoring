class TrainModel:

    import numpy as np
    import os
    import cv2
    import tensorflow as tf
    import random

    training_data = []

    __slots__ = ['rootPath', 'categories', 'img_size', 'dataAmount', 'modelOutputPath', 'epochs']

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


    # Extracts pixels from training data images and appends them to the array. Afterwards features and labels are stored in two arrays and returned.
    def createTrainingData(self):
     
        for categorie in str(getattr(self, 'categories')).split(","):

            categoriePath = self.os.path.join(getattr(self, 'rootPath'), categorie)
            categorieIndex = str(getattr(self, 'categories')).split(",").index(categorie)
        
            try:

                for idx, img in enumerate(self.os.listdir(categoriePath)):
            
                    if idx == int(getattr(self, 'dataAmount')):
                        break
            
                    # Try to read the current image in grayscale, resize it to the defined size and append it to the training data array / label array.
                    try:
                        
                        if str(img)[-3:] == "png)":
                            img_array = self.cv2.imread(self.os.path.join(categoriePath,img), self.cv2.IMREAD_GRAYSCALE)
                            resized_array = self.cv2.resize(img_array, (int(getattr(self, 'img_size')), int(getattr(self, 'img_size'))))
                            self.training_data.append([resized_array, categorieIndex])

                    except Exception as e:

                        print("Can't process image.",categoriePath,img,"\n")
                        print(e)

                        pass
                    
                    pass

            except Exception as e:

                print("Categorie folder not found.")
                print(e)
                print("\n")

                pass

            pass

        self.random.shuffle(self.training_data)

        featureArray = []
        labelArray = []

        for features, label in self.training_data:

            featureArray.append(features)
            labelArray.append(label)
    
        featureArray = self.np.array(featureArray).reshape(-1, int(getattr(self, 'img_size')), int(getattr(self, 'img_size')))
        labelArray = self.np.array(labelArray)
        # Normalize values (values < 1)
        featureArray = featureArray / 255

        return featureArray, labelArray


    # Create, train and save the model
    def createModel(self):
    
        # Defines model properties
        model = self.tf.keras.Sequential ([
    
            self.tf.keras.layers.Flatten(input_shape=(int(getattr(self, 'img_size')), int(getattr(self, 'img_size')))),
            self.tf.keras.layers.Dense(128, activation=self.tf.nn.relu),
            self.tf.keras.layers.Dense(10, activation=self.tf.nn.softmax)
    
        ])
    
        model.compile(optimizer=self.tf.train.AdamOptimizer(),
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])
        
        features, labels = self.createTrainingData()

        # Train the model
        model.fit(features, labels, epochs = int(getattr(self, 'epochs')))
        model.save(getattr(self, 'modelOutputPath'))
    
        pass
    

    pass