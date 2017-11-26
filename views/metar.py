from flask import Blueprint, request
from lib.commons import json_response
from lib.metarservice import get_station_report

# Register routes blueprint
metar = Blueprint ('metar', __name__)

@metar.route("/ping")
def ping():
    res = {"data": "pong"}
    return json_response(res)

@metar.route("/info")
def station_info():
    scode = request.args.get('scode')
    if not scode:
        # Note: We're using custom response code for more flexibility. Clients(browser) will see the response code
        # as 200 but we can show custom messages later on the basis of our custom code.
        return json_response({'message': 'Station code is required', 'status': 'error', 'code': 1400})

    nocache = request.args.get('nocache', 0)
    try:
        nocache = int(nocache)
    except ValueError:
        nocache = 0
        #return json_response({'message': 'Invalid value for nocache', 'status': 'error', 'code': 1400})

    processed_metar_res = get_station_report(scode, nocache)
    print processed_metar_res
    return json_response(processed_metar_res)