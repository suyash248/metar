import traceback
import json
from lib.commons import knots_to_mph, celsius_to_fahrenheit
from lib.redisutil import redis_connection
from settings import METAR_ENDPOINT
from commons import http, jsonify


def get_station_report(scode, nocache=0):
    """
    Fetches station report either from cache(if present, and nocache=0) or directly from METAR(if not present in cache
    or nocache=1) and updates cache accordingly.
    :param scode: Station code.
    :param nocache: 0 or 1
    :return: Station weather report.
    """
    processed_metar_res = dict()
    if nocache == 0:
        processed_metar_res = get_cached_response(scode, asjson=False)
    if nocache == 1 or len(processed_metar_res) == 0:
        station_endpoint = METAR_ENDPOINT + '/stations/{scode}.TXT'.format(scode=scode)
        metar_sresp = http.request('GET', station_endpoint)
        if metar_sresp.status == 404:
            processed_metar_res = {
               'message': 'No such station code found - %s' % scode,
               'status': 'success',
               'code': 1404
            }
        else:
            processed_metar_res = process_metar_response(metar_sresp.data)
            # Update cache
            encache_response(processed_metar_res)

    return processed_metar_res

def encache_response(processed_metar_res, ttl=300):
    """
    Caches the station report with expiry(ttl), where redis key is station code.
    :param processed_metar_res: Station weather report to be cached.
    :param ttl: Time to live
    """
    redis_connection.setex(name=processed_metar_res['station'], value=jsonify(processed_metar_res), time=ttl)

def get_cached_response(scode, asjson=True):
    """
    Fetches the cached report for the station.
    :param scode: Station code
    :param asjson:
    :return: Cached report either in json(string) or as dictionary depending upon `asjson` attribute.
    """
    json_res = redis_connection.get(name=scode) or '{}'
    return json_res if asjson else json.loads(json_res)

def process_metar_response(metar_resp):
    """
    Process the response received from metar and returns the JSON data in following format -
    {
    'data': {
            'station': 'KSGS',
            'ast_observation': '2017/04/11 at 16:00 GMT',
            'temperature': '-1 C (30 F)',
            'wind': 'S at 6 mph (5 knots)'
        }
    }
    :param metar_resp:
    :return: Processed metar response in JSON format
    """
    if not metar_resp:
        return {"message": "No response received from metar"}

    # Sample response sent by metar -
    # 2017/11/25 18:33 KSGS 251833Z AUTO 29006KT 10SM CLR 04/M06 A3009 RMK AO2 T00381061
    try:
        metar_resp = metar_resp.replace('\n', ' ').strip()
        print metar_resp
        metar_attrs = metar_resp.split(' ')

        date = metar_attrs[0]
        time = metar_attrs[1]
        scode = metar_attrs[2]
        #datetime = metar_attrs[3]
        #auto = metar_attrs[4] = 'AUTO',
        wind = metar_attrs[5]
        #visibility = metar_attrs[6]
        #sky = metar_attrs[7]
        temperature_dew = metar_attrs[8]
        #pressure = metar_attrs[9]

        # Parse temperature
        temperature = temperature_dew.split('/')[0]
        temperature_in_celsius = int('-'+temperature.replace('M', '') if temperature.startswith('M') else temperature)
        temperature_in_fahrenheit = celsius_to_fahrenheit(temperature_in_celsius)

        # Parse wind
        wind_angle = int(wind[:3])
        wind_sustained_speed_in_knots = int(wind[3:5])
        wind_sustained_speed_in_mph = knots_to_mph(wind_sustained_speed_in_knots)

        wind_stmt = '{wind_angle} degrees at a sustained speed of {wind_sustained_speed_in_mph} mph ({wind_sustained_speed_in_knots} knots)'\
            .format(wind_angle=wind_angle, wind_sustained_speed_in_mph=wind_sustained_speed_in_mph,
                    wind_sustained_speed_in_knots=wind_sustained_speed_in_knots)

        # Checking for gusting speed as it's optional
        if wind.find('G'):
            wind_gusted_speed_in_knots = int(wind[wind.find('G') + 1:wind.find('KT')])
            wind_gusted_speed_in_mph = knots_to_mph(wind_gusted_speed_in_knots)
            wind_stmt + ' with {wind_gusted_speed_in_mph} mph (wind_gusted_speed_in_knots knots) gusts'.format(
                wind_gusted_speed_in_mph=wind_gusted_speed_in_mph,
                wind_gusted_speed_in_knots=wind_gusted_speed_in_knots
            )

        return {
            'station': scode,
            'last_observation': date + ' at {time} GMT'.format(time=time),
            'temperature': str(temperature_in_celsius) + ' C ({fahrenheit} F)'.format(fahrenheit=temperature_in_fahrenheit),
            'wind': wind_stmt
        }
    except Exception as ex:
        traceback.print_exc()
        return {"message": "Error occurred while parsing the metar response", "response": metar_resp}