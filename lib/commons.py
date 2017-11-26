import json
from flask import Response
import urllib3

http = urllib3.PoolManager()

def jsonify(data=None):
    """
    Converts data to it's corresponding JSON format. If data is string then return data as it is.
    If data is `None` return empty json as '{}'.
    :param data: str or dictionary/list/array
    :return: Jsonified version of data.
    """
    json_res = None
    if not data:
        json_res = '{}'
    if type(data) != str:
        data = {} if not data else data
        json_res = json.dumps(data)
    return json_res

def json_response(res=None):
    """
    Converts dictionary/array/list to corresponding JSON structure.
    :param res: dictionary/array/list or a valid json string
    :return: JSON
    """
    json_res = jsonify(res)
    return Response(json_res, mimetype="application/json")

def celsius_to_fahrenheit(celsius):
    """
    Converts celsius to fahrenheit, rounds off the result and returns integer part.
    C/5 = (F-32)/9
    :param celsius:
    :return: fahrenheit
    """
    f_raw = (celsius * 1.8) + 32
    return int(round(f_raw))

def knots_to_mph(kts):
    """Knots (kt) to miles/hour (mph), rounds off the result and returns integer part."""
    mph_raw = kts * 1.1507794
    return int(round(mph_raw))
