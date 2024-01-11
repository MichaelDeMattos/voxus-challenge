# -*- coding: utf-8 -*-

import aiohttp
import traceback
from datetime import datetime, timedelta
from pydantic import ValidationError
from schemas.schema_sunrise_sunset import (
    InputSunriseSunsetSchema, ExternalSubmmitSunriseSunsetSchema, ExternalResponseSunriseSunsetSchema)

class SunriseSunsetApi(object):
    def __init__(self, inputed_params: InputSunriseSunsetSchema) -> None:
        self.inputed_params = inputed_params
        self.url_api = 'https://api.sunrise-sunset.org/json'

    async def get_external_data(self) -> tuple:
        """ GET request to https://api.sunrise-sunset.org/json """
        try:
            sended_params = {
                'lat': self.inputed_params.latitude,
                'lng': self.inputed_params.longitude}
            external_params = ExternalSubmmitSunriseSunsetSchema(**sended_params).dict(exclude_none=True)
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url_api, params=external_params, timeout=60) as resp:
                    if resp.status != 200:
                        return (resp.status, await resp.json())
                    else:
                        print(resp.request_info, flush=True)
                        resp_json = await resp.json()
                        request_datetime = datetime.now()
                        validated_output_external_api = ExternalResponseSunriseSunsetSchema(**resp_json)
                        exact_time_str_12hr_to_sunrise = datetime.strptime(
                            f'{request_datetime.day}-{request_datetime.month}-{request_datetime.year} ' + \
                            validated_output_external_api.results.get('sunrise'), '%d-%m-%Y %I:%M:%S %p')
                        exact_time_str_24hr_to_sunrise = exact_time_str_12hr_to_sunrise.strftime("%d-%m-%Y %H:%M:%S")
                        exact_time_str_12hr_to_sunset = datetime.strptime(
                            f'{request_datetime.day}-{request_datetime.month}-{request_datetime.year} ' + \
                            validated_output_external_api.results.get('sunset'), '%d-%m-%Y %I:%M:%S %p')
                        exact_time_str_24hr_to_sunset = exact_time_str_12hr_to_sunset.strftime("%H:%M:%S")    
                        return (200, resp_json.get('results'))
        except ValidationError as e:
            traceback.print_exc()
            return (422, str(e.errors()))
        except Exception:
            traceback.print_exc()
            return (502, '502 - Bad Gateway')
