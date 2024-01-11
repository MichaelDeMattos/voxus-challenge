# -*- coding: utf-8 -*-

import traceback
from pydantic import ValidationError
from services.service_sunrise_sunset import SunriseSunsetApi
from schemas.schema_sunrise_sunset import InputSunriseSunsetSchema
from flask import Blueprint, make_response, jsonify, request, Response


sunrise_sunset_bp = Blueprint('controller_sunrise_sunset', __name__)

@sunrise_sunset_bp.route('/api/sunrise_sunset', methods=['GET'])
async def sunrise_sunset_api() -> Response:
    """ """
    try:
        inputed_params = InputSunriseSunsetSchema(**request.args)
        sunrise_sunset_object = SunriseSunsetApi(inputed_params=inputed_params)
        http_status, message_object = await sunrise_sunset_object.get_external_data()
        return make_response(jsonify({
            'status': http_status,
            'response': message_object}), http_status)
    except ValidationError as e:
        traceback.print_exc()
        return make_response(jsonify({
            'response': str(e.errors()),
            'status': 422}), 422)
    except Exception:
        traceback.print_exc()
        return make_response(jsonify({
            'response': '503 - Internal server error',
            'status': 503}), 503)
