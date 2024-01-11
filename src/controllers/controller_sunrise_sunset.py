# -*- coding: utf-8 -*-

import traceback
from flask import Blueprint, make_response, jsonify, request, Response


sunrise_sunset_bp = Blueprint('controller_sunrise_sunset', __name__)

@sunrise_sunset_bp.route('/api/sunrise_sunset', methods=['GET'])
async def sunrise_sunset_api() -> Response:
    """ """
    try:
        ...
    except Exception:
        traceback.print_exc()
        return make_response(jsonify({
            'response': '503 - Internal server error',
            'status': 503}), 503)
