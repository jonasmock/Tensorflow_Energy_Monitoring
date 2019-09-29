# Energy monitoring with Tensorflow

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
static esp_err_t capture_handler(httpd_req_t *req){
    camera_fb_t * fb = NULL;
    esp_err_t res = ESP_OK;
    int64_t fr_start = esp_timer_get_time();
    pinMode(4,OUTPUT);
    digitalWrite(4,HIGH);
    fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("Camera capture failed");
        httpd_resp_send_500(req);
        return ESP_FAIL;
    }

    httpd_resp_set_type(req, "image/jpeg");
    httpd_resp_set_hdr(req, "Content-Disposition", "inline; filename=capture.jpg");

    size_t out_len, out_width, out_height;
    uint8_t * out_buf;
    bool s;
    bool detected = false;
    int face_id = 0;
    if(!detection_enabled || fb->width > 400){
        size_t fb_len = 0;
        if(fb->format == PIXFORMAT_JPEG){
            fb_len = fb->len;
            res = httpd_resp_send(req, (const char *)fb->buf, fb->len);
        } else {
            jpg_chunking_t jchunk = {req, 0};
            res = frame2jpg_cb(fb, 80, jpg_encode_stream, &jchunk)?ESP_OK:ESP_FAIL;
            httpd_resp_send_chunk(req, NULL, 0);
            fb_len = jchunk.len;
        }
        esp_camera_fb_return(fb);
        int64_t fr_end = esp_timer_get_time();
        Serial.printf("JPG: %uB %ums\n", (uint32_t)(fb_len), (uint32_t)((fr_end - fr_start)/1000));
        digitalWrite(4,LOW);
        return res;
    }
```

The microprocessor is connected to the IoT WiFi and firewall rules to access the web server from the Ubuntu server are in place.


## How it works

#### 1. Preparation

Install **[Tensorflow](https://www.tensorflow.org/ "Tensorflow")** and **[Python3.7](https://www.anaconda.com/ "Python3.7")**. 
I used **[Anaconda](https://www.anaconda.com/ "Anaconda")** virtual environment.

Afterwards a folder structure must be created. 

![Folder structure](/readme_images/folders.PNG "Folder structure")

#### 2. Classification and training

Edit necessary paths, urls and crop parameters in **classify.py**. Install additional Python-Modules if needed.

*python3 classify.py*

Now the raw image will be cropped. Afterwards the cropped image will be divided into multiple files. Each time the program shows the picture and asks which digit is displayed. After entering the answer, the image will be moved to the specifiy category / digit folder.

After some pictures have been classified, preferably a few hundred, the training can be started. 

Edit necessary paths, urls and crop parameters in **trainModel.py**. Install additional Python-Modules if needed.

*python3 trainModel.py*

Now the previously classified images are stored in a trained model using Tenserflow / Keras.


#### 3. Recognition and visualization

Edit necessary paths, urls and crop parameters in **predictService.py**. Install additional Python-Modules if needed.

*python3 predictService.py*

The program gets a current image from the web server.

![Raw image](/readme_images/29-09-2019-15-40-03.png "Raw image")

Then the image is cut into several parts, just like it is when classifying.

![Cropped image](/readme_images/1569764404.png "Cropped image")
![Cropped image](/readme_images/1569764406.png "Cropped image")
![Cropped image](/readme_images/1569764408.png "Cropped image")
![Cropped image](/readme_images/1569764410.png "Cropped image")
![Cropped image](/readme_images/1569764412.png "Cropped image")

Then the trained model tries to recognize the number in each image. If the probability is more than 85%, the recognized image is moved to a folder of the specific category, just as it is when classifying. The new pictures can be used in the future for the independent training of the model.

![Prediction / log file](/readme_images/Bildschirmfoto%202019-09-29%20um%2015.48.46.png "Prediction / log file")

## Coming soon

- Save prediction to Influx database
- Train model by itself with new detected images
- Display data in Grafana
- Grafana alerts
