# Flask app configuration.
APP = {
    "HOST": "0.0.0.0",
    "PORT": 8080
}
METAR_ENDPOINT = "http://tgftp.nws.noaa.gov/data/observations/metar"

# Redis database configuration.
REDIS = {
    "HOST": "127.0.0.1",
    "PORT": 6379,
    "DB": 0,
    "PASSWORD": None
}