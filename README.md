# METAR - current weather information for aviation

### Requirements
Python 2.7+, pip, Redis

### How to run?
1. Copy ```settings.sample.py``` and create ```settings.py```. Default configuration/settings will suffice in most of the cases. 
Edit the configuration if required.

> Note: step-1 is required because ```settings.py``` contains configurations & settings which can vary platform-to-plaform.

2. Move to ```<project-dir>```, create virual environment and then activate it as


```sh
$ cd <project-dir>
$ virtualenv .environment
$ source .environment/bin/activate
```

3. Add project to ```PYTHONPATH``` as 

```sh 
$ export PYTHONPATH="$PYTHONPATH:." # . corresponds to current directory(project-dir)
```

3. Under ```<project-dir>``` install requirements/dependencies as 

```sh 
$ pip install -r requirements.txt
```

4. Then run ```app.py``` as  

```sh
$ python app.py
```

Now you can access the application by visiting ```http://localhost:8080``` (default settings)

> Note: You can change ```host``` and ```port``` under ```settings.py``` file.

### Endpoints

| Method | URL | Body | Description |
| ------ | --- | ---- | ----------- |
| GET | {host} | NA | Homepage |
| GET | {host}/metar/ping | NA | ```{"data": "pong"}``` |
| GET | {host}/metar/info?scode={station_code}&nocache={0 or 1} | NA | Returns station weather report |

Station codes can be found at http://tgftp.nws.noaa.gov/data/observations/metar/stations

> Assumption: Assumint that metar endpoint will return reponse in foillowing format - 
```sh
2001/11/17 15:38
KSGS 171538Z AUTO 19005KT 7SM CLR M01/M05 A3021 RMK AO2
```
