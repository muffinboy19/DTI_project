# AnomAlert 
A groundbreaking application designed to link your smartphones with installed cameras across various locations including homes, shops, roads, and highways. This multifaceted app offers users a convenient means to monitor their properties while also empowering traffic police to bolster surveillance efforts against suspicious behavior. By harnessing live video feeds and issuing alerts in the event of irregularities, AnomAlert strives to bolster community safety, tranquility, and law enforcement.

## Tech Stack 
* Flask
* MongoDB
* Tensorflow
* PyTorch
* Flutter
* Firebase
* AWS

## Features

1. **Secure Authentication & Authorization:**
   - Robust user authentication and authorization ensure a secure environment.

2. **Seamless Connectivity:**
   - AnomAlert effortlessly connects your smartphones to cameras with a RTSP URL, offering an integrated monitoring experience.

3. **Real-time Monitoring:**
   - Activate the app tracker to instantly access and monitor real-time video feeds from your cameras.

4. **Instant Notifications:**
   - AnomAlert is designed to detect and notify users promptly in case of accidents, altercations, harassment, theft, and other potential threats.
    
5. **Community Safety:**
   - By facilitating quick response and communication, AnomAlert promotes community safety and collaborative efforts towards maintaining a secure environment.

6. **Machine Learning Integration:**
   - The project incorporates Machine Learning algorithms to enhance the detection and alert system, improving accuracy over time.
  
## Dependencies
You need python and pip installed in your local machine to run the api.  
#### Version Support:
- python (3.11.0)
- pip (22.3)


## Installation

```bash
  pip install -r requirements.txt
  py main.py
```

## How To Setup

* Make sure your device is having internet connection.
* Open shell (which ever your OS support) on your PC.
* Change drive to the location where you want your project to be copied.
* Clone it to your local setup by using command git clone ```<repo link>```.
* Once cloned, Run the following command in the root directory of the project ```pip install virtualenv```.
* To setup virtual environment, run ```python -m venv <virtual_env_name>```.
* To activate virtual environment in the directory run the command ```.\virtual\Scripts\activate```.
* Install all dependencies in your virtual env by command  ```pip install -r requirements.txt```. This will take few minutes to install all packages.
* Make sure you have required enviornment variables saved in the ```.env``` file in the root of the project. A file ```.env.example``` is attached for reference.
* After the process is completed, run the command ```py main.py``` to start main file.
* The backend will be live on ```localhost:5111```.

> For more information about the RTSP URL you may click [here](https://www.getscw.com/decoding/rtsp#:~:text=1.210.-,You%20can%20also%20encode%20credentials%20into%20the%20URL%20by%20entering,and%2012345%20is%20the%20password.)

## Frontend Application Link
[AnomAlert Frontend](https://github.com/shashank-lol/AnomAlert/)

Let's build a safer and more secure community together with AnomAlert!
