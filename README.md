# Energy monitoring with Tensorflow

## Warning: Currently it's not Pylint conform and there are no tests available.

#### Motivation:

I am a computer science student and currently live in my own apartment. My server, several sensors / microcontrollers / smart home devices and especially my electric heating in an old building, consumes quite a lot of electricity.

Since only an analog electricity meter is installed, I would like to automate the reading process and visualize the data. In addition, notifications would be nice.

I decided to recognize the numbers via "artificial intelligence". Due to my low cost setup, the images from the camera are pretty bad. Existing models from the internet were not reliable enough. I decided to create my own model. *The classification and training process had begun...*

#### Setup:

- analog electricity meter
- NVIDIA RTX 2070
- [ESP32 CAM](https://www.amazon.de/QooTec-ESP32-CAM-Bluetooth-Development-Arduino/dp/B07RDHX18P/ref=sr_1_3?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=esp32+cam&qid=1569767194&s=computers&sr=1-3 "ESP32 CAM") + USB power cable
- [Breadboard / Jumper wire](https://www.amazon.de/AZDelivery-%E2%AD%90%E2%AD%90%E2%AD%90%E2%AD%90%E2%AD%90-Jumper-Breadboard-Arduino/dp/B078JGQKWP/ref=sr_1_5?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=breadboard+jumper&qid=1569767386&s=gateway&sr=8-5 "Breadboard / Jumper wire")
- [IoT WiFi](https://www.sophos.com/de-de/products/next-gen-firewall.aspx "IoT WiFi")
- Virtual [Ubuntu 18.04.03 LTS](https://ubuntu.com/download/desktop "Ubuntu 18.04.03 LTS") maschine


###### ESP32 CAM

The ESP32 CAM microprocessor, was basically flashed with the template of the camera web server from Espressif examples. Only in the file *app_httpd.cpp* changes were made in the *capture* function to switch on the LED (pin 4) before each image.

```cpp

    pinMode(4,OUTPUT); // Defines pin 4 as output pin
    digitalWrite(4,HIGH); // turns LED on
    digitalWrite(4,LOW); // turns LED off

```

The microprocessor is connected to the IoT WiFi and firewall rules to access the web server from the Ubuntu server are in place.

## How it works

#### 1. Preparation

Based on **[Tensorflow](https://www.tensorflow.org/ "Tensorflow")**, **[Python3.7](https://www.anaconda.com/ "Python3.7")** and **[Anaconda](https://www.anaconda.com/ "Anaconda")** virtual environment.

1. Clone repo.
2. Install **[Anaconda](https://www.anaconda.com/ "Anaconda")**.
3. Make sure requirments for Tensorflow are fulfilled. In my case I had to install CUDA etc. for my NVIDIA GPU.

**[NVIDIA GPU requirements](https://www.tensorflow.org/install/gpu)**

4. Create new virtual enviroment with prepared **conda_requirements.txt** from setup folder. Currently the Anaconda requirements are only adjusted to Windows 10 + NVIDIA GPU. If you want to use a Linux distribution or train and predict with **[CPU](https://www.tensorflow.org/install)** you have to install additionally packages manually.

```
conda create --name myNewEnv --file [Path to /setup/conda_requirements.txt]
```
6. Every time you want to use the program, first activate the Anaconda enviroment.

```
conda activate myNewEnv
```
Unfortunately I didn't find a package for InfluxDB in Anaconda, install package via pip inside the Anaconda env.

```
pip install influxdb
```

In **config.ini** file in the *Prepare* section add the path where the default folder structure should be created. Afterwards run **Main.py** and enter the path to **config.ini**.

Enter *prepare* to select preparation mode. 

Enter the root folder name for the default folder structure.

Enter *y* to update paths in **config.ini**. They'll point to the recently created folders.

Now you have to enter the few missing parameters in **config.ini** manually.

This process is only necesarry if you want to create a new folder structure or if you want to update all paths at once in the config. To run predictions as a service for example as cronjob, its possible to start **Main.py** with parameters. Four modes are available: *prepare*, *classify*, *train*, *predict*

```
python Main.py [pathToConfig] [mode]
```

#### 2. Classification and training

Run **Main.py** with desired parameter. Additional Python modules may need to be installed.

```
python Main.py [pathToConfig] classify
```

Now the raw image will be cropped. Afterwards the cropped image will be divided into multiple files. Each time the program shows the picture and asks which digit is displayed. After entering the answer, the image will be moved to the specifiy category / digit folder.

After some pictures have been classified, preferably a few hundred, the training can be started. 

Run **Main.py** with desired parameter. Additional Python modules may need to be installed.

```
python Main.py [pathToConfig] train
```

Now the previously classified images are stored in a trained model using Tenserflow / Keras.


#### 3. Recognition and visualization

Run **Main.py** with desired parameter. Additional Python modules may need to be installed.

```
python Main.py [pathToConfig] predict
```

The program gets a current image from the web server.

![Raw image](/readme_images/29-09-2019-15-40-03.png "Raw image")

Then the image is cut into several parts, just like it is when classifying.

![Cropped image](/readme_images/1569764404.png "Cropped image")
![Cropped image](/readme_images/1569764406.png "Cropped image")
![Cropped image](/readme_images/1569764408.png "Cropped image")
![Cropped image](/readme_images/1569764410.png "Cropped image")
![Cropped image](/readme_images/1569764412.png "Cropped image")

The trained model tries to recognize the number in each image. If the probability is more than 95%, the recognized image is moved to a folder of the specific category, just as it is when classifying. The new pictures can be used in the future for the autonomously training of the model. 

![Prediction / log file](/readme_images/Bildschirmfoto%202019-09-29%20um%2015.48.46.png "Prediction / log file")

If the probability is more than 95% and the predicted value is higher or equal than the last electricity meter value, it's saved to an InfluxDB database. The predicted values and some additional information like the the maximum electricity meter value per day according to the contract are combined in a Grafana dashboard. The red points display the maximum electricity meter value per day according to the contract and the green graph shows the current value.

![Grafana](/readme_images/grafana.png "Grafana")

## Coming soon

- Train model by itself with new detected images
- Check electricity meter via Telegram bot
- Grafana alerts
